---
name: chinglish-collect
description: Mine Chinese documents and their existing English translations for Chinglish case fragments, filing each into a cases folder as a source plus bad-English pair. Bulk collection step of the chinglish-* pipeline; copies both sides verbatim and writes no English of its own.
argument-hint: "<where the Chinese and English material is, how it corresponds, and which cases folder to file into>"
allowed-tools: "Read Write Glob Grep Agent Bash(mkdir *) Bash(cp *) Bash(ls *) Bash(find *) Bash(rg *) Bash(head *) Bash(wc *)"
---

# Collect Chinglish cases

**Before anything else, invoke the `chinglish-spec` skill** (or read
`.claude/skills/chinglish-spec/SKILL.md`). It defines what a case is, the five types, the
folder layout, and the meta and index formats. This skill assumes all of it and does not
restate it.

Mine documents for fragments where the English is visibly damaged by a Chinese construction.
File each fragment as `00-meta.toml` + `01-source.md` + `02-literal.md`.

## This skill writes no English

Both sides of every case already exist on disk. The user supplies Chinese documents and their
English translations; this skill excerpts from them.

- `01-source.md` is copied verbatim out of the Chinese document.
- `02-literal.md` is copied verbatim out of the English document.
- `03-good.md` is not written here at all. `chinglish-rewrite` fills it in later.

**Never translate, never generate, never touch up.** Not when the English looks unfinished,
not when a fragment reads so badly you could obviously improve it, not when the English side
is missing. If a Chinese document has no English counterpart, it is not usable material for
this skill: report it and move on. Producing the missing side yourself would put text into the
corpus that no real pipeline ever emitted, and nothing downstream could tell it apart from the
genuine article.

Both files are evidence. Copy them, do not author them.

## Inputs

Two things, in plain language, from the user:

1. **Where the material is and how the two sides correspond.** A directory, a set of paths,
   two parallel trees, or an explicit list.
2. **Which cases folder to file into.**

Ask about anything not stated. Never infer the destination, never guess a register from a path.

## Execution flow

### Step 1 — Resolve the destination

Confirm the cases folder path. Create it if missing, with an `INDEX.md` holding only the
header rows. Read any existing `INDEX.md` to learn which numbers are taken.

### Step 2 — Resolve the material

Turn the user's description into an explicit list of (Chinese document, English document)
pairs.

**Default pairing convention**, absent anything else from the user: within one directory, two
files sharing a stem where one carries a `-cn` suffix are a pair — `foo-cn.md` is Chinese,
`foo.md` is English.

Treat that as a hint. **Verify against the files**: the Chinese side is the one whose prose is
predominantly CJK. If suffix and content disagree, trust the content and say so in the report.

Other shapes, all stated by the user rather than detected: parallel `zh/` and `en/` trees,
`.zh.md` / `.en.md` stems, or an explicit list of paths.

Any Chinese document with no English counterpart is skipped and reported. Do not translate it.

**Before doing any work, show the resolved pair list and get confirmation** — Chinese path,
English path, and the register you were told. A mispaired document poisons every case mined
from it and nothing downstream will catch it.

### Step 3 — Mine each document

One subagent per document, in parallel. Each receives the Chinese source and its English
counterpart, and returns candidates. It writes nothing — the main agent does all filing, so
numbering stays consistent across parallel subagents.

Each mining subagent:

1. **Aligns the two texts.** Anchor on headings first, then paragraph order within a section.
   Where alignment becomes ambiguous, skip that stretch rather than guessing.
2. **Walks the whole document looking for all five types.** Make a deliberate pass for
   `diagram` and `passage`; they are the ones that get missed. If the document has no
   diagrams, it produces no `diagram` cases — that is fine and expected. Do not invent one,
   do not stretch some other fragment to fill the slot.
3. **Applies the selection criteria below.**
4. **Returns candidates.** For each: `type`, both fragments quoted verbatim, a proposed slug
   for the fragment, and one or two Chinese sentences of `context`.

### Step 4 — Selection criteria

- **Only damage traceable to a Chinese construction**, and the subagent must be able to name
  that construction. If it cannot, discard.
- **The gap must be visible.** If a reader has to be told why the English is bad, the case is
  too subtle to teach anything.
- **Verbatim only.** Never paraphrase, clean up, trim, or repair either side.
- **Discard any fragment whose English side is still Chinese.** An untranslated mermaid label,
  a list item left in CJK, a code comment nobody touched — that is a hole in the material, not
  a case. Count these and report the total; many of them means the English document is
  unfinished and the user should know before mining more of it.
- **At most three instances of the same construction per document.** A sampling budget on the
  mining side, not deduplication at filing time.
- Ignore two known defects that are **not** Chinglish: heavy em-dash use, and cross-document
  links still pointing at Chinese targets. A different skill owns both.

### Step 5 — File

For each candidate, in the order the subagents returned them:

1. Take the next number: highest four-digit prefix in the folder, plus one.
2. Create `NNNN-slug/`, write `00-meta.toml`, `01-source.md`, `02-literal.md`.
3. Append one row to `INDEX.md`.

**Append blindly.** Do not deduplicate against existing cases, do not reorder, do not merge,
do not skip a candidate because it resembles `0042`, and do not balance the type distribution.
`chinglish-index` prunes later with the whole pile in view; it works better on an unfiltered
one.

### Step 6 — Report

1. Destination folder and the number range added (`0031`–`0119`).
2. Type distribution: count per type. State it flatly, as a record of what the material held.
   A skewed run is not a problem to fix here.
3. Documents processed, and cases yielded by each.
4. **Fragments discarded because their English side was still Chinese**, per document.
5. Chinese documents skipped for having no English counterpart.
6. Any pair where the `-cn` convention disagreed with the file contents.
7. Any stretch skipped because the two texts would not align.
8. One line: these cases have no `03-good.md` yet, and `chinglish-rewrite` is what fills them.
