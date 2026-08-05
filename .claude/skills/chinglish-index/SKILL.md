---
name: chinglish-index
description: Regroup and renumber a Chinglish cases folder, then regenerate its INDEX.md and its human-readable tmp/view.md. Final step of the chinglish-* pipeline; run it after a collection round, before committing.
argument-hint: "<cases folder>"
allowed-tools: "Read Glob Bash(python3 *) Bash(ls *) Bash(find *) Bash(git status *) Bash(git check-ignore *)"
---

# Reorganize a cases folder

**Before anything else, invoke the `chinglish-spec` skill** (or read
`.claude/skills/chinglish-spec/SKILL.md`).

One run does three things, in this order:

1. **Regroup and renumber.** Sort every case by its group, cluster same-group cases together,
   and renumber from `0001`.
2. **Write `INDEX.md`** at the folder root, in the three-column format the spec defines. This
   file is committed.
3. **Write `tmp/view.md`.** Every case as one `##` section with its Chinese, its bad English,
   and its good English if it exists, so the author can read a few hundred cases without
   opening a few hundred files. `tmp/` is gitignored; this file is for eyes, not for git.

All three are done by one script. Do not do any of this by hand.

## Usage

For `evals/rewrite-en-tutorial/chinglish` there is a task that needs no arguments:

```bash
mise run update-rewrite-en-tutorial-chinglish-index-and-review
```

For any other folder:

```bash
python3 .claude/skills/chinglish-index/scripts/reindex.py --folder <cases-folder>
```

Preview the renames without touching anything:

```bash
python3 .claude/skills/chinglish-index/scripts/reindex.py --folder <cases-folder> --dry_run
```

Run `--dry_run` first whenever the folder has been through a previous round, so the user sees
which numbers are about to move before it happens.

The script needs no dependencies and runs on any Python 3. It reads `00-meta.toml` with
`tomllib` where available and falls back to a line parser for the flat schema the spec
mandates.

## What "group" means

The sort key is each case's group, then its slug. A case's group is `group` from its
`00-meta.toml` when that key is present, and `type` otherwise.

Slug rather than the existing number, on purpose. Sorting by number would also be idempotent,
but the layout would then depend on the order cases happened to be collected in, and two
folders holding identical cases would look different. Sorting by slug makes the layout a
function of the content alone, and it clusters related slugs so every `*-comma-splice` ends up
adjacent, which is what the deduplication and pattern work needs. The number survives only as a
tiebreaker between duplicate slugs.

The cost is churn: one new case sorting into the middle of a group shifts every number after
it. That is why `--dry_run` exists and why this skill runs before a commit rather than after.

Right now nothing writes `group`, so the script sorts by the five case types, in the canonical
order the spec lists. When pattern induction eventually assigns finer groups, writing a `group`
key into the meta files is all it takes for this script to sort by them instead.

Groups the script does not recognize are sorted last and named in a warning. That is how a
typo in a `type` value surfaces.

## Renumbering changes identifiers

This is the only skill permitted to renumber. Everything else in the pipeline treats case
numbers as permanent.

That is safe only because of when this runs: after a collection round, before the folder is
committed, while nothing outside the folder cites a case number yet. **Once notes, patterns,
or a SKILL.md start referring to specific case numbers, renumbering breaks those references.**
If that has happened, say so and stop rather than running the script.

The rename is two-phase, so a case moving into a slot another case still occupies is handled
correctly. Every rename is printed. The script only renames directories; it never deletes a
case, and it never edits a case's own files.

## After running

1. Report the group counts and the full rename map the script printed.
2. Report any unrecognized group it warned about.
3. Confirm `tmp/view.md` is gitignored at that path with `git check-ignore`, since a cases
   folder can live anywhere and the ignore rule is inherited, not local.
4. Tell the user the folder is ready to commit, and that `INDEX.md` goes in while `tmp/` stays
   out.

## Not built yet

The spec assigns two more jobs to this skill. Neither is implemented, and neither should be
faked by hand:

- **Deduplication and pruning toward a balanced type distribution.** The open question is
  whether pruning deletes or just marks. Deleting loses evidence permanently; a `retired` flag
  in the meta keeps it but leaves the folder cluttered. Probably the flag, with deletion as a
  separate explicit call the user makes on purpose.
- **Pattern induction.** Grouping cases by induced pattern, with per-pattern counts, is the
  actual deliverable that feeds the `rewrite-en-*` skills — a case appearing only once does not
  belong in a SKILL.md, and only counts can establish that. This may deserve to be its own
  skill rather than a side effect of indexing.

Until those exist, this skill is exactly the three mechanical passes above.
