.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


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
