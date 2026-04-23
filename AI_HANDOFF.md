# AI Handoff

Last updated: 2026-04-23

## Current Branch

- `main`

## Latest Known Commit

- `b7236b7` - Keep games metadata in sync from admin writes

## Current State

- GitHub Pages publishes from `main`.
- Database side arrows are working on desktop.
- Home page KPI counters animate on load without layout shift.
- Admin import/delete flow has extra safety checks and preview escaping.
- Admin import/delete now writes `data/games.json` and `data/games-meta.json` together through the Git database API (blob/tree/commit/ref), avoiding the old contents-endpoint size ceiling and keeping home-page totals in sync.
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
- Admin writes still target `main`, update both JSON data files in one commit, and fail safely if GitHub advances between fetch and commit.
