# AI Handoff

Last updated: 2026-04-22

## Current Branch

- `main`

## Latest Known Commit

- `9b375db` - Fix regressions from Codex commits

## Current State

- GitHub Pages publishes from `main`.
- Database side arrows are working on desktop.
- Home page KPI counters animate on load without layout shift.
- Admin import/delete flow has extra safety checks and preview escaping.
- Stats payout badges were corrected to avoid relying on Tailwind arbitrary classes inside JS-rendered HTML.
- Database date column width was reduced from the earlier oversized value to better preserve secret-item alignment.

## Working Agreement

- Pull/rebase `origin/main` before making edits if remote has moved.
- Leave all work on `main`.
- Update this file after meaningful changes so the next agent can pick up quickly.

## Things Worth Double-Checking After Future UI Edits

- GitHub Pages reflects the newest commit on `main`.
- Desktop database arrows remain visible and clickable while scrolling.
- Date column width still keeps secret items aligned.
- Home KPI counters do not cause layout shift.
- Admin import previews render safely and publish in the intended order.
