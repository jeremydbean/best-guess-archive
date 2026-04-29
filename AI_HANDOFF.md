# AI Handoff

Last updated: 2026-04-28

## Current Branch

- `main`

## Latest Known Implementation Commit

- Current commit - Speed up database clue explanation hover
- `bc0a690` - Bonus indicator opens highlighted details
- `e47f7e4` - Reformat April 27 transcript to canonical Results layout
- `17fcff7` - Update Apr 27, 2026: screen-verified clues, winner names, wrong guesses, transcript
- `fbb8b4a` - Reformat all Dec/Jan/Feb/Mar transcripts to match established Results format

## Current State

- GitHub Pages publishes from `main`.
- Main-only workflow is in effect. Do not create branches; remove stale non-main branches after confirming their commits are already represented on `main`.
- Database side arrows are working on desktop.
- Home page KPI counters animate on load without layout shift.
- **Admin panel removed**: All game/transcript updates are now done by AI agents (Claude/Codex) directly editing the data files and committing. See "Daily Update Workflow" below.
- **Bonus/promo data migrated**: `bonusMap` moved from hardcoded JS in `index.html` to a `bonus: {title, desc}` field on each game in `games.json`. Rendering code reads `g.bonus` directly. `bonus.desc` may contain safe HTML (`<br>` and `<b>` tags).
- **Scripts cleaned up**: `scripts/` directory removed entirely; `import_transcripts_from_docx.py`, `admin-panel-archive.js`, and `KindaCharming's Best Guess Live Show Transcripts.docx` are gone. Recover from git history if ever needed.
- Latest imported episode: Tuesday, April 28, 2026 with BRUNO MARS and TAXI. Fan Appreciation K-pop Demon Hunters glass voucher bonus is attached to both rounds; v2 `totalWinners` reflects paid medal winners (`goldWinners + silverWinners + bronzeWinners`).
- 102 total game days (101 playable + 1 cancelled: Thursday, April 9, 2026).
- 203 game objects in `data/games.json` (most dates have two rounds).
- **Transcripts reimported** from `Best_Guess_Live_Clean_Readable_Transcripts.docx` (uploaded to repo root). All 100 transcripts use games.json as canonical source for rounds/clues/host/pot/format. Section tags now read "Round 1 Results" / "Round 2 Results" (previously "Reveal").
- **Jan 1-14 transcripts fixed**: These episodes had no Heading2 section markers in the docx. A heuristic state machine now splits them into 6 sections using phrase triggers ("crystal ball reveals", "correct answer was", etc.) and space-normalized secret-item matching. All 10 episodes are now fully populated.
- **Mobile transcript layout fixed**: episode list max-height reduced from 32rem to 9rem on mobile; tapping an episode smooth-scrolls to the transcript detail panel. Desktop still uses 32rem two-column layout.
- **Clue lines** in transcript sections now render as left-bordered callout blocks consistently across all episode formats. Pattern matches "Clue N:" and "Clue number N:" (spelled or numeric) on any line regardless of speaker attribution.
- **All transcripts reformatted** (commits `8b3c0b9`, `fbb8b4a`): All episodes (Dec 2025 through Apr 2026) now use consistent Results section format — speaker reveal line + null-speaker "Clue 5→1" breakdowns from games.json + null-speaker winner announcement. 21 episodes lack a speaker-attributed reveal (source had none) and fall back to a null-speaker constructed line. Clue callout formatting (indented border blocks) now applies only in Results sections, not Round sections.
- **Beta notice** added to Transcripts page header (commit `d1a30c9`): yellow banner noting formatting is still being updated.
- **Codex validation 2026-04-28**: `AGENTS.md` now matches the canonical `Round 1 Results` / `Round 2 Results` section tags. The cancelled Thursday, April 9, 2026 transcript now keeps the same six-section shell as playable episodes with `secretItems: []` and `rounds: []`; the game/meta records use an empty `secretItem` and `format: "v2"`. Validation passed for JSON parsing, inline script parsing, regenerated `games-meta.json`, v2 winner totals, distinct medal clues, and all 101 transcript section schemas. Browser smoke passed on `http://127.0.0.1:5173/` for Home, Transcripts, and Stats with no console errors; the Avg Payout Per Winner by Clue chart renders the Clue 5 bar visibly on its log scale.
- **Codex UI update 2026-04-28**: The April 27 Netflix Shop K-pop Demon Hunters glass voucher bonus is now attached to both TOOTHPICK and WILLY WONKA so both database detail modals display it. Database detail modals now show a full "Episode transcript" action that opens the selected date's transcript and jumps to the matching round. The Transcripts page sidebar/detail layout was tightened with stronger episode cards, section jump buttons, top-level database detail links, and sticky desktop navigation.
- **Transcript consistency audit 2026-04-28**: All 101 transcripts match the 101 game dates, use the canonical six-section order, have consistent `secretItems`/`rounds` metadata against `games.json`, and include expected result clue text under loose punctuation matching. Cleaned remaining escaped HTML entities in transcript text (`&amp;` → `&`) so M&M, S&P, and H&M render correctly.
- **Import/UI quality-of-life update 2026-04-28**: Added `npm run audit` via `tools/audit-data.mjs`, an `incoming/` raw transcript drop folder, and `docs/DAILY_IMPORT.md`, `docs/DAILY_IMPORT_PROMPT.md`, and `docs/IMPORT_REPORT_TEMPLATE.md`. Home now has Latest Episode shortcuts and an optional `?health=1` data-health panel with copy buttons for the import prompt/audit command. Database rows now show bonus badges, transcript action icons, and quick-filter chips for bonus, transcripts, v2 rules, solo wins, and host.
- **Footer/latest/health polish 2026-04-28**: Footer status now counts playable rounds only, excluding cancelled games. The health panel remains behind `?health=1` and has a discreet footer icon link. Latest Game card is more polished with host/round/winner metadata. Transcript section jump buttons were removed to keep the transcript header quieter.
- **Audit self-healing update 2026-04-28**: `npm run audit:fix` regenerates `data/games-meta.json` from `data/games.json`; `npm run audit` now also validates archive date format/weekday, missing clue explanations, and non-negative numeric payout fields.
- **Latest game card layout fix 2026-04-28**: Home hero has bottom padding again, and the latest game card is explicitly full-width/max-width with safer text wrapping, extra inner gutters, and tip-jar-sized action buttons so the card/text does not get clipped on mobile-width screens.
- **Latest game medal clue chips 2026-04-28**: The Latest Game card now shows compact medal clue indicators like `R1 🥇1 🥈2 🥉3`. `games-meta.json` now includes `goldClue`, `silverClue`, and `bronzeClue`, regenerated by `npm run audit:fix`, so the home page can show this without loading full `games.json`.
- **Database bonus indicator 2026-04-28**: Bonus rounds use a pink sticky present icon immediately left of the Details column. Clicking it opens the round details modal and scrolls/highlights the bonus block.
- **UI declutter 2026-04-28**: Latest Game card resized to match the Tip Jar (`max-w-md`, centered vertical layout). Special Bonus block in details modal restyled to match the Episode transcript label pattern (small uppercase pink "Special Bonus" header + pink card_giftcard icon + bold pink title + neutral description). Database table no longer shows the per-row bonus or transcript icon buttons — only the Details visibility button remains. K-pop Demon Hunters bonus description trimmed to remove the stale "Last week's $5 Netflix Shop vouchers expire..." sentence.
- **Footer health popup polish 2026-04-28**: Footer playable-round status stays green once metadata loads, and the data health panel is now a closable fixed popup instead of an embedded Home section. `?health=1` opens the same popup.
- **Simplified footer health popup 2026-04-28**: Footer health affordance now reads as quiet green status text (`200 rounds`) rather than a visible button. Data Health popup no longer includes copy prompt/audit buttons and has explicit safe padding/width so content is not clipped on mobile.
- **Footer health indicator split 2026-04-28**: Footer round count is plain white text again, with a separate small circular health button beside it. The indicator is green for clean, yellow for issues, red for load failure, and opens the Data Health popup.
- **Data health count cleanup 2026-04-28**: Data Health popup shows Playable Rounds, Game Dates, and Transcripts only; the Bonus Rounds card was removed.
- **Automated import hardening 2026-04-28**: `scripts/auto-import.py` now validates Claude JSON before writing data, uses real `America/New_York` timezone conversion, rejects unsupported bonus HTML, and the frontend sanitizes bonus descriptions to an allowlist. The GitHub workflow rebases and reruns audit/fix before committing imported data.
- **YouTube auto-import fallback 2026-04-28**: The Chris S YouTube RSS feed can return 404 even while the channel page works. `scripts/auto-import.py` now falls back to scraping the channel videos page and extracting the archive date from titles like `Best Guess Live (April 28, 2026)`. The workflow installs Python `tzdata`, and the script also has a DST-aware Eastern-time fallback for Windows runners without IANA timezone data.
- **Database details declutter 2026-04-29**: The database details modal now uses a compact stat grid for pot/host/paid winners/format, short `G`/`S`/`B` clue indicators instead of long medal labels, a smaller transcript action, a tighter bonus block, and collapsed common wrong guesses.
- **Database clue hover 2026-04-29**: Clue text in the Database table exposes the host explanation without changing the visible table layout.
- **Fast database clue hover 2026-04-29**: Native browser clue tooltips were too slow, so the Database table now uses one floating custom tooltip for clue explanations. It appears quickly on hover/focus and does not change the normal spreadsheet layout.

