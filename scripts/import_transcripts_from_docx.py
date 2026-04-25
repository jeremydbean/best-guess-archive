#!/usr/bin/env python3
"""Import show transcripts from the exported Google Docs .docx file.

The source document includes clue summaries and appendix tables around each
transcript. This importer keeps only the paragraphs under each episode's
"Show Transcript" heading and stops at the next table/appendix heading.
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
SPEAKER_RE = re.compile(r"^([A-Z][A-Za-z .'\-]+):\s*(.+)$")
STOP_HEADINGS = {
    "Explanation Table",
    "Clue & Answer Results Table (Google Sheets Ready)",
    "Clue & Answer Results Table",
    "JSON",
    "JSON Data",
}
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
    # The doc uses decorative emoji on Title paragraphs. Strip those while
    # keeping the real date text untouched.
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


def is_date_heading(paragraph: dict[str, str | None]) -> bool:
    text = normalize_date(str(paragraph["text"]))
    return paragraph["style"] in {"Title", "Heading1"} and bool(DATE_RE.match(text))


def line_from_text(text: str) -> dict[str, str | None]:
    speaker_match = SPEAKER_RE.match(text)
    if speaker_match:
        return {"speaker": speaker_match.group(1), "text": speaker_match.group(2)}
    return {"speaker": None, "text": text}


def parse_transcripts(paragraphs: list[dict[str, str | None]]) -> list[dict[str, Any]]:
    transcripts: list[dict[str, Any]] = []
    i = 0
    while i < len(paragraphs):
        paragraph = paragraphs[i]
        if not is_date_heading(paragraph):
            i += 1
            continue

        date = normalize_date(str(paragraph["text"]))
        i += 1

        while i < len(paragraphs) and not is_date_heading(paragraphs[i]):
            if paragraphs[i]["style"] == "Heading1" and paragraphs[i]["text"] == "Show Transcript":
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

            if is_date_heading(paragraph):
                break
            if paragraph["style"] == "Heading1" and text in STOP_HEADINGS:
                break

            section_match = SECTION_RE.match(text)
            if section_match:
                current = {"tag": section_match.group(1), "lines": []}
                sections.append(current)
                i += 1
                continue

            if text.startswith("Here is the full transcript"):
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

    if not transcripts:
        print("No transcripts found.", file=sys.stderr)
        return 1

    destination.write_text(json.dumps(transcripts, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(transcripts)} transcripts to {destination}")
    print(f"First: {transcripts[0]['date']}")
    print(f"Last: {transcripts[-1]['date']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
