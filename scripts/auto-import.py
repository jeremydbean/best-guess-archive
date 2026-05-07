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
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import anthropic
from youtube_transcript_api import YouTubeTranscriptApi

CHANNEL_ID = "UCcJVrF8GextFm229zgllU4w"
CHANNEL_RSS = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
CHANNEL_VIDEOS_URL = f"https://www.youtube.com/channel/{CHANNEL_ID}/videos"
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
EXPECTED_SECTIONS = ["Intro", "Round 1", "Round 1 Results", "Round 2", "Round 2 Results", "Outro"]
ALLOWED_BONUS_TAG_RE = re.compile(r"</?(?:br|b|strong)\s*/?>", re.IGNORECASE)
ANY_HTML_TAG_RE = re.compile(r"<[^>]+>")
TITLE_DATE_RE = re.compile(
    r"\(([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})\)"
)


def fetch_url(url: str) -> bytes:
    """Fetch YouTube pages with a browser-like user agent."""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=15) as resp:
        return resp.read()


def decode_json_text(value: str) -> str:
    """Decode a JSON string fragment captured from YouTube's page data."""
    try:
        return json.loads(f'"{value}"')
    except json.JSONDecodeError:
        return html.unescape(value)


def archive_datetime_from_title(title: str) -> datetime | None:
    """Extract dates from titles like 'Best Guess Live (April 28, 2026)'."""
    match = TITLE_DATE_RE.search(title or "")
    if not match:
        return None
    month_name, day, year = match.groups()
    try:
        month = MONTH_NAMES.index(month_name) + 1
    except ValueError:
        return None
    # Noon UTC keeps the calendar date stable after Eastern conversion.
    return datetime(int(year), month, int(day), 12, tzinfo=timezone.utc)


def fetch_channel_page_videos():
    """
    Return videos from the channel page when YouTube's RSS feed is unavailable.

    The Chris S channel titles include the show date, so this fallback can still
    produce stable archive dates without spending Claude/API credits first.
    """
    html_text = fetch_url(CHANNEL_VIDEOS_URL).decode("utf-8", errors="replace")
    videos = []
    seen = set()

    renderer_re = re.compile(
        r'"videoRenderer":\{"videoId":"([^"]+)".{0,6000}?'
        r'"title":\{"runs":\[\{"text":"((?:\\.|[^"\\])*)"',
        re.DOTALL,
    )
    for match in renderer_re.finditer(html_text):
        video_id = match.group(1)
        title = decode_json_text(match.group(2))
        published_dt = archive_datetime_from_title(title)
        if not published_dt or video_id in seen:
            continue
        seen.add(video_id)
        videos.append((video_id, title, published_dt))

    title_re = re.compile(r'"title":\{"runs":\[\{"text":"((?:\\.|[^"\\])*)"')
    for match in title_re.finditer(html_text):
        title = decode_json_text(match.group(1))
        published_dt = archive_datetime_from_title(title)
        if not published_dt:
            continue
        window = html_text[max(0, match.start() - 1500):match.end() + 2500]
        video_matches = list(re.finditer(r'"videoId":"([^"]+)"', window))
        video_match = min(
            video_matches,
            key=lambda m: abs((max(0, match.start() - 1500) + m.start()) - match.start()),
            default=None,
        )
        if not video_match:
            continue
        video_id = video_match.group(1)
        if video_id in seen:
            continue
        seen.add(video_id)
        videos.append((video_id, title, published_dt))
    videos.sort(key=lambda v: v[2])  # oldest first
    return videos


def fetch_rss_videos():
    """Return list of (video_id, title, published_dt) sorted oldest-first."""
    try:
        xml_data = fetch_url(CHANNEL_RSS)
    except urllib.error.HTTPError as exc:
        print(f"RSS feed unavailable ({exc.code}); falling back to channel page.")
        videos = []
        for attempt in range(1, 4):
            videos = fetch_channel_page_videos()
            if videos:
                return videos
            print(f"Channel page fallback returned no videos (attempt {attempt}/3).")
        return videos
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
            # Prefer the air date embedded in the title (e.g. "Best Guess Live (May 6, 2026)")
            # over the RSS publish date, which is often the following morning.
            title_dt = archive_datetime_from_title(title)
            episode_dt = title_dt if title_dt else published_dt
            videos.append((video_id, title, episode_dt))
    videos.sort(key=lambda v: v[2])  # oldest first
    return videos


