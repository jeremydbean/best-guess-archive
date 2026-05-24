# AI Handoff

Last updated: 2026-05-24 (session end)

## Current Branch

- `main`

## ⚠️ Push Workflow — Read Before Committing

`git push origin main` **always fails with 403** in CCR/web sessions. Permanent, unfixable via credentials. Do NOT try MCP `push_files` — it burns the user's API rate limit.

**Correct workflow every session:**
1. Commit on local `main` as normal
2. `git push -u origin <session-branch>` (branch name is in the session-level instructions)
3. `git reset --hard origin/main`
4. GitHub Actions (`.github/workflows/merge-claude-branch.yml`) auto-merges `claude/*` → `main`, deletes the session branch, and GitHub Pages updates

## Latest Known Implementation Commit

- `1b952d5` - Match daily puzzle clue font size and wrapping to live games table
- `4dc37b4` - Keep search when switching tabs; add cross-tab match hint
- `489cc8c` - Show Daily Puzzles tab count immediately on database load
- `ce0709f` - Fold Daily Puzzles into Database as a tab, remove standalone nav tab
- `8430dd2` - Update AI_HANDOFF.md and AGENTS.md for May 15–24 session
- `0f76222` - Cross-search daily puzzles from main database search bar
- Earlier: Stats wrong-guesses v2 filter, game attribution, Daily Puzzles section
- Earlier: Imports for May 15–22, 2026 (TETRIS through WATERSLIDE)

## Current State

- **Year-based data sharding**: `data/games.json` has been split into per-year shard files — `data/games-2025.json` (36 games) and `data/games-2026.json` (181+ games). `data/games.json` is kept as a read-only backup but is **no longer authoritative**. All tooling reads from and writes to the year shards.
  - `data/games-meta.json` is now a `{years: [...], games: [...]}` object instead of a bare array. `years` lists the available shard years. `games` is the lightweight meta array used by the home page.
  - `tools/audit-data.mjs` reads from all `data/games-YYYY.json` shards (scanning the directory), regenerates `games-meta.json` as the `{years, games}` object.
  - `scripts/auto-import.py` writes new games to the correct `data/games-YYYY.json` shard based on the episode year. If a new-year shard does not exist it is created automatically.
  - `index.html` `init()` parses the new meta format; `_ensureFullGamesLoaded()` fetches all year shards in parallel; `refreshStats()` also loads from shards. A `_availableYears` property drives which shards to fetch; falls back to `['2025','2026']` if meta load failed.
  - When a brand-new year starts: auto-import creates `data/games-YYYY.json` automatically; `npm run audit:fix` adds the new year to `games-meta.json`; no manual steps needed.
