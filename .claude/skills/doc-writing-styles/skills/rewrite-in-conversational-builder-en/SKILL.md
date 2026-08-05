---
name: rewrite-in-conversational-builder-en
description: Rewrite blog draft in conversational-builder style (English output)
argument-hint: <draft-file-path> [output-path]
---

# Rewrite in Conversational Builder Style (English)

## Execution Steps

1. Read draft file: `$0`

2. Invoke `rewrite-in-conversational-builder` agent skill for style guide

3. Rewrite draft following the style guide, paying attention to:
   - Use first-person narrative anchored in real experience
   - Structure with clear headers but allow for exploration
   - Connect specific observations to larger patterns and analogies
   - Let honest emotions show — enthusiasm, frustration, concern
   - Treat readers as peers, not students
   - Use flowing prose with strategic bold emphasis
   - Don't force conclusions if uncertainty is honest

4. Output in English

5. Write result to: `$1` (if not specified, write to `./tmp/output/conversational-builder-en/{original-filename}`)
