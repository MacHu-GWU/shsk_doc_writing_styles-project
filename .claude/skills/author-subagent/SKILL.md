---
name: author-subagent
description: Write or revise a Claude Code subagent — the .claude/agents/*.md file, its frontmatter, and its system prompt.
argument-hint: "[path-to-agent-file]"
---
Target: $ARGUMENTS

If no target is given, ask which subagent file to create or revise.

Default location is `<project>/.claude/agents/<name>.md`. Never write to `~/.claude/` unless the user asks for it explicitly.

Read references/create-custom-subagents.md for the subagent spec, then author or revise the subagent as requested — whether that means creating one from scratch or reworking an existing one.
