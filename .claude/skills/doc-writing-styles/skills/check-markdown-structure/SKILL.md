---
name: check-markdown-structure
description: Compare the structural skeleton of two Markdown documents and report where they stop lining up. Use after producing a translated or rewritten version of a document to confirm that headings, code blocks, tables, quotes, images, lists, and rules still appear in the same order. Reads only and never edits. Takes two file paths, in either language, in either direction.
argument-hint: "--left <a.md> --right <b.md> [--inventory] [--json_output]"
---

# Check that two Markdown documents still line up

## 1. What this does, and what it will not do

It reads two Markdown files, lists the block elements each one is built from, lines the two
sequences up, and prints where they part ways.

**It makes no edits. It proposes none.** Fixing a divergence belongs to whoever wrote the
document, using whatever rewrite skill produced it. Keeping detection separate from repair is
what lets a rewrite step and a check step be composed in any order, and it is the reason this
skill has no opinions about writing.

It also does not judge the prose. Whether the English reads well is not a question a script can
answer, and pretending otherwise has cost this project more than it ever returned.

---

## 2. When to run it

After a document has been rewritten into another language, compare the version you rewrote from
against the version you produced.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/check-markdown-structure/scripts/structure_report.py \
    --left lesson-cn.md --right lesson.md
```

If `${CLAUDE_PLUGIN_ROOT}` is not set, the script sits at
`<plugin-root>/skills/check-markdown-structure/scripts/structure_report.py`, where
`<plugin-root>` is the directory holding `.claude-plugin/plugin.json`.

`--left` is the document you rewrote from and `--right` is the one you produced. Add
`--inventory` to also list each file's elements on its own, and `--json_output` to parse the
result instead of reading the table. Exit code 0 means the skeletons agree, 1 means they
diverge, 2 is a usage error.

**Do not run it across a restyle in the same language.** Restyling is allowed to add a table,
split a section, or drop a paragraph, so a divergence there carries no information.

**Do not run it across a whole document set.** Consistency between sibling documents depends on
how a particular batch was organized, which is a property of your workflow and not of this
plugin. This skill compares exactly two files.

---

## 3. What it compares, and what it deliberately ignores

Elements tracked, in document order: **headings** with their level, **code blocks** with their
language, **tables**, **blockquotes**, **images**, **lists** with their kind and item count, and
**horizontal rules**. Front matter is skipped as metadata.

**Matching is by element type and position, never by text.** The two documents are usually in
different languages, so heading text cannot line up and is not expected to. The excerpt printed
beside each element is there for you to recognize it by, not for the comparison.

Three kinds do carry content that should survive a translation untouched, and those are compared
for real:

| Kind | What is compared |
| :--- | :--- |
| Code block | The body. Comments are stripped before the comparison, since a comment is prose and is supposed to be translated. A block whose comments moved but whose code did not is marked `~` and is not a finding |
| Table | Row and column count |
| Image | The path |

---

## 4. Reading the report

```text
    #  lesson-cn.md                                  lesson.md
  -----------------------------------------------------------------------------
   15  h2            5. 你会的其实是一条完整的主线  =  h2       5. What you know is really
   16  image         在 Licensing 页面查看当前套餐  -
   17  table 5x3     机器配置 倍率 每月实际可用时长 !  table 4x3  Machine size Multiplier Real
```

| Mark | Meaning |
| :--- | :--- |
| `=` | Same kind in the same place |
| `-` | Present on the left only |
| `+` | Present on the right only |
| `x` | Different kind in the same place |
| `!` | Same kind, but the content check failed |
| `~` | Code block whose comments were translated and whose code is unchanged. Not a finding |

A run of `+` or `-` followed by the sequence resyncing means something was inserted or dropped.
A long tail of `x` means the two documents went out of step earlier and never recovered, so read
upward to the first divergence rather than treating each line as its own problem.

---

## 5. What to do with a finding

Report it. Name the file, the line, and the element. Then stop.

If you are being asked to repair as well, that is a separate instruction and a separate step:
open the document that is wrong, put the missing element back or take the extra one out, and
leave every sentence around it alone. A structural repair that rewrites neighboring prose is a
worse outcome than the divergence it fixed.

**One divergence is not automatically a defect.** A rewriter may have had a real reason, and the
author is the one who decides. Say what diverged and let them rule on it.
