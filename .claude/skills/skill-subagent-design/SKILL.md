---
name: skill-subagent-design
description: The skill-as-caller / subagent-as-doer design pattern — how skills and subagents differ and how to combine them.
---
Read references/claude-code-skills-subagents-and-slash-commands.md.

It covers the real dividing line between the two primitives (visibility and steering vs. an isolated result), why legacy `.claude/commands/` files are obsolete, and the recommended caller/doer pattern: a skill provides the discoverable `/name` front door, while a subagent does the noisy legwork in an isolated context and returns a clean summary.

Apply it when choosing between a skill and a subagent, or when wiring the two together.
