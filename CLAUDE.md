# Claude Notes

Use `AGENTS.md` as the source of truth for repository workflow.

## ⚠️ Critical: How Pushing Works in CCR Sessions

**`git push origin main` will ALWAYS fail with HTTP 403 in Claude Code Remote (web) sessions.**
This is a permanent system-level block — not a credential problem. Do NOT waste time trying
different tokens, OAuth keys, or credential helpers. It cannot be fixed.

**The correct push workflow:**
1. Commit work locally on `main` as normal
2. Push to the session feature branch: `git push -u origin <session-branch>`
3. Reset local main to remote: `git reset --hard origin/main`
4. GitHub Actions auto-merges `claude/*` branches to `main`, deletes the session branch, and GitHub Pages updates

**Never use MCP `push_files` as a workaround** — it exhausts the user's API rate limit.

The session branch name is in the session-level instructions at the top of the conversation
(e.g. `claude/code-review-improvements-TImSY`).

---

Before editing:

- read `AGENTS.md`
- read `AI_HANDOFF.md`
- run `git fetch origin`
- sync local `main` with `origin/main` if needed

After editing:

- update `AI_HANDOFF.md`
- commit on `main`
- push to the session feature branch: `git push -u origin <session-branch-from-instructions>`
- reset local main: `git reset --hard origin/main`
- GitHub Actions handles the merge to `main` automatically
- the merge workflow deletes the session branch after a successful merge