- **No-winner medal tiers / redistribution**: Every playable round still has exactly five clue objects. For v2 rounds where a silver or bronze tier has no winners, keep the data literal: the empty tier has `0` winners and `0` payout, and its medal clue field should be omitted or `0`. Do not invent a medal clue. Empty tiers cascade from the bottom upward, so bronze can be empty by itself, or silver and bronze can both be empty. The app/importer calculate official redistribution display from the winner counts. Example: May 7 `SPARKLER` has gold on Clue 4, silver on Clue 5, no bronze, `bronzeWinners: 0`, no `bronzeClue`, and bronze pot redistributed into the shown gold/silver payouts.
- **Standard redistribution UI 2026-05-07**: No-winner medal tiers are now rendered as a normal generated "Prize redistribution" block in Database details, based on winner counts. Do not add one-off `adminNote` text for standard no-bronze/no-silver rounds. Reserve `adminNote` for unrelated data-quality notes, such as incomplete wrong guesses due to technical issues.
- **No-winner validation hardening 2026-05-07**: `scripts/auto-import.py` now accepts empty silver/bronze tiers only when their medal clue field is omitted or `0`, while still requiring all five clue objects. `tools/audit-data.mjs` enforces the same shape and verifies v2 payout math including official redistribution, so bad imports cannot make Play award a nonexistent medal tier.
- **Auto-import bug check 2026-05-08**: `scripts/auto-import.py` now catches URL/time-out/XML RSS failures before falling back to the channel page, prefers title dates for manual video imports, treats date-only publish metadata as noon UTC to avoid previous-day Eastern drift, and validates Claude output more strictly before writing: archive date shape, v2 format, host/pot/wrongGuesses, clue numbers, numeric correct/guess counts, medal tier order, winner totals, payouts, and full-pot `winnerPayout`. `tools/audit-data.mjs` mirrors the new clue-number, count-shape, medal-order, and v2 `winnerPayout` checks while tolerating legacy unknown count strings in old data.
- **Auto-import cost guard 2026-05-12**: `.github/workflows/auto-import.yml` now runs a cheap `git push --dry-run origin HEAD:main` preflight before installing Python dependencies or calling Claude. If GitHub cannot accept a main push, the job stops before spending Anthropic API tokens. The workflow also skips the duplicate DST schedule when the Eastern hour is not 9, uses workflow concurrency, and passes `--max-episodes=1` so a backlog cannot spend multiple Claude calls in one scheduled run.
- **Hybrid rules beginning Monday, May 11, 2026**: Round 1 stays `format: "v2"` tiered gold/silver/bronze. Round 2 returns to `format: "v1"` classic mode, where only the earliest clue with correct answers splits the full $7,500 pot. `scripts/auto-import.py`, `docs/DAILY_IMPORT.md`, `docs/DAILY_IMPORT_PROMPT.md`, `docs/PLAUD_AUDIO_PROMPT.md`, `AGENTS.md`, the in-app Gemini/Plaud copy prompts, and `tools/audit-data.mjs` have been updated for this. In the Database, classic v1 winning clues are now marked with the same 🥇 clue indicator used for v2 instead of a yellow highlighted clue box.

