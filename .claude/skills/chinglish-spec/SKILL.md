---
name: chinglish-spec
description: Background and shared contract for the Chinglish case library — why it exists, what a case is, the five case types, the cases folder layout, and the meta and index formats. Loaded by chinglish-collect, chinglish-rewrite, and chinglish-index. Not a task; it defines the vocabulary they all share.
---

# Chinglish case library — spec

Shared background and data contract for the `chinglish-*` skills. Read this before running
any of them. It defines terms the other three assume; none of them restate it.

## 1. Why this library exists

The `rewrite-en-*` skills need a handful of ❌/✅ examples that teach what Chinglish is. The
temptation is to sit down and invent them. That fails two ways: invented examples cover
whatever the inventor happened to think of, and a model shown a short list of specific bad
phrasings starts pattern-matching against the list instead of judging the sentence in front
of it.

So the examples have to be earned. Collect a few hundred real cases first, induce recurring
patterns from the pile, then pick one or two representatives per pattern. **A case that
appears only once in the library does not belong in a SKILL.md.** The library is the
evidence; the handful of examples that ship are the conclusion.

That is the whole point of the pipeline, and it explains the design choices below —
especially why collection appends indiscriminately and why nothing is judged until the end.

## 2. A case is a fragment, not a document

One case directory holds one excerpt: a sentence, a paragraph, a bullet list, a diagram, a
run of paragraphs. A single source document normally yields five to thirty cases.

Never file a whole document as one case. A case must be small enough that a reader sees the
Chinese construction, the damage it caused, and the fix, all at once.

Three texts define a case:

| | What it is | Where it comes from |
| :--- | :--- | :--- |
| **source** | the Chinese fragment, verbatim | excerpted from the Chinese document |
| **literal** | the same fragment as it appears in an existing English translation, stiff and over-faithful — the negative example | excerpted from that document's English translation |
| **good** | that fragment as an English writer would actually have written it | authored by `chinglish-rewrite` |

The first two are **found, not made**. Both sides of the negative example already exist on
disk before collection starts; nothing in the pipeline translates Chinese into English.

## 3. The five case types

Every case carries exactly one `type`. Use these terms verbatim.

| `type` | Size | What it captures |
| :--- | :--- | :--- |
| `sentence` | one sentence | word-for-word rendering of a single Chinese sentence |
| `paragraph` | one paragraph, roughly 3–10 sentences | a paragraph whose internal flow is carried over from Chinese |
| `passage` | 2–4 consecutive paragraphs | fragments that read acceptably alone but badly together — repetition, dead transitions, lost argument shape |
| `bullet-list` | one list, or a contiguous run of items | items that stay parallel in Chinese but fall apart in English |
| `diagram` | one `mermaid` or other diagram block | node and edge labels, and coined Chinese terms that have a real English name |

**A balanced library is the goal, but balance is never achieved during collection.** Real
documents supply whatever they supply — some have no diagrams, some are one long argument.
Collection takes everything it finds and records the type. `chinglish-index` prunes the
over-represented types later, when the whole pile is visible. Nobody balances by padding.

## 4. The cases folder

The destination is an ordinary directory; any path can be one. In this repo they live per
register, for example `evals/rewrite-en-tutorial/chinglish/`.

```text
<cases-folder>/
├── INDEX.md
├── 0001-mini-task-chain/
│   ├── 00-meta.toml
│   ├── 01-source.md    Chinese fragment          written by chinglish-collect
│   ├── 02-literal.md   stiff English             written by chinglish-collect
│   └── 03-good.md      good English              written by chinglish-rewrite
├── 0002-repo-setup-steps/
└── ...
```

- Directory name is `NNNN-slug`: four digits, hyphen, then a short kebab-case English label
  **for the fragment itself**, not for the document it came from.
- Filenames are fixed. Readers open them by position.
- Numbering is per folder and starts at `0001`. It is permanent everywhere except in
  `chinglish-index`, which reassigns numbers when it regroups. That is safe only because it
  runs before the folder is committed and before anything outside the folder cites a number.
- One cases folder holds one register. Do not mix.
- A case is **incomplete** until `03-good.md` exists. Incomplete cases are normal — collection
  runs well ahead of rewriting.

**These files belong in version control.** They are the reference material for comparison
testing, not scratch output. The author commits a folder once it has been through
`chinglish-index`, so an uncommitted folder mid-collection is expected and fine.

### `00-meta.toml`

TOML, because `chinglish-index` parses these to regroup and prune.

