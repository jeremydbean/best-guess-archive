# Contributing

This repository intentionally uses a simple main-only workflow.

Rules:

- Make all changes directly on `main`.
- Commit directly on `main`.
- Push directly to `origin/main`.
- Do not create or use feature branches, working branches, revert branches, backup branches, or pull-request branches unless the owner explicitly asks for them.
- Treat pushes to `origin/main` as live-site deploys because GitHub Pages publishes from `main`.

If `origin/main` has moved, update with:

```bash
git pull --rebase origin main
```

Then continue working on `main`.