def fetch_video_metadata(video_id: str) -> tuple[str, datetime | None]:
    """Return (title, published_dt) from a video page when RSS cannot be used."""
    page = fetch_url(f"https://www.youtube.com/watch?v={video_id}").decode("utf-8", errors="replace")
    title_match = re.search(r'"title":"((?:\\.|[^"\\])*)"', page)
    title = decode_json_text(title_match.group(1)) if title_match else f"https://youtu.be/{video_id}"
    publish_match = re.search(r'"(?:publishDate|uploadDate)":"([^"]+)"', page)
    if publish_match:
        return title, datetime.fromisoformat(publish_match.group(1))
    return title, archive_datetime_from_title(title)


def us_eastern_fallback(dt: datetime) -> datetime:
    """DST-aware Eastern conversion for Windows Python without tzdata installed."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    utc = dt.astimezone(timezone.utc)
    year = utc.year

    march_1 = datetime(year, 3, 1, tzinfo=timezone.utc)
    first_sunday_march = 1 + ((6 - march_1.weekday()) % 7)
    second_sunday_march = first_sunday_march + 7
    dst_start_utc = datetime(year, 3, second_sunday_march, 7, tzinfo=timezone.utc)

    nov_1 = datetime(year, 11, 1, tzinfo=timezone.utc)
    first_sunday_nov = 1 + ((6 - nov_1.weekday()) % 7)
    dst_end_utc = datetime(year, 11, first_sunday_nov, 6, tzinfo=timezone.utc)

    offset_hours = -4 if dst_start_utc <= utc < dst_end_utc else -5
    return utc + timedelta(hours=offset_hours)


def format_archive_date(dt: datetime) -> str:
    """Convert a datetime to 'Weekday, Month D, YYYY' archive format."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    try:
        local = dt.astimezone(ZoneInfo("America/New_York"))
    except ZoneInfoNotFoundError:
        local = us_eastern_fallback(dt)
    weekday = WEEKDAY_NAMES[local.weekday()]
    month = MONTH_NAMES[local.month - 1]
    return f"{weekday}, {month} {local.day}, {local.year}"


def get_imported_dates() -> set:
    """Return dates already present in games.json."""
    try:
        with open("data/games.json", encoding="utf-8") as f:
            return {g["date"] for g in json.load(f)}
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def load_skip_ids() -> set:
    """Load manually excluded video IDs from scripts/skip-videos.txt."""
    try:
        with open("scripts/skip-videos.txt", encoding="utf-8") as f:
            return {line.split("#")[0].strip() for line in f if line.split("#")[0].strip()}
    except FileNotFoundError:
        return set()


def is_best_guess_episode(title: str) -> bool:
    """Accept any video whose title contains 'Best Guess Live' (case-insensitive)."""
    return "best guess live" in (title or "").lower()


def fetch_transcript(video_id: str) -> str:
    """
    Fetch the YouTube auto-caption transcript and return it as plain text.

    Chunks are joined into sentences; [Music] / [Applause] tags are stripped.
    HTML entities are unescaped so the audit's escaped-entity check doesn't fire.

    If YOUTUBE_COOKIES env var is set (Netscape-format cookie file contents),
    it's written to a temp file and passed to the API — needed when running on
    cloud-provider IPs that YouTube blocks for unauthenticated requests.
    """
    cookie_file = None
    cookie_path = None
    cookies_env = os.environ.get("YOUTUBE_COOKIES", "").strip()
    if cookies_env:
        import tempfile
        cookie_file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
        cookie_file.write(cookies_env)
        cookie_file.close()
        cookie_path = cookie_file.name

    try:
        ytt_api = YouTubeTranscriptApi(cookie_path=cookie_path) if cookie_path else YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id, languages=["en"])
    finally:
        if cookie_path:
            os.unlink(cookie_path)
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
    Send the transcript to Claude and get back structured game data only.

    Returns a dict with keys: episode_date, cancelled, games.
    Transcript stub is generated separately by build_stub_transcript().
    """
    client = anthropic.Anthropic()

    with open("data/games.json", encoding="utf-8") as f:
        all_games = json.load(f)
    schema_games = json.dumps(all_games[-4:], indent=2)

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
        '  "games": [...]\n'
        "}\n\n"
        "If the episode was cancelled, set cancelled=true and games=[]."
    )

    user_prompt = f"""Import this Best Guess Live episode. Extract game data only — no transcript needed.

