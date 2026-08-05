# Changelog

All notable changes to the `check-markdown-structure` skill are documented here.

## [0.1.0] - 2026-08-08

- Initial release. Compares the structural skeleton of two Markdown documents and reports where
  the two element sequences stop lining up.
- Reads only. Detection is deliberately separate from repair so that a rewrite step and a check
  step can be composed in any order.
- Matching is by element type and position rather than by text, since the usual pair is two
  languages. Code bodies, table dimensions, and image paths are the exception and are compared
  for real.
- Replaces the `rewrite-in-en-*` orchestration layer and its three agents, which are gone. That
  design tried to own drafting, rewriting, cross-document terminology, and verification in one
  pipeline. Every quality failure traced back to something the orchestrating layer injected into
  the writing stage, and the per-document style skills in this plugin already do the writing
  better without it. Cross-document consistency is a property of how a batch is organized and
  now belongs to the caller.
