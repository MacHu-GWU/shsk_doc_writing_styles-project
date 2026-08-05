# Understanding and Coding the KV Cache in LLMs from Scratch

## What Is a KV Cache?

**In short:** KV cache stores intermediate key (K) and value (V) computations for reuse during inference, resulting in substantial speed-ups during text generation.

### The Core Problem

When an LLM generates text one token at a time, there's massive redundancy:

**Without KV cache:**
1. Generate token 1 from prompt: compute attention for all previous tokens
2. Generate token 2: compute attention for ALL previous tokens again (including token 1)
3. Generate token 3: compute attention for ALL previous tokens again (including tokens 1 and 2)

Example: Generating "Time flies fast"

| Step | Input Sequence | New Computation | Redundant? |
|------|-----------------|-----------------|-----------|
| 1 | "Time" | k₁, v₁ | — |
| 2 | "Time flies" | k₁, v₁, k₂, v₂ | k₁, v₁ recomputed |
| 3 | "Time flies fast" | k₁, v₁, k₂, v₂, k₃, v₃ | k₁, v₁, k₂, v₂ recomputed |

**The inefficiency:** We recompute the same key-value pairs over and over.

---

## How the Attention Mechanism Works

During attention computation, each token gets transformed:

```
Token embedding → [Matrix W_k] → Key vector (k)
Token embedding → [Matrix W_v] → Value vector (v)
Token embedding → [Matrix W_q] → Query vector (q)
```

**The redundancy:** At step 3, we recompute k₁ and v₁ even though they're identical to what we computed at step 1.

---

## Text Generation: With vs. Without KV Cache

### Without KV Cache

**Step 1:** Input "Time"
- Compute: k₁, v₁, q₁
- Output: logits for next token

**Step 2:** Input "Time flies"
- Compute: k₁, v₁, k₂, v₂, q₁, q₂ ← **k₁, v₁ recomputed!**
- Output: logits for next token

**Step 3:** Input "Time flies fast"
- Compute: k₁, v₁, k₂, v₂, k₃, v₃, q₁, q₂, q₃ ← **k₁, v₁, k₂, v₂ recomputed!**
- Output: logits for next token

### With KV Cache

**Step 1:** Input "Time"
- Compute: k₁, v₁, q₁
- **Cache:** Store k₁, v₁
- Output: logits for next token

**Step 2:** Input "flies" (only the new token!)
- Compute: k₂, v₂, q₂
- **Cache:** Retrieve k₁, v₁ from cache + add k₂, v₂
- Attend to: [k₁, k₂] and [v₁, v₂]
- Output: logits for next token

**Step 3:** Input "fast" (only the new token!)
- Compute: k₃, v₃, q₃
- **Cache:** Retrieve k₁, v₁, k₂, v₂ from cache + add k₃, v₃
- Attend to: [k₁, k₂, k₃] and [v₁, v₂, v₃]
- Output: logits for next token

**Key difference:** We only compute for the new token, not the entire sequence.

---

## Implementing KV Cache from Scratch

### 1. Register Cache Buffers

In the `MultiHeadAttention` constructor, add two buffers to hold cached keys and values:

```python
self.register_buffer("cache_k", None)
self.register_buffer("cache_v", None)
```

Buffers are PyTorch's way of storing tensors that should be saved with the model but aren't parameters.

### 2. Forward Pass with use_cache Flag

Extend the `forward` method to accept a `use_cache` argument:

```python
def forward(self, x, use_cache=False):
    b, num_tokens, d_in = x.shape
    
    # Always compute new keys and values
    keys_new = self.W_key(x)
    values_new = self.W_value(x)
    queries = self.W_query(x)
    
    if use_cache:
        # First call: initialize cache
        if self.cache_k is None:
            self.cache_k = keys_new
            self.cache_v = values_new
        else:
            # Subsequent calls: append new keys/values
            self.cache_k = torch.cat([self.cache_k, keys_new], dim=1)
            self.cache_v = torch.cat([self.cache_v, values_new], dim=1)
        
        # Retrieve full cache (old + new)
        keys = self.cache_k
        values = self.cache_v
    else:
        # No caching: use only current tokens
        keys = keys_new
        values = values_new
    
    # Attention computation using keys and values
    # ...
```

**The core mechanism:**
- **Store:** Append new keys/values to cache via `torch.cat`
- **Retrieve:** Use cached keys/values for attention computation

### 3. Clear the Cache

Between separate generation calls, reset the buffers:

```python
def reset_cache(self):
    self.cache_k = None
    self.cache_v = None
```

**Why?** Without clearing, new prompts will attend to stale keys from previous sequences, producing incoherent output.

### 4. Propagate use_cache Through the Model

In the main `GPTModel`, track token position and pass `use_cache` through all transformer blocks:

```python
def forward(self, in_idx, use_cache=False):
    if use_cache:
        # Track position for new tokens
        pos_ids = torch.arange(
            self.current_pos, 
            self.current_pos + seq_len,
            device=in_idx.device, dtype=torch.long
        )
        self.current_pos += seq_len
    else:
        pos_ids = torch.arange(0, seq_len, device=in_idx.device, dtype=torch.long)
    
    pos_embeds = self.pos_emb(pos_ids).unsqueeze(0)
    x = tok_embeds + pos_embeds
    
    # Pass use_cache through each transformer block
    for blk in self.trf_blocks:
        x = blk(x, use_cache=use_cache)
    
    return x
```