Episode date: {episode_date}
Video title: {video_title}

--- RAW TRANSCRIPT ---
{transcript_text}

--- GAMES SCHEMA (last 4 entries from games.json) ---
{schema_games}

--- EXTRACTION RULES ---
1. Extract both rounds. Each game entry must match the games.json schema exactly.
2. For v2 format: include goldClue, silverClue, bronzeClue (clue numbers 1–5),
   goldWinners, silverWinners, bronzeWinners, goldPayout, silverPayout, bronzePayout.
   totalWinners = goldWinners + silverWinners + bronzeWinners.
   winnerPayout = formatted pot string e.g. "$7,500.00".
3. Each game must include: date, secretItem, host, format, clues (5 items each with
   text in ALL CAPS, explanation, clue number, correct count), all medal fields,
   winnerNames, popularWrongGuesses.
4. Do NOT include HTML entities in text — use plain Unicode.
5. If a bonus/promo is announced for the week, add bonus:{{"title":"...","desc":"..."}}
   to BOTH game entries.

Respond with JSON only."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    usage = response.usage
    input_tok = usage.input_tokens
    output_tok = usage.output_tokens
    cost = (input_tok * 3.00 + output_tok * 15.00) / 1_000_000
    print(f"Tokens — input: {input_tok:,}  output: {output_tok:,}  estimated cost: ${cost:.4f}")

    raw = response.content[0].text.strip()
    # Strip accidental markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def loose(value) -> str:
    """Normalize answer strings for cross-file comparison."""
    return re.sub(r"[^A-Z0-9]+", "", str(value or "").upper())


def validate_bonus_html(desc: str, context: str) -> None:
    """Allow only the tiny formatting subset the app intentionally renders."""
    for tag in ANY_HTML_TAG_RE.findall(str(desc or "")):
        if not ALLOWED_BONUS_TAG_RE.fullmatch(tag):
            raise ValueError(f"{context} contains unsupported HTML tag: {tag}")


def validate_import_data(data: dict, expected_date: str | None) -> None:
    """Reject malformed Claude output before writing any archive files."""
    if not isinstance(data, dict):
        raise ValueError("Claude output must be a JSON object.")

    games = data.get("games")
    episode_date = data.get("episode_date")
    cancelled = bool(data.get("cancelled", False))

    if not isinstance(games, list):
        raise ValueError("games must be an array.")
    if expected_date and expected_date != "unknown" and episode_date != expected_date:
        raise ValueError(f"episode_date {episode_date!r} does not match expected date {expected_date!r}.")

    if cancelled:
        if games:
            raise ValueError("Cancelled episodes must not include playable games.")
        return

    if len(games) != 2:
        raise ValueError(f"Playable episodes must include exactly 2 games, got {len(games)}.")
    for index, game in enumerate(games, start=1):
        if game.get("date") != episode_date:
            raise ValueError(f"Game {index} date must match episode_date.")
        if not game.get("secretItem"):
            raise ValueError(f"Game {index} is missing secretItem.")
        clues = game.get("clues")
        if not isinstance(clues, list) or len(clues) != 5:
            raise ValueError(f"Game {index} must have exactly 5 clues.")
        for clue_index, clue in enumerate(clues, start=1):
            if not isinstance(clue, dict) or not clue.get("text"):
                raise ValueError(f"Game {index} clue {clue_index} is missing text.")
            if not str(clue.get("explanation") or "").strip():
                raise ValueError(f"Game {index} clue {clue_index} is missing explanation.")
        if game.get("format") == "v2":
            medal_clues = [int(game.get(k) or 0) for k in ("goldClue", "silverClue", "bronzeClue")]
            if any(n < 1 or n > 5 for n in medal_clues) or len(set(medal_clues)) != 3:
                raise ValueError(f"Game {index} v2 medal clue numbers must be distinct values 1-5.")
            winner_sum = sum(int(game.get(k) or 0) for k in ("goldWinners", "silverWinners", "bronzeWinners"))
            if winner_sum != int(game.get("totalWinners") or 0):
                raise ValueError(f"Game {index} totalWinners must equal medal winner sum.")
        bonus = game.get("bonus")
        if bonus:
            if not isinstance(bonus, dict) or not bonus.get("title") or not bonus.get("desc"):
                raise ValueError(f"Game {index} bonus must include title and desc.")
            validate_bonus_html(bonus.get("desc", ""), f"Game {index} bonus.desc")


