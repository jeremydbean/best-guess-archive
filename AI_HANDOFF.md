# AI Handoff

Last updated: 2026-04-25

## Current Branch

- `main`

## Latest Known Implementation Commit

- `22551c6` - Fix Jan 1-14 missing transcript content; make clue callouts consistent

## Current State

- GitHub Pages publishes from `main`.
- Main-only workflow is in effect. Do not create branches; remove stale non-main branches after confirming their commits are already represented on `main`.
- Database side arrows are working on desktop.
- Home page KPI counters animate on load without layout shift.
- **Admin panel removed**: All game/transcript updates are now done by AI agents (Claude/Codex) directly editing the data files and committing. See "Daily Update Workflow" below.
- **Bonus/promo data migrated**: `bonusMap` moved from hardcoded JS in `index.html` to a `bonus: {title, desc}` field on each game in `games.json`. Rendering code reads `g.bonus` directly. `bonus.desc` may contain safe HTML (`<br>` and `<b>` tags).
- **Scripts cleaned up**: `scripts/import_transcripts_from_docx.py` and `KindaCharming's Best Guess Live Show Transcripts.docx` removed (all past transcripts are imported). Admin code archived to `scripts/admin-panel-archive.js`.
- Latest imported episode: Friday, April 24, 2026 with BENJAMIN FRANKLIN and CHAMPAGNE.
- 100 total game days (99 playable + 1 cancelled: Thursday, April 9, 2026).
- 199 game objects in `data/games.json` (most dates have two rounds).
- **Transcripts reimported** from `Best_Guess_Live_Clean_Readable_Transcripts.docx` (uploaded to repo root). All 100 transcripts use games.json as canonical source for rounds/clues/host/pot/format. Section tags now read "Round 1 Results" / "Round 2 Results" (previously "Reveal").
- **Jan 1-14 transcripts fixed**: These episodes had no Heading2 section markers in the docx. A heuristic state machine now splits them into 6 sections using phrase triggers ("crystal ball reveals", "correct answer was", etc.) and space-normalized secret-item matching. All 10 episodes are now fully populated.
- **Mobile transcript layout fixed**: episode list max-height reduced from 32rem to 9rem on mobile; tapping an episode smooth-scrolls to the transcript detail panel. Desktop still uses 32rem two-column layout.
- **Clue lines** in transcript sections now render as left-bordered callout blocks consistently across all episode formats. Pattern matches "Clue N:" and "Clue number N:" (spelled or numeric) on any line regardless of speaker attribution.

## Daily Update Workflow

Every episode day, paste the following block to Claude or Codex. Claude/Codex will update `data/games.json`, `data/games-meta.json`, `data/transcripts.json`, and any special promo fields, then commit and push to `main`.

### How to Prepare the Paste Block

**Step 1 — Get structured transcript from Gemini/Plaud:**

Feed the raw Plaud/YouTube transcript to Gemini with this prompt:

```
You are formatting a raw Best Guess Live show transcript into a strict structured template. Follow these rules exactly:

1. Find the DATE of the episode (usually said at the start).
2. Find the HOST name(s).
3. For EACH ROUND (there are always two rounds):
   a. Find the SECRET ITEM (the answer) — revealed at the end of the round.
   b. Extract exactly 5 CLUES in order. Each clue is a short all-caps phrase read on screen. Copy them verbatim (verify spelling from video if needed).
   c. For each clue, write one sentence EXPLANATION of why it points to the secret item.
   d. Extract the CORRECT count and TOTAL GUESSES for each clue — the hosts announce these numbers aloud. Also extract Gold/Silver/Bronze winner counts and payouts, total winners, winner names (up to 4), and wrong guesses shown on screen.
4. Format all dialogue as a transcript with speaker labels. Use "HOST:" for the main host, "GUEST:" for any co-host/guest, and "RECAP:" for any recap narrator voice. No invented speakers.
5. Output NOTHING except the template below.

OUTPUT THIS EXACT TEMPLATE (fill in the [brackets]):

DATE: [Full date, e.g. "Friday, April 25, 2026"]
HOST: [Full host name(s), comma-separated if multiple]

ROUND 1
Secret Item: [THE ANSWER IN ALL CAPS]
Clue 1: [CLUE TEXT IN ALL CAPS] | Correct: [n] | Guesses: [n,nnn]
Clue 2: [CLUE TEXT IN ALL CAPS] | Correct: [n] | Guesses: [n,nnn]
Clue 3: [CLUE TEXT IN ALL CAPS] | Correct: [n] | Guesses: [n,nnn]
Clue 4: [CLUE TEXT IN ALL CAPS] | Correct: [n] | Guesses: [n,nnn]
Clue 5: [CLUE TEXT IN ALL CAPS] | Correct: [n] | Guesses: [n,nnn]

Gold Clue: [1-5]   Gold Winners: [n]   Gold Payout: $[n,nnn.nn]
Silver Clue: [1-5] Silver Winners: [n] Silver Payout: $[n.nn]
Bronze Clue: [1-5] Bronze Winners: [n] Bronze Payout: $[n.nn]
Total Winners: [n]
Winner Names: [Name1, Name2, Name3, Name4]
Wrong Guesses: [WORD1, WORD2, WORD3]

Clue 1 Explanation: [One sentence explaining why this clue points to the secret item]
Clue 2 Explanation: [One sentence]
Clue 3 Explanation: [One sentence]
Clue 4 Explanation: [One sentence]
Clue 5 Explanation: [One sentence]

ROUND 2
[same structure as Round 1]

TRANSCRIPT
[Full labeled dialogue from start to finish:
HOST: line
GUEST: line
RECAP: line
Lines with no clear speaker: just the text with no label.]
```