- GitHub Pages publishes from `main`.
- Main-only workflow is in effect. Do not create branches; remove stale non-main branches after confirming their commits are already represented on `main`.
- Database side arrows are working on desktop.
- Home page KPI counters animate on load without layout shift.
- **Admin panel removed**: All game/transcript updates are now done by AI agents (Claude/Codex) directly editing the data files and committing. See "Daily Update Workflow" below.
- **Bonus/promo data migrated**: `bonusMap` moved from hardcoded JS in `index.html` to a `bonus: {title, desc}` field on each game in the year shards. Rendering code reads `g.bonus` directly. `bonus.desc` may contain safe HTML (`<br>` and `<b>` tags).
- **Scripts cleaned up**: Legacy docx/admin importer scripts are gone; current automation lives in `scripts/auto-import.py`, with a few one-off historical cleanup scripts still present.
- Latest imported episode: Friday, May 22, 2026 with PRINGLES (Round 1, v2) and WATERSLIDE (Round 2, v1 classic).
- 120 total game days (119 playable + 1 cancelled: Thursday, April 9, 2026).
- 239 game objects across year shards (`data/games-2025.json`: 36, `data/games-2026.json`: 203).
- 120 transcript entries in `data/transcripts.json`.
- **Daily Puzzles**: new `data/daily-puzzles.json` file for the Best Guess app's daily practice puzzles. First entry: BAND-AID (Saturday, May 24, 2026). See schema below. These are separate from live-show game rounds — no host, no prizes, no winners, no transcript.
- **Most Popular Wrong Guesses (Stats)**: now filtered to `format === 'v2'` games only (starting Thursday, April 23, 2026, CHOPSTICKS — the first v2 game). Pre-v2 wrong guesses are excluded from this stat. Each wrong guess in the top-10 also now shows which secret items it appeared in (same style as Reused Clue Text section).
- **Secret item article rule**: Strip leading "A" and "AN" from secret items (e.g. "AN ELEPHANT" → "ELEPHANT"). Keep "THE" when it is semantically part of the answer (e.g. "THE MIDDLE SEAT" stays as-is). Apply this during any import.
- **Payout math rule**: Always pre-calculate payouts using `floorCents(v) = Math.floor(v * 100) / 100`. Gemini-provided payout figures are unreliable — always recalculate from winner counts. goldPayout = floorCents(3000 / goldWinners), silverPayout = floorCents(2500 / silverWinners), bronzePayout = floorCents(2000 / bronzeWinners), v1 winnerPayout = floorCents(7500 / winnerCount).
- **Gemini transcript date bug**: Gemini consistently labels transcripts with the NEXT day's date (off by +1). Always verify both weekday name and day number against calendar before importing. The host usually names the day in the intro.
- **Curly quotes in JSON**: Transcript annotation lines (null-speaker recap lines) use Unicode curly quotes `"…"`. `sed` patterns with straight quotes won't match — use Python `content.replace()` for any edits to those strings.
- **winningClue for v1 with zero-correct early clues**: Set `winningClue` to the earliest clue with `correct > 0`, not necessarily clue 1. Example: BAD BUNNY has `winningClue: 2` (clue 1 had 0 correct); THE MIDDLE SEAT has `winningClue: 3`.
- **Transcripts reimported** from `Best_Guess_Live_Clean_Readable_Transcripts.docx` (uploaded to repo root). All 100 transcripts use the game data as canonical source for rounds/clues/host/pot/format. Section tags now read "Round 1 Results" / "Round 2 Results" (previously "Reveal").
- **Jan 1-14 transcripts fixed**: These episodes had no Heading2 section markers in the docx. A heuristic state machine now splits them into 6 sections using phrase triggers ("crystal ball reveals", "correct answer was", etc.) and space-normalized secret-item matching. All 10 episodes are now fully populated.
- **Mobile transcript layout fixed**: episode list max-height reduced from 32rem to 9rem on mobile; tapping an episode smooth-scrolls to the transcript detail panel. Desktop still uses 32rem two-column layout.
- **Clue lines** in transcript sections now render as left-bordered callout blocks consistently across all episode formats. Pattern matches "Clue N:" and "Clue number N:" (spelled or numeric) on any line regardless of speaker attribution.
- **All transcripts reformatted** (commits `8b3c0b9`, `fbb8b4a`): All episodes (Dec 2025 through Apr 2026) now use consistent Results section format — speaker reveal line + null-speaker "Clue 5→1" breakdowns from game data + null-speaker winner announcement. 21 episodes lack a speaker-attributed reveal (source had none) and fall back to a null-speaker constructed line. Clue callout formatting (indented border blocks) now applies only in Results sections, not Round sections.
- **Beta notice** added to Transcripts page header (commit `d1a30c9`): yellow banner noting formatting is still being updated.
- **Codex validation 2026-04-28**: `AGENTS.md` now matches the canonical `Round 1 Results` / `Round 2 Results` section tags. The cancelled Thursday, April 9, 2026 transcript now keeps the same six-section shell as playable episodes with `secretItems: []` and `rounds: []`; the game/meta records use an empty `secretItem` and `format: "v2"`. Validation passed for JSON parsing, inline script parsing, regenerated `games-meta.json`, v2 winner totals, distinct medal clues, and all 101 transcript section schemas. Browser smoke passed on `http://127.0.0.1:5173/` for Home, Transcripts, and Stats with no console errors; the Avg Payout Per Winner by Clue chart renders the Clue 5 bar visibly on its log scale.
- **Codex UI update 2026-04-28**: The April 27 Netflix Shop K-pop Demon Hunters glass voucher bonus is now attached to both TOOTHPICK and WILLY WONKA so both database detail modals display it. Database detail modals now show a full "Episode transcript" action that opens the selected date's transcript and jumps to the matching round. The Transcripts page sidebar/detail layout was tightened with stronger episode cards, section jump buttons, top-level database detail links, and sticky desktop navigation.
- **Transcript consistency audit 2026-04-28**: All 101 transcripts match the 101 game dates, use the canonical six-section order, have consistent `secretItems`/`rounds` metadata against game data, and include expected result clue text under loose punctuation matching. Cleaned remaining escaped HTML entities in transcript text (`&amp;` → `&`) so M&M, S&P, and H&M render correctly.
- **Import/UI quality-of-life update 2026-04-28**: Added `npm run audit` via `tools/audit-data.mjs`, an `incoming/` raw transcript drop folder, and `docs/DAILY_IMPORT.md`, `docs/DAILY_IMPORT_PROMPT.md`, and `docs/IMPORT_REPORT_TEMPLATE.md`. Home now has Latest Episode shortcuts and an optional `?health=1` data-health panel with copy buttons for the import prompt/audit command. Database rows now show bonus badges, transcript action icons, and quick-filter chips for bonus, transcripts, v2 rules, solo wins, and host.
- **Footer/latest/health polish 2026-04-28**: Footer status now counts playable rounds only, excluding cancelled games. The health panel remains behind `?health=1` and has a discreet footer icon link. Latest Game card is more polished with host/round/winner metadata. Transcript section jump buttons were removed to keep the transcript header quieter.
- **Audit self-healing update 2026-04-28**: `npm run audit:fix` regenerates `data/games-meta.json` from all year shards; `npm run audit` now also validates archive date format/weekday, missing clue explanations, and non-negative numeric payout fields.
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
- **Database cleanup 2026-04-29**: Removed the Database quick-filter chip row and unused quick-filter code paths. The sticky Details column is now a polished action lane with a clearer `View` pill button.
- **Database details styling 2026-04-29**: Rolled back the box-heavy details modal header. It now uses centered title text, compact metadata chips, and lightweight medal summary pills closer to the original modal style.
- **Details transcript action 2026-04-29**: The details modal transcript link is intentionally a quiet text-size action placed below the clue explanations so it does not crowd the winners line.
- **Details header spacing 2026-04-29**: The pot/host/winners/format row and medal payout row use wider wrap gaps so the compact header stays readable without reintroducing boxed stat cards.
- **Details clue spacing 2026-04-29**: Clue rows in the database details modal use larger internal padding and bigger vertical gaps between clue number/counts, clue text, and host explanation. Keep future modal edits generous with padding.
- **Details row gaps 2026-04-29**: Header metadata and medal rows use inline `column-gap`/`row-gap` styles because the dynamic modal markup did not reliably preserve Tailwind gap utilities in the rendered details view.
- **Details bonus disclosure 2026-04-29**: Special Bonus in the details modal is a native collapsible disclosure with the gift/title in the summary; Common wrong guesses is a plain always-visible block.
- **Simulated result screens 2026-04-29**: Play-mode end screens now use original generated `assets/result/` artwork for Best Guess Archive gold/silver/bronze medals plus Good Job/Good Try emblems, with a mobile game-style top result screen and archive stats below.
- **V1 simulated win screen 2026-04-29**: Classic/pre-medal wins use `assets/result/emblem-v1-winner.png`, a wide generated "You're a Winner" marquee with orange-to-purple end-screen background. V2 wins continue to use medal-specific result art.
- **Result layout polish 2026-04-29**: Simulated end screens use `dvh`, smaller responsive emblem/text sizing, a scroll cue for archive stats, and payout formatting with exactly two cents.
- **Wrong-answer result screen 2026-04-29**: Misses intentionally use a blue stage background, CSS `GOOD TRY!` sign, red-X guessed-answer pill, separate Correct Answer block, and no payout pill. Do not reuse silver/medal art for this state.
- **Result answer/result art cleanup 2026-04-29**: Result screens no longer show the player-count pill. The guessed/answer pill uses explicit green-check/red-X icon classes, payout pills are smaller with more spacing, and generated result PNGs were rematted to remove faint rectangular background boxes.
- **Result emblem positioning 2026-04-29**: V1 winner art is nudged slightly left; Good Job and Good Try states have larger/lower emblem sizing so they do not inherit the smaller medal scale.
- **Result copy alignment 2026-04-29**: Result headline/subhead copy follows screenshot text by state. Gold says "were one of the fastest players"; Good Job says `The main primary correct answer is "ANSWER".`; wrong answers show a separate Correct Answer block. Payout pill is only shown for actual winning states.
- **Good Try text 2026-04-29**: Wrong-answer result text mirrors the screenshot copy: `NOT QUITE`, `That wasn’t the correct answer, but every attempt makes you better.`, and literal `CORRECT ANSWER:` above the uppercase answer.

