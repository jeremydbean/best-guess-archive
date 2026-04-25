#!/usr/bin/env python3
"""Import show transcripts from the exported Google Docs .docx file.

The source document includes clue summaries and appendix tables around each
transcript. This importer keeps only the paragraphs under each episode's
"Show Transcript" heading and stops at the next table/appendix heading.

Doc structure per episode:
  [Title]    🎉 WEEKDAY, MONTH DAY, YEAR   ← authoritative date (may have emoji)
  [Heading1] WEEKDAY, MONTH DAY, YEAR      ← sometimes mis-typed; skipped in favour of Title
  ... clue/answer section ...
  [Heading1 or Heading3] Show Transcript   ← Heading3 used in early January 2026 episodes
  ... transcript lines ...
  [Title]    next episode                  ← terminates content
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
DATE_RE = re.compile(
    r"^(?:[\W_]+\s*)?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"\d{1,2},\s+\d{4}$",
    re.IGNORECASE,
)
SECTION_RE = re.compile(r"^\[(.+)\]$")
TIMESTAMP_RE = re.compile(r"^\[\d{1,2}:\d{2}(?::\d{2})?\]$")
SPEAKER_RE = re.compile(r"^([^:]{1,40}):\s*(.+)$")
STOP_HEADINGS = {
    "Explanation Table",
    "Clue & Answer Results Table (Google Sheets Ready)",
    "Clue & Answer Results Table",
    "Results Table",
    "JSON",
    "JSON Data",
}
CANONICAL_SECTION_TAGS = (
    "Intro",
    "Round 1",
    "Round 1 Reveal",
    "Round 2",
    "Round 2 Reveal",
    "Outro",
)
PREFACE_RE = re.compile(r"^Here is the (?:full|formatted) transcript", re.IGNORECASE)
DATE_CORRECTIONS = {
    # The exported transcript doc has this MANICURE/COASTER episode misdated.
    "Wednesday, February 5, 2025": "Thursday, February 5, 2026",
}


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()


def paragraph_style(paragraph: ET.Element) -> str | None:
    style = paragraph.find("./w:pPr/w:pStyle", NS)
    if style is None:
        return None
    return style.attrib.get(f"{{{NS['w']}}}val")


def iter_paragraphs(docx_path: Path) -> list[dict[str, str | None]]:
    with ZipFile(docx_path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))

    paragraphs: list[dict[str, str | None]] = []
    for paragraph in root.findall(".//w:body/w:p", NS):
        text = paragraph_text(paragraph)
        if text:
            paragraphs.append({"style": paragraph_style(paragraph), "text": text})
    return paragraphs


def normalize_date(text: str) -> str:
    match = re.search(
        r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
        r"\d{1,2},\s+\d{4}",
        text,
        re.IGNORECASE,
    )
    if not match:
        return text.strip()
    parsed = datetime.strptime(match.group(0).title(), "%A, %B %d, %Y")
    normalized = parsed.strftime(f"%A, %B {parsed.day}, %Y")
    return DATE_CORRECTIONS.get(normalized, normalized)


def is_title_date(paragraph: dict[str, str | None]) -> bool:
    """Return True only for Title-style date headings (the authoritative date source)."""
    return paragraph["style"] == "Title" and bool(DATE_RE.match(normalize_date(str(paragraph["text"]))))


def is_any_date_heading(paragraph: dict[str, str | None]) -> bool:
    """Return True for Title or Heading1 date headings."""
    text = normalize_date(str(paragraph["text"]))
    return paragraph["style"] in {"Title", "Heading1"} and bool(DATE_RE.match(text))


def is_likely_speaker(candidate: str) -> bool:
    words = [word.strip(".") for word in candidate.split()]
    if not 1 <= len(words) <= 4:
        return False
    if words[0] in {"And", "Anyway", "Bottom", "But", "Clue", "Here", "Okay", "On", "Puzzle", "So", "The", "Time", "Which"}:
        return False
    return all(word and (word[0].isupper() or word.isupper()) for word in words)


def line_from_text(text: str) -> dict[str, str | None]:
    speaker_match = SPEAKER_RE.match(text)
    if speaker_match and is_likely_speaker(speaker_match.group(1)):
        return {"speaker": speaker_match.group(1), "text": speaker_match.group(2)}
    return {"speaker": None, "text": text}


def compact_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def contains_compact(text: str, needle: str | None) -> bool:
    compact_needle = compact_key(needle or "")
    return bool(compact_needle) and compact_needle in compact_key(text)


def is_stub_game(game: dict[str, Any]) -> bool:
    return bool(game.get("note") and not game.get("clues"))


def load_games_by_date(games_path: Path) -> dict[str, list[dict[str, Any]]]:
    if not games_path.exists():
        return {}
    games = json.loads(games_path.read_text())
    by_date: dict[str, list[dict[str, Any]]] = {}
    for game in games:
        by_date.setdefault(str(game.get("date", "")), []).append(game)
    return by_date


def unique_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        clean = str(value or "").strip()
        if clean and clean not in seen:
            unique.append(clean)
            seen.add(clean)
    return unique


def transcript_metadata(date: str, games_by_date: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    games = games_by_date.get(date, [])
    playable = [game for game in games if not is_stub_game(game)]
    host_games = playable or games
    hosts = unique_values([str(game.get("host", "")) for game in host_games])
    rounds = [
        {
            "round": index,
            "secretItem": game.get("secretItem", ""),
            "host": game.get("host", ""),
            "pot": game.get("pot", 0),
            "format": game.get("format", ""),
            "clues": [clue.get("text", "") for clue in game.get("clues", [])],
        }
        for index, game in enumerate(playable, start=1)
    ]
    return {
        "host": ", ".join(hosts),
        "secretItems": [round_info["secretItem"] for round_info in rounds],
        "rounds": rounds,
    }


def should_skip_transcript_line(line: dict[str, str | None]) -> bool:
    speaker = str(line.get("speaker") or "").strip().lower()
    text = str(line.get("text") or "").strip()
    if speaker == "host":
        return True
    return bool(PREFACE_RE.match(text))


def canonical_tag(tag: str | None) -> str | None:
    key = re.sub(r"[^a-z0-9]+", " ", str(tag or "").lower()).strip()
    mapping = {
        "intro": "Intro",
        "round 1": "Round 1",
        "round one": "Round 1",
        "reveal round 1": "Round 1 Reveal",
        "round 1 reveal": "Round 1 Reveal",
        "round 1 recap": "Round 1 Reveal",
        "reveal round one": "Round 1 Reveal",
        "round one reveal": "Round 1 Reveal",
        "round one recap": "Round 1 Reveal",
        "round 2": "Round 2",
        "round two": "Round 2",
        "reveal round 2": "Round 2 Reveal",
        "round 2 reveal": "Round 2 Reveal",
        "round 2 recap": "Round 2 Reveal",
        "reveal round two": "Round 2 Reveal",
        "round two reveal": "Round 2 Reveal",
        "round two recap": "Round 2 Reveal",
        "outro": "Outro",
        "outtro": "Outro",
    }
    return mapping.get(key)


def text_for_line(line: dict[str, str | None]) -> str:
    speaker = line.get("speaker")
    text = line.get("text") or ""
    return f"{speaker}: {text}" if speaker else text


def contains_item(text: str, item: str | None) -> bool:
    return contains_compact(text, item)


def round_clues(round_info: dict[str, Any] | None) -> list[str]:
    if not round_info:
        return []
    return [str(clue or "") for clue in round_info.get("clues", []) if str(clue or "").strip()]


def line_mentions_clue(text: str, clue: str | None) -> bool:
    return contains_compact(text, clue)


def is_round_start(text: str, round_number: int) -> bool:
    low = text.lower()
    names = ("one", "1") if round_number == 1 else ("two", "2")
    if any(f"round {name}" in low for name in names):
        return any(token in low for token in ("worth", "let's play", "lets play", "load", "prize", "start"))
    if round_number == 1:
        return bool(re.search(r"\b(first clue|clue number one|clue 1)\b", low))
    return False


def is_reveal_start(text: str, item: str | None) -> bool:
    low = text.lower()
    if contains_item(text, item) and any(token in low for token in (
        "answer",
        "crystal ball",
        "how the clues fit",
        "what the clues mean",
        "clue number five",
    )):
        return True
    return any(token in low for token in (
        "inside the crystal ball",
        "open the crystal ball",
        "reveal what",
        "correct answer",
        "answer was",
        "let's take a look at how the clues fit",
        "lets take a look at how the clues fit",
    ))


def is_outro_start(text: str) -> bool:
    low = text.lower()
    return any(token in low for token in (
        "that's it for this episode",
        "that is it for this episode",
        "congratulations again",
        "we're here every weekday",
        "we are here every weekday",
        "come back",
        "good night",
        "see you tomorrow",
    ))


def find_index(lines: list[dict[str, str | None]], start: int, predicate: Any) -> int | None:
    for index in range(max(start, 0), len(lines)):
        if predicate(text_for_line(lines[index])):
            return index
    return None


def find_clue_index(lines: list[dict[str, str | None]], start: int, clue: str | None) -> int | None:
    if not clue:
        return None
    return find_index(lines, start, lambda text: line_mentions_clue(text, clue))


def backtrack_round_start(lines: list[dict[str, str | None]], clue_index: int) -> int:
    start = clue_index
    for index in range(clue_index - 1, max(-1, clue_index - 3), -1):
        low = text_for_line(lines[index]).lower()
        if any(token in low for token in (
            "$10,000",
            "$5,000",
            "10,000",
            "5,000",
            "first clue",
            "last chance",
            "load the crystal",
            "round number two",
            "round one",
            "round 1",
            "round 2",
            "round two",
            "you know how it works",
        )):
            start = index
    return start


def find_reveal_index(
    lines: list[dict[str, str | None]],
    start: int,
    round_info: dict[str, Any] | None,
) -> int | None:
    clues = round_clues(round_info)
    search_start = start
    if clues:
        final_clue = find_clue_index(lines, start, clues[-1])
        if final_clue is not None:
            search_start = final_clue + 1
    return find_index(lines, search_start, lambda text: is_reveal_start(text, round_info.get("secretItem") if round_info else None))


def empty_section_map() -> dict[str, list[dict[str, str | None]]]:
    return {tag: [] for tag in CANONICAL_SECTION_TAGS}


def sections_from_map(section_map: dict[str, list[dict[str, str | None]]]) -> list[dict[str, Any]]:
    return [{"tag": tag, "lines": section_map[tag]} for tag in CANONICAL_SECTION_TAGS]


def finalize_section_map(section_map: dict[str, list[dict[str, str | None]]]) -> list[dict[str, Any]]:
    if not section_map["Outro"] and section_map["Round 2 Reveal"]:
        outro_index = find_index(section_map["Round 2 Reveal"], 0, is_outro_start)
        if outro_index is not None:
            section_map["Outro"] = section_map["Round 2 Reveal"][outro_index:]
            section_map["Round 2 Reveal"] = section_map["Round 2 Reveal"][:outro_index]
    return sections_from_map(section_map)


def split_unsectioned_transcript(
    lines: list[dict[str, str | None]],
    rounds: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lines = [line for line in lines if not should_skip_transcript_line(line)]
    if not lines:
        return sections_from_map(empty_section_map())

    first_round = rounds[0] if len(rounds) >= 1 else None
    second_round = rounds[1] if len(rounds) >= 2 else None
    first_clues = round_clues(first_round)
    second_clues = round_clues(second_round)

    r1_clue = find_clue_index(lines, 0, first_clues[0] if first_clues else None)
    r1 = backtrack_round_start(lines, r1_clue) if r1_clue is not None else None
    if r1 is None:
        r1 = find_index(lines, 0, lambda text: is_round_start(text, 1))
    if r1 is None:
        section_map = empty_section_map()
        section_map["Intro"] = lines
        return sections_from_map(section_map)

    reveal1 = find_reveal_index(lines, r1 + 1, first_round)
    if reveal1 is None:
        reveal1 = len(lines)

    r2_clue = find_clue_index(lines, reveal1 + 1, second_clues[0] if second_clues else None)
    r2 = backtrack_round_start(lines, r2_clue) if r2_clue is not None else None
    if r2 is None:
        r2 = find_index(lines, reveal1 + 1, lambda text: is_round_start(text, 2))
    if r2 is None:
        r2 = len(lines)

    reveal2 = find_reveal_index(lines, r2 + 1, second_round)
    if reveal2 is None:
        reveal2 = len(lines)

    outro = find_index(lines, reveal2 + 1, is_outro_start)
    if outro is None:
        outro = len(lines)

    section_map = empty_section_map()
    section_map["Intro"] = lines[:r1]
    section_map["Round 1"] = lines[r1:reveal1]
    section_map["Round 1 Reveal"] = lines[reveal1:r2]
    section_map["Round 2"] = lines[r2:reveal2]
    section_map["Round 2 Reveal"] = lines[reveal2:outro]
    section_map["Outro"] = lines[outro:]
    return finalize_section_map(section_map)


def standardize_sections(
    sections: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if len(sections) == 1 and sections[0].get("tag") == "Transcript":
        return split_unsectioned_transcript(sections[0].get("lines", []), rounds)

    section_map = empty_section_map()
    current = "Intro"
    for section in sections:
        mapped = canonical_tag(section.get("tag"))
        if mapped:
            current = mapped
        lines = [line for line in section.get("lines", []) if not should_skip_transcript_line(line)]
        section_map[current].extend(lines)
    return finalize_section_map(section_map)


def enrich_transcripts(
    transcripts: list[dict[str, Any]],
    games_by_date: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for transcript in transcripts:
        date = transcript["date"]
        metadata = transcript_metadata(date, games_by_date)
        enriched.append({
            "date": date,
            **metadata,
            "sections": standardize_sections(transcript.get("sections", []), metadata["rounds"]),
        })
    return enriched


def parse_transcripts(paragraphs: list[dict[str, str | None]]) -> list[dict[str, Any]]:
    transcripts: list[dict[str, Any]] = []
    i = 0
    while i < len(paragraphs):
        paragraph = paragraphs[i]

        # Only Title-style date headings start a new transcript.
        # Heading1 date headings are skipped here — they follow immediately after
        # the Title and can be mis-typed in the doc; the Title is authoritative.
        if not is_title_date(paragraph):
            i += 1
            continue

        date = normalize_date(str(paragraph["text"]))
        i += 1

        # Skip the Heading1 (or plain-text) date line that immediately follows
        # the Title. It may have a different (incorrect) date, so we ignore it.
        if i < len(paragraphs):
            nxt = paragraphs[i]
            nxt_date = normalize_date(str(nxt["text"]))
            if nxt["style"] in ("Heading1", None) and DATE_RE.match(nxt_date):
                i += 1

        # Scan forward for "Show Transcript" marker.
        # Later episodes use Heading1; early Jan 2026 use Heading3; Jan 13 uses plain None style.
        while i < len(paragraphs):
            para = paragraphs[i]
            if is_title_date(para):
                break  # next episode — no transcript found for this date
            if para["text"] == "Show Transcript":
                break
            i += 1

        if i >= len(paragraphs) or paragraphs[i]["text"] != "Show Transcript":
            continue

        i += 1
        sections: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None

        while i < len(paragraphs):
            paragraph = paragraphs[i]
            text = str(paragraph["text"])

            if is_title_date(paragraph):
                break
            if paragraph["style"] in ("Heading1", "Heading3") and text in STOP_HEADINGS:
                break

            # Skip intro summary line (with or without leading curly/straight quote)
            stripped = text.lstrip('“‘”’"\'')
            if stripped.startswith("Here is the full transcript"):
                i += 1
                continue

            # Skip bare timestamp lines like [02:34] or [00:01:05]
            if TIMESTAMP_RE.match(text):
                i += 1
                continue

            section_match = SECTION_RE.match(text)
            if section_match:
                tag = section_match.group(1)
                # Skip timestamp-only section tags e.g. [02:34]
                if not TIMESTAMP_RE.match(text):
                    current = {"tag": tag, "lines": []}
                    sections.append(current)
                i += 1
                continue

            if current is None:
                current = {"tag": "Transcript", "lines": []}
                sections.append(current)
            current["lines"].append(line_from_text(text))
            i += 1

        if sections:
            transcripts.append({"date": date, "sections": sections})

    return transcripts


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: import_transcripts_from_docx.py SOURCE.docx data/transcripts.json", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    transcripts = parse_transcripts(iter_paragraphs(source))
    games_by_date = load_games_by_date(destination.parent / "games.json")
    transcripts = enrich_transcripts(transcripts, games_by_date)

    if not transcripts:
        print("No transcripts found.", file=sys.stderr)
        return 1

    dates = [transcript["date"] for transcript in transcripts]
    duplicate_dates = sorted(date for date in set(dates) if dates.count(date) > 1)
    if duplicate_dates:
        print(f"Duplicate transcript dates found: {', '.join(duplicate_dates)}", file=sys.stderr)
        return 1

    destination.write_text(json.dumps(transcripts, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(transcripts)} transcripts to {destination}")
    print(f"First: {transcripts[0]['date']}")
    print(f"Last: {transcripts[-1]['date']}")
    if games_by_date:
        game_dates = set(games_by_date)
        transcript_dates = set(dates)
        missing = sorted(game_dates - transcript_dates)
        extra = sorted(transcript_dates - game_dates)
        print(f"Coverage: {len(transcript_dates & game_dates)} of {len(game_dates)} game dates")
        if missing:
            print(f"Missing game dates: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"Transcript dates without games: {', '.join(extra)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
