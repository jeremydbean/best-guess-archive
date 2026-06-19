# AI Handoff

Last updated: 2026-06-11 (session end)

## Most Recent Changes (2026-06-11)

- **Daily puzzle added — Friday, June 19, 2026: CORNHOLE**: Appended to `data/daily-puzzles.json` (now 28 entries). Clues: LANDSLIDE VICTORY / IMPRESSIVE HANDBAG COLLECTION / TOSSES AND TURNS / INCLINED TO BE A GOOD TIME / BEANBAGS GO THROUGH THE O WITH EVERY A-MAIZE-ING THROW. `npm run audit` passes.
- **June 18, 2026 episode imported — CALCULATOR (R1) and FISHING (R2), host Hunter March** (both `format: "v2"`). Appended to `data/games-2026.json` (now 241 games) + full transcript in `data/transcripts.json` (now 139); meta regenerated; `npm run audit` passes 0/0. Payload was clean — all payouts verified: R1 CALCULATOR gold 2 @ $1,500 / silver 5 @ $500 / bronze 691 @ $2.89 (total 698); R2 FISHING gold 63 @ $47.61 / silver 778 @ $3.21 / bronze 2,415 @ $0.82 (total 3,256). No results screenshot, so wrong guesses are from the payload. (Live episode — separate from the June 18 PEANUT BUTTER daily puzzle.)
- **Daily puzzle added — Thursday, June 18, 2026: PEANUT BUTTER**: Appended to `data/daily-puzzles.json` (now 27 entries). The screenshot was on the "Show Results" screen (answer not revealed), but all five clues unambiguously point to PEANUT BUTTER (sandwich spread, PB&J, ants-on-a-log, Reese's cup). Clues: RICH AND FAMOUS / GREAT IN A CUP BUT YOU CAN'T DRINK IT / KEEPS LOGS ANT-INFESTED / DON'T GET JELLY OF JELLY'S BESTIE / CRUNCHY OR CREAMY, THIS SANDWICH SPREAD'S DREAMY. `npm run audit` passes.
- **BRAIN (June 17) Clue 1 guess count fixed**: "ON TOP OF IT" guesses corrected 45,561 → **4,561** (transcript had an ambiguous "45,561 out of 4,561"; user confirmed 4,561). Correct count stays 1. Meta regenerated; `npm run audit` passes 0/0.
- **June 17, 2026 episode finalized — BRAIN (R1) and HIDE AND SEEK (R2), host Hunter March** (both `format: "v2"`). Replaced the earlier "results pending" stubs in place (**kept June 17** — user confirmed it's yesterday's game; the supplied transcript's "June 18" was a processing-date slip). Full data: R1 BRAIN gold 1 @ $3,000 (Clue 1) / silver 1 @ $2,500 (Clue 2) / bronze 648 @ **$3.08** (Clue 3), total 650 — bronze was supplied as $3.09 but floorCents(2000/648)=$3.08 (audit-enforced). R2 HIDE AND SEEK gold 5 @ $600 (Clue 1) / silver 303 @ $8.25 (Clue 2) / bronze 588 @ $3.40 (Clue 3), total 896. Medal clues restored (gold 1 / silver 2 / bronze 3 both rounds), `adminNote` removed, per-clue counts + medal emoji added, full transcript replaces the skeleton. Wrong guesses: R1 `CHERRY, GOOGLE, ELON MUSK, SIRI, APPLE`; R2 `ROCKET, TIMER, TAG, ELEVATOR, FIREWORKS`. `npm run audit` passes 0/0.
- **Daily puzzle added — Wednesday, June 17, 2026: DRACULA**: Appended to `data/daily-puzzles.json` (now 26 entries). Clues: A BATMAN / HAS A DRINKING PROBLEM / ALWAYS ON THE VERGE OF A HEART ATTACK / BEEN GOING THROUGH A GOTH PHASE / COUNT ON HIM TO BE LITERATURE'S SUCKIEST CHARACTER. `npm run audit` passes.
- **June 16, 2026 episode imported — HOME RUN (R1) and SCOOBY DOO (R2), host Howie Mandel** (both `format: "v2"`). Appended to `data/games-2026.json` (now 237 games) + full transcript in `data/transcripts.json` (now 137); meta regenerated; `npm run audit` passes 0/0. **One payout fix**: SCOOBY DOO gold was given as $20.39 but floorCents(3000/147) = **$20.40** (audit-enforced) — corrected in the game data and the two transcript mentions. Other payouts verified: R1 gold 5 @ $600 / silver 5 @ $500 / bronze 656 @ $3.04 (total 666); R2 silver 487 @ $5.13 / bronze 1,684 @ $1.18 (total 2,318). No results screenshot, so wrong guesses are from the payload. (Live episode — separate from the June 16 FERRIS WHEEL daily puzzle.)
- **Stats page: "Payout Per Winner Over Time" chart**: Single-axis log line chart on the Stats page under "Players Over Time" — 3 color-coded lines (gold `#FBBF24` / silver `#CBD5E1` / bronze `#FB923C`) showing what each tier's winner took home per **v2** episode by air date (`#chart-medal-payout`). Empty tiers (0 winners) map to `null` → gaps, skipped in tooltips; tooltip title = `secretItem · date`. Data in `_getStatsData()` (`v2SortedByDate`, `v2TimeLabels`, `gold/silver/bronzePayoutData`); built via the shared `buildMedalChart` helper in `_renderStatsCharts()` (`this._charts.medalPayout`); node `chartMedalPayout`. *(History: started as one 6-line dual-axis chart → split into Winners + Payout charts → the user asked to keep only the Payout chart, so the Winners chart was removed.)* `npm run audit` passes.
- **Host rename — "Karen Fox" → "Corinne Foxx"**: Replaced all 31 occurrences (2 in `data/games-2026.json`, 25 in `data/transcripts.json` host+speaker fields, 2 in the stale `data/games.json` backup); `data/games-meta.json` regenerated via `npm run audit:fix`. No code change needed: the Play host-cartoon picker (`_pickHostCartoon`) already matches on the `'fox'` substring, so "Corinne Foxx" keeps using `karen-fox-denim-jumpsuit.png`. `npm run audit` passes 0/0.
- **Daily puzzle added — Tuesday, June 16, 2026: FERRIS WHEEL**: Appended to `data/daily-puzzles.json` (now 25 entries). Clues: HANGING AROUND / RIGHT BACK WHERE WE STARTED / REINVENTED WHAT YOU DON'T REINVENT / A FAIRLY AMUSING EXPERIENCE / GRAB A PIC AT THE TOP IF THIS CIRCULAR RIDE SHOULD STOP. `npm run audit` passes.
- **June 15, 2026 episode imported — CANDLE (R1) and SEATBELT (R2), host Corinne Foxx** (both `format: "v2"`). Appended to `data/games-2026.json` (now 235 games) + full transcript in `data/transcripts.json` (now 136); `npm run audit:fix` regenerated meta; `npm run audit` passes 0/0. Payload was clean — payouts verified: R1 gold 49 @ $61.22 / silver 818 @ $3.05 / bronze 338 @ $5.91 (total 1,205); R2 gold 88 @ $34.09 / silver 1,269 @ $1.97 / bronze 4,913 @ $0.40 (total 6,270). No results screenshot, so wrong guesses are from the payload. (This is the live episode; separate from the June 15 SNOW daily puzzle.)
- **Daily puzzle added — Monday, June 15, 2026: SNOW**: Appended to `data/daily-puzzles.json` (now 24 entries). Clues: WHAT MAKES A MAN / BANK DEPOSIT / BLANKET THAT WON'T KEEP YOU WARM / FROSTED FLAKES / IT'S A REAL PAIN TO SHOVEL THIS WHITE, FLUFFY RAIN. `npm run audit` passes.
- **Daily puzzle added — Sunday, June 14, 2026: WEED**: Appended to `data/daily-puzzles.json` (now 23 entries). Clues: INTRUDER ALERT! / TOPIC OF GROWING CONCERN / ALWAYS SLIPPING THROUGH THE CRACKS / TOTAL WHACK JOB, ACCORDING TO GROUNDSKEEPERS / I BEG YOUR PARDON - UNWANTED PLANTS IN MY GARDEN? `npm run audit` passes.
- **Play mode: accept "KENTUCKY FRIED CHICKEN" for KFC**: `_getAcceptedAnswers()` now adds `kentuckyfriedchicken` as an accepted alias when the answer normalizes to `kfc` (same mechanism as the mayonnaise→mayo alias).
- **Play mode: accelerated clue playout before the result**: When you lock in a guess on clues 1–4, the simulation no longer jumps straight to win/loss. `submitGuess()` now computes the outcome as a deferred `finish()` closure and calls `_revealRemainingCluesThenFinish(finish)`, which exposes each remaining clue ~2.2s apart (`_renderAcceleratedClue()` renders the stack with text already visible, no guess timer), holds on clue 5 for ~3s, then runs `finish()` to show the result. Guesses on clue 5 resolve immediately (nothing left to reveal). A `this._revealing` flag (init in constructor, reset in `startRandomGame`/`exitGame`) guards `nextClue()` so the SKIP button can't interrupt the playout. Input is disabled (`setGuessingState('timeup')`) and the timer shows "Revealing…" then "Results…" during the sequence. `npm run audit` passes (inline scripts parse).
- **Daily puzzle added — Saturday, June 13, 2026: APPLE**: Appended to `data/daily-puzzles.json` (now 22 entries). Clues: OCCASIONALLY GETS SAUCY / SEEDY AT ITS CORE / TEACHERS LOVE THEM, DOCTORS DON'T? / GRANNY SMITH THAT'S NOT YOUR NANA / GIVE THIS FRUIT A TRY, THE KEY FLAVOR OF AMERICAN PIE. `npm run audit` passes.
- **Database Secret Item column wraps long names**: The live-games Secret Item cell used `white-space:nowrap` + `overflow:hidden;text-overflow:ellipsis` (max-width 200px), which clipped long answers like "RUDOLPH THE RED-NOSED REINDEER". Switched to wrapping (`leading-snug`, `overflow-wrap:break-word`, no nowrap/ellipsis) so long revealed answers flow onto multiple lines like the clue cells. Scratch-off cover (hidden state) is unaffected (fixed-width box).
- **TOM HANKS (Fri June 5, 2026) Clue 4 counts backfilled**: Clue 4 ("HAS GIVEN 4 WOODEN PERFORMANCES, SO FAR") was recorded as `0`/`0` (missing data); updated from a screenshot to `correct: "1,310"`, `guesses: "3,186"`, and the matching transcript recap line ("0 got it right" → "1,310 got it right"). Clue 4 is not a medal clue (gold/silver/bronze = clues 1/2/3), so winner counts and payouts are unchanged. `npm run audit` passes 0/0.
- **June 12, 2026 episode imported — ZOMBIE (R1) and DISCO BALL (R2), host Howie Mandel** (both `format: "v2"`). Appended to `data/games-2026.json` (now 233 games) + full transcript in `data/transcripts.json` (now 135). Fixes applied during import: R1 Clue 1 text was empty in the payload → filled `BIT BY BIT` (from the transcript); R2 silver payout was wrong ($1.80 → **$1.87** = floorCents(2500/1335), enforced by audit) in both the game data and the transcript summary line; cleaned doubled `?.`/`!.` punctuation and the empty-clue text in the Results recap lines. Wrong guesses kept from the transcript (no results screenshot this time). Payouts verified: R1 gold 5 @ $600 / silver 23 @ $108.69 / bronze 10 @ $200 (total 38); R2 gold 4 @ $750 / silver 1,335 @ $1.87 / bronze 1,418 @ $1.41 (total 2,757). `npm run audit` passes 0/0.
- **Daily puzzle added — Friday, June 12, 2026: HOODIE**: Appended to `data/daily-puzzles.json` (now 21 entries). The submitted screenshot's answer label glitched to "POLE VAULT", but all five clues are HOODIE clues (kangaroo pocket, hooded sweatshirt for Rocky/Eminem, goes over your head) and the user confirmed HOODIE. `npm run audit` passes.
- **June 11, 2026 episode imported — OCTOPUS (R1) and ROBIN HOOD (R2), host Howie Mandel** (both `format: "v2"`). Appended to `data/games-2026.json` (now 231 games) with a full transcript in `data/transcripts.json` (now 134). `npm run audit:fix` regenerated meta; `npm run audit` passes 0/0. **Clue wording was corrected to match the submitted screenshots**: R1 Clue 1 `EVENHANDED` (no hyphen), R1 Clue 4 `KING OF THE INKIN' EMPIRE` (ink pun, not "INCAN"); R2 Clue 2 `ARCH-ENEMY OF INJUSTICE` (hyphen), R2 Clue 4 `WOULD HE LIVE IN THE FOREST? SURE WOULD!` (exclamation). **Wrong guesses use the official "most-submitted" results screen** (per repo convention): R1 `SQUID, JELLYFISH, CLOCK, HANDSHAKE, SCALE`; R2 `BATMAN, TUG OF WAR, TREE, PENNY, SCALE`. Two transcript-source errors were fixed during import: a Round 1 Results line read "octopus has **HTML** arms" (→ "eight"), and the Clue 3 results recap was duplicated from Clue 1 (→ corrected to `O THAT SUCKS`). Payouts verified: R1 gold 187 @ $16.04 / silver 2,437 @ $1.02 / bronze 3,878 @ $0.51 (total 6,502); R2 gold 27 @ $111.11 / silver 756 @ $3.30 / bronze 1,408 @ $1.42 (total 2,191).
- **Daily puzzle added — Thursday, June 11, 2026: WALKIE TALKIE**: Appended to `data/daily-puzzles.json` (now 20 entries; previous latest was Wed June 10 LION KING). Five clues with short explanations; `npm run audit` passes (no `audit:fix` needed for daily-puzzle-only edits).
- **Host name fix — "Corinne Five" → "Corinne Foxx"**: The host previously transcribed as "Corinne Five" (a mishearing of Foxx) is now "Corinne Foxx" everywhere — 2 host fields in `data/games-2026.json` and 277 occurrences in `data/transcripts.json`. `data/games-meta.json` regenerated via `npm run audit:fix`.
- **SPARKLER (Thu May 7, 2026) silver payout corrected to $1.07**: Per real-show data, silver winners received $1.07 each (the final amount *after* the empty $2,000 bronze pot was redistributed to gold+silver). Back-solved the winner count under the audit's redistribution formula `floorCents(2500/sW) + floorCents(2000/(15+sW)) = 1.07` → silver = 4,160 winners (base $0.60 + $0.47 bronze share). Updated: `silverWinners` 2975→4160, `silverPayout` 1.5→1.07, `goldPayout` 200.66→200.47 (its bronze-redistribution share changed), `totalWinners` 2990→4175, Clue 5 `correct` 2975→4160, and the two SPARKLER Round 1 Results transcript lines. There is still **no bronze tier** (bronzeWinners 0). `npm run audit` passes 0/0.
- **Database secret-item spoiler (scratch-off bar)**: On the Database view, secret items / daily-puzzle answers are hidden behind a **standardized fixed-width (7.5rem) scratch-off-style bar** (silver brushed-metal gradient + diagonal hatch + "TAP TO REVEAL"). Every cover is identical, so the answer's length cannot be inferred from the box. Click/tap (or Enter/Space) reveals one; a "Reveal all secret items" checkbox (unchecked by default, near the tab bar) reveals the whole column via the `#db-view-root.db-reveal-all` class. State persists across tab switches/re-renders (`this._dbRevealAll`). Implemented with the `.db-secret` CSS class (hidden = `display:inline-flex` fixed box with `color:transparent` + `overflow:hidden`; revealed = `display:inline`, `color:inherit`, no background) and `revealSecret` / `revealSecretKey` / `toggleRevealAll` methods. CSS-only cover (no new Tailwind classes), so `tailwind.css` did not need regenerating. *(Earlier in this session the cover was a blur, but blur leaked answer length — replaced with the uniform scratch-off bar.)*
- **Details modal secret-item reveal**: The Database **Details** modal heading now also hides the secret item behind the scratch-off cover (click/Enter/Space to reveal), using a larger fixed-width variant `.db-secret.db-secret-lg` (16rem × 3rem) so it fits the `text-4xl` heading while staying length-independent. Empty/stub answers are not wrapped.
- **Details modal host explanations blurred until answer revealed**: In the Database **Details** modal, each clue's host explanation `<p>` now has class `db-explanation` and is `filter: blur(6px)` by default (spoiler protection). It un-blurs only when the modal's answer is revealed: `#modal-content` gets the `.answer-revealed` class either at render time (`secretAlreadyRevealed` — answer already revealed in the table or "Reveal all" on, or a stub with no secret item) or when the cover is clicked (`revealSecret` adds it via `el.closest('#modal-content')`). Purely linked to the secret-item reveal — no separate control. **CSS relocation**: the `.db-secret` / `.db-explanation` reveal styles were moved from the database-view template `<style>` into the global `<head>` `<style>` so they apply to the Details modal even when it's opened from the **Transcripts** page (`openDatabaseDetailsFromButton`), where the database template isn't mounted.
- **Reveal state linked between table and Details modal**: A persistent `this._revealedSecrets` Set (keyed `"date::secretItem"`) remembers which answers have been revealed. `revealSecret(el)` records `el.dataset.secretKey`; every `.db-secret` (live row, daily row, modal heading) now carries `data-secret-key`. After a table re-render, `_applyRevealedState()` re-adds `.revealed` to known keys (so reveals survive search/filter/tab re-renders). When opening the Details modal, the heading renders already-revealed if `this._dbRevealAll` is on **or** the key is in the Set — so an answer revealed in the table view (individually or via "Reveal all") shows revealed in Details without another click. Reveals in the modal also record into the Set, so the table reflects them on its next render.

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

- `305c476` - Import May 27, 2026: THE GYM (v2) and JUGGLING (v2); confirm both-v2 era
- `3aa82b7` - Add daily puzzle May 27: TIKTOK; daily puzzle explanations shortened to one-liners
- `06fda33` - Import May 26, 2026: BRUNCH (v2) and ASTRONAUT (v1 classic, last ever)
- Transcript cleanup: remove 17 duplicate host clue-recap lines from May 25–27 Results sections
- Earlier: SHARK/BRACES (May 25), BANANA SPLIT puzzle, How to Play rewrite, SHERLOCK HOLMES, BAND-AID date fix
- Earlier: Tabbed database (Live/Daily), cross-tab search, Stats wrong-guesses v2 filter
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
- **Hybrid rules window Monday, May 11 through Tuesday, May 26, 2026**: During this window, Round 1 is `format: "v2"` tiered gold/silver/bronze and Round 2 is `format: "v1"` classic mode, where only the earliest clue with correct answers splits the full $7,500 pot. In the Database, classic v1 winning clues are marked with the same 🥇 clue indicator used for v2 instead of a yellow highlighted clue box.
- **Rules change confirmed: both rounds v2 tiered starting Wednesday, May 27, 2026**: Confirmed by the May 27 episode (THE GYM + JUGGLING both `format: "v2"`). The last classic v1 Round 2 episodes were May 25 and May 26. `tools/audit-data.mjs`, `scripts/auto-import.py`, `docs/DAILY_IMPORT.md`, `docs/DAILY_IMPORT_PROMPT.md`, `docs/PLAUD_AUDIO_PROMPT.md`, `AGENTS.md`, and the in-app Gemini/Plaud copy prompts now use the bounded May 11–26 hybrid rule and treat May 27+ episodes as both-v2 unless the broadcast explicitly says otherwise.

- GitHub Pages publishes from `main`.
- Main-only workflow is in effect. Do not create branches; remove stale non-main branches after confirming their commits are already represented on `main`.
- Database side arrows are working on desktop.
- Home page KPI counters animate on load without layout shift.
- **Admin panel removed**: All game/transcript updates are now done by AI agents (Claude/Codex) directly editing the data files and committing. See "Daily Update Workflow" below.
- **Bonus/promo data migrated**: `bonusMap` moved from hardcoded JS in `index.html` to a `bonus: {title, desc}` field on each game in the year shards. Rendering code reads `g.bonus` directly. `bonus.desc` may contain safe HTML (`<br>` and `<b>` tags).
- **Scripts cleaned up**: Legacy docx/admin importer scripts are gone; current automation lives in `scripts/auto-import.py`, with a few one-off historical cleanup scripts still present.
- Latest imported episode: Friday, June 12, 2026 with ZOMBIE (Round 1, v2) and DISCO BALL (Round 2, v2).
- 135 total game days (134 playable + 1 cancelled: Thursday, April 9, 2026).
- 269 game objects across year shards (`data/games-2025.json`: 36, `data/games-2026.json`: 233).
- 135 transcript entries in `data/transcripts.json`.
- **Daily Puzzles**: `data/daily-puzzles.json` stores Best Guess app daily practice puzzles. Launched Saturday, May 23, 2026. Current latest entry: APPLE (Saturday, June 13, 2026), with 22 total daily puzzles. Each clue has an optional `explanation` field (short one-liner) shown as hover tooltip in the Daily Puzzles database table. These are separate from live-show game rounds — no host, no prizes, no winners, no transcript. `npm run audit` validates this file; `npm run audit:fix` is not needed for daily-puzzle-only edits.
- **Daily puzzle audit hardening 2026-05-24**: `tools/audit-data.mjs` now validates `data/daily-puzzles.json` as part of `npm run audit`, including flat-array shape, valid weekday/date strings, oldest-first order, duplicate dates, ALL CAPS secret item/clue text, no leading `A`/`AN` secret-item articles, exactly five ordered clues, and no live-game clue fields.
- **Daily Puzzles KPI on Stats page 2026-05-24**: The Stats page first KPI group now includes a "Daily Puzzles Archived" card (purple, puzzle-piece icon) showing the count of puzzles in `data/daily-puzzles.json`. If any dates are missing since May 23, 2026 (the launch date), a warning badge shows "X dates missing". `setView('stats')` now loads daily puzzles alongside full games before rendering, and the stats cache key includes `dp${dailyPuzzles.length}` to invalidate on puzzle count change.
- **How to Play modal rewrite 2026-05-25**: The How to Play modal (`#how-to-play-modal` template in `index.html`) now contains real game instructions: five-clue structure (hardest first), one-guess-per-round rule, lock-in mechanic, v2 gold/silver/bronze prize tier table ($3K/$2.5K/$2K pools), v1 classic mode explanation, and a blue callout noting the archive maps your result to real-show tier thresholds.
- **BAND-AID date fix 2026-05-25**: The first daily puzzle was incorrectly dated "Sunday, May 24" (Codex had fixed the wrong field). Corrected to "Saturday, May 23, 2026". The puzzle launched May 23; May 24's puzzle is SHERLOCK HOLMES.
- **Daily puzzle imports May 23–27**: BAND-AID (Sat May 23), SHERLOCK HOLMES (Sun May 24), BANANA SPLIT (Mon May 25), NEW YORK CITY (Tue May 26), TIKTOK (Wed May 27) — all in `data/daily-puzzles.json`. Each clue has a short one-liner `explanation` field for hover tooltips. `tools/audit-data.mjs` now allows `explanation` in daily puzzle clue objects (removed from forbidden fields list; only `correct` and `guesses` remain forbidden).
- **May 26, 2026 episode imported**: Hosted by Howie Mandel. BRUNCH (Round 1, v2): gold Clue 1 (3 winners, $1,000 each), silver Clue 2 (24 winners, $104.16 each), bronze Clue 3 (36 winners, $55.55 each). ASTRONAUT (Round 2, v1 classic — last-ever classic v1 episode): winning Clue 2, 2 winners ($3,750 each).
- **May 27, 2026 episode imported**: Hosted by Howie Mandel. THE GYM (Round 1, v2): gold Clue 1 (1176 winners, $2.55 each), silver Clue 2 (2213 winners, $1.13 each), bronze Clue 3 (1822 winners, $1.10 each). JUGGLING (Round 2, v2 — first-ever Round 2 v2 under new era): gold Clue 1 (1 winner, $3,000 — Apples the Journey), silver Clue 2 (3 winners, $833.33 each), bronze Clue 3 (25 winners, $80.00 each).
- **Transcript cleanup (May 25–27)**: Results sections in May 25–27 transcripts had both host-spoken clue recap lines (e.g. "Clue one: ...") and null-speaker annotation lines for the same clues. The 17 duplicate host-recap lines were removed; null-speaker annotations remain as canonical structured data.
- **May 25, 2026 episode imported**: Memorial Day, hosted by Howie Mandel. SHARK (Round 1, v2): gold Clue 1 (1 winner, $3,000 — Chris Etrada93), silver Clue 2 (4 winners, $625 each), bronze Clue 3 (128 winners, $15.62 each). BRACES (Round 2, v1 classic): winning Clue 1, 2 winners ($3,750 each — teamblender591, acatchy84).
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

For audio-only Plaud output, use `docs/PLAUD_AUDIO_PROMPT.md` or the hidden Data Health popup's "Plaud Audio Prompt" copy button. For screenshot-backed cleanup, use the hidden Data Health popup's "Gemini Import Prompt" copy button. The in-app prompts account for the format timeline: pre-May 11 usually both v2, May 11–26 hybrid, and May 27+ both v2 unless the show says otherwise.

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
Monday, May 11 through Tuesday, May 26, 2026: use Format: v1 classic mode, include Winning Clue, Winner Count, Winner Payout, Total Winners, winner names, wrong guesses, and all five clue/explanation lines. Keep Gold Clue equal to Winning Clue for compatibility, and set medal winner/payout fields to 0.
Starting Wednesday, May 27, 2026: same v2 tiered structure as Round 1 unless the show says otherwise.]

--- SPECIAL PROMO (omit section if none) ---
Title: [e.g. Netflix Shop Voucher]
Description: [full text including how-to-qualify. May use <br> and <b> tags.]

--- TRANSCRIPT ---
[paste Gemini TRANSCRIPT section here]
```

**Notes:**
- For episodes before Monday, May 11, 2026, both rounds are normally `format: v2` unless the show says otherwise. Monday, May 11 through Tuesday, May 26, 2026 is hybrid: Round 1 is `format: "v2"` tiered gold/silver/bronze, and Round 2 is `format: "v1"` classic mode. Starting Wednesday, May 27, 2026, both rounds are normally `format: "v2"` tiered.
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

Fields: `date` (full weekday string), `secretItem` (ALL CAPS, no leading article unless "THE" is part of the answer), `clues` array of exactly 5 objects with `clueNumber` (1–5), `text` (ALL CAPS), and optional `explanation` (short one-liner shown as hover tooltip in the Daily Puzzles database table). No winners, no payouts, no host, no transcript.

To add a new daily puzzle, append a new object to the END of `data/daily-puzzles.json`, then run `npm run audit`. Do not run `npm run audit:fix` for daily-puzzle-only edits. The audit validates the file is a flat array, dates are valid/unique/oldest-first, secret items and clue text are ALL CAPS, each puzzle has exactly five ordered clues, and clues do not include live-game-only fields `correct` or `guesses`. The `explanation` field IS allowed on daily puzzle clues.

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
- **Data audit**: `npm run audit:fix` regenerates `games-meta.json`; `npm run audit` validates JSON, inline scripts, generated meta, archive dates, payout values, missing clue explanations, v2 winner totals/payout math, v1 classic winning-clue shape, hybrid format order for May 11–26, bonus coverage, transcript schemas, transcript/game alignment, result clue text, escaped HTML entities, and daily puzzle schema/order/casing.
- **_homeStatsCache**: Invalidated when year shards finish loading or refreshStats() runs.

## Things Worth Double-Checking After Future Edits

- GitHub Pages reflects the newest commit on `main`.
- Latest manual import completed: Friday, June 12, 2026 (`ZOMBIE`, `DISCO BALL`). For screenshot-backed imports, prefer exact clue wording and popular wrong guesses from screenshots over rough transcript text.
- Always verify Gemini-provided dates against a calendar (weekday name AND day number). Transcript headers from Gemini are consistently +1 day off.
- Recalculate all payouts with `Math.floor(v * 100) / 100` — never trust Gemini's payout figures.
- Strip "A"/"AN" from secret items; keep "THE" only when semantically part of the answer.
- Friday, May 1, 2026 bonus metadata is attached to both `ZOOM` and `JUMPING JACKS`; audit should have 0 warnings.
- Desktop database arrows remain visible and clickable while scrolling.
- Home KPI counters do not cause layout shift.
- Database details modal shows bonus section for promo dates; verify `g.bonus` is present in the year shard and the title is escaped, desc is trusted HTML.
- Play feature (`startRandomGame`) awaits full year-shard load before starting.
- Stats charts render all 5 canvases; Clue 5 bar in "Avg Payout Per Winner by Clue" shows `Avg payout: $2`.
- `npm run audit:fix` regenerates `data/games-meta.json` from all year shards after every live-game import. Daily puzzles do not need `audit:fix`, but they do need `npm run audit`.
- Transcripts: search finds new date, shows host/chips/sections, database detail buttons work.
- Daily Puzzles tab: inside the Database page (not a separate nav item). Tab count loads immediately on page open. Search persists across tab switches. Cross-tab matches shown via inline blue hint banner.

## Working Agreement

- Pull/rebase `origin/main` before making edits if remote has moved.
- Leave all work on `main`.
- Commit directly to `main` and push to `origin/main` when finished.
- Update this file after meaningful changes so the next agent can pick up quickly.