## Daily Update Workflow

Every episode day, paste the following block to Claude or Codex. Claude/Codex will update the appropriate `data/games-YYYY.json` year shard, `data/games-meta.json`, `data/transcripts.json`, and any special promo fields, then commit and push to `main`.

**Important**: Append new game entries to the END of the correct year shard (`data/games-2026.json` for 2026 games, etc.), not to `data/games.json`. Run `npm run audit:fix` after editing any shard to keep `games-meta.json` in sync.

Preferred no-preformat path: put the raw transcript at `incoming/YYYY-MM-DD.txt` and use `docs/DAILY_IMPORT_PROMPT.md`. Before every import commit, run `npm run audit:fix`, then `npm run audit`, and fix every error.

### How to Prepare the Paste Block

**Step 1 — Get structured transcript from Gemini/Plaud:**

For audio-only Plaud output, use `docs/PLAUD_AUDIO_PROMPT.md` or the hidden Data Health popup's "Plaud Audio Prompt" copy button. For screenshot-backed cleanup, use the hidden Data Health popup's "Gemini Import Prompt" copy button. The in-app prompt already accounts for the Monday, May 11, 2026 hybrid rule: Round 1 v2 tiered, Round 2 v1 classic.

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
[Before Monday, May 11, 2026: same structure as Round 1 unless the show says otherwise.
Starting Monday, May 11, 2026: use Format: v1 classic mode, include Winning Clue, Winner Count, Winner Payout, Total Winners, winner names, wrong guesses, and all five clue/explanation lines. Keep Gold Clue equal to Winning Clue for compatibility, and set medal winner/payout fields to 0.]

