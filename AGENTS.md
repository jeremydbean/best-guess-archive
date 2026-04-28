# Agent Workflow

This repository uses a main-only workflow and is often edited by more than one coding agent.

## Before You Start

- Read `AI_HANDOFF.md`.
- Run `git fetch origin`.
- Compare local `main` to `origin/main`.
- If `origin/main` moved, sync before editing:

```bash
git pull --rebase origin main
```

## Branch Rules

- Work directly on `main`.
- Commit directly on `main`.
- Push directly to `origin/main`.
- Do not create feature branches, backup branches, or PR branches unless the owner explicitly asks.
- Do not leave non-main remote branches behind. If one exists and its commits are already on `main`, delete it before handoff.

## Handoff Rules

- Treat every push to `main` as a live-site deploy.
- Keep `AI_HANDOFF.md` current.
- When handing off, record:
  - latest commit hash
  - what changed
  - anything still in progress
  - anything another agent should verify

## Practical Preference

- Prefer small, clean commits.
- If another agent has pushed since you started, sync first instead of guessing.
- If you see unexpected changes, assume they may be intentional and avoid reverting them unless explicitly asked.

---

## Daily Game Import Procedure

Preferred path for raw transcript imports:
- Save the raw dump as `incoming/YYYY-MM-DD.txt`.
- Use `docs/DAILY_IMPORT_PROMPT.md` as the agent prompt/checklist.
- Use `docs/IMPORT_REPORT_TEMPLATE.md` when a fuller import report is useful.

When the user pastes a `=== DAILY GAME UPDATE ===` block, do the following in order:

### 1. Parse the paste

Extract from the paste:
- DATE, HOST
- ROUND 1: secretItem, 5 clues (text/correct/guesses), goldClue/silverClue/bronzeClue, winner counts, payouts, winner names, wrong guesses, clue explanations
- ROUND 2: same fields
- SPECIAL PROMO (optional): title + description
- TRANSCRIPT: the labeled dialogue block

### 2. Build two game objects (one per round)

Use the schema in `AI_HANDOFF.md`. Always `format: "v2"` and `pot: 7500` unless the user specifies otherwise.

Medal emoji in the `guesses` field: append ` 🥇` after the number for gold clue, ` 🥈` for silver, ` 🥉` for bronze. Non-winner clues have no emoji.

`winnerPayout` is typically `"$7,500.00"` (full pot to gold winners in v2).

`bonus` field: only include if SPECIAL PROMO section is present.
If a promo applies to the whole episode, add the same `bonus` object to both round objects.

### 3. Update data/games.json

Append the two new game objects to the END of the array. Do not prepend.

### 4. Regenerate data/games-meta.json

Run or replicate this logic:
```python
import json
with open('data/games.json') as f:
    games = json.load(f)
meta = []
for g in games:
    entry = {
        "date": g["date"], "secretItem": g["secretItem"],
        "pot": g["pot"], "host": g.get("host"), "format": g.get("format"),
        "totalWinners": g.get("totalWinners", 0),
        "clueCount": len(g.get("clues", []))
    }
    if g.get("note"): entry["note"] = g["note"]
    meta.append(entry)
with open('data/games-meta.json', 'w') as f:
    json.dump(meta, f, indent=2)
```

### 5. Add transcript entry to data/transcripts.json

Build a new transcript object with:
- `date`, `host`, `secretItems` (array of both round answers)
- `rounds` array (one object per round with round number, secretItem, host, pot, format, clues list)
- `sections` array: exactly 6 sections in order: `Intro`, `Round 1`, `Round 1 Results`, `Round 2`, `Round 2 Results`, `Outro`

Split the TRANSCRIPT dialogue into these sections by looking for round start/results cues. Each section has `tag` and `lines` array; each line has `speaker` (string or null) and `text`.

Append the new entry to the END of the `transcripts.json` array.

### 6. Commit all changes

```bash
npm run audit
git add data/games.json data/games-meta.json data/transcripts.json
git commit -m "Import [DATE]: [ROUND1_ANSWER] and [ROUND2_ANSWER]"
git push -u origin main
```

### Cancelled Episode

If the paste says `CANCELLED`, create one stub game:
```json
{
  "date": "...", "pot": 0, "format": "v2", "host": "...",
  "secretItem": "", "clues": [], "totalWinners": 0,
  "winnerPayout": "", "winnerNames": "", "wrongGuesses": "",
  "note": "No game played."
}
```
Also add a transcript entry with empty round content, `secretItems: []`, `rounds: []`, and the same six canonical section tags used by playable episodes.

### Validation Checks

Before committing, verify:
- `npm run audit` passes with 0 errors.
- Both games have exactly 5 clues.
- `totalWinners` == `goldWinners` + `silverWinners` + `bronzeWinners`.
- Gold/silver/bronze clue numbers are distinct integers 1–5.
- New transcript has exactly 6 sections in the correct order.
- `data/games-meta.json` entry count matches `data/games.json` entry count.