def build_stub_transcript(episode_date: str, games: list) -> dict:
    """Build a placeholder transcript with clue recap lines populated in Results sections."""

    def _winner_int(val) -> int:
        return int(str(val).replace(",", ""))

    def _medal_part(label: str, clue_num: int, count: int, payout) -> str:
        amount = f"${float(payout):,.2f}"
        if count == 1:
            return f"{label} (Clue {clue_num}): 1 winner at {amount}"
        return f"{label} (Clue {clue_num}): {count} winners at {amount} each"

    def _results_lines(game: dict) -> list:
        clues = game.get("clues", [])
        lines = []
        for i in range(len(clues) - 1, -1, -1):  # Clue 5 → Clue 1
            clue = clues[i]
            clue_num = i + 1
            lines.append({
                "speaker": None,
                "text": (
                    f'Clue {clue_num}: "{clue.get("text", "")}." '
                    f'{clue.get("explanation", "")} '
                    f'{clue.get("correct", "?")} got it right.'
                ),
            })
        gc = int(game.get("goldClue", 1))
        sc = int(game.get("silverClue", 2))
        bc = int(game.get("bronzeClue", 3))
        summary = ". ".join([
            _medal_part("Gold",   gc, _winner_int(game.get("goldWinners",   0)), game.get("goldPayout",   0)),
            _medal_part("Silver", sc, _winner_int(game.get("silverWinners", 0)), game.get("silverPayout", 0)),
            _medal_part("Bronze", bc, _winner_int(game.get("bronzeWinners", 0)), game.get("bronzePayout", 0)),
        ]) + "."
        lines.append({"speaker": None, "text": summary})
        return lines

    secret_items = [g.get("secretItem", "") for g in games]
    rounds = [{"round": i + 1, "secretItem": item} for i, item in enumerate(secret_items)]
    note = "Transcript not yet imported." if games else "Episode cancelled — no playable games."

    sections = [{"tag": "Intro", "lines": [{"speaker": None, "text": note}]}]
    for tag in ["Round 1", "Round 1 Results", "Round 2", "Round 2 Results"]:
        if "Results" in tag:
            idx = 0 if "1" in tag else 1
            game = games[idx] if idx < len(games) else None
            lines = _results_lines(game) if game else []
        else:
            lines = []
        sections.append({"tag": tag, "lines": lines})
    sections.append({"tag": "Outro", "lines": []})

    return {
        "date": episode_date,
        "secretItems": secret_items,
        "rounds": rounds,
        "sections": sections,
    }