```toml
type = "sentence"
context = "出自一篇 GitHub 入门课的索引型 README, 作者在说明各篇 mini task 之间的依赖关系."
source_doc = "evals/rewrite-en-tutorial/pairs/001-github-basics-overview/source.md"
literal_doc = "evals/rewrite-en-tutorial/pairs/001-github-basics-overview/gold.md"
```

| Key | Written by | Value |
| :--- | :--- | :--- |
| `type` | collect | one of the five terms above, verbatim |
| `context` | collect | one or two Chinese sentences: what kind of article this came from and what the author was doing at that point. The only thing that lets a later reader judge register without opening the source. **Describe the setting; do not diagnose the translation.** |
| `source_doc` | collect | path to the Chinese original |
| `literal_doc` | collect | path to the English document the stiff fragment was excerpted from |
| `good_origin` | rewrite | `generated` or `manual` |

Keep values on one line. Use basic strings and escape embedded quotes.

### `INDEX.md`

Three columns, nothing else:

```markdown
# Chinglish cases

| folder | type | 中文原文 |
| :--- | :--- | :--- |
| 0001-mini-task-chain | sentence | 这门课的 mini task 是一路长起来的: 前几篇都在你自己的同一个 repo 上操作… |
```

The third column previews the Chinese fragment. `chinglish-index` generates it; the rules are
recorded here so a hand-written row looks the same:

- **One line, the first one.** Not the whole fragment flattened. A bullet list previews as its
  first bullet; a passage as its opening line. Code-fence markers hold no content and are
  skipped, so a diagram previews as its first real line. If the first line happens to carry no
  Chinese, look ahead for one — this column is 中文原文.
- **Markdown link syntax reduces to its visible text** before anything is counted:
  `[文字](https://…)` becomes `文字`, `![说明](img.png)` becomes `说明`. A URL must never eat
  the character budget or widen the table.
- Then collapse whitespace, truncate at 50 characters, append `…`, and escape `|` as `\|`.
  Escaping comes last so the backslash costs nothing.

`chinglish-collect` appends rows in creation order and does nothing else to this file.
`chinglish-index` owns every other operation on it.

## 5. Rules every chinglish-* skill obeys

- **Fragments are quoted verbatim.** Never paraphrase, clean up, or trim a fragment to make a
  point land harder. All three files are evidence.
- **Never edit `02-literal.md` because it reads badly.** Reading badly is its purpose.
- **Never file a case whose English side is still Chinese.** If a fragment's English never got
  translated — a mermaid label left in CJK, an untouched list item — that is a defect in the
  material, not a case. Skip the fragment and count the skip. A case whose `02-literal.md` is
  Chinese is a corrupt row that someone will have to find by hand later.
- **Never file a case whose Chinese trigger cannot be named.** If nobody can point at the
  construction on the Chinese side that caused the bad output, the case teaches rewriting by
  vibe. Wording preference, sentence-length taste, and paragraph-splitting differences are not
  cases.
- **Never renumber, sort, or deduplicate during collection.** Collection cannot see the whole
  pile, so it is not equipped to judge either one. `chinglish-index` reorders the folder later
  from the case content, so nothing is lost by appending blindly.
- **Never mix registers in one folder.**

## 6. Who owns what

| Skill | Does |
| :--- | :--- |
| `chinglish-collect` | mines document pairs for fragments; writes `00-meta.toml` and copies both sides into `01-source.md` and `02-literal.md`; appends to `INDEX.md` |
| `chinglish-rewrite` | writes `03-good.md` for cases that lack it; adds `good_origin` to meta |
| `chinglish-review` | reads `tmp/view.md` and reports which `03-good.md` are not good enough; writes nothing but its own report |
| `chinglish-index` | rebuilds `INDEX.md`, prunes toward a balanced type distribution, deduplicates, groups by induced pattern |

Split this way on purpose. Collection is bulk work over many documents and wants to be cheap
and indiscriminate. Rewriting is careful authoring, one fragment at a time. Reorganizing needs
the whole pile in view. Running them together produces a library that is none of the three.

**No skill in this pipeline translates Chinese into English.** The negative example is always
excerpted from an English document that already existed, produced by some upstream process
without any good version in view. That is what makes it evidence.

The moment a skill is allowed to supply a missing English side, the corpus starts containing
text no real pipeline ever emitted, and nothing downstream can tell the two apart. Worse, a
generator that has the Chinese in front of it and knows the output is meant to be the bad
example will produce a caricature, and a caricature teaches nothing. So a Chinese document
with no English counterpart is not material: it gets skipped and reported, never filled in.