**Step 2 — Paste to Claude/Codex in this format:**

```
=== DAILY GAME UPDATE ===

DATE: [e.g. Friday, April 25, 2026]
HOST: [e.g. Howie Mandel, Hunter March]

--- ROUND 1 ---
Secret Item: [ALL CAPS]
Pot: 7500
Format: v2

Clue 1: [ALL CAPS CLUE TEXT] | Correct: [n] | Guesses: [n,nnn]
Clue 2: [ALL CAPS CLUE TEXT] | Correct: [n] | Guesses: [n,nnn]
Clue 3: [ALL CAPS CLUE TEXT] | Correct: [n] | Guesses: [n,nnn]
Clue 4: [ALL CAPS CLUE TEXT] | Correct: [n] | Guesses: [n,nnn]
Clue 5: [ALL CAPS CLUE TEXT] | Correct: [n] | Guesses: [n,nnn]

Gold Clue: [1-5]   Gold Winners: [n]   Gold Payout: $[n,nnn.nn]
Silver Clue: [1-5] Silver Winners: [n] Silver Payout: $[n.nn]
Bronze Clue: [1-5] Bronze Winners: [n] Bronze Payout: $[n.nn]
Total Winners: [n]

Winner Names: [Name1, Name2, Name3, Name4]
Wrong Guesses: [WORD1, WORD2, WORD3]

Clue 1 Explanation: [from Gemini output]
Clue 2 Explanation: [from Gemini output]
Clue 3 Explanation: [from Gemini output]
Clue 4 Explanation: [from Gemini output]
Clue 5 Explanation: [from Gemini output]

--- ROUND 2 ---
[same structure as Round 1]

--- SPECIAL PROMO (omit section if none) ---
Title: [e.g. Netflix Shop Voucher]
Description: [full text including how-to-qualify. May use <br> and <b> tags.]

--- TRANSCRIPT ---
[paste Gemini TRANSCRIPT section here]
```

**Notes:**
- All games from late April 2026 onward use `format: v2` with a $7,500 pot per round. Use `format: v1` only if the show announces a return to the old variable-pot format.
- `winnerPayout` is computed as: `$${(7500).toFixed(2)}` unless payout is split (most rounds have one payout winner who receives the full pot). Actually it should be whichever payout value shown on screen. For v2 it's typically `"$7,500.00"` if there was a gold winner, otherwise N/A.
- `bonus.desc` may contain `<br>` and `<b>` tags; they are rendered as HTML in the modal. Keep descriptions clean and avoid other HTML tags.
- Clue text on-screen uses all caps and may include punctuation; verify spelling from the video still frame if Gemini misheard a word.

### What Claude/Codex Does with the Paste

1. Parses the paste into two game objects (one per round).
2. Appends them to `data/games.json` (most recent dates go at the end — the database sorts descending by date at render time).
3. Rebuilds `data/games-meta.json` from the full `games.json`.
4. Adds a new transcript entry to `data/transcripts.json` with all six canonical sections (Intro, Round 1, Round 1 Reveal, Round 2, Round 2 Reveal, Outro) and the round metadata.
5. Commits all changed files to `main` and pushes.

