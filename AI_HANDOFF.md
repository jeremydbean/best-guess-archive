# AI Handoff

Last updated: 2026-04-24

## Current Branch

- `main`

## Latest Known Commit

- `1226608` - Update AI_HANDOFF after play-feature fix and lazy-load hardening

## Current State

- GitHub Pages publishes from `main`.
- Main-only workflow is in effect. Do not create branches; remove stale non-main branches after confirming their commits are already represented on `main`.
- Database side arrows are working on desktop.
- Home page KPI counters animate on load without layout shift.
- Admin import/delete flow has extra safety checks and preview escaping.
- Admin import/delete now writes `data/games.json` and `data/games-meta.json` together through the Git database API (blob/tree/commit/ref), avoiding the old contents-endpoint size ceiling and keeping home-page totals in sync.
- Latest imported episode: Thursday, April 23, 2026 with CHOPSTICKS and TIME, including the Fan Appreciation Week Netflix Shop voucher detail.
- Review pass hardened database rows, details modals, result screens, stats lists, play clue rendering, and tip-jar URLs so imported/archive text is escaped before being rendered through `innerHTML`.
- Stats payout badges were corrected to avoid relying on Tailwind arbitrary classes inside JS-rendered HTML.
- Database date column width was reduced from the earlier oversized value to better preserve secret-item alignment.

## Working Agreement

- Pull/rebase `origin/main` before making edits if remote has moved.
- Leave all work on `main`.
- Update this file after meaningful changes so the next agent can pick up quickly.

## Performance Architecture (added 2026-04-23)

- **Tailwind**: Static `tailwind.css` (33KB prebuilt). If new Tailwind classes are added to index.html, regenerate with: `npx tailwindcss@3 -i tailwind-input.css -o tailwind.css --minify`
- **games-meta.json**: Lightweight (36KB) file loaded on init for home stats. Full `games.json` (358KB) lazy-loads when user first visits Database or Stats. If `games.json` changes, regenerate meta with the Python script in AI_HANDOFF history or reuse the pattern from the commit.
- **Chart.js**: Injected dynamically on first Stats page visit only.
- **filterDatabase**: Debounced 150ms.
- **_homeStatsCache**: Invalidated when full games.json loads or refreshStats() runs.

## Things Worth Double-Checking After Future UI Edits

- GitHub Pages reflects the newest commit on `main`.
- Desktop database arrows remain visible and clickable while scrolling.
- Date column width still keeps secret items aligned.
- Home KPI counters do not cause layout shift.
- Admin import previews render safely and publish in the intended order.
- Admin writes still target `main`, update both JSON data files in one commit, and fail safely if GitHub advances between fetch and commit (ref PATCH is fast-forward-only, no explicit `force: false` needed).
- `_commitGamesState` takes the pre-fetched state object instead of re-reading — one tree walk per admin action instead of two.
- Play feature (`startRandomGame`) now awaits the full games.json load before starting — previously it would crash unless the user had opened Database or Stats first (which is what triggers the lazy load of clues data).
- `_ensureFullGamesLoaded` now propagates fetch errors; all three call sites (database, stats, play) have `.catch` handlers that surface the failure. `_showDataLoadError` reuses the top-bar status indicator.
- Clue-time `<select>` no longer has an inline onchange handler; calls `app.setClueDuration(value)`.
- Re-check visible database details and play result screens after future `innerHTML` edits, especially any new fields that come from pasted/imported game JSON.

## Codex Verification (2026-04-24)

- Verified `main` includes Claude branch commit `6af60cf`; the remaining Claude remote branch is stale relative to `main` and should be deleted during cleanup.
- `data/games.json` and `data/games-meta.json` parse cleanly and metadata regenerates exactly from the full games file.
- Inline browser scripts in `index.html` pass syntax checks.
- Static local asset references in the rendered HTML all exist.
- Local browser smoke test at `http://127.0.0.1:5173/` passed for Home, Play, Database, and Stats with no console errors:
  - Home loaded 197 rounds from `games-meta.json`.
  - Play Random Game loaded full clues before selecting a game and rendered date/player count.
  - Database rendered 197 rows.
  - Stats rendered headline values including `$2,619,998` total paid out and `285` average winners.
