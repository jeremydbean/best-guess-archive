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

## AI Handoff Workflow

This repo is sometimes edited by multiple coding agents (for example Codex and Claude Code) while the owner moves between them.

To reduce drift, every agent should:

- Read [AGENTS.md](AGENTS.md) before making changes.
- Read [AI_HANDOFF.md](AI_HANDOFF.md) for the latest known repo state and open concerns.
- Run `git fetch origin` and confirm whether `origin/main` has moved before starting work.
- Fast-forward or rebase onto `origin/main` before editing if the remote changed.
- After finishing work, update `AI_HANDOFF.md` with the new commit, what changed, and anything the next agent should know.

The goal is simple: one live branch, one current handoff note, and no hidden work in side branches.
