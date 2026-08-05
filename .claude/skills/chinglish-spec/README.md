# The Chinglish case library: design of the five skills

This document explains why `chinglish-spec`, `chinglish-collect`, `chinglish-rewrite`,
`chinglish-index`, and `chinglish-review` exist, and why the work is cut into these five
pieces. Directory layout, field schemas, and execution steps live in the individual SKILL.md
files and are not repeated here.

Chinese version: [README-cn.md](README-cn.md).

---

## 1. The problem

The `rewrite-en-*` skills turn the author's Chinese technical documents into English. Their
SKILL.md files need a set of ❌/✅ examples that teach the model what Chinglish is and what
idiomatic English looks like.

The trouble is that this set cannot be invented at a desk. Hand-enumerating examples fails two
ways at once:

- **Coverage equals whatever the author happened to think of that day.** An entire class of
  problem that did not come to mind never lands on the list, and so never gets fixed.
- **The model overfits to the list.** Given a roster of specific bad phrasings, it starts
  matching sentences against the roster instead of judging, from the source, what would
  actually read well. The more concrete the examples, the stronger this effect.

The two pressures conflict: too few examples fail to convey what Chinglish is, too many pull
the model off the source. Guessing at the balance point does not work.

So the examples have to be **earned rather than invented**. Collect a few hundred real cases,
induce the recurring patterns, then pick one or two representatives per pattern. The test is
blunt: **a case that appears only once in the library does not belong in a SKILL.md.** The
library is the evidence; the dozen or so examples that ship are the conclusion.

These five skills are the pipeline that runs from evidence to conclusion.

---

## 2. Flow

```text
     Chinese documents, plus whatever English versions exist
                        |
        chinglish-collect      cut into fragments, keep (Chinese, bad English),
                        |      append indiscriminately
        chinglish-rewrite      add what an English writer would have written
                        |
        chinglish-index        dedupe, prune, group by pattern, and emit the reading copy
                        |
        chinglish-review       read it through, name which good versions fall short, send them back
                        |
                 a list of patterns
                        |
                 into rewrite-en-*/SKILL.md

        chinglish-spec  ----  the shared vocabulary and data contract the other four depend on
```

`rewrite` and `review` form a loop: review's output is a list of case names fed straight back
into rewrite. A person decides when the loop stops. No score does.

A case is a **fragment**, not a whole document. It has to be small enough that a reader sees
three things at once: the Chinese construction, the damage it caused, and how it should have
been written. A whole document cannot do that.

---

## 3. Why five skills

In one line: **these five jobs differ in cost, in the judgment they demand, and in how much
they need to see at once.** Merged, they produce something that does none of them well.

**`chinglish-collect` is bulk labor. It should be cheap and undiscriminating.** It sweeps
hundreds of documents and pulls anywhere from a handful to a few dozen fragments out of each.
Fastidiousness here is actively harmful: it cannot see the whole pile, so it is in no position
to judge whether a case is a duplicate or whether the type distribution is balanced. Its job
is to append.

**`chinglish-rewrite` is careful authoring, one fragment at a time.** Producing what a native
writer would actually have written is the most expensive and most judgment-heavy step in the
chain, and it is a different operation from bulk scanning. Folded into collection, it gets
dragged down to collection's pace and turns perfunctory.

**`chinglish-index` cannot work without seeing everything.** Deduplication, pruning, and
pattern induction all require global view. It is the only skill permitted to delete, reorder,
or renumber.

**`chinglish-review` has to be read-only.** It finds problems; it does not fix them. An agent
that can do both quietly fixes what it finds, so nobody learns what changed and nobody can
judge whether its judgment is worth trusting. It is not even allowed to propose replacement
text: a suggested rewrite in a report becomes the final wording, and it was written without the
Chinese in view the way `chinglish-rewrite` has it.

**`chinglish-spec` is not a task, it is a vocabulary.** The other four share one data contract.
Written out four times, the copies drift, and the drift only surfaces after several hundred
cases have already been filed. So the contract lives in exactly one place and the other four
load it before doing anything. It is not user-invocable, because it is not an action anyone can
run.

---

## 4. Three decisions that shape everything

### 4.1 The bad English is found, not made

**No step in this pipeline translates Chinese into English.** Both sides are already on disk
before collection starts: the Chinese is the author's original, the English is what some
upstream process actually emitted. Collection only excerpts.

