# Daily Import Prompt

Paste this to Claude or Codex with the raw transcript path or the transcript text.

```text
Import this Best Guess Live episode into the archive.

Inputs:
- Raw transcript: [paste text or path, usually incoming/YYYY-MM-DD.txt]
- Date: [full date if known]
- Host(s): [if known]
- Special promo/bonus: [describe if announced, otherwise "none known"]

Tasks:
1. Extract two rounds unless the episode was cancelled.
2. For each playable round, determine:
   - secret item
   - 5 clues in order
   - correct count and total guesses for each clue
   - format (`v2` tiered or `v1` classic)
   - gold/silver/bronze clue numbers, winner counts, and payouts for v2 games
   - winning clue, winner count, and per-winner payout for v1 classic games
   - total winners
   - winner names
   - common wrong guesses
   - clue explanations
3. Update the correct `data/games-YYYY.json` year shard. Do not update stale backup `data/games.json`.
4. Run `npm run audit:fix` to regenerate `data/games-meta.json` from all year shards.
5. Add or update the matching `data/transcripts.json` entry using exactly these sections:
   `Intro`, `Round 1`, `Round 1 Results`, `Round 2`, `Round 2 Results`, `Outro`.
6. Keep transcript lines shaped as `{ "speaker": string_or_null, "text": string }`.
7. If a promo/bonus applies to the episode, add the same `bonus: { "title", "desc" }` object to both round objects unless the transcript clearly says it only applies to one round.
8. If silver or bronze had no winners, keep all five clue objects and record that medal tier with `0` winners and `0` payout. Omit that tier's medal clue field or set it to `0`; do not invent a medal clue number and do not move later winners into that tier. Empty medal tiers cascade from the bottom upward, so silver cannot be empty while bronze has winners. The archive handles official redistribution separately, so do not add an `adminNote` just to explain standard redistribution.
9. Use these format rules unless the episode states otherwise:
   - Before Monday, May 11, 2026: both rounds are usually `format: "v2"` tiered gold/silver/bronze.
   - Monday, May 11 through Tuesday, May 26, 2026: hybrid format. Round 1 is `format: "v2"`. Round 2 is `format: "v1"` classic mode: set `winningClue` to the earliest clue with correct answers, `winnerCount` and `totalWinners` to that clue's correct count, and `winnerPayout` to the per-winner share of the full $7,500 pot. Set medal winner/payout fields to `0`, with `goldClue` equal to `winningClue` for compatibility and `silverClue`/`bronzeClue` set to `0`.
   - Starting Wednesday, May 27, 2026: both rounds are `format: "v2"` tiered gold/silver/bronze.
10. Run `npm run audit` one final time and fix every error before committing.
11. Commit directly on `main` and push to `origin/main`. Do not create a branch.

After finishing, report:
- commit hash
- episode date and secret items
- audit result
- any uncertain fields
```
