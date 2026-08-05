---
name: author-agent-skill
description: Write or revise a Claude Code Agent Skill — SKILL.md frontmatter, references/, and bundled scripts.
argument-hint: "[path-to-skill-dir]"
---
Target: $ARGUMENTS

If no target is given, ask which skill directory to create or revise.

Default location is `<project>/.claude/skills/<name>/`. Never write to `~/.claude/` unless the user asks for it explicitly.

Read references/extend-claude-with-skills.md for the SKILL.md spec, then author or revise the skill as requested — whether that means creating one from scratch or reworking an existing one.

If the skill bundles a CLI script (pure Python, no third-party dependencies), it must follow references/python-cli-script-standard.md.
