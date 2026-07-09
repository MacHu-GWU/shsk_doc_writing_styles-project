---
name: translate-to-en
description: Translate/rewrite files into English. Supports PDF, Markdown, plain text, and other formats. Generates an -en.md file in the same directory. Use when user wants to translate documents into English for easier reading.
argument-hint: "[file1 file2 ...] or leave empty to be prompted"
---

# Translate to English

Translate/rewrite files into English to produce a readable English version.

## Usage

```
/translate-to-en                     # No arguments, prompt user for files or directory
/translate-to-en file1.pdf file2.md  # Translate the specified files
```

## Execution Flow

### Step 1: Determine the files to translate

**If arguments are provided ($ARGUMENTS)**:
- The arguments are the list of files to translate
- Verify each file exists

**If no arguments are provided**:
- Use the AskUserQuestion tool to ask the user:
  - Question: "Please provide the file path(s) or a directory path to translate"
  - Options can include: "Enter file path", "Enter directory path", "Cancel"
- If a directory is given, scan it for all non-English files (excluding any that already end in `-en.md`)

### Step 2: Translate files one by one

For each file:

1. **Read the source file**
   - Use the Read tool to read the file
   - PDF files are automatically parsed into text

2. **Generate the translated Markdown file**
   - Output path: replace the source file's extension with `-en.md`
   - Example: `/path/to/document.pdf` → `/path/to/document-en.md`
   - Example: `/path/to/notes.txt` → `/path/to/notes-en.md`

3. **Translation rules** (very important):

   **The goal is "rewriting", not word-for-word translation**:
   - Rewrite using natural English logic, phrasing, and everyday scenarios familiar to English readers
   - Work paragraph by paragraph, preserving the original structure
   - The goal is to make the content easier for English readers to understand

   **Preserve original content**:
   - Keep all technical terms and domain-specific terminology in their original form (do not over-translate established terms)
   - Keep Chapter titles and Section titles in their original form (they are important anchors)
   - Keep names of people and places in their original form
   - Keep code, formulas, and variable names in their original form

   **About examples and scenarios — localize, don't transliterate**:
   - When the source contains culturally Chinese examples, **replace them** with equivalents that feel native to a North American (US) English reader. The goal is for the translated text to read as if it were originally written for a US audience, not as a translation of Chinese content.
   - **Personal names**: replace Chinese names (张三 / 李四 / 王五, etc.) with common English names (e.g., John Smith, Jane Doe, Michael Johnson, Emily Davis).
   - **Company names**: replace Chinese companies (阿里巴巴, 腾讯, 字节跳动, 美团, 华为, etc.) with comparable US/North American companies (e.g., Amazon, Google, Meta, Uber, Microsoft) — pick one that matches the *role* the company plays in the example (e-commerce giant, social platform, ride-hailing, etc.).
   - **Software / products / services**: replace China-specific apps and services (微信, 支付宝, 淘宝, 滴滴, 钉钉, 高德地图, 百度, etc.) with their Western counterparts (WhatsApp/iMessage, Apple Pay/Venmo, Amazon, Uber/Lyft, Slack, Google Maps, Google, etc.) — again, pick by functional role.
   - **Everyday-life scenarios**: rewrite scenarios rooted in Chinese daily life (春节抢红包, 双十一, 外卖小哥, 共享单车 in a Chinese city, 国庆假期, etc.) into culturally equivalent North American scenarios (Black Friday / Cyber Monday, holiday tipping, DoorDash delivery driver, Citi Bike in NYC, Thanksgiving weekend travel, etc.).
   - **Places & geography**: swap Chinese cities/regions (北京, 上海, 深圳, 杭州) for US cities that play a comparable role (New York, San Francisco, Seattle, Austin) when the geographic detail is illustrative rather than essential.
   - **Money, units, formats**: convert RMB amounts to roughly equivalent USD amounts (round to natural figures, don't compute exact FX), and use US-style date/number/address formats.
   - **Exception — preserve the original when**:
     - The example is a real, named case study about a specific Chinese company/person/event (e.g., "阿里巴巴 2014 IPO") — keep the real entity, just translate the description.
     - The example's *point* depends on Chinese specifics (e.g., explaining how 支付宝's QR-code payment flow works) — keep it, and add a brief parenthetical for context if helpful.
     - Technical identifiers, dataset values, code samples, or anything where changing the literal would break the meaning.

   **Non-text content handling**:
   - Images: use `[Image: description]` as a placeholder
   - Figures/diagrams: use `[Figure: description]` as a placeholder
   - Tables: rebuild as Markdown tables when possible; use a placeholder for complex tables

4. **Output format**:
   ```markdown
   # [Original title]

   [Translated English content...]

   ## [Original Section title]

   [Translated English content...]

   [Image: original image description]

   [Translated English content continues...]
   ```

### Step 3: Report completion

After translation, report:
- The list of successfully translated files and their output paths
- For any failures, explain the reason

## Example

User input: `/translate-to-en /path/to/lecture1.pdf /path/to/notes.md`

Execution:
1. Read lecture1.pdf
2. Generate /path/to/lecture1-en.md (English translation)
3. Read notes.md
4. Generate /path/to/notes-en.md (English translation)
5. Report completion

---

**Begin execution**: $ARGUMENTS