## Daily Update Workflow

Every episode day, paste the following block to Claude or Codex. Claude/Codex will update `data/games.json`, `data/games-meta.json`, `data/transcripts.json`, and any special promo fields, then commit and push to `main`.

Preferred no-preformat path: put the raw transcript at `incoming/YYYY-MM-DD.txt` and use `docs/DAILY_IMPORT_PROMPT.md`. Before every import commit, run `npm run audit:fix`, then `npm run audit`, and fix every error.

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
3. Runs `npm run audit:fix` to rebuild `data/games-meta.json` from the full `games.json`.
4. Adds a new transcript entry to `data/transcripts.json` with all six canonical sections (Intro, Round 1, Round 1 Results, Round 2, Round 2 Results, Outro) and the round metadata.
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
    {"tag": "Intro", "lines": [{"speaker": "HOST", "text": "..."}, ...]},
    {"tag": "Round 1", "lines": [...]},
    {"tag": "Round 1 Results", "lines": [...]},
    {"tag": "Round 2", "lines": [...]},
    {"tag": "Round 2 Results", "lines": [...]},
    {"tag": "Outro", "lines": [...]}
  ]
}
```

Sections always appear in exactly this order. `speaker` is a string (host name, "RECAP", etc.) or `null` for lines without a clear speaker.

## Performance Architecture

- **Tailwind**: Static `tailwind.css` (33KB prebuilt). If new Tailwind classes are added to index.html, regenerate with: `npx tailwindcss@3 -i tailwind-input.css -o tailwind.css --minify`
- **games-meta.json**: Lightweight (36KB) loaded on init for home stats. Full `games.json` lazy-loads when user first visits Database or Stats.
- **Chart.js**: Injected dynamically on first Stats page visit only.
- **filterDatabase**: Debounced 150ms.
- **Data audit**: `npm run audit:fix` regenerates `games-meta.json`; `npm run audit` validates JSON, inline scripts, generated meta, archive dates, payout values, missing clue explanations, v2 winner totals, bonus coverage, transcript schemas, transcript/game alignment, result clue text, and escaped HTML entities.
- **_homeStatsCache**: Invalidated when full games.json loads or refreshStats() runs.

## Things Worth Double-Checking After Future Edits

- GitHub Pages reflects the newest commit on `main`.
- Desktop database arrows remain visible and clickable while scrolling.
- Home KPI counters do not cause layout shift.
- Database details modal shows bonus section for promo dates; verify `g.bonus` is present in games.json and the title is escaped, desc is trusted HTML.
- Play feature (`startRandomGame`) awaits full games.json load before starting.
- Stats charts render all 5 canvases; Clue 5 bar in "Avg Payout Per Winner by Clue" shows `Avg payout: $2`.
- `npm run audit:fix` regenerates `data/games-meta.json` from `data/games.json` after every import.
- Transcripts: search finds new date, shows host/chips/sections, database detail buttons work.

## Working Agreement

- Pull/rebase `origin/main` before making edits if remote has moved.
- Leave all work on `main`.
- Commit directly to `main` and push to `origin/main` when finished.
- Update this file after meaningful changes so the next agent can pick up quickly.
