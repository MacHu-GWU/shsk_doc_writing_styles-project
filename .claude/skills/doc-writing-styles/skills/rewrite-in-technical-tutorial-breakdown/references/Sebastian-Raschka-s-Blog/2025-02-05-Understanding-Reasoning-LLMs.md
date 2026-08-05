# Understanding Reasoning LLMs: Methods and Strategies for Building and Refining Reasoning Models

## What Is a Reasoning Model?

### Definition

A **reasoning model** is an LLM that excels at answering questions requiring **complex, multi-step generation with intermediate steps.**

### Examples

**Does NOT require reasoning:**
- "What is the capital of France?" → Direct factual answer

**DOES require reasoning:**
- "If a train moves at 60 mph for 3 hours, how far does it go?" → Requires recognizing relationships between distance, speed, and time

**Complex reasoning (what we focus on today):**
- Mathematical proofs
- Challenging coding problems
- Riddles and puzzles
- Advanced problem-solving

### Key Characteristics

Regular LLMs can provide reasoning, but **specialized reasoning models:**
- Excel at complex tasks (not just basic reasoning)
- Include explicit "thinking" or intermediate steps in responses
- Process information through multiple iterations (sometimes hidden from users)

**Note:** Some reasoning models (like OpenAI's o1) may show reasoning internally but not to the user.

---

## When Should We Use Reasoning Models?

### When to Use Reasoning Models ✅

- Complex math problems
- Advanced coding challenges
- Proof verification
- Puzzle solving
- Multi-step logic problems

### When NOT to Use Reasoning Models ❌

- Summarization
- Translation
- Knowledge-based Q&A
- Simple factual questions
- Real-time applications requiring speed

### The Cost-Benefit Tradeoff

**Reasoning models are:**
- More expensive to run (more compute)
- More verbose (longer responses)
- Sometimes more error-prone (overthinking simple problems)

**Rule:** Use the right tool for the task. Don't use reasoning models for everything.

---

## The 4 Main Ways to Build Reasoning Models

### 1. Inference-Time Scaling

**Concept:** Increase compute resources during inference (not training) to improve reasoning.

**Analogy:** Like humans thinking more deeply about a problem when given extra time.

#### Approaches

**Chain-of-Thought (CoT) Prompting:**
- Add phrases like "think step by step" to prompts
- Model generates intermediate reasoning steps
- Often improves accuracy on complex problems
- Example: "Let me work through this step by step..."

**Voting and Search Strategies:**
- Generate multiple candidate answers
- Use majority voting to select the best answer
- Employ beam search or Monte Carlo tree search
- Use process-reward models to evaluate intermediate steps

#### Advantages
- No training required
- Can be added to existing models
- Works with any LLM

#### Disadvantages
- Increases inference cost (more tokens = more compute)
- More expensive for production deployment

---

### 2. Pure Reinforcement Learning (RL)

**Key Discovery:** Reasoning can emerge as a behavior from pure RL without supervised fine-tuning!

#### How DeepSeek-R1-Zero Works

**Training process:**
1. Start with DeepSeek V3 base model
2. Apply RL without any supervised fine-tuning (SFT)
3. No human preference labeling needed

**Rewards used:**
- **Accuracy reward:** LeetCode compiler verifies code; deterministic system evaluates math
- **Format reward:** LLM judge ensures proper response format (e.g., reasoning inside tags)

**The breakthrough:** Model develops reasoning traces naturally despite not being explicitly trained to do so.

#### Why This Matters

- Proves reasoning isn't something you need to teach via supervision
- Reasoning emerges as a learned behavior
- Opens new directions for reasoning model development

#### Performance

DeepSeek-R1-Zero isn't the strongest reasoning model, but it **demonstrates basic reasoning capabilities** through pure RL alone.

#### Limitations

- Not as strong as RL + SFT combined
- Likely requires very large models to work well

---

### 3. Supervised Fine-Tuning + Reinforcement Learning (SFT + RL)

**This is the current gold standard** for building high-performance reasoning models.

#### How DeepSeek-R1 Works

**Step 1: Generate cold-start SFT data**
- Use DeepSeek-R1-Zero (which had no SFT) to generate training examples
- Called "cold start" because it wasn't trained on SFT data

**Step 2: Supervised fine-tuning**
- Train model on the generated reasoning traces
- Helps model learn better instruction following

**Step 3: First RL round**
- Use same rewards as R1-Zero (accuracy + format)
- Add language consistency reward (prevent code-switching)

**Step 4: Generate higher-quality SFT data**
- Use improved model to generate 600K Chain-of-Thought (CoT) examples
- Add 200K knowledge-based examples from V3 base model

**Step 5: Final SFT round**
- Train on both reasoning and knowledge examples

**Step 6: Final RL round**
- Rule-based accuracy rewards for math/coding
- Human preference labels for other types
- Combines symbolic verification + human feedback

#### Performance

DeepSeek-R1 shows substantial improvements over R1-Zero through this iterative process.

#### Why This Works

- SFT gives model good starting point
- RL refines reasoning through verifiable rewards
- Multiple rounds let model improve progressively

---

### 4. Pure Supervised Fine-Tuning (SFT) and Distillation

**Definition:** Train smaller models on reasoning traces generated by larger models.

**Note:** In LLM context, "distillation" ≠ classical knowledge distillation. It simply means:
- Take SFT data from a large reasoning model
- Fine-tune smaller models (8B-70B) on this data
- No RL applied

#### DeepSeek-R1-Distill Examples

**Smaller models trained:**
- Llama 8B and 70B
- Qwen 1.5B-32B

**Training data:** Same 800K SFT samples used for DeepSeek-R1

#### Why Do This?

1. **Efficiency:** Smaller models are cheaper and run on lower-end hardware
2. **Research:** Shows how far pure SFT can take reasoning without RL

#### Performance

- Weaker than DeepSeek-R1
- Surprisingly strong relative to R1-Zero
- Competitive with o1-mini

#### Key Finding: RL vs. SFT for Small Models

Comparison on 32B models:
- **Pure RL:** Weaker reasoning
- **Pure SFT (distillation):** Much stronger reasoning

**Conclusion:** For small models, **distillation (SFT) > pure RL**.

---

## Comparison of All 4 Approaches

| Approach | Training Cost | Speed | Strength | Best For |
|----------|---------------|-------|----------|----------|
| Inference-time scaling | None | Slower | Good | Adding to existing models |
| Pure RL | Medium | Fast | Moderate | Research insights |
| SFT + RL | High | Medium | Excellent | High-performance models |
| Distillation | Medium | Fast | Good | Efficient deployment |

---

## Thoughts on DeepSeek R1

### Compared to OpenAI's o1

**Performance:** Roughly equivalent (both exceptional)

**Key difference:** DeepSeek-R1 is more efficient at inference time
- Suggests DeepSeek optimized training (SFT + RL)
- Suggests OpenAI relies more on inference-time scaling
- Makes R1 cheaper to deploy

### Why We Can't Compare Directly

OpenAI hasn't disclosed o1 details:
- Is o1 using MoE architecture?
- How large is o1?
- How much RL vs. inference-time scaling?

Without this info, direct comparison is difficult.

### Training Cost

**Misconception:** "DeepSeek-R1 cost $6 million"
- This likely conflates V3 base model + R1
- $6M was estimated for DeepSeek-V3 only
- **Actual R1 cost never disclosed** (speculation only)

### The Achievement

DeepSeek-R1 is a major milestone because:
- Open-weight (MIT license, very permissive)
- Excellent performance
- Efficient inference
- Detailed technical report (researchers can learn from methodology)

---

## Building Reasoning Models on a Limited Budget

### The Challenge

Building DeepSeek-R1-level models requires:
- Hundreds of thousands to millions of dollars
- Massive compute infrastructure
- Can feel impossible for small teams

### The Good News: Budget-Friendly Approaches

#### Approach 1: Distillation (Sky-T1)

**What:** Fine-tune open-weight models on reasoning data

**Results:**
- 32B model trained with 17K SFT samples
- Cost: **$450** (less than AI conference registration!)
- Performance: Roughly on par with o1

**Key insight:** You don't need massive datasets—high-quality reasoning data matters more.

#### Approach 2: Pure RL (TinyZero)

**What:** Apply pure RL approach to small models

**Results:**
- 3B parameter model
- Shows emergent self-verification abilities
- Cost: **Less than $30** to train

**Key insight:** Reasoning can emerge in small models through RL alone.

#### Approach 3: Journey Learning

**Novel approach:** Include incorrect solution paths in training data, not just correct ones

**Idea:**
- Traditional SFT (shortcut learning): Only teach correct paths
- Journey learning: Also show wrong paths and corrections
- Model learns self-correction alongside solving

**Advantage:** May improve reasoning reliability through pure SFT

---

## Key Takeaways

### For Researchers

1. **Inference-time scaling** is easy, no-brainer win, but expensive at scale
2. **Pure RL** is fascinating for understanding reasoning emergence, but SFT + RL performs better
3. **SFT + RL** is the gold standard for strong reasoning models
4. **Distillation** works surprisingly well for smaller, efficient models

### For Practitioners

1. Consider whether you actually need a reasoning model (they're expensive)
2. If you do: Use SFT + RL if you have the budget; distillation if you want efficiency
3. Inference-time scaling is always worth adding

### For Budget-Constrained Teams

1. **Distillation can achieve impressive results** with limited compute ($450-$5K)
2. **Pure RL shows promise** at tiny scale (<$30)
3. **Journey learning** might unlock SFT-only approaches with better reliability

---

## The Future of Reasoning Models

**Emerging directions:**
- Combining inference-time scaling (approach 1) with SFT + RL (approach 3)
  - Likely what OpenAI o1 does
  - Provides both training efficiency and inference flexibility
- Exploring journey learning for better self-correction
- Scaling reasoning to smaller models efficiently

**What we expect:**
- More specialization (different models for different reasoning tasks)
- Better efficiency (reasoning without massive compute)
- Novel training approaches (journey learning, hybrid methods)

---

## Practical Implications

### If Building Your Own Reasoning Model

**Large budget ($1M+):**
- Train base model + apply SFT + RL pipeline
- Add inference-time scaling on top

**Medium budget ($100K-$500K):**
- Distill from existing reasoning models
- Use journey learning for better SFT

**Small budget ($<$10K):**
- Apply pure RL to 3B-7B models (TinyZero approach)
- Use high-quality but small SFT datasets

**No budget:**
- Use inference-time scaling on existing models
- Implement CoT prompting
- Use voting/search strategies

---

## Conclusion

Reasoning models represent an important specialization of LLMs, but they're not the right tool for every task. The four main approaches offer different tradeoffs:

1. **Inference-time scaling:** Cheap, effective, but expensive at scale
2. **Pure RL:** Insightful, but not production-grade alone
3. **SFT + RL:** Gold standard, but expensive
4. **Distillation:** Practical alternative, surprisingly effective

The emergence of budget-friendly approaches (Sky-T1 at $450, TinyZero at <$30) suggests reasoning model development is becoming more democratized—exciting news for researchers everywhere.