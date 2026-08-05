---
name: chinglish-rewrite
description: Write the good English side of Chinglish cases in bulk. Reads each case's meta, Chinese fragment, and bad English, then authors 03-good.md as a native writer would have written it. Second step of the chinglish-* pipeline.
argument-hint: "<cases folder> [which cases, e.g. all missing / 0031-0080 / type=diagram]"
allowed-tools: "Read Write Edit Glob Grep Agent Bash(ls *) Bash(find *) Bash(rg *) Bash(wc *)"
---

# Write the good English for collected cases

**Before anything else, invoke the `chinglish-spec` skill** (or read
`.claude/skills/chinglish-spec/SKILL.md`). It defines what a case is, the five types, the
folder layout, and the meta schema. This skill assumes all of it.

For each case: read `00-meta.toml`, `01-source.md`, and `02-literal.md`; write `03-good.md`;
add `good_origin = "generated"` to the meta. Nothing else in the case directory is touched.

## What "good" has to mean here

These fragments are not going to be read as English. They are going to be **copied into
`rewrite-en-*/SKILL.md` as the ✅ side of ❌/✅ example pairs.** Whatever habit shows up here
gets taught. So the bar is not "better than `02-literal.md`", it is "correct enough to be held
up as the model answer".

Everything you need is in this section. Do not go read the project's style specs; fragments
are small and this short list is the whole standard for them.

### Never

- **No dash characters in body text.** No em dash, no en dash, no ASCII hyphen used as a
  sentence break. Use a period and a new sentence, or parentheses for a genuine aside.
  Hyphens inside compound words (`read-only`, `high-quality`) and as list markers are fine.
  This one matters more here than anywhere else in the project: the known-good English the
  author has been producing leans hard on em dashes, and reproduced across a few hundred ✅
  examples, that habit gets taught to every downstream skill.
- **No LLM tells.** `moreover` · `furthermore` · `it is worth noting that` ·
  `it is important to note` · `delve into` · `crucial` · `pivotal` · `seamless` ·
  `robust` (unless a technical term of art) · `leverage` as a verb · `at its core` ·
  `when it comes to` · `that being said` · `landscape` / `realm` / `tapestry` as metaphor ·
  `not only ... but also` as a default connector. Swapping one connector for another is not a
  fix. Usually the fix is to delete it and let the two sentences sit next to each other.
- **No CJK survives**, including inside code comments and diagram labels.

### Always

- **Register**: a competent professional explaining something to a colleague who is sharp but
  new to this particular topic. Contractions belong there, and their absence is most of what
  makes prose read cold. Second person beats impersonal constructions. Active voice unless the
  actor is genuinely unknown.
- **Sentence length varies.** Fragments are short, so this bites fast: three sentences of
  similar length in a row already reads as machine output.

### The symptoms you are removing

This is what `02-literal.md` did wrong. Naming which one applies is how you know your version
actually fixed something:

- English clause order mirroring Chinese clause order, especially long modifiers piled in front
  of a noun, and topic-comment structures kept intact.
- Calques: set phrases and 成语 rendered word for word instead of by their English equivalent
  or by plain description.
- Literal term choices where English has its own name for the thing. `版本管理` is **version
  control**, not "version management". `链路` is a **pipeline**, not a "chain".
- Connector overuse mirroring Chinese paragraph transitions.
- Missing or wrong articles.
- Redundancy carried over from Chinese emphasis patterns.
- Register collapse: the source is a person talking, the output is a manual.

## Method, per case

Order matters. Do not read ahead.

1. **Read `00-meta.toml` and `01-source.md`.** The `context` field tells you what kind of
   article this is and what the author was doing at that point. That is your register target.
2. **Write the English from the Chinese.** Understand the whole fragment, then express it as a
   native writer would express that idea from scratch. Not sentence by sentence.