def apply_import(data: dict) -> bool:
    """
    Write parsed episode data into games.json and transcripts.json.
    Returns True if anything was written.
    """
    with open("data/games.json", encoding="utf-8") as f:
        games = json.load(f)
    with open("data/transcripts.json", encoding="utf-8") as f:
        transcripts = json.load(f)

    existing_keys = {(g["date"], g.get("secretItem")) for g in games}
    new_games = [
        g for g in data["games"]
        if (g["date"], g.get("secretItem")) not in existing_keys
    ]
    episode_date = data["episode_date"]
    existing_transcript_dates = {t["date"] for t in transcripts}

    if not new_games and episode_date in existing_transcript_dates:
        print("Episode already present in data files — nothing to do.")
        return False

    games.extend(new_games)

    if episode_date not in existing_transcript_dates:
        transcripts.append(build_stub_transcript(episode_date, data.get("games", [])))

    with open("data/games.json", "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open("data/transcripts.json", "w", encoding="utf-8") as f:
        json.dump(transcripts, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return True


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    resolved = cmd[:]
    executable = shutil.which(cmd[0])
    if executable:
        resolved[0] = executable
    else:
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=127,
            stdout="",
            stderr=(
                f"Required command not found: {cmd[0]}. "
                "Install Node.js/npm or ensure actions/setup-node ran before auto-import."
            ),
        )
    return subprocess.run(resolved, capture_output=True, text=True, shell=False)


def restore_data_files() -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "checkout", "--", "data/games.json", "data/games-meta.json", "data/transcripts.json"],
        capture_output=True,
        text=True,
        shell=False,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", help="Specific YouTube video ID to import")
    parser.add_argument("--dry-run", action="store_true", help="Parse but don't write files")
    args = parser.parse_args()

    imported_dates = get_imported_dates()

    if args.video_id:
        video_id = args.video_id
        episode_date = None
        video_title = f"https://youtu.be/{video_id}"
        # Resolve date from RSS/channel listing so we can check if already imported.
        for vid, title, dt in fetch_rss_videos():
            if vid == video_id:
                episode_date = format_archive_date(dt)
                video_title = title
                break
        if not episode_date:
            video_title, published_dt = fetch_video_metadata(video_id)
            if published_dt:
                episode_date = format_archive_date(published_dt)
        if episode_date and episode_date in imported_dates:
            print(f"{episode_date} is already in the archive. No API credits used.")
            sys.exit(0)
        episodes_to_import = [(video_id, video_title, None, episode_date)]
    else:
        print("Fetching RSS feed…")
        videos = fetch_rss_videos()
        if not videos:
            print("No videos found in RSS feed.")
            sys.exit(0)

        skip_ids = load_skip_ids()
        pending = [
            (vid, title, dt, format_archive_date(dt))
            for vid, title, dt in videos
            if format_archive_date(dt) not in imported_dates
            and is_best_guess_episode(title)
            and vid not in skip_ids
        ]

        if not pending:
            # No new videos — exits before any API call.
            print("No new Best Guess Live episodes found. No API credits used.")
            sys.exit(0)

        print(f"Found {len(pending)} episode(s) to import.")
        # Process oldest-first so a late upload is caught the next day
        # alongside the new episode without manual backfill.
        episodes_to_import = pending

    any_imported = False
    for video_id, video_title, _dt, episode_date in episodes_to_import:
        print(f"\n--- {episode_date} — {video_title} ---")

        print(f"Fetching transcript for {video_id}…")
        try:
            transcript_text = fetch_transcript(video_id)
        except Exception as exc:
            print(f"Transcript fetch failed: {exc}")
            sys.exit(1)

        print(f"Transcript: {len(transcript_text):,} chars / {len(transcript_text.splitlines())} lines")

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

        try:
            validate_import_data(data, episode_date)
        except ValueError as exc:
            print(f"Claude output failed validation: {exc}")
            sys.exit(1)

        print(f"Episode date: {data.get('episode_date')}")
        print(f"Cancelled:    {data.get('cancelled', False)}")
        for g in data.get("games", []):
            print(f"  Round: {g.get('secretItem')} — {g.get('totalWinners')} winners")

        if args.dry_run:
            print("\n--- DRY RUN OUTPUT ---")
            print(json.dumps(data, indent=2))
            continue

        applied = apply_import(data)
        if applied:
            any_imported = True

    if args.dry_run:
        sys.exit(0)

    if not any_imported:
        sys.exit(0)

    print("\nRunning audit:fix…")
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
        restore_result = restore_data_files()
        if restore_result.returncode != 0:
            print(restore_result.stderr)
        sys.exit(1)

    print("All imports complete.")


if __name__ == "__main__":
    main()
