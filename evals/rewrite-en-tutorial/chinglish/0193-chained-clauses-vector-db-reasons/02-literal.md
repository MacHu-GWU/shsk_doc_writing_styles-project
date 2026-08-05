**First, speed**. Every query has to compute cosine 1M times, each one a 1536-dimensional float multiply-add. Even with numpy it takes several seconds, and user experience falls apart. Production RAG queries want 50 to 200 ms response time, and anything slower is unacceptable.

**Second, memory**. One vector is 1536 float32s, which is 6 KB. 1M vectors is 6 GB. 10M vectors is 60 GB. That doesn't fit in server memory, you have to shard to disk.

**Third, query capability**. Production rarely does semantic retrieval alone, you usually stack **structured filters** on top: "only in documents from 2025 onward", "only in documents where source=knowledge_base", "only in documents this user has permission to read". Expressing those filters in a hand-rolled list means more layers of for loops, and the code gets uglier and uglier.