3. **Only now read `02-literal.md`**, and use it for exactly two checks:
   - **Coverage.** Did your version drop anything the Chinese actually says? Restore it.
   - **Contrast.** Does your version differ from the bad one on the construction this case is
     about, or only in word choice? If swapping two words would turn yours into `02`, one of
     two things happened: you anchored on it, or the case never had much to teach. Say which,
     in the report. Do not widen the gap artificially to make the pair look better.
4. **Write `03-good.md`.**
5. **Append `good_origin = "generated"`** to `00-meta.toml`.

Step 3 is where the risk lives. Reading `02-literal.md` at all is a deliberate choice: without
it you cannot confirm the pair isolates one construction. But a rewriter that reads it first
stops writing and starts patching, and a patched version carries the Chinese sentence
architecture straight through. Writing before looking is the whole mitigation, so do not
collapse steps 2 and 3.

## What is fixed and what is free

**Form is preserved.** A `bullet-list` case stays a bullet list with the same number of items.
A `diagram` case keeps its graph syntax byte for byte and rewrites only node labels, edge
labels, and subgraph titles. A `passage` case keeps its paragraph count.

**Sentence architecture is free.** Inside that form, split, merge, reorder, and re-subject
whatever you need to. A single Chinese sentence becoming two English ones is usually the fix,
not a liberty.

**Content is fixed.** Nothing added, nothing dropped, no explanatory aside the Chinese does not
have. This is one half of a matched pair; content the other half lacks pollutes the contrast
and makes the example teach two things at once.

**No CJK survives** into `03-good.md`, including inside code comments and diagram labels.

## Execution flow

### Step 1 — Resolve the work list

Default target: every case in the folder that has `01-source.md` and `02-literal.md` and whose
`03-good.md` is missing or empty. The user may narrow it by number range or by `type`.

**Never overwrite a non-empty `03-good.md`.** A case with `good_origin = "manual"` is one the
author wrote or fixed by hand, and it outranks anything this skill produces. To redo one, the
user has to say so explicitly and name the cases.

Report the count before starting.

### Step 2 — Batch

Group the work list by `source_doc`, then split into batches of at most 8 cases. Run batches in
parallel, one subagent each.

Batching by source document is deliberate: fragments from one article share a register and a
vocabulary, and the same Chinese term should come out as the same English term across all of
them. Batching by `type` instead would put fifty unrelated sentences in one context and give
them all one voice.

Eight is a ceiling, not a target. Fragments are short, but attention is not free, and the last
case in a long batch is the one that gets rushed.

### Step 3 — Each subagent

Receives the paths of its cases and the method above. For each case in turn it runs the five
steps, writes the two files, and moves on. It returns only a short per-case line: the case
folder, and either `ok` or a flag.

Flags worth returning:

- `weak` — the good version and the bad one barely differ. See method step 3.
- `unclear` — the Chinese fragment cannot be understood without more of the source document
  than the fragment and its `context` provide.
- `broken` — the fragment's English side is still Chinese, or a file is missing. Something got
  past collection.

Flagged cases still get a `03-good.md` written unless the files are missing. The flag is
information for `chinglish-index`, not a reason to leave a hole.

### Step 4 — Report

1. Cases written, cases skipped as already done.
2. Every flagged case, grouped by flag, with one line each on why.
3. Any case where you had to guess at the Chinese, and what you assumed.
4. One line naming what runs next: `chinglish-index`, to regroup, renumber, and rebuild
   `INDEX.md` and `tmp/view.md`.

Do not summarize the rewriting itself, and do not quote examples of your own good output back
at the user. The place to read this work is `tmp/view.md` after `chinglish-index` runs, where
all three versions sit next to each other.

---

**Maintenance note, for a human, not to be acted on at run time.** The rules under "What
'good' has to mean here" are a deliberate condensation of the project's fidelity contract and
markdown style spec, cut down to what applies to a fragment of a few sentences. It is kept
self-contained on purpose: this skill runs over hundreds of short cases, and loading two full
specs per run buys nothing. If those specs change in a way that matters at fragment scale,
edit this section by hand.
