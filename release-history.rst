.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


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
