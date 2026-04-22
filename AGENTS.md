# Agent Workflow

This repository uses a main-only workflow and is often edited by more than one coding agent.

## Before You Start

- Read `AI_HANDOFF.md`.
- Run `git fetch origin`.
- Compare local `main` to `origin/main`.
- If `origin/main` moved, sync before editing:

```bash
git pull --rebase origin main
```

## Branch Rules

- Work directly on `main`.
- Commit directly on `main`.
- Push directly to `origin/main`.
- Do not create feature branches, backup branches, or PR branches unless the owner explicitly asks.

## Handoff Rules

- Treat every push to `main` as a live-site deploy.
- Keep `AI_HANDOFF.md` current.
- When handing off, record:
  - latest commit hash
  - what changed
  - anything still in progress
  - anything another agent should verify

## Practical Preference

- Prefer small, clean commits.
- If another agent has pushed since you started, sync first instead of guessing.
- If you see unexpected changes, assume they may be intentional and avoid reverting them unless explicitly asked.
