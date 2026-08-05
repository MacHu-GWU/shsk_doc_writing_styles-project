# DeepSeek V3 to V3.2: Architecture Evolution, Sparse Attention, and RL Advances

## The DeepSeek Timeline

DeepSeek V3 (December 2024) didn't become popular immediately. It was **DeepSeek R1**, a reasoning-specialized variant of V3, that made DeepSeek a mainstream alternative to OpenAI, Google, and Anthropic.

Since then, there's been about 10-11 months of relative quiet (which is normal—major LLM releases take enormous effort). The journey from V3 to V3.2 includes several intermediate steps:

- **DeepSeek V3.1** (hybrid reasoning model)
- **DeepSeek R1-0528** (minor version upgrade)
- **DeepSeek V3.2-Exp** (September 2025, experimental sparse attention)
- **DeepSeekMath V2** (November 27, 2025, proof of concept)
- **DeepSeek V3.2** (December 1, 2025, flagship release)

---

## Model Types: Dedicated vs. Hybrid Reasoning

An important distinction emerged this year: **dedicated reasoning models vs. hybrid models**.

### Dedicated Reasoning Models
- Separate model optimized for reasoning (e.g., DeepSeek R1)
- Better performance in reasoning tasks
- Requires separate inference paths

### Hybrid Reasoning Models
- Single model with toggleable reasoning mode (e.g., Qwen3, DeepSeek V3.1, V3.2)
- Users switch modes via chat template
- More convenient but potentially less optimal for each mode

**The industry pattern:** Some teams (Qwen) moved from hybrid → dedicated. DeepSeek moved from dedicated (R1) → hybrid (V3.1, V3.2). This suggests R1 may have been a research testbed, with V3.2 being the production hybrid model.

---

## From V3 to V3.1: The Baseline

### DeepSeek V3 Core Architecture

**Two key innovations:**

1. **Mixture-of-Experts (MoE)**: Selectively activates different expert networks for efficiency
2. **Multi-Head Latent Attention (MLA)**: Compresses key-value tensors before storing in cache

#### How MLA Works

Standard attention requires storing all key-value pairs. MLA instead:

1. **Down-project** keys and values to a lower-dimensional "latent" space
2. **Store** the compressed tensors in KV cache (saves memory)
3. **Up-project** back to original size during inference (adds one matrix multiplication)

This is similar to LoRA's dimension reduction approach—you trade a little computation for significant memory savings.

### DeepSeek R1: Reasoning via RL

R1 uses the **exact same architecture** as V3. The difference is training:

**RLVR (Reinforcement Learning with Verifiable Rewards)** trains the model to solve verifiable tasks (math, code) by:
- Having the model generate step-by-step reasoning
- Checking if the answer is correct programmatically
- Rewarding correct solutions

**GRPO (Group Relative Policy Optimization)** is the algorithm—a simpler variant of PPO that:
- Eliminates the critic model (value function)
- Uses actual verifiable rewards instead of a learned reward model
- Reduces complexity while maintaining effectiveness

---

## The Big Innovation: DeepSeek Sparse Attention (DSA)

Starting with **V3.2-Exp** (September 2025), DeepSeek introduced a game-changing efficiency mechanism.

### The Problem with Standard Attention

Standard attention is **O(L²)** complexity, where L is sequence length. This scales badly for long contexts.

**Sliding window attention** (used by Gemma 3, Olmo 3) fixes this by limiting queries to attend only to recent tokens in a fixed window. But this is **too rigid**—sometimes you need to reference tokens far back.

### DeepSeek Sparse Attention (DSA): Smart Selection

Instead of a fixed window, DSA:

1. **Learns which past tokens matter** for each new query
2. **Computes relevance scores** using a "lightning indexer"
3. **Selects top-k tokens** (k=2048 in practice)
4. **Creates sparse attention mask** that only attends to selected tokens

#### How the Lightning Indexer Works

For each query token at position t, compute similarity to all previous tokens:

```
Score(t,s) = Σ w_j * ReLU(q_t,j · k_s)
```

Where:
- `q_t,j` = query vector for token t in indexer head j
- `k_s` = key vector for past token s
- `w_j` = learned per-head weighting
- ReLU zeros out negative similarities

The token selector then keeps only the top-k highest-scoring tokens.

**Result:** Complexity reduces from **O(L²) to O(L·k)**, where k ≪ L.

---

## DeepSeekMath V2: Self-Verification Innovation

Before V3.2's release, DeepSeek released **DeepSeekMath V2** on Thanksgiving (November 27), which proved out new RL techniques.

### The Problem with Standard RLVR

1. **Correct answers don't guarantee correct reasoning** — a model might get lucky
2. **Theorem proving** requires step-by-step derivation, not just final answer checking

### The Solution: Three-Model Architecture

#### LLM 1: Proof Generator
- Generates mathematical proofs
- Main model being improved

