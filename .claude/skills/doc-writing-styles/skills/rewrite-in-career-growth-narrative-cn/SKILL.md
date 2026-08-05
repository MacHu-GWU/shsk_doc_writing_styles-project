---
name: rewrite-in-career-growth-narrative-cn
description: 用 career-growth-narrative 风格重写博客草稿（中文输出）
argument-hint: <draft-file-path> [output-path]
---

# 用 Career Growth Narrative 风格重写（中文）

## 执行步骤

1. 读取草稿文件: `$0`
2. 调用 /rewrite-in-career-growth-narrative 获取风格指南
3. 按照风格指南重写草稿
4. 输出为中文
5. 将结果写入: `$1` (如未指定，则写入 `workspace/output/career-growth-narrative-cn/{original-filename}`)
