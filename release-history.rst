.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.2.1 (2026-08-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add a ``rewrite-in-*`` style skill collection to the ``doc-writing-styles`` plugin. Each style is a skill that rewrites a blog draft into one recognizable voice, with the voice defined by reference articles bundled alongside the skill rather than by a long list of rules. Four styles ship in this release:

  - ``rewrite-in-analytical-deep-dive-essay``: thesis-driven argumentative essay that builds a case, takes counterarguments seriously, and closes with implications. Reference articles from Dan Luu's blog.
  - ``rewrite-in-career-growth-narrative``: mentor-to-peer career advice delivered through stories and frameworks rather than formal argument. Reference articles from Swizec's blog.
  - ``rewrite-in-conversational-builder``: a senior engineer thinking out loud about what they built, opinionated but willing to say "I don't know". Reference articles from Armin Ronacher's blog.
  - ``rewrite-in-technical-tutorial-breakdown``: dense technical material broken into a scannable hierarchy, concepts defined before they are explained, code sandwiched between explanations. Reference articles from Sebastian Raschka's blog.

- Each style also ships a ``-cn`` and a ``-en`` variant that pins the output language and the default output path, so the same style guide can produce a Chinese or an English draft. These variants are still thin, and multi-language output is not solid yet. Treat them as a first cut rather than a finished feature.

**Minor Improvements**

- Add the ``check-markdown-structure`` skill to the plugin. It lines up the block skeletons (headings, code blocks, tables, quotes, images, lists, rules) of two Markdown files and reports where they stop matching. Intended as a check after a translation or rewrite. It reads only and never edits.
- Update the plugin description to say what the plugin now does: a Chinese to English rewriting pipeline that aims at natively-written English and verifies nothing was lost.

**Miscellaneous**

- Add ``evals/rewrite-en-tutorial/chinglish``, a case library of 220 Chinglish fragments. Each case holds the Chinese source, the literal English a machine produced from it, and the English a native writer would have written. The library exists to supply voice samples for the style skills and material for manual smoke tests, not to score the pipeline. Its ``README.md`` records why the original rubric-and-LLM-judge plan was dropped.
- Add the ``chinglish-*`` maintenance skills for that library: ``chinglish-spec`` (shared vocabulary and data contract), ``chinglish-collect`` (mine documents for case pairs), ``chinglish-rewrite`` (author the good English side in bulk), ``chinglish-review`` (flag good versions that are not good enough), and ``chinglish-index`` (regroup, renumber, and regenerate ``INDEX.md``). Add the matching ``mise`` task ``update-rewrite-en-tutorial-chinglish-index-and-review``.
- Add ``docs/cn-to-en-rewrite-design.md`` to the plugin, recording the design work behind the Chinese to English pipeline, including the measured finding that a thin prompt beat a twelve-thousand-word specification.
- Rework the repository's own authoring skills: rename ``write-agent-skill`` to ``author-agent-skill`` and give it a Python CLI script standard, add ``author-subagent``, ``create-sub-agent``, ``skill-subagent-design``, and ``init-claude-messages``. These are development tooling for this repository and are not part of the published plugin.
- Bump the ``doc-writing-styles`` plugin version to ``0.2.1`` in ``plugin.json``.


0.1.5 (2026-08-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- ``translate-to-en``: rework the per-file flow into a mandatory two-pass process. Pass A produces a first draft translation; Pass B re-reads that draft against the original source and rewrites the wording to read as native English, specifically targeting Chinglish symptoms (clause order mirrored from the source language, literal calques, repetitive connector words, article errors) while leaving heading structure, Markdown formatting, and preserved terms unchanged.

**Miscellaneous**

- Bump the ``doc-writing-styles`` plugin version to ``0.1.5`` in ``plugin.json``.


0.1.4 (2026-08-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- ``chinese-english-punctuation``: drop the bundled ``scripts/chinese_to_english_punctuation.py`` linter now that the ``chinese_to_english_punctuation`` PyPI package covers the same behavior. Lint by running its ``c2ep`` CLI via ``uvx --from "chinese_to_english_punctuation>=0.1.2" c2ep file --path ...`` instead.
- Bump the ``chinese-english-punctuation`` skill version to ``0.1.3`` in its own ``VERSION``/``CHANGELOG.md``.
- Bump the ``doc-writing-styles`` plugin version to ``0.1.4`` in ``plugin.json``.


0.1.3 (2026-07-29)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- ``chinese-english-punctuation``: extend bracket handling beyond ``（）``/``“”`` to also cover ``【】``, ``［］``, ``《》``, ``〈〉``, ``＜＞``, and ``｛｝``, including correct spacing for nested or adjacent pairs (e.g. ``【《书名》】`` -> ``[<书名>]``).
- ``chinese-english-punctuation``: preserve leading indentation (spaces/tabs) so Markdown and reStructuredText code blocks and list continuations are no longer mangled by the linter.

**Bugfixes**

- ``chinese-english-punctuation``: normalize empty or whitespace-only lines, and lines consisting of a single punctuation mark, to an empty line instead of leaving stray trailing whitespace.

**Miscellaneous**

- Update ``README.rst`` to link directly to the ``doc-writing-styles`` plugin directory and comment out the CI/codecov/PyPI badges that no longer apply.
- Bump the ``doc-writing-styles`` plugin version to ``0.1.3`` in ``plugin.json``.


0.1.2 (2026-07-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- Rename the plugin folder from ``.claude/skills/doc_writing_styles`` to ``.claude/skills/doc-writing-styles`` to match the ``doc-writing-styles`` plugin name.


0.1.1 (2026-07-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release. Add the ``doc-writing-styles`` Claude Code plugin (``.claude/skills/doc_writing_styles``) with three skills:

  - ``markdown-style``: Markdown heading structure, punctuation, and tone conventions for project documents.
  - ``chinese-english-punctuation``: keeps punctuation in English (ASCII) form for documents that mix Chinese narrative with English technical terms, plus a standalone linter script to check/rewrite ``.md`` files in place.
  - ``translate-to-en``: translates/rewrites PDF, Markdown, and plain text files into English.

- Add the ``maintain-claude-plugins`` skill, the personal spec and tooling (``scripts/plugin_release.py``) for building, versioning, and releasing this project's Claude Code plugins.

**Miscellaneous**

- Update ``README.rst`` and ``pyproject.toml`` description to describe the project as the ``doc-writing-styles`` Claude Code plugin.
- Fill in ``plugin.json`` metadata (description, keywords) for the ``doc-writing-styles`` plugin.
