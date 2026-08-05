---
name: rewrite-in-technical-tutorial-breakdown
description: Rewrite blog drafts in technical-tutorial-breakdown style based on extracted patterns from Sebastian Raschka's writing.
user-invocable: false
---

# Rewrite in Technical Tutorial Breakdown Style

## Style Guide

### Core Identity

The Technical Tutorial Breakdown style transforms complex technical concepts into structured, digestible educational content. It reads like a patient, expert teacher walking you through a topic—explaining not just the "what" but the "why" and "how" with systematic clarity.

This style excels at taking dense technical material (LLM architectures, training methods, optimization techniques) and breaking it down into scannable sections with clear hierarchies. The reader always knows where they are, what they're learning, and why it matters. The writing is direct, practical, and respects the reader's intelligence while ensuring they never feel lost.

Key differentiators:
- **Hierarchical structure obsession**: Heavy use of headers, sub-headers, and visual separators (---) to chunk information
- **Definition-first approach**: Concepts are named and defined before being explained
- **Code + explanation integration**: Code blocks are sandwiched between explanations of what they do and why
- **Tradeoff awareness**: Every technique has advantages AND disadvantages, both presented fairly

---

### Dimension 1: Narrative Perspective (叙事视角)

**Style: Hybrid Teacher-Observer**

The perspective shifts between explaining concepts objectively and occasionally inserting personal experience or opinion. Use "you" frequently to engage the reader directly. Use "we" occasionally for shared exploration.

**Rules:**
- Default to objective explanation ("KV cache stores intermediate computations")
- Use "you" when explaining reader benefits or actions ("You don't need to retrain the model")
- Insert "I" sparingly for personal validation ("In a recent chapter, I improved accuracy from 15% to 52%")
- Never lecture down; treat reader as competent peer learning a new topic

**Examples:**
- DO: "You now have two independent ways to improve LLMs"
- DO: "If you deploy LLMs, you now have a new tool in your toolkit"
- DON'T: "One must understand that the KV cache is essential"

---

### Dimension 2: Structural Pattern (结构组织方式)

**Style: Hierarchical Breakdown with Visual Chunking**

This is the defining characteristic. Every article follows a predictable, learnable structure.

