# Changelog

All notable changes to the `chinese-english-punctuation` skill are documented here.

## [0.1.2] - 2026-07-29

- Ported bracket handling to a generic `BracketPair` table and extended it beyond
  `（）`/`“”` to `【】`, `［］`, `《》`, `〈〉`, `＜＞`, `｛｝`, including correct spacing
  for nested/adjacent pairs (e.g. `【《书名》】` -> `[<书名>]`).
- Preserve leading indentation (spaces/tabs) so Markdown/reST code blocks and list
  continuations are no longer mangled.
- Empty/whitespace-only lines, and lines that consist of a single punctuation mark,
  now normalize to an empty line instead of leaving stray whitespace.
- Ported from the latest `chinese_to_english_punctuation` implementation
  (`impl.py`), keeping this skill self-contained with no dependency on the PyPI
  package.

## [0.1.1] - 2026-07-04

- Initial release.
