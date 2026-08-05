这是这一节的核心心法, 值得单独讲。lesson 12 的 RAG 是程序员**直接调用**的: `contexts = retrieve(query)`, 然后**程序员**把 contexts 拼进 prompt 喂给 LLM, **程序员**决定 retrieve 的时机。