#### LLM 2: Proof Verifier
- Trained to evaluate proofs using a rubric:
  - **1.0**: Complete, rigorous, all steps justified
  - **0.5**: Sound logic but minor errors
  - **0.0**: Fundamentally flawed

#### LLM 3: Meta-Verifier
- Checks whether the verifier (LLM 2) is evaluating correctly
- Prevents the verifier from hallucinating false issues
- Analogous to GAN discriminator

**Training dynamics:** Generator improves via verifier feedback → generator produces better proofs → verifier gets better training signal. (Similar to GANs.)

### Self-Refinement During Inference

**Naive self-refinement problem:** When a single LLM generates AND evaluates its own proof, it tends to claim correctness even when wrong.

**DeepSeekMath V2's approach:** Train with separate verifier (LLM 1 and 2), but use only the trained generator (LLM 1) at inference with self-refinement, since the generator has learned the verifier's rubrics during training.

**Key insight:** The separate verifier is essential for training but not needed at inference once the model is strong enough. This saves compute while maintaining quality.

**Iterative refinement:** The team ran up to 8 self-refinement iterations with continuing accuracy improvements—not yet saturating.

---

## DeepSeek V3.2: The Full Package

Combines all previous innovations:

### Architecture (Same as V3.2-Exp)
- **Mixture-of-Experts** for efficiency
- **Multi-Head Latent Attention** for memory savings
- **DeepSeek Sparse Attention** for long-context efficiency

### RL Training Updates

**Hybrid reward strategy:**

For **verifiable domains** (math, code):
- Rule-based outcome rewards
- Length penalty (shorter answers preferred)
- Language consistency reward

For **general tasks** (no symbolic verifier):
- Generative reward model (LLM-as-judge)
- Task-specific rubrics

**Math tasks specifically:** Incorporates DeepSeekMath V2's self-verification approach.

### GRPO Improvements

DeepSeek V3.2 keeps the original GRPO structure but adds stability tweaks:

**Domain-specific KL strengths:** Instead of removing KL penalty entirely (like DAPO), tune its weight per domain. For math, zero KL often works best (but remains tunable).

**Unbiased KL estimate:** Reweight KL term with importance ratio so gradients match the actual policy distribution.

**Off-policy sequence masking:** Drop sequences that drift too far from original policy while having negative advantage.

**MoE routing preservation:** During training, force the same expert routing patterns used during rollout generation.

**Sampling mask preservation:** When using top-p/top-k sampling during rollout, preserve those masks during loss computation.

**Keep original GRPO normalization:** Unlike Dr. GRPO, keep length and group standard-deviation normalization instead of removing them.

---

## DeepSeek V3.2-Speciale: Extended Thinking

An extreme variant for reasoning-only tasks:

- **Trained only on reasoning data** (like R1)
- **Reduced length penalty** to allow longer outputs
- **Trades tokens for accuracy** (inference-scaling tradeoff)

Achieves higher accuracy but at the cost of significantly more tokens per response.

---

## Performance Highlights

**DeepSeek V3.2** achieves:
- Gold-level performance on math competitions
- Strong code performance
- Tool-use and agentic capabilities
- Competitive with GPT-5.1 and Gemini 3.0 Pro on many benchmarks

**Efficiency gains from DSA:**
- Significant inference cost savings, especially for long-context scenarios
- Lower training overhead

---

## Key Architectural Progression

### V3 → V3.1
- Base model + dedicated reasoning model
- Hybrid reasoning model introduced

### V3.1 → V3.2-Exp
- Added DeepSeek Sparse Attention (DSA)
- Maintains same overall architecture
- Improves efficiency

### V3.2-Exp → V3.2
- Incorporated DeepSeekMath V2's self-verification
- Hybrid reward strategy (RLVR + reward models)
- GRPO stability improvements
- Maintained architecture, improved training

---

## Bonus: mHC (Manifold-Constrained Hyper-Connections)

December 31, 2025, DeepSeek released research on improving the residual path itself:

**Hyper-Connections (HC):** Generalize identity residuals into learned connections with parallel paths for information mixing.

**Manifold-Constrained HC (mHC):** Constrains the residual mixing to a norm-preserving manifold.

**Benefits:** Better training stability and convergence with minimal overhead.

This suggests focus is shifting from attention/normalization/FFN optimization to the fundamental residual connection architecture.

---

## Key Takeaways

1. **Architecture stabilized:** V3's foundation (MoE + MLA) persists through V3.2
2. **Sparse attention is critical:** DSA enables efficiency at long context lengths
3. **RL keeps improving:** GRPO tweaks and hybrid verifier approaches unlock better reasoning
4. **Training beats parameters:** Self-verification and self-refinement deliver gains without bigger models
5. **Hybrid models winning:** DeepSeek moved from dedicated R1 to hybrid V3.2, suggesting this is the production direction

The evolution from V3 to V3.2 shows **iteration on training methodology** more than architectural revolution—but these training improvements are substantial enough to create a competitive flagship model.