**Why position tracking?** New queries must align with keys/values already in cache. Without a counter, each step would start at position 0, treating new tokens as overlapping earlier ones.

### 5. Use the Cache in Generation

Here's how text generation works with caching:

```python
def generate_text_simple_cached(model, idx, max_new_tokens, use_cache=True):
    model.eval()
    ctx_len = model.pos_emb.num_embeddings  # max sequence length
    
    if use_cache:
        model.reset_kv_cache()
        
        # Initialize cache with full prompt
        with torch.no_grad():
            logits = model(idx[:, -ctx_len:], use_cache=True)
        
        # Generate new tokens one at a time
        for _ in range(max_new_tokens):
            # Pick highest probability token
            next_idx = logits[:, -1].argmax(dim=-1, keepdim=True)
            # Add to sequence
            idx = torch.cat([idx, next_idx], dim=1)
            # Feed ONLY the new token to model
            with torch.no_grad():
                logits = model(next_idx, use_cache=True)
    else:
        # Without cache: feed full sequence each time
        for _ in range(max_new_tokens):
            with torch.no_grad():
                logits = model(idx[:, -ctx_len:], use_cache=False)
            next_idx = logits[:, -1].argmax(dim=-1, keepdim=True)
            idx = torch.cat([idx, next_idx], dim=1)
    
    return idx
```

**Key difference:** With cache, we feed `model(next_idx, ...)` (just the new token). Without cache, we feed `model(idx[:, -ctx_len:], ...)` (the full context).

---

## Performance Comparison

On a Mac Mini M4 (CPU), generating 200 new tokens from a 124M parameter model:

| Method | Time |
|--------|------|
| Without KV Cache | 15.25 seconds |
| With KV Cache | 2.89 seconds |
| **Speedup** | **~5.3x** |

**Note:** This is a simple implementation optimized for readability, not performance. Production implementations use GPU optimizations (CUDA, etc.) and would see even larger speedups.

---

## Advantages and Disadvantages

### ✅ Advantages

**Computational efficiency increases:** 
- Without cache: O(n²) complexity—each step compares new query with all n previous keys
- With cache: O(n) complexity—each key/value computed once, then reused
- For long sequences, this is massive savings

### ❌ Disadvantages

**Memory usage grows:**
- Each new token appends to KV cache
- For very long sequences and large models, GPU memory can be exhausted
- Tradeoff: faster generation vs. more memory usage

---

## Optimizing KV Cache for Production

The simple implementation above has pitfalls when scaling:

### Problem 1: Memory Fragmentation

Repeatedly concatenating tensors via `torch.cat` causes:
- Frequent memory allocation/reallocation
- Significant performance overhead
- Unpredictable memory usage patterns

### Solution 1: Pre-allocate Memory

Pre-allocate a large tensor upfront and write into it:

```python
max_seq_len = 1024  # Expected maximum length
cache_k = torch.zeros(
    (batch_size, num_heads, max_seq_len, head_dim), 
    device=device
)
cache_v = torch.zeros(
    (batch_size, num_heads, max_seq_len, head_dim), 
    device=device
)

# During generation, write to specific positions
pos = current_token_position
cache_k[:, :, pos, :] = keys_new
cache_v[:, :, pos, :] = values_new
```

**Benefits:**
- Single memory allocation upfront
- O(1) insertion instead of O(n) concatenation
- Predictable memory usage

### Problem 2: Memory Blowup for Long Sequences

KV cache grows linearly with sequence length. For very long contexts, GPU memory explodes.

### Solution 2: Sliding Window Cache

Only keep the last N tokens in cache:

```python
window_size = 512  # Keep only last 512 tokens

# Truncate cache to window
cache_k = cache_k[:, :, -window_size:, :]
cache_v = cache_v[:, :, -window_size:, :]
```

**Tradeoff:**
- Uses much less memory
- Model can only attend to last `window_size` tokens
- Many tasks don't need full attention span

---

## Key Takeaways

1. **KV cache solves redundancy:** Each key/value computed once, reused across generation steps

2. **Simple core idea:** Cache stores previously computed K/V tensors → retrieve on next step

3. **Significant speedup:** ~5x on CPU for modest-sized models; even larger on GPU

4. **Production requires optimization:**
   - Pre-allocate memory (avoid repeated concatenation)
   - Use sliding window (avoid memory blowup)
   - Handle position tracking carefully

5. **Implementation is subtle:** Easy to make indexing mistakes—test by comparing cached vs. uncached outputs

---

## Important Implementation Details

### Position Tracking is Critical

Without proper position tracking:
- New query for token 3 might overlap with key/value for token 2
- Model attends to wrong positions
- Generates incoherent text

### Cache Must Be Reset Between Sequences

Old cache + new prompt = stale context → incoherent output. Always call `reset_cache()` before generating from a new prompt.

### Only Cache During Inference

During training, all tokens are available, so caching adds unnecessary complexity. Only use for inference (text generation).

---

## Conclusion

KV cache is one of the most impactful optimizations for LLM inference:

- **Conceptually simple:** Store intermediate computations, reuse them
- **Practically important:** 5-10x speedup on modest hardware; even more on production GPUs
- **Production-ready:** Requires thoughtful optimizations to handle memory and correctness

The tradeoff between code complexity and inference speed typically favors using KV cache in production environments.