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

Use the schema in `AI_HANDOFF.md`. Use `pot: 7500` unless the user specifies otherwise.

**Format rules by date:**
- Before Monday, May 11, 2026: both rounds are normally `format: "v2"` unless the episode says otherwise.
- Monday, May 11, 2026 through Tuesday, May 26, 2026: hybrid format — Round 1 is `format: "v2"` tiered gold/silver/bronze, Round 2 is `format: "v1"` classic mode (earliest correct clue splits the full $7,500 pot).
- Starting Wednesday, May 27, 2026: both rounds use `format: "v2"` tiered gold/silver/bronze (announced on the May 25, 2026 episode). Each round has three pools: gold $3,000, silver $2,500, bronze $2,000.

**Secret item article rule**: Strip leading "A" and "AN" from `secretItem` values (e.g. Gemini says "AN ELEPHANT" → store as "ELEPHANT"). Keep "THE" only when it is semantically part of the answer (e.g. "THE MIDDLE SEAT" stays as-is).

**Payout math**: Never trust Gemini's payout figures. Always pre-calculate using `Math.floor(value * 100) / 100`. goldPayout = floorCents(3000 / goldWinners), silverPayout = floorCents(2500 / silverWinners), bronzePayout = floorCents(2000 / bronzeWinners), v1 per-winner = floorCents(7500 / winnerCount).

**Gemini date rule**: Gemini consistently dates transcripts one day ahead of the actual game date. Always verify both the weekday name and day number against a calendar. The host usually states the day in the intro. Correct the date before importing.

**winningClue for v1 with zero-correct early clues**: Set `winningClue` to the earliest clue where `correct > 0`. If clues 1 and 2 had 0 correct and clue 3 was the first correct clue, set `winningClue: 3`.

**Curly quotes in JSON**: Null-speaker transcript annotation lines use Unicode curly quotes (`"…"`). Use Python `content.replace()` for edits — `sed` straight-quote patterns will not match.

Medal emoji in the `guesses` field: append ` 🥇` after the number for the gold clue, ` 🥈` for the silver clue, and ` 🥉` for the bronze clue. Non-winner clues have no emoji. Every playable round still has exactly five clue objects. If a tier had no winners, set that tier's winner count and payout to `0`; omit that tier's medal clue field or set it to `0`.

Unknown counts in an otherwise-complete round use the literal string `"N/A"` — this is distinct from a `dataStatus: "partial"` record, which uses JSON `null`. **Never append a medal emoji to an `"N/A"` value**: the audit parses that field as a number and ` 🥉` on a non-numeric value fails `count-value`. Nothing is lost by leaving it bare, since the tier is already recorded in `goldClue`/`silverClue`/`bronzeClue` and the emoji is only a display marker.

`winnerPayout` is typically `"$7,500.00"` for v2 rounds. Do not change it to a per-tier amount when a silver or bronze pool is redistributed.

For Round 2 classic mode, set `winningClue` to the earliest clue with correct answers, set `winnerCount` and `totalWinners` to that clue's correct count, and set `winnerPayout` to the per-winner share of the full round pot. Keep `goldClue` equal to `winningClue` for compatibility, and set `goldWinners`, `silverWinners`, `bronzeWinners`, `goldPayout`, `silverPayout`, and `bronzePayout` to `0`.

No-winner redistribution rule: empty medal tiers cascade from the bottom upward. If bronze has no winners, set `bronzeWinners: 0`, `bronzePayout: 0`, and no `bronzeClue` medal field; the $2,000 bronze pool is redistributed upward by the importer/app logic. If silver has no winners, bronze must also have no winners; set both empty tiers to `0` and omit both medal clue fields. In that case both pools cascade to gold. `totalWinners` must still equal the sum of actual winner counts.

Do not add `adminNote` just to explain standard no-winner redistribution. The app generates that explanation automatically from the winner counts. Use `adminNote` only for unrelated data-quality notes.

`bonus` field: only include if SPECIAL PROMO section is present.
If a promo applies to the whole episode, add the same `bonus` object to both round objects.

### 3. Update the year shard

Append the two new game objects to the END of the correct `data/games-YYYY.json` array. Do not prepend. `data/games.json` is a stale backup and is not authoritative.

### 4. Regenerate data/games-meta.json

Run the audit fixer after editing a year shard:

```bash
npm run audit:fix
```

This rewrites `data/games-meta.json` from all year shards and keeps the home-page stats in sync.

### 5. Add transcript entry to data/transcripts.json

Build a new transcript object with:
- `date`, `host`, `secretItems` (array of both round answers)
- `rounds` array (one object per round with round number, secretItem, host, pot, format, clues list)
- `sections` array: exactly 6 sections in order: `Intro`, `Round 1`, `Round 1 Results`, `Round 2`, `Round 2 Results`, `Outro`

Split the TRANSCRIPT dialogue into these sections by looking for round start/results cues. Each section has `tag` and `lines` array; each line has `speaker` (string or null) and `text`.

Append the new entry to the END of the `transcripts.json` array.

### 6. Commit all changes

```bash
npm run audit:fix
npm run audit
git add data/games-YYYY.json data/games-meta.json data/transcripts.json
git commit -m "Import [DATE]: [ROUND1_ANSWER] and [ROUND2_ANSWER]"
git push -u origin main
```

### Partial or Missing-Recording Episode

A played episode with missing source material is **not** cancelled. Preserve every confirmed fact and allow the record to become more complete over time:

