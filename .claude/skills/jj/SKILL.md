---
name: jj
description: Use this skill for any version-control action in this repo (committing, describing, branching, undoing, rebasing, resolving conflicts, pushing) and for any general question about jj/Jujutsu. This repo uses jj, not git, as its day-to-day VCS, with a gitmoji-prefixed one-line commit message convention. Trigger whenever the user asks to commit/describe/save changes, mentions jj commands, asks about bookmarks/rebase/undo/conflicts/revsets, or you are about to run a git command in this repo.
---

# jj in this repo

This repo (zink) uses **jj (Jujutsu)**, colocated with a git backend (both `.jj/` and `.git/` exist), for version control. Reach for `jj` commands, not raw `git` commands, for all day-to-day work here — see "Colocated repo: don't mix in raw git" below for why mixing them is risky.

## Agent-safety rules (always follow these)

These avoid hanging the session in a non-interactive environment:

- **Always pass `--no-pager`** on commands that can produce long output: `jj --no-pager log`, `jj --no-pager diff`, `jj --no-pager show <rev>`, `jj --no-pager bookmark list`. Without it, jj may invoke an interactive pager that blocks forever.
- **Always pass `-m` inline** on commands that'd otherwise open an editor: `jj describe -m "..."`, `jj new -m "..."`, `jj squash -m "..."`. Never rely on the editor prompt.
- **Never run interactive subcommands**: `jj split` (no args), `jj squash -i`, and `jj resolve` all open an interactive UI and will hang the session. Use the non-interactive alternatives described below instead.
- **Verify with `jj st` after mutations** (`squash`, `abandon`, `rebase`, `restore`) to confirm the operation did what you expected.

## Commit workflow (always follow this for changes in this repo)

1. **TDD first.** Before or alongside implementing, add/extend a test in the relevant app's `tests.py` using Django's `TestCase`. Run `uv run manage.py test` and confirm it passes before describing a commit.
2. **One logical change per commit.** Don't batch unrelated work into a single changeset. If you've already made multiple unrelated changes in one working-copy commit, pull one out with `jj restore --from <rev> <path>` plus a `jj new`, or use `jj absorb` to auto-distribute hunks into the commits that last touched those lines — don't use `jj split` (interactive, hangs).
3. **Describe with a gitmoji-prefixed, one-line message**, matching the style in `jj log`:
   ```
   jj describe -m ":sparkles: Add contact form"
   ```
   - Pick the gitmoji from https://gitmoji.dev/ that matches the change's nature (`:sparkles:` new feature, `:bug:` fix, `:memo:`/`:pencil2:` docs/typos, `:wrench:` config, `:arrow_up:` dependency bump, `:lock:` security fix, etc.) — check `jj --no-pager log` for precedent if unsure.
   - One line only. No body, no trailer, unless the user asks for one.
4. **Start new work with `jj new`** once a changeset is described, so further edits land in a fresh working-copy commit rather than amending the one you just finished.

Why this matters: jj's working copy *is* a commit (see below), so "committing" here really means describing the working-copy commit and moving on — there's no separate staging step to forget.

## Change IDs vs commit IDs

jj shows two identifiers per commit:

- **Change ID** (e.g. `yoqwstzk`) — stable across rewrites. Prefer this when referring back to a commit you (or a prior command) already touched, since `jj describe`/`jj rebase`/etc. change the commit ID but keep the change ID.
- **Commit ID** (e.g. `245dc553`) — a content hash; changes whenever the commit's content changes (new description, rebase, squash...).

## Revsets

jj commands that take a revision (`-r`) accept a small expression language, not just raw IDs:

- `@` — the working-copy commit
- `@-` — its parent
- `::@` — all ancestors of `@`
- `@::` — all descendants of `@`
- `trunk()..@` — commits between trunk and `@` (useful for seeing "my branch's" commits)
- `bookmarks()` — all commits with a bookmark

Example: `jj --no-pager log -r 'trunk()..@'`.

## Quick command reference

| Task | Command |
|---|---|
| See status | `jj st` |
| Diff working copy (git-style `+`/`-`) | `jj --no-pager diff --git` |
| View history | `jj --no-pager log` |
| Show a specific commit's full diff | `jj --no-pager show <rev> --git` |
| Set/change the current commit's message | `jj describe -m "..."` |
| Start a new empty commit on top | `jj new` (check `jj st` first — skip if `@` is already empty) |
| Base new work on another commit | `jj new <rev>` |
| Edit an existing (non-working-copy) commit | `jj edit <rev>` |
| Fold current commit into its parent | `jj squash` |
| Auto-distribute hunks into the commits that last touched those lines | `jj absorb` |
| Discard working-copy changes (or to specific paths) | `jj restore [path...]` |
| Pull specific paths from another revision | `jj restore --from <rev> <path...>` |
| Drop a commit entirely (descendants reparented) | `jj abandon <rev>` |
| Rebase a commit (and descendants) onto another | `jj rebase -d <rev>` |
| Rebase just one commit (no descendants) | `jj rebase -r <rev> -d <dest>` |
| List/create/move a branch-equivalent | `jj --no-pager bookmark list`, `jj bookmark create <name>`, `jj bookmark move <name> --to <rev>` |
| Push a bookmark to the remote | `jj git push -b <name>` |
| Fetch remote changes | `jj git fetch` |
| See every operation (safety net) | `jj --no-pager op log` |
| Undo the last operation | `jj undo` (or `jj op restore <op-id>` for further back) |

## Key mental model differences from git

- **No staging area / index.** The working copy *is* a commit (an anonymous one until you `jj describe` it). Every edit you make to files is already "committed" to that working-copy commit automatically — there's nothing to `git add`.
- **Commits are mutable.** Unlike git, you can freely update a commit's description, contents, or position (squash/rebase/absorb) without the rewrite anxiety git trains you to have. Refine commits in place rather than piling on fixup commits.
- **`jj new` vs git's commit.** Since the working copy is always a live commit, finishing a unit of work means describing it (`jj describe -m "..."`) and then calling `jj new` to start the next one — not "committing" in the git sense.
- **Bookmarks, not branches.** jj's bookmarks are git-branch-equivalents, but they don't auto-advance the way a git branch does when you commit. Before pushing, explicitly move the bookmark: `jj bookmark move <name> --to @` (or `jj bookmark create <name>` if none exists yet), then `jj git push -b <name>`.
- **Conflicts don't block you.** jj lets a commit hold unresolved conflicts, so rebases and other operations never interrupt you demanding resolution first. To resolve: edit the conflicted file directly to remove the conflict markers, then run `jj st` to confirm it cleared — don't use `jj resolve` (interactive, hangs).
- **The operation log is a full undo history.** Every jj command (describe, rebase, squash, abandon...) is an "operation" you can inspect with `jj --no-pager op log` and revert with `jj undo`. This makes jj commands safe to try — if something goes sideways, `jj undo` gets you back.

## Colocated repo: don't mix in raw git

This repo has both `.jj/` and `.git/` (colocated). That makes it *possible* to run git commands here, but doing so outside of a deliberate, narrow handoff risks desyncing jj's view of the repo from git's. Concretely:

- Don't run git commands for anything this skill's jj commands already cover (status, diff, log, commit/describe, branch/bookmark, rebase) — use the `jj` equivalents above.
- If you must briefly use `git` (e.g. a merge-tool workflow only git supports), first confirm `jj st` is clean, do the git operation, then run `jj st` again or `jj edit <change-id>` to let jj re-sync — never leave the repo mid-git-operation and resume with jj.

## When unsure

Run `jj --no-pager log` first to see current state and match the existing commit-message style before describing anything new.
