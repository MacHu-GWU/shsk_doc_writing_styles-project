**First, speed.** Each query has to run a million cosine calculations, and every one of those is a 1536 dimensional multiply add. Even with numpy that takes several seconds, which kills the user experience. Production RAG queries need to come back in 50 to 200 milliseconds. Anything slower just doesn't work.

**Second, memory.** A single vector with 1536 float32 values takes up 6 KB. A million vectors add up to 6 GB, and 10 million reach 60 GB. That's more than a server can hold in memory, so you end up sharding to disk.

**Third, query capability.** Production systems rarely rely on semantic search alone. They usually layer on **structured filters** too: search only documents from 2025 onward, only documents where source equals knowledge_base, only documents the current user has permission to read. Expressing those filters with a hand-rolled list means piling on more for loops, and the code just gets messier and messier.