- Set `dataStatus: "partial"` on each affected game.
- Require a confirmed `secretItem`; use JSON `null` for unknown counts or payouts, never `0`, an empty string, a range guess, or explanatory prose.
- Before all five clue texts are known, keep `clues: []` and store only verified fragments in `partialClues` using `clueNumber`, `text`, and any confirmed `correct`, `guesses`, or `explanation` fields.
- Once all five clue texts are known, move them into the normal five-entry `clues` array in clue order. Keep `dataStatus: "partial"` until the remaining game facts are complete.
- Put winner counts, payouts, medal clues, host, wrong guesses, and explanations in their normal structured fields as they become known.
- If a screenshot shows the round-level player count in the upper corner, store it as numeric `totalPlayers`. This is distinct from per-clue `guesses`; never derive or overwrite one from the other when the explicit player count is available.
- Do not use public-facing `note`, `noteUrl`, `reportedResult`, or `adminNote` fields to discuss missing sources, requests for submissions, inference history, or agent uncertainty.
- The UI derives its public **Incomplete archive record** badge, missing-field list, and support-form link directly from `dataStatus: "partial"` plus the fields that are still null or empty. Do not hand-author that list; fill confirmed fields normally and it will shrink automatically.
- Add one transcript placeholder with `dataStatus: "unavailable"`, confirmed `host`, `secretItems`, and `rounds` metadata, plus the six canonical sections with empty `lines` arrays. Never invent dialogue.
- Remove the partial/unavailable statuses only when the game data and transcript are genuinely complete.

### Cancelled Episode

Use this state only when the broadcast truly did not air a game. If the paste says `CANCELLED`, create one stub game:
```json
{
  "date": "...", "pot": 0, "format": "v2", "host": "...",
  "secretItem": "", "clues": [], "totalWinners": 0,
  "winnerPayout": "", "winnerNames": "", "wrongGuesses": "",
  "note": "No game played."
}
```
Also add a transcript entry with empty round content, `secretItems: []`, `rounds: []`, and the same six canonical section tags used by playable episodes.

---

## Daily Puzzle Import Procedure

The Best Guess app releases one new practice puzzle per day. These are separate from live-show game rounds — no host, no prize money, no transcript, no winners. They are stored in `data/daily-puzzles.json`.

### Schema

```json
{
  "date": "Sunday, May 24, 2026",
  "secretItem": "BAND-AID",
  "clues": [
    {"clueNumber": 1, "text": "A WORLDWIDE COVER-UP"},
    {"clueNumber": 2, "text": "MAY FOLLOW A SOFT KISS"},
    {"clueNumber": 3, "text": "WON'T HELP YOUR BRUISED EGO"},
    {"clueNumber": 4, "text": "CAN BE A REAL PAIN"},
    {"clueNumber": 5, "text": "YOU STICK WITH THEM 'CAUSE THEY'RE STUCK ON YOU"}
  ]
}
```

### Rules

- `date`: full weekday + month + day + year string (e.g. "Sunday, May 24, 2026").
- `secretItem`: ALL CAPS. Strip leading "A"/"AN" article (same rule as live game imports). Keep "THE" only when semantically integral to the answer.
- `clues`: exactly 5 objects with `clueNumber` (integer 1–5), `text` (ALL CAPS clue string), and optional short `explanation` for hover tooltips. No `correct` or `guesses` fields.
- Append new entries to the **END** of `data/daily-puzzles.json` (oldest first, newest last).
- Do **not** run `npm run audit:fix` for daily-puzzle-only edits because there is no meta file to regenerate.
- Do run `npm run audit`; it validates daily puzzle dates, ordering, all-caps secret items/clues, exact five-clue shape, duplicate dates, and rejects live-game-only clue fields (`correct` and `guesses`).

### Missing Daily Puzzle

The app publishes one puzzle a day with no gaps, so a day nobody screenshotted is a hole in a known-continuous run, not an absence of data. Record it rather than skipping the date — a skipped date is indistinguishable from a day that never existed, and it silently disappears from the run.

```json
{
  "date": "Sunday, August 23, 2026",
  "secretItem": "",
  "dataStatus": "missing",
  "clues": []
}
```

- `dataStatus: "missing"` is the only value the audit accepts, and it requires `secretItem` to be an empty string and `clues` to be an empty array. **Never part-fill one** — do not guess the answer from a later reference, and do not add clues you have not seen. The audit rejects both.
- Placeholders keep their normal date position in the file (oldest first, newest last) so the run stays continuous.
- The Database view renders the row itself, with a "Puzzle not archived" note and a link to the feedback form. **Do not hand-author that text into the data**, exactly as with partial episodes.
- Placeholders are excluded from the archived-puzzle count everywhere (`_archivedDailyCount()`), so recording a gap never makes coverage look better than it is.
- To fill one in later, replace the whole entry with a normal puzzle object — drop `dataStatus`, set `secretItem`, and add the five clues.

### Commit

```bash
git add data/daily-puzzles.json
git commit -m "Add daily puzzle [DATE]: [SECRET_ITEM]"
git push -u origin <session-branch>
```

---

### Validation Checks

Before committing, verify:
- `npm run audit:fix` has regenerated `data/games-meta.json`.
- `npm run audit` passes with 0 errors.
- Both games have exactly 5 clues.
- `totalWinners` == `goldWinners` + `silverWinners` + `bronzeWinners`.
- Gold/silver/bronze medal clue numbers are distinct integers 1–5 for tiers with winners. Tiers with no winners may omit that medal clue field or use `0`. This does not change the five clue objects in the round.
- New transcript has exactly 6 sections in the correct order.
- `data/games-meta.json` entry count matches the combined year-shard game count.
- Daily puzzle entries pass `npm run audit` after any `data/daily-puzzles.json` edit.