### Cancelled Episode

If no game was played:

```
=== DAILY GAME UPDATE ===
DATE: Thursday, April 9, 2026
HOST: [host name]
CANCELLED - No game played
[optional note about why]
```

Agent writes one stub game object with `note` field and no `clues` array.

## games.json Schema

Each game object:
```json
{
  "date": "Friday, April 25, 2026",
  "pot": 7500,
  "format": "v2",
  "host": "Howie Mandel, Hunter March",
  "secretItem": "WIDGET",
  "clues": [
    {"text": "CLUE TEXT", "correct": "123", "guesses": "4,567 🥇", "explanation": "One sentence."},
    ...
  ],
  "goldClue": 1,
  "silverClue": 2,
  "bronzeClue": 3,
  "goldWinners": 123,
  "silverWinners": 456,
  "bronzeWinners": 789,
  "totalWinners": 1368,
  "goldPayout": 60.98,
  "silverPayout": 16.45,
  "bronzePayout": 9.51,
  "winnerPayout": "$7,500.00",
  "winnerNames": "Name1, Name2, Name3",
  "wrongGuesses": "WORD1, WORD2, WORD3",
  "bonus": {"title": "Promo Name", "desc": "Description with optional <br>/<b> HTML."}
}
```

Medal emoji in `guesses` field: append ` 🥇` / ` 🥈` / ` 🥉` after the number for the gold/silver/bronze clue respectively.

`bonus` is optional — only include when there's a special promo for that day.

## transcripts.json Schema

Each transcript entry:
```json
{
  "date": "Friday, April 25, 2026",
  "host": "Howie Mandel",
  "secretItems": ["ROUND1 ANSWER", "ROUND2 ANSWER"],
  "rounds": [
    {
      "round": 1,
      "secretItem": "ROUND1 ANSWER",
      "host": "Howie Mandel",
      "pot": 7500,
      "format": "v2",
      "clues": ["CLUE 1 TEXT", "CLUE 2 TEXT", ...]
    },
    { "round": 2, ... }
  ],
  "sections": [
    {"title": "Intro", "lines": [{"speaker": "HOST", "text": "..."}, ...]},
    {"title": "Round 1", "lines": [...]},
    {"title": "Round 1 Reveal", "lines": [...]},
    {"title": "Round 2", "lines": [...]},
    {"title": "Round 2 Reveal", "lines": [...]},
    {"title": "Outro", "lines": [...]}
  ]
}
```

Sections always appear in exactly this order. `speaker` is a string (host name, "RECAP", etc.) or `null` for lines without a clear speaker.

## Performance Architecture

- **Tailwind**: Static `tailwind.css` (33KB prebuilt). If new Tailwind classes are added to index.html, regenerate with: `npx tailwindcss@3 -i tailwind-input.css -o tailwind.css --minify`
- **games-meta.json**: Lightweight (36KB) loaded on init for home stats. Full `games.json` lazy-loads when user first visits Database or Stats.
- **Chart.js**: Injected dynamically on first Stats page visit only.
- **filterDatabase**: Debounced 150ms.
- **_homeStatsCache**: Invalidated when full games.json loads or refreshStats() runs.

## Things Worth Double-Checking After Future Edits

- GitHub Pages reflects the newest commit on `main`.
- Desktop database arrows remain visible and clickable while scrolling.
- Home KPI counters do not cause layout shift.
- Database details modal shows bonus section for promo dates; verify `g.bonus` is present in games.json and the title is escaped, desc is trusted HTML.
- Play feature (`startRandomGame`) awaits full games.json load before starting.
- Stats charts render all 5 canvases; Clue 5 bar in "Avg Payout Per Winner by Clue" shows `Avg payout: $2`.
- `data/games-meta.json` regenerates exactly from `data/games.json` after every import.
- Transcripts: search finds new date, shows host/chips/sections, database detail buttons work.

## Working Agreement

- Pull/rebase `origin/main` before making edits if remote has moved.
- Leave all work on `main`.
- Commit directly to `main` and push to `origin/main` when finished.
- Update this file after meaningful changes so the next agent can pick up quickly.
