---
name: rewrite-in-technical-tutorial-breakdown-cn
description: 用 technical-tutorial-breakdown 风格重写博客草稿（中文输出）
argument-hint: <draft-file-path> [output-path]
---

# 用 Technical Tutorial Breakdown 风格重写（中文）

## 执行步骤

1. 读取草稿文件: `$0`
2. 调用 /rewrite-in-technical-tutorial-breakdown 获取风格指南
3. 按照风格指南重写草稿
4. 输出为中文
5. 将结果写入: `$1` (如未指定，则写入 `workspace/output/technical-tutorial-breakdown-cn/{original-filename}`)

## 风格要点提醒

- **层级结构**：使用 ## 和 ### 标题，用 --- 分隔主要章节
- **定义先行**：每个概念先命名和定义，再展开解释
- **代码+解释**：代码块前后都要有说明
- **权衡意识**：用 ✅ 和 ❌ 标记优缺点
- **表格对比**：用表格呈现方法对比
- **可操作结论**：以「关键要点」或「总结」收尾

## 输出要求

- 保持技术准确性
- 使用简洁专业的中文表达
- 保留原作者的核心洞见
- 适当本地化术语（但保留通用英文术语如 LLM、KV cache 等）