**Rules:**
- Start with a clear overview/definition section (often titled "What Is X?" or "The Core Idea")
- Use H2 (##) for major topic shifts, H3 (###) for sub-concepts
- Insert horizontal rules (---) between major sections
- Group related items using numbered lists or bullet points
- Use tables for comparisons or specifications
- End with "Key Takeaways" or "Conclusion" that summarizes actionable points

**Standard article skeleton:**
```
## What Is [Concept]? / The Core Idea
## Why This Matters / When to Use This
## The Main Approaches / How It Works
### Approach 1: [Name]
### Approach 2: [Name]
## Advantages and Disadvantages
## Key Takeaways / Conclusion
```

**Examples:**
- DO: Use "---" to visually separate sections
- DO: Number approaches, steps, or methods ("The 4 Main Ways to...")
- DON'T: Write long paragraphs without subheadings
- DON'T: Bury key concepts mid-paragraph

---

### Dimension 3: Depth of Thinking (思维深度)

**Style: Mechanism Explainer with Practical Anchoring**

Go deep into technical mechanisms but always connect back to practical implications. Explain the "how" at a level that helps readers implement or evaluate, not just recognize.

**Rules:**
- Explain mechanisms with enough detail to implement or understand tradeoffs
- Include mathematical or algorithmic details when they clarify (but don't drown in them)
- Always connect technical depth to practical implications ("This matters because...")
- Include cross-references to related techniques when relevant

**Examples:**
- DO: "MLA down-projects keys and values to a lower-dimensional space, stores compressed tensors, then up-projects during inference. Similar to LoRA's approach—trade computation for memory savings."
- DO: Include complexity analysis when relevant ("O(L²) to O(L·k)")
- DON'T: Stay purely abstract without implementation guidance
- DON'T: Explain only at the surface level when depth illuminates

---

### Dimension 4: Emotional Tone (情绪气质)

**Style: Calm, Direct, Mildly Encouraging**

The tone is confident and matter-of-fact. Excitement is expressed through clarity and practical value, not exclamation points. Occasional mild enthusiasm is appropriate when something is genuinely notable.

**Rules:**
- Default to calm, professional tone
- Express significance through framing ("This is one of the most rewarding improvements...")
- Avoid hyperbole or excessive qualifiers
- Use emphatic statements sparingly and only when warranted

**Examples:**
- DO: "The trend is clear: inference scaling is becoming as important as model size itself."
- DO: "This is the current gold standard for building high-performance reasoning models."
- DON'T: "This is absolutely revolutionary!!!"
- DON'T: "You'll be amazed by how incredibly powerful this technique is!"

---

### Dimension 5: Reader Relationship (与读者的关系)

**Style: Expert Peer Explaining to Competent Learner**

Treat the reader as technically competent but learning this specific topic. Don't over-explain basics, but don't assume domain expertise. The reader can handle complexity if it's structured well.

**Rules:**
- Assume reader knows programming and basic ML concepts
- Define domain-specific terms when first introduced
- Use analogies sparingly but effectively ("Read the map before hiking the trail")
- Provide practical tips ("Don't spend hours debugging. Move on and return later.")

**Examples:**
- DO: "Buffers are PyTorch's way of storing tensors that should be saved with the model but aren't parameters."
- DO: "This is similar to LoRA's dimension reduction approach"
- DON'T: Explain what a function is
- DON'T: Assume reader knows architecture-specific details without introduction

---

### Dimension 6: Information Density (信息密度)

**Style: High Density, Low Friction**

Pack substantial information per section but make it scannable. Use formatting to reduce cognitive load—readers should be able to skim headers and bullet points to get the gist.

**Rules:**
- Dense paragraphs are okay if broken by lists, code, or subheadings
- Use bold for key terms and important phrases
- Use checkmarks (✅) and crosses (❌) for quick scanning of pros/cons
- Tables for structured comparisons
- Keep individual paragraphs focused on one idea

**Examples:**
- DO: "Key characteristics: ✅ No retraining required ✅ No weight modifications ⚠️ Adds latency"
- DO: Use comparison tables with clear headers
- DON'T: Write wall-of-text paragraphs with multiple ideas
- DON'T: Underutilize formatting when it would help

---

### Dimension 7: Evidence & Support (证据与引用)

**Style: Experience + Research + Code**

Authority comes from demonstrated expertise (personal results), referenced research (papers, model releases), and working code examples.

**Rules:**
- Reference specific results ("improved from 15% to 52%")
- Cite papers, model releases, or technical reports where relevant
- Include code blocks that actually work and can be adapted
- Acknowledge limitations and unknowns ("OpenAI hasn't disclosed...")

**Examples:**
- DO: "DeepSeek V3.2 achieves gold-level performance on math competitions"
- DO: Include runnable code with comments
- DON'T: Make claims without grounding
- DON'T: Pretend certainty about unknown details

---

### Dimension 8: Presentation Format (内容呈现形式)

**Style: Tutorial-Code Hybrid**

Mix explanatory prose with code blocks, tables, and visual markers. Code is essential but always explained.

**Rules:**
- Code blocks should be preceded by context and followed by explanation
- Use inline code (backticks) for technical terms, function names, parameters
- Tables for specifications, comparisons, or structured data
- Emoji sparingly (✅, ❌, ⚠️ for scanning; rarely for decoration)

**Examples:**
- DO: "Here's how text generation works with caching: [code block] Key difference: we only compute for the new token."
- DO: Use | tables | for | comparisons |
- DON'T: Drop code without explaining what it does
- DON'T: Over-use emoji for decoration

---

### Dimension 9: Rhythm & Flow (节奏与可读性)

**Style: Short Sentences, Frequent Breaks, Strong Forward Motion**

Sentences tend short-to-medium. Paragraphs are compact. Frequent whitespace and visual breaks. The reader should feel momentum.

**Rules:**
- Vary sentence length but bias toward concise
- One idea per paragraph (usually 2-4 sentences)
- Use horizontal rules (---) between major sections
- Bold key phrases to guide the eye
- Lists and bullets create visual rhythm

**Examples:**
- DO: "The tradeoff is clear. More inference compute means better quality. It also means longer response time."
- DO: Use --- to create visual breathing room
- DON'T: Write paragraph-length sentences with multiple clauses
- DON'T: Create walls of unbroken text

---

### Dimension 10: Intent Orientation (目的导向)

**Style: Teach to Enable**

The goal is practical enablement. Readers should finish knowing how to apply what they learned, evaluate tradeoffs, and make informed decisions.

**Rules:**
- Always include practical implications ("For practitioners...")
- Provide clear recommendations or decision frameworks
- End with actionable takeaways
- Address both "what" and "when to use"

**Examples:**
- DO: "If building your own reasoning model: [budget-based recommendations]"
- DO: "Rule: Use the right tool for the task. Don't use reasoning models for everything."
- DON'T: Leave readers with theory but no application
- DON'T: End abruptly without synthesis

---

## Do vs Don't

| DO | DON'T |
|----|-------|
| Start with clear definition: "A reasoning model is an LLM that excels at..." | Start with vague introduction: "In today's rapidly evolving AI landscape..." |
| Use hierarchical headers: "## What Is X?" → "### How X Works" → "#### Step 1" | Write long sections without subheadings |
| Include code with explanation before AND after | Drop code blocks without context |
| State tradeoffs explicitly: "✅ Advantages ... ❌ Disadvantages" | Present only positives or only negatives |
| Use tables for comparisons: approach / cost / performance / best-for | Describe comparisons in prose only |
| End with "Key Takeaways" as numbered actionable points | End abruptly or with vague conclusions |
| Bold important terms: "**KV cache** stores intermediate computations" | Leave key terms unmarked in flowing text |
| Use --- to visually separate major sections | Write continuous text without breaks |

---

## Reference Articles

For deeper understanding, optionally read one reference article from:
- [references/Sebastian-Raschka-s-Blog/2026-01-24-Categories-of-Inference-Time-Scaling-for-Improved-LLM-Reasoning.md](references/Sebastian-Raschka-s-Blog/2026-01-24-Categories-of-Inference-Time-Scaling-for-Improved-LLM-Reasoning.md)
- [references/Sebastian-Raschka-s-Blog/2025-12-03-From-DeepSeek-V3-toV3-2-Architecture-Sparse-Attention-and-RL-Updates.md](references/Sebastian-Raschka-s-Blog/2025-12-03-From-DeepSeek-V3-toV3-2-Architecture-Sparse-Attention-and-RL-Updates.md)
- [references/Sebastian-Raschka-s-Blog/2025-06-17-coding-the-kv-cache-in-llms.md](references/Sebastian-Raschka-s-Blog/2025-06-17-coding-the-kv-cache-in-llms.md)
- [references/Sebastian-Raschka-s-Blog/2025-11-12-Recommendations-for-Getting-the-Most-Out-of-a-Technical-Book.md](references/Sebastian-Raschka-s-Blog/2025-11-12-Recommendations-for-Getting-the-Most-Out-of-a-Technical-Book.md)
- [references/Sebastian-Raschka-s-Blog/2025-02-05-Understanding-Reasoning-LLMs.md](references/Sebastian-Raschka-s-Blog/2025-02-05-Understanding-Reasoning-LLMs.md)

When you need to see full examples of this style in action, randomly select ONE article to read.

---

## Rewrite Process

1. **Read the user's draft** - Understand the core topic, arguments, and materials
2. **Identify the article type** - Is this explaining a concept, comparing approaches, teaching a technique, or analyzing a system?
3. **Extract key components:**
   - Main concept/topic
   - Sub-components or approaches
   - Practical implications
   - Tradeoffs or limitations
4. **Apply structural template:**
   - Open with definition or core idea
   - Use hierarchical headers
   - Insert --- between major sections
   - Include comparison tables where relevant
   - End with actionable takeaways
5. **Apply stylistic elements:**
   - Short sentences with strong rhythm
   - Bold key terms
   - Use ✅/❌ for scanning
   - Code with before/after explanation
6. **Preserve the author's insights** - Don't lose original arguments; restructure them
7. **Output the rewritten post** in clean markdown format
