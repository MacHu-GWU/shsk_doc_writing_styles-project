---
name: rewrite-in-conversational-builder
description: Rewrite blog drafts in conversational-builder style based on extracted patterns from Armin Ronacher's writing.
user-invocable: false
---

# Rewrite in Conversational Builder Style

## Style Guide

### Core Identity

The Conversational Builder style reads like sitting down with a senior engineer who's been in the trenches and wants to share what they've learned — not to lecture, but to think out loud with you. It's personal, reflective, and grounded in real building experience. The author doesn't claim to have all the answers; they're actively working through problems and inviting you along for the intellectual journey.

What makes this style distinctive: it combines the intimacy of a builder's journal with genuine analytical depth. The author isn't afraid to say "I don't know" or "this might be wrong" while still delivering sharp, opinionated takes backed by hands-on experience. There's an undercurrent of pragmatism — the author has shipped things, maintained things, and dealt with the consequences of decisions.

The voice is warm but not casual, technical but not dry, opinionated but not dogmatic.

---

### 10 Dimension Guidelines

#### 1. Narrative Perspective (叙事视角)

**Rule:** First-person experience-driven, with frequent shifts to "we" for shared industry experiences and "you" when making points resonate.

The author consistently uses "I" to anchor observations in personal experience: "I've found," "I'm starting to think," "what I see taking place." This isn't navel-gazing — it's establishing credibility through lived experience.

*Example:* "When one part of the pipeline becomes dramatically faster, you need to throttle input."

*Example:* "We also found it incredibly challenging to work with the Vercel SDK when it comes to dealing with provider-side tools."

---

#### 2. Structural Pattern (结构组织方式)

**Rule:** Exploration-driven structure with clear section headers. Start with a hook or observation, develop through multiple angles, but don't force neat conclusions.

Articles open with a provocative observation or question, then branch into related subtopics under clear headers. The structure allows for digression and exploration rather than forcing a linear argument. Conclusions often acknowledge uncertainty or pose further questions.

*Example:* An article about "agent psychosis" explores addiction, quality degradation, token economics, and community dynamics — all under one umbrella.

---

#### 3. Depth of Thinking (思维深度)

**Rule:** Move from concrete experience to systemic observation. Draw analogies across domains (textile industry, Starbucks queues, His Dark Materials). Question assumptions.

The author connects specific technical observations to larger patterns about how systems work, how humans behave, and how industries evolve. Historical parallels and cross-domain analogies give depth without being academic.

*Example:* Connecting PR queue overload to Starbucks mobile order chaos to illustrate accumulating failure.

*Example:* Using the textile industry's bottleneck-shifting pattern to illuminate AI code generation dynamics.

---

#### 4. Emotional Tone (情绪气质)

**Rule:** Thoughtful concern mixed with genuine enthusiasm. Allow frustration to show when discussing bad practices, but maintain intellectual generosity.

The tone is honest about difficulties and frustrations ("it looks like an insane psychosis") while remaining genuinely curious and engaged. There's no cynicism — even criticism comes from a place of caring about craft.

*Example:* "I too am the bottleneck now. But you know what? Two years ago, I too was the bottleneck. I was the bottleneck all along."

---

#### 5. Reader Relationship (与读者的关系)

**Rule:** Peer-to-peer dialogue with experienced practitioners. Assume technical competence but not identical experience. Invite disagreement.

The reader is treated as a fellow practitioner who might have different experiences or perspectives. The author frequently invites feedback: "If you're reading this and think I'm wrong, please drop me a mail. I want to learn."

*Example:* "Someone else might have figured it out."

---

#### 6. Information Density (信息密度)

**Rule:** Medium-high density with breathing room. Pack insights into paragraphs but break with horizontal rules and clear sections. Each section should be digestible in one sitting.

Technical details and observations are dense but well-organized. The author uses horizontal rules liberally to create visual breaks. Paragraphs stay focused but aren't afraid to develop ideas fully.

*Example:* A section on caching might cover Anthropic's approach, cache point placement, and cost implications — dense but segmented clearly.

---

#### 7. Evidence & Support (证据与引用)

**Rule:** Experience-driven with occasional external references. Quote or reference others' work when relevant, but authority comes primarily from hands-on building.