--- SPECIAL PROMO (omit section if none) ---
Title: [e.g. Netflix Shop Voucher]
Description: [full text including how-to-qualify. May use <br> and <b> tags.]

--- TRANSCRIPT ---
[paste Gemini TRANSCRIPT section here]
```

**Notes:**
- For episodes before Monday, May 11, 2026, both rounds are normally `format: v2` unless the show says otherwise. Starting Monday, May 11, 2026, the standard import is hybrid: Round 1 is `format: "v2"` tiered gold/silver/bronze, and Round 2 is `format: "v1"` classic mode.
- For v2, `winnerPayout` stays the full round pot string, normally `"$7,500.00"`, and medal payouts go in `goldPayout`, `silverPayout`, and `bronzePayout`. For v1 classic, set `winningClue`, `winnerCount`, `totalWinners`, and `winnerPayout` to the per-winner share of the full pot; keep `goldClue` equal to `winningClue` for compatibility.
- `bonus.desc` may contain `<br>` and `<b>` tags; they are rendered as HTML in the modal. Keep descriptions clean and avoid other HTML tags.
- Clue text on-screen uses all caps and may include punctuation; verify spelling from the video still frame if Gemini misheard a word.

### What Claude/Codex Does with the Paste

1. Parses the paste into two game objects (one per round).
2. Appends them to the correct `data/games-YYYY.json` year shard (e.g. `data/games-2026.json`). The database sorts descending by date at render time.
3. Runs `npm run audit:fix` to rebuild `data/games-meta.json` from all year shards.
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

## Year Shard Game Schema

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

If a silver or bronze tier had no winners, keep all five clue objects, set that medal tier's winners and payout to `0`, and omit that tier's medal clue field or set it to `0`. Empty tiers cascade from the bottom upward: bronze can be empty by itself, or silver and bronze can both be empty. `totalWinners` is always the actual sum of `goldWinners + silverWinners + bronzeWinners`.

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

## daily-puzzles.json Schema

`data/daily-puzzles.json` is a flat JSON array (oldest first). Each entry:

```json
{
  "date": "Saturday, May 24, 2026",
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

Fields: `date` (full weekday string), `secretItem` (ALL CAPS, no leading article unless "THE" is part of the answer), `clues` array of exactly 5 objects with `clueNumber` (1–5) and `text` (ALL CAPS). No winners, no payouts, no host, no transcript.

To add a new daily puzzle, append a new object to the END of `data/daily-puzzles.json`. No audit step needed (this file is not read by `npm run audit`).

## UI Features Added in This Session

- **Daily Puzzles tab inside Database**: the Database page has two tabs — "Live Games" and "Daily Puzzles". The standalone Daily nav tab was removed. Tab badges always show total counts and update to "X matches" during a search. Daily puzzles are preloaded when the Database view opens so the count shows immediately without clicking.
- **Unified cross-tab search**: the single search bar filters whichever tab is active. The query persists when switching tabs (no reset). When the active tab has no matches but the other tab does, a blue info banner appears inline: *"Also found N daily puzzles matching 'X' — switch tab to see them"* with a clickable link.
- **Daily clue text**: same font, size, and wrapping as the live games table (`font-medium text-slate-200 leading-snug`, `min-width:200px`). No truncation.
- **Most Popular Wrong Guesses (Stats)**: filtered to v2-only games (since April 23, 2026); each entry now shows which secret items the wrong guess appeared in (same pattern as Reused Clue Text).

## Performance Architecture

- **Tailwind**: Static `tailwind.css` (33KB prebuilt). If new Tailwind classes are added to index.html, regenerate with: `npx tailwindcss@3 -i tailwind-input.css -o tailwind.css --minify`
- **games-meta.json**: Lightweight `{years, games}` object loaded on init for home stats. Year shards (`games-2025.json`, `games-2026.json`, …) lazy-load in parallel when the user first visits Database or Stats. No monolithic `games.json` download.
- **Chart.js**: Injected dynamically on first Stats page visit only.
- **filterDatabase**: Debounced 150ms.
- **Data audit**: `npm run audit:fix` regenerates `games-meta.json`; `npm run audit` validates JSON, inline scripts, generated meta, archive dates, payout values, missing clue explanations, v2 winner totals/payout math, v1 classic winning-clue shape, hybrid format order from May 11 onward, bonus coverage, transcript schemas, transcript/game alignment, result clue text, and escaped HTML entities.
- **_homeStatsCache**: Invalidated when year shards finish loading or refreshStats() runs.

## Things Worth Double-Checking After Future Edits

- GitHub Pages reflects the newest commit on `main`.
- Latest manual import completed: Friday, May 22, 2026 (`PRINGLES`, `WATERSLIDE`). For screenshot-backed imports, prefer exact clue wording and popular wrong guesses from screenshots over rough transcript text.
- Always verify Gemini-provided dates against a calendar (weekday name AND day number). Transcript headers from Gemini are consistently +1 day off.
- Recalculate all payouts with `Math.floor(v * 100) / 100` — never trust Gemini's payout figures.
- Strip "A"/"AN" from secret items; keep "THE" only when semantically part of the answer.
- Friday, May 1, 2026 bonus metadata is attached to both `ZOOM` and `JUMPING JACKS`; audit should have 0 warnings.
- Desktop database arrows remain visible and clickable while scrolling.
- Home KPI counters do not cause layout shift.
- Database details modal shows bonus section for promo dates; verify `g.bonus` is present in the year shard and the title is escaped, desc is trusted HTML.
- Play feature (`startRandomGame`) awaits full year-shard load before starting.
- Stats charts render all 5 canvases; Clue 5 bar in "Avg Payout Per Winner by Clue" shows `Avg payout: $2`.
- `npm run audit:fix` regenerates `data/games-meta.json` from all year shards after every import. Daily puzzles do NOT need an audit step.
- Transcripts: search finds new date, shows host/chips/sections, database detail buttons work.
- Daily Puzzles tab: inside the Database page (not a separate nav item). Tab count loads immediately on page open. Search persists across tab switches. Cross-tab matches shown via inline blue hint banner.

## Working Agreement

- Pull/rebase `origin/main` before making edits if remote has moved.
- Leave all work on `main`.
- Commit directly to `main` and push to `origin/main` when finished.
- Update this file after meaningful changes so the next agent can pick up quickly.
