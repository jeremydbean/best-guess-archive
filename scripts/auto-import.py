#!/usr/bin/env python3
"""
Auto-import a Best Guess Live episode from YouTube into the archive.

Usage:
    python scripts/auto-import.py                       # auto-detect from RSS feed
    python scripts/auto-import.py --video-id=abc123     # specific video
    python scripts/auto-import.py --dry-run             # parse but don't write files
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import anthropic
from youtube_transcript_api import YouTubeTranscriptApi

CHANNEL_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCcJVrF8GextFm229zgllU4w"
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def fetch_rss_videos():
    """Return list of (video_id, title, published_dt) sorted oldest-first."""
    with urllib.request.urlopen(CHANNEL_RSS, timeout=15) as resp:
        xml_data = resp.read()
    root = ET.fromstring(xml_data)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    videos = []
    for entry in root.findall("atom:entry", ns):
        video_id = entry.findtext("yt:videoId", namespaces=ns)
        title = entry.findtext("atom:title", namespaces=ns) or ""
        published_str = entry.findtext("atom:published", namespaces=ns) or ""
        if video_id and published_str:
            published_dt = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
            videos.append((video_id, title, published_dt))
    videos.sort(key=lambda v: v[2])  # oldest first
    return videos


def to_eastern_date(dt: datetime) -> datetime:
    """Shift UTC datetime to approximate US Eastern date (EDT = UTC-4)."""
    return dt - timedelta(hours=4)


def format_archive_date(dt: datetime) -> str:
    """Convert a datetime to 'Weekday, Month D, YYYY' archive format."""
    local = to_eastern_date(dt)
    weekday = WEEKDAY_NAMES[local.weekday()]
    month = MONTH_NAMES[local.month - 1]
    return f"{weekday}, {month} {local.day}, {local.year}"


def get_imported_dates() -> set:
    """Return the set of dates already present in transcripts.json."""
    try:
        with open("data/transcripts.json") as f:
            return {t["date"] for t in json.load(f)}
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


SPECIAL_EPISODE_RE = re.compile(r"\b(EXTRA|RECAP|BONUS|BEHIND[ -]THE[ -]SCENES|TRAILER|PREVIEW)\b", re.IGNORECASE)


def is_regular_episode(title: str) -> bool:
    """Skip EXTRA/recap/bonus videos — auto-import only handles regular two-round episodes."""
    return not SPECIAL_EPISODE_RE.search(title or "")


def fetch_transcript(video_id: str) -> str:
    """
    Fetch the YouTube auto-caption transcript and return it as plain text.

    Chunks are joined into sentences; [Music] / [Applause] tags are stripped.
    HTML entities are unescaped so the audit's escaped-entity check doesn't fire.
    """
    ytt_api = YouTubeTranscriptApi()
    fetched = ytt_api.fetch(video_id, languages=["en"])
    chunks = fetched.to_raw_data()  # [{text, start, duration}, ...]
    noise = re.compile(r"^\s*\[.*?\]\s*$", re.IGNORECASE)
    lines = []
    buf = []
    for chunk in chunks:
        text = html.unescape(chunk["text"].replace("\n", " ").strip())
        if not text or noise.match(text):
            continue
        buf.append(text)
        if text[-1] in ".!?":
            lines.append(" ".join(buf))
            buf = []
    if buf:
        lines.append(" ".join(buf))
    return "\n".join(lines)


def call_claude(transcript_text: str, episode_date: str, video_title: str) -> dict:
    """
    Send the transcript to Claude and get back structured episode data.

    Returns a dict with keys: episode_date, cancelled, games, transcript.
    """
    client = anthropic.Anthropic()

    with open("data/games.json") as f:
        all_games = json.load(f)
    schema_games = json.dumps(all_games[-4:], indent=2)

    with open("data/transcripts.json") as f:
        all_transcripts = json.load(f)
    schema_transcript = json.dumps(all_transcripts[-1], indent=2)

    system_prompt = (
        "You are a data extractor for the Best Guess Live game show archive.\n"
        "Best Guess Live is a daily Netflix interactive game show. Each episode has two rounds.\n"
        "In each round, viewers guess a secret item from five clues revealed one at a time.\n"
        "In v2 format, gold/silver/bronze winners get separate payouts based on which clue "
        "they first answered correctly (gold = earliest = highest payout).\n\n"
        "Respond with valid JSON ONLY — no markdown, no explanation, no code fences.\n"
        "The JSON must have exactly this top-level structure:\n"
        "{\n"
        '  "episode_date": "Weekday, Month D, YYYY",\n'
        '  "cancelled": false,\n'
        '  "games": [...],\n'
        '  "transcript": {...}\n'
        "}\n\n"
        "If the episode was cancelled, set cancelled=true, games=[], "
        "and populate transcript with a stub (secretItems:[], rounds:[])."
    )

    user_prompt = f"""Import this Best Guess Live episode.

Episode date: {episode_date}
Video title: {video_title}

--- RAW TRANSCRIPT ---
{transcript_text}

