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
   - gold/silver/bronze clue numbers, winner counts, and payouts for v2 games
   - total winners
   - winner names
   - common wrong guesses
   - clue explanations
3. Update `data/games.json`.
4. Run `npm run audit:fix` to regenerate `data/games-meta.json` from `data/games.json`.
5. Add or update the matching `data/transcripts.json` entry using exactly these sections:
   `Intro`, `Round 1`, `Round 1 Results`, `Round 2`, `Round 2 Results`, `Outro`.
6. Keep transcript lines shaped as `{ "speaker": string_or_null, "text": string }`.
7. If a promo/bonus applies to the episode, add the same `bonus: { "title", "desc" }` object to both round objects unless the transcript clearly says it only applies to one round.
8. Run `npm run audit` one final time and fix every error before committing.
9. Commit directly on `main` and push to `origin/main`. Do not create a branch.

After finishing, report:
- commit hash
- episode date and secret items
- audit result
- any uncertain fields
```