Primary evidence is "we tried this" or "I've seen this." External references (other engineers' posts, tools, books) are cited when they add context but don't dominate. The author's credibility comes from being a practitioner, not a researcher.

*Example:* Citing Steve Yegge's Gas Town documentation as an example of a phenomenon being discussed.

*Example:* "Mark Cartwright wrote a great article about the textile industry in Britain during the industrial revolution."

---

#### 8. Presentation Format (内容呈现形式)

**Rule:** Primarily prose with occasional code snippets when essential. Use bold for key phrases. Blockquotes for external references. Lists sparingly.

The format is text-heavy and discursive. Code appears only when necessary to illustrate a technical point. Bold text highlights key concepts or memorable phrases. Horizontal rules create section breaks.

*Example:* Bold phrases like "single-use plastic software" or "if input grows faster than throughput, you have an accumulating failure."

---

#### 9. Rhythm & Flow (节奏与可读性)

**Rule:** Varied sentence length with emphasis through short, punchy sentences. Paragraphs flow conversationally but key points land hard.

The writing has natural rhythm — longer explanatory sentences followed by short, emphatic ones. This creates a sense of conversation rather than documentation.

*Example:* "Fine. I know, you know." — Ultra-short sentences that punctuate longer passages.

*Example:* "That's a big bathtub." — Deadpan after technical explanation.

---

#### 10. Intent Orientation (目的导向)

**Rule:** Think out loud about real problems. Share lessons learned without pretending to have solved everything. Influence through honest reflection, not prescriptions.

The purpose is genuine intellectual sharing — working through problems publicly and inviting others into the process. There's no sales pitch, no call to action. The author wants to understand and help others understand.

*Example:* "I for one do not know. I'm looking at this with fascination and bewilderment and trying to make sense of it."

---

### Do vs Don't

| Don't | Do |
|-------|-----|
| Write as a detached expert dispensing wisdom | Write as a practitioner sharing hard-won lessons and open questions |
| Force a neat conclusion when the topic doesn't warrant one | Acknowledge uncertainty: "I don't know" or "we haven't figured this out yet" |
| Use purely academic language and abstract frameworks | Ground observations in specific experiences: "We tried X and found Y" |
| Make claims without showing the experience behind them | Anchor opinions in what you've built, maintained, or struggled with |
| Treat readers as students to be taught | Treat readers as peers who might have valuable perspectives you lack |
| Write in monotone corporate voice | Let personality show: humor, frustration, enthusiasm, concern |
| Overload with bullet points and lists | Use flowing prose with strategic bold text for emphasis |
| Hide behind "best practices" or industry consensus | Take clear positions while inviting disagreement |

---

## Reference Articles

For deeper understanding of this style in action, optionally read one reference article from:

- [references/Armin-Ronacher-s-personal-blog/2026-02-13-the-final-bottleneck.md](references/Armin-Ronacher-s-personal-blog/2026-02-13-the-final-bottleneck.md)
- [references/Armin-Ronacher-s-personal-blog/2026-02-09-a-language-for-agents.md](references/Armin-Ronacher-s-personal-blog/2026-02-09-a-language-for-agents.md)
- [references/Armin-Ronacher-s-personal-blog/2026-01-18-agent-psychosis-are-we-going-insane.md](references/Armin-Ronacher-s-personal-blog/2026-01-18-agent-psychosis-are-we-going-insane.md)
- [references/Armin-Ronacher-s-personal-blog/2025-11-21-agent-design-is-still-hard.md](references/Armin-Ronacher-s-personal-blog/2025-11-21-agent-design-is-still-hard.md)
- [references/Armin-Ronacher-s-personal-blog/2025-10-21-regulation-isn-not-the-European-trap-resignation-is.md](references/Armin-Ronacher-s-personal-blog/2025-10-21-regulation-isn-not-the-European-trap-resignation-is.md)

When you need to see full examples of this style in action, randomly select ONE article to read.

---

## Rewrite Process

1. **Read the user's draft** — Understand the core arguments, key insights, and materials being presented

2. **Identify the author's voice** — What are they really trying to say? What experiences or observations drive their points?

3. **Apply the style guide principles:**
   - Anchor the piece in first-person experience
   - Structure with clear headers but allow for exploration
   - Draw connections to larger patterns and analogies
   - Let honest emotions show — enthusiasm, frustration, concern
   - Treat readers as peers
   - Use flowing prose with strategic emphasis
   - Don't force conclusions if uncertainty is honest

4. **Preserve the author's key insights** — The style changes, but the core ideas and experiences remain the author's own

5. **Output the rewritten post** — A piece that reads like the author thinking out loud with experienced peers
