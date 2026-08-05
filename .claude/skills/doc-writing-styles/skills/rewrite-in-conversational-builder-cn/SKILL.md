---
name: rewrite-in-conversational-builder-cn
description: 用 conversational-builder 风格重写博客草稿（中文输出）
argument-hint: <draft-file-path> [output-path]
---

# 用 Conversational Builder 风格重写（中文）

## 执行步骤

1. 读取草稿文件: `$0`

2. 调用 `rewrite-in-conversational-builder` agent skill 获取风格指南

3. 按照风格指南重写草稿，注意：
   - 使用第一人称叙述，锚定在实际经验中
   - 结构清晰但允许探索性展开
   - 连接具体观察到更大的模式和类比
   - 让真实情绪自然流露——热情、困惑、关切
   - 将读者视为同行而非学生
   - 使用流畅的散文体，战略性地加粗重点
   - 如果确实存在不确定性，不要强行得出结论

4. 输出为中文

5. 将结果写入: `$1` (如未指定，则写入 `./tmp/output/conversational-builder-cn/{original-filename}`)
