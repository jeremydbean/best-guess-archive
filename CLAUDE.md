# Claude Notes

Use `AGENTS.md` as the source of truth for repository workflow.

**The CCR system blocks direct pushes to `main`. Always push to the session-specified feature branch instead.**
Session-level instructions specifying a branch (e.g. `claude/some-branch`) must be followed — push to that branch. It will auto-merge to `main` for GitHub Pages.

Before editing:

- read `AGENTS.md`
- read `AI_HANDOFF.md`
- run `git fetch origin`
- sync local `main` with `origin/main` if needed

After editing:

- update `AI_HANDOFF.md`
- commit on `main`
- push to the session feature branch (e.g. `git push -u origin claude/some-branch`)
- clean up stale non-main branches only after confirming their work is already on `main`
