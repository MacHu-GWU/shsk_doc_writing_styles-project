---
name: rewrite-in-analytical-deep-dive-essay-cn
description: 用 analytical-deep-dive-essay 风格重写博客草稿（中文输出）
argument-hint: <draft-file-path> [output-path]
---

# 用 Analytical Deep Dive Essay 风格重写（中文）

## 执行步骤

1. 读取草稿文件: `$0`
2. 调用 /rewrite-in-analytical-deep-dive-essay 获取风格指南
3. 按照风格指南重写草稿
4. 输出为中文
5. 将结果写入: `$1` (如未指定，则写入 `workspace/output/analytical-deep-dive-essay-cn/{original-filename}`)

## 风格要点提示

重写时请确保：

- **论点明确** — 文章开头即表明核心观点
- **结构严谨** — 使用层级标题组织论证：问题 → 常见观点 → 为何失效 → 深入分析 → 结论
- **证据充分** — 引用具体数据、案例、实例支撑每一个论点
- **反驳有力** — 主动识别并回应可能的质疑
- **语气冷静** — 保持分析性语调，偶尔带有干练的幽默
- **信息密度高** — 每段都应推进论证，避免空泛描述

## 中文表达注意事项

- 使用书面语，避免口语化表达
- 保持逻辑连接词的使用（然而、因此、换言之、关键在于）
- 可适当使用短句强调重点
- 数据和引用需保留精确性
