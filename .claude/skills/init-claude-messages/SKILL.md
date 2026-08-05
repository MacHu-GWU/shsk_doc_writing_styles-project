---
name: init-claude-messages
description: Generate a blank, fillable claude-code-messages.md template (numbered prompt slots) at the current project's .claude/claude-code-messages.md. Use when the user asks to init/create/generate a claude-code-messages log, or invokes /init-claude-messages directly.
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(git rev-parse *)
---

# Init claude-code-messages.md

Generates a fresh `claude-code-messages.md` template — numbered, empty prompt slots to fill in later — at the current project's `.claude/claude-code-messages.md`. Backed by the bundled script [scripts/gen_claude_code_message_md.py](scripts/gen_claude_code_message_md.py).

## Steps

1. Find the project root:
   ```bash
   git rev-parse --show-toplevel
   ```
2. Run the script against `<project-root>/.claude/claude-code-messages.md`:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/gen_claude_code_message_md.py" --path "$(git rev-parse --show-toplevel)/.claude/claude-code-messages.md"
   ```
3. If the file already exists, the script exits 1 with:
   `ERROR: <path> already exists, pass --overwrite to replace it`
   Do not pass `--overwrite` on your own. Tell the user the file already exists and suggest renaming/archiving it first (e.g. `claude-code-messages-2026-08-01.md`), then re-run. Only add `--overwrite` if the user explicitly asks to replace it.
4. On success the script prints `Wrote N template entries to <path>` — report that exact path back to the user as the result.

## Optional flags

Pass these through only if the user asks for something non-default:
- `--n <int>` — number of numbered slots (default 99)
- `--zfill <int>` — zero-padding width for slot numbers (default 4)
- `--overwrite` — replace an existing file