--- GAMES SCHEMA (last 4 entries from games.json) ---
{schema_games}

--- TRANSCRIPT SCHEMA (last entry from transcripts.json) ---
{schema_transcript}

--- EXTRACTION RULES ---
1. Extract both rounds. Each game entry must match the games.json schema.
2. For v2 format: include goldClue, silverClue, bronzeClue (clue numbers 1–5),
   goldWinners, silverWinners, bronzeWinners, goldPayout, silverPayout, bronzePayout.
   totalWinners = goldWinners + silverWinners + bronzeWinners.
   winnerPayout = formatted pot string e.g. "$7,500.00".
3. The transcript must have exactly these six sections in order:
   Intro, Round 1, Round 1 Results, Round 2, Round 2 Results, Outro.
4. transcript.secretItems = [round1Item, round2Item].
5. transcript.rounds = [{{"round":1,"secretItem":"..."}},{{"round":2,"secretItem":"..."}}].
6. Each transcript line: {{"speaker": "Name or null", "text": "..."}}
7. Do NOT include HTML entities in text — use plain Unicode.
8. If a bonus/promo is announced for the week, add bonus:{{"title":"...","desc":"..."}}
   to BOTH game entries.

Respond with JSON only."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip accidental markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def apply_import(data: dict) -> bool:
    """
    Write parsed episode data into games.json and transcripts.json.
    Returns True if anything was written.
    """
    with open("data/games.json") as f:
        games = json.load(f)
    with open("data/transcripts.json") as f:
        transcripts = json.load(f)

    existing_keys = {(g["date"], g.get("secretItem")) for g in games}
    new_games = [
        g for g in data["games"]
        if (g["date"], g.get("secretItem")) not in existing_keys
    ]
    if not new_games and data["transcript"]["date"] in {t["date"] for t in transcripts}:
        print("Episode already present in data files — nothing to do.")
        return False

    games.extend(new_games)

    existing_transcript_dates = {t["date"] for t in transcripts}
    if data["transcript"]["date"] not in existing_transcript_dates:
        transcripts.append(data["transcript"])

    with open("data/games.json", "w") as f:
        json.dump(games, f, indent=2)
        f.write("\n")
    with open("data/transcripts.json", "w") as f:
        json.dump(transcripts, f, indent=2)
        f.write("\n")

    return True


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", help="Specific YouTube video ID to import")
    parser.add_argument("--dry-run", action="store_true", help="Parse but don't write files")
    args = parser.parse_args()

    if args.video_id:
        video_id = args.video_id
        episode_date = None
        video_title = f"https://youtu.be/{video_id}"
        print(f"Processing specified video: {video_id}")
    else:
        print("Fetching RSS feed…")
        videos = fetch_rss_videos()
        if not videos:
            print("No videos found in RSS feed.")
            sys.exit(0)

        imported_dates = get_imported_dates()
        pending = [
            (vid, title, dt, format_archive_date(dt))
            for vid, title, dt in videos
            if format_archive_date(dt) not in imported_dates
            and is_regular_episode(title)
        ]

        if not pending:
            print("No new regular episodes found (EXTRA/recap/bonus videos are skipped).")
            sys.exit(0)

        video_id, video_title, _dt, episode_date = pending[0]  # oldest first
        print(f"New episode: {episode_date} — {video_title}")

    print(f"Fetching transcript for {video_id}…")
    try:
        transcript_text = fetch_transcript(video_id)
    except Exception as exc:
        print(f"Transcript fetch failed: {exc}")
        sys.exit(1)

    print(f"Transcript: {len(transcript_text):,} chars / {len(transcript_text.splitlines())} lines")

    # If we didn't get the date from RSS, look it up now
    if not episode_date:
        for vid, _title, dt in fetch_rss_videos():
            if vid == video_id:
                episode_date = format_archive_date(dt)
                break
        if not episode_date:
            episode_date = "unknown"

    print("Calling Claude API…")
    try:
        data = call_claude(transcript_text, episode_date, video_title)
    except json.JSONDecodeError as exc:
        print(f"Claude returned invalid JSON: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Claude API error: {exc}")
        sys.exit(1)

    print(f"Episode date: {data.get('episode_date')}")
    print(f"Cancelled:    {data.get('cancelled', False)}")
    for g in data.get("games", []):
        print(f"  Round: {g.get('secretItem')} — {g.get('totalWinners')} winners")

    if args.dry_run:
        print("\n--- DRY RUN OUTPUT ---")
        print(json.dumps(data, indent=2))
        sys.exit(0)

    applied = apply_import(data)
    if not applied:
        sys.exit(0)

    print("Running audit:fix…")
    result = run(["npm", "run", "audit:fix"])
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)

    print("Running audit…")
    result = run(["npm", "run", "audit"])
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr)
        print("Audit failed — reverting data/ changes.")
        run(["git", "checkout", "data/"])
        sys.exit(1)

    print("Import complete.")


if __name__ == "__main__":
    main()