That sounds like a detail and is in fact what the library's value rests on. The moment a skill
is allowed to supply a missing English side, the corpus starts containing text no real
pipeline ever produced, and **nothing downstream can tell the difference**. Worse, a generator
holding the Chinese source and knowing its output is meant to be the bad example writes a
caricature, and a caricature teaches nothing.

So a Chinese document with no English counterpart is not material. It gets skipped and
reported, never filled in.

This project already paid tuition on the same lesson. An earlier design translated faithfully
but stiffly first, then had a downstream pass polish the result. It failed, because **editing
and writing are two different cognitive operations**: once a grammatical sentence exists on the
page, the downstream pass only patches locally and never regenerates. The mirror image holds
too — a literal translator that has glimpsed a good version stops producing translationese and
starts producing lightly edited good English, and once the two sides converge the pair teaches
nothing.

For the same reason, the bad English is frozen once excerpted. Reading badly is its purpose.

### 4.2 Balance is a property of the finished library, not an act of collection

Cases come in five types, from single sentences through runs of paragraphs to diagram labels.
The finished library wants them roughly balanced, because the five fail in different ways and a
library that is 80% single sentences has taught only the easiest slice of the problem.

But real documents supply what they supply. Some articles contain no diagrams; some are one
long argument end to end. Asking the collection step to hit a ratio only produces a pile of
marginal cases, and a weak case is worse than no case.

So collection takes everything and records the type. Balance is reached later by
`chinglish-index`, **by removing the over-represented types** once the whole pile is visible.
Nothing is ever balanced by padding.

### 4.3 Append while collecting, organize while cleaning

Collection does not deduplicate, sort, merge, or skip a candidate because it resembles case 42.
Two reasons: collection cannot see the whole pile, so it is not equipped to judge "duplicate"
in the first place; and to tell which patterns are genuinely frequent, the cleanup step needs an
unfiltered pile.

The order cases arrive in does not matter either, because `chinglish-index` reorders by slug
rather than by number. After that step the layout is determined by the case content alone, not
by collection history, so the same material collected again lays out the same way.

The cost is that the library looks messy mid-collection. That is expected. The case files
belong in version control, since they are reference material for comparison testing rather than
scratch output, but the author's habit is to **commit only after `chinglish-index` has run**, so
an uncommitted folder during collection is the normal state.

---

## 5. One quality line that is easy to miss

**Any case whose Chinese trigger cannot be named is discarded.**

"Reads unnaturally" is worthless. A case that cannot explain its own cause teaches the model to
rewrite by vibe, which is precisely what this pipeline exists to eliminate. Wording preference,
sentence-length taste, and paragraph-splitting differences are not cases.

By the same rule, a fragment whose English side is still Chinese (an untranslated diagram
label, a skipped list item) is a hole in the material rather than a case. Skip it and count it.
Many such holes mean that English document was never finished, and the material should be fixed
before more is mined from it.

---

## 6. Current state

All five skills run. `chinglish-index` does its renumbering, indexing, and reading-copy passes
through one script; deduplication, pruning toward balance, and pattern induction are not built
yet and that skill carries the open questions for them.

`chinglish-review` carries a trap worth naming, and its SKILL.md names it. This project already
rejected LLM scoring of translations because **cold, formulaic English is the model's own
default voice**: asked to rate naturalness, a model rates the exact prose we are trying to
eliminate as excellent. The same trap applies to reviewing. So the reviewer is forbidden to
judge by ear, must check against the checklist and against the Chinese, and **must quote the
offending span and name the rule it breaks** for every finding. No quote, no finding. The other
direction is closed too: no manufacturing findings to look diligent, since each false positive
costs a real rewrite.

The question that was open, whether the rewriter should see the bad English, is settled:
**yes, but only after writing its own version.** Without it there is no way to confirm the pair
isolates a single construction; with it read first, rewriting degenerates into patching, and a
patch carries the Chinese sentence architecture straight through. So `chinglish-rewrite`'s
method is ordered into five steps, write before compare, and it says explicitly that those two
steps must not be collapsed.

One more thing worth recording. The good side eventually gets copied into `rewrite-en-*/SKILL.md`
as the ✅ half of example pairs, so it has to obey the author's own conventions, in particular
**no dash characters in body text**. The Claude Project prompt the author has been using leans
hard on em dashes. Reproduced across a few hundred ✅ examples, that habit would be taught to
every downstream skill.
