---
name: markdown-style
description: Markdown writing conventions for project documents. Use when authoring or revising any .md file in this project (meeting notes, project docs, design notes, READMEs, tickets) to keep heading structure, punctuation, and tone consistent. Trigger phrases include "write a doc", "draft a markdown", "format this note", "tidy up this markdown", or any request that produces or edits a .md file.
---

Apply these rules whenever you write or revise a markdown document in this project. They exist so documents stay scannable, stay consistent across contributors, and convert cleanly into other formats (PDF, Lark Docs, Confluence) without surprises.

---

## 1. Heading Structure

H1 is the document title. Use exactly one H1 per file. It must not contain any dash character (em dash `—`, en dash `–`, hyphen `-`), straight or curly quotes (`'`, `"`, `‘`, `’`, `“`, `”`), or square brackets (`[`, `]`). Commas and colons are the only punctuation marks allowed inside an H1.

H2 sections must be numbered using the form `## 1. Section Title`, `## 2. Section Title`, and so on. Place a horizontal rule (`---`) on its own line between every pair of H2 sections, so the document reads as a clear, ordered sequence.

H3 headings are not numbered by default. The single exception is when an H3 sequence is strongly parallel (for example, ordered steps of a procedure, or sequential phases of a plan). In that case numbering is allowed for clarity.

Avoid H4 and any deeper heading level. When the urge to introduce one shows up, restructure instead. Promote the section into its own H2, or replace the would be subheadings with a bullet list, a small table, or a short paragraph.

---

## 2. Punctuation and Tone

Avoid all three dash characters inside body text: the em dash (`—`), the en dash (`–`), and the ASCII hyphen used as a sentence break (`-`). Replace them with a period and a fresh sentence, a pair of parentheses for a side comment, or a new paragraph when the thought genuinely shifts. The hyphen is still fine for compound words (`high-quality`, `read-only`) and as a bullet list marker, since those are word formation and markdown syntax rather than punctuation.

Write in a narrative, conversational voice. Lead the reader from one idea to the next the way a person would, instead of producing bullet heavy, formulaic prose that reads as machine output. Avoid hollow connectors and AI style filler such as "in summary", "it is important to note", "additionally", "furthermore", and "as an AI". Prefer plain verbs and direct sentences.

---

## 3. Allowed Constructs

The following constructs are encouraged whenever they earn their place in the document:

- Plain paragraphs of prose, which should carry most of the meaning.
- Bullet lists, but only for items that are genuinely parallel.
- Fenced code blocks, always tagged with their language, for example ```python, ```bash, ```sql, ```yaml, ```json.
- Markdown tables for grid shaped data with clear column semantics.
- Mermaid diagrams (```mermaid) for flows, sequences, state machines, or entity relationships.

When in doubt, prefer a paragraph over a list, and a list over a table. Reach for a mermaid diagram only when the relationships are too tangled to describe linearly.

---

## 4. Forbidden Constructs

The following constructs hurt readability or render poorly across viewers, and should not appear in project markdown:

- ASCII diagrams, ASCII tables, and ASCII decorations such as boxes drawn with `+`, `|`, `=`, or `*`, banner text, and underline rows made of repeated characters.
- Deeply nested bullet lists. Cap nesting at two levels. When the content wants to go deeper, a short table or a fresh H2 section almost always reads better.
- Decorative emoji bullets, ornamental dividers, and any other glyph that does not carry information. The single allowed divider is the H2 separator `---`.
- Inline HTML used purely for styling (custom colors, fonts, alignment). Stick to plain markdown so the document stays portable.
