---
name: rewrite-in-technical-tutorial-breakdown-en
description: Rewrite blog draft in technical-tutorial-breakdown style (English output)
argument-hint: <draft-file-path> [output-path]
---

# Rewrite in Technical Tutorial Breakdown (English)

## Execution Steps

1. Read draft file: `$0`
2. Invoke /rewrite-in-technical-tutorial-breakdown for style guide
3. Rewrite draft following the style guide
4. Output in English
5. Write result to: `$1` (if not specified, write to `workspace/output/technical-tutorial-breakdown-en/{original-filename}`)

## Style Reminders

- **Hierarchical structure**: Use ## and ### headers, separate major sections with ---
- **Definition-first**: Name and define each concept before explaining
- **Code + explanation**: Include context before AND after code blocks
- **Tradeoff awareness**: Mark pros/cons with ✅ and ❌
- **Comparison tables**: Use tables to compare approaches
- **Actionable conclusions**: End with "Key Takeaways" or "Conclusion"

## Output Requirements

- Maintain technical accuracy
- Use concise, professional English
- Preserve the author's core insights
- Keep standard technical terminology