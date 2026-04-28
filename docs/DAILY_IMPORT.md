# Daily Import Workflow

Use this when you have a raw Plaud, YouTube, or AI transcript dump.

1. Put the raw transcript in `incoming/YYYY-MM-DD.txt`.
2. Ask Claude or Codex to import that file using `docs/DAILY_IMPORT_PROMPT.md`.
3. The agent should update `data/games.json` and `data/transcripts.json`, run `npm run audit:fix`, run `npm run audit`, commit on `main`, and push.
4. If there is a special promo or bonus, apply the same `bonus` object to both rounds for that episode unless the promo clearly applies to one round only.

Expected final checks:

```sh
npm run audit:fix
npm run audit
git status --short --branch
git ls-remote --heads origin
```

The only remote branch should be `main`.
