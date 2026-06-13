# Daily Import Workflow

Use this when you have a raw Plaud, YouTube, or AI transcript dump.

1. Put the raw transcript in `incoming/YYYY-MM-DD.txt`.
2. If starting from audio only, use `docs/PLAUD_AUDIO_PROMPT.md` first to generate a structured transcript/count pass from spoken audio only. Do not ask Plaud to infer screenshot-only data.
3. Ask Claude or Codex to import that file using `docs/DAILY_IMPORT_PROMPT.md`.
4. The agent should update the correct year shard (`data/games-2026.json`, `data/games-2027.json`, etc.) and `data/transcripts.json`, run `npm run audit:fix`, run `npm run audit`, commit on `main`, and push.
5. If there is a special promo or bonus, apply the same `bonus` object to both rounds for that episode unless the promo clearly applies to one round only.
6. If a silver or bronze tier had no winners, record the actual tier as empty: keep all five clue objects, set that tier's winners and payout to `0`, omit its medal clue field or set it to `0`, and let importer/app logic handle official redistribution. Empty medal tiers cascade from the bottom upward, so bronze can be empty by itself, or silver and bronze can both be empty. Do not add an `adminNote` just to explain this standard redistribution.
7. Use the date-based format rules unless the broadcast says otherwise: before Monday, May 11, 2026 both rounds are usually `format: "v2"`; Monday, May 11 through Tuesday, May 26, 2026 is hybrid with Round 1 `format: "v2"` and Round 2 `format: "v1"` classic; starting Wednesday, May 27, 2026 both rounds are `format: "v2"` tiered.

Expected final checks:

```sh
npm run audit:fix
npm run audit
git status --short --branch
git ls-remote --heads origin
```

The only remote branch should be `main`.
