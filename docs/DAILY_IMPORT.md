# Daily Import Workflow

Use this when you have a raw Plaud, YouTube, or AI transcript dump.

1. Put the raw transcript in `incoming/YYYY-MM-DD.txt`.
2. If starting from audio only, use `docs/PLAUD_AUDIO_PROMPT.md` first to generate a structured transcript/count pass from spoken audio only. Do not ask Plaud to infer screenshot-only data.
3. Ask Claude or Codex to import that file using `docs/DAILY_IMPORT_PROMPT.md`.
4. The agent should update the correct year shard (`data/games-2026.json`, `data/games-2027.json`, etc.) and `data/transcripts.json`, run `npm run audit:fix`, run `npm run audit`, commit on `main`, and push.
5. If there is a special promo or bonus, apply the same `bonus` object to both rounds for that episode unless the promo clearly applies to one round only.
6. If a silver or bronze tier had no winners, record the actual tier as empty: keep all five clue objects, set that tier's winners and payout to `0`, omit its medal clue field or set it to `0`, and let importer/app logic handle official redistribution. Empty medal tiers cascade from the bottom upward, so bronze can be empty by itself, or silver and bronze can both be empty. Do not add an `adminNote` just to explain this standard redistribution.
7. Use the date-based format rules unless the broadcast says otherwise: before Monday, May 11, 2026 both rounds are usually `format: "v2"`; Monday, May 11 through Tuesday, May 26, 2026 is hybrid with Round 1 `format: "v2"` and Round 2 `format: "v1"` classic; starting Wednesday, May 27, 2026 both rounds are `format: "v2"` tiered.
8. If an episode aired but the transcript, screenshots, or result counts are missing, import it as partial data rather than cancelled. Set `dataStatus: "partial"`, store known facts in their normal structured fields, and use JSON `null` for unknown numeric values. Use `partialClues` only until all five clue texts are known; then promote them to the normal `clues` array. Add a transcript placeholder with `dataStatus: "unavailable"`, confirmed round metadata, and six empty canonical sections. Never fabricate dialogue or expose collection/provenance notes in public game fields.
9. If a screenshot shows a round-level audience count in the top corner, store it as numeric `totalPlayers`. Keep it separate from each clue's `guesses`; those are clue submission counts and remain the source for guess-based statistics.
10. Partial records automatically receive an **Incomplete archive record** marker, an exact missing-field list, and a support-form upload link in the public UI. Do not write a custom public note for this. Add recovered values to their canonical fields and keep `dataStatus: "partial"` until the generated list is empty and the transcript is available.

Expected final checks:

```sh
npm run audit:fix
npm run audit
git status --short --branch
git ls-remote --heads origin
```

The only remote branch should be `main`.
