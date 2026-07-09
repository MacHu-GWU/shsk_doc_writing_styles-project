# -*- coding: utf-8 -*-

"""
Chinese to English punctuation linter for mixed Chinese/English Markdown.

This module normalizes a document whose narrative is mostly Chinese but whose
technical terms are English. In that style every punctuation mark should be the
English (ASCII) form, and English words/numbers should be separated from the
surrounding Chinese text by a single space.

What it does, line by line:

- Converts Chinese punctuation to its English equivalent
  （，、。；：？！（）"" -> , , . ; : ? ! () ""）.
- Adds a single space after sentence punctuation (`, . : ; ? !`).
- Adds a single space between adjacent Chinese and English/number runs
  (e.g. "使用 Python 3.12" instead of "使用Python3.12").
- Collapses runs of the same Chinese punctuation (。。。 -> ...).
- Removes stray spaces inside paired Markdown markers (e.g. `** bold **` -> `**bold**`).

Use it as a command line linter that rewrites a `.md` file in place:

    python chinese_to_english_punctuation.py path/to/doc.md

Add ``--check`` to report whether the file would change without writing it
(useful in CI):

    python chinese_to_english_punctuation.py --check path/to/doc.md

The module is pure standard library so it has no third party dependencies.
"""

from __future__ import annotations

import re
import sys
import argparse
from dataclasses import dataclass
from pathlib import Path


LQ = "\u201c"  # left double quotation mark
RQ = "\u201d"  # right double quotation mark
chinese_punctuation = "，、。；：？！" + LQ + RQ + "''（）【】《》"


@dataclass
class PairMatch:
    """
    表示一对闭合标记的匹配信息

    :param marker: 标记符号，如 "**"、"()"、"[]" 等
    :param open_start: 开始标记的起始位置（索引）
    :param open_end: 开始标记的结束位置（索引，不包含）
    :param close_start: 结束标记的起始位置（索引）
    :param close_end: 结束标记的结束位置（索引，不包含）
    """
    marker: str
    open_start: int
    open_end: int
    close_start: int
    close_end: int


def find_pair_markers(line: str, marker: str) -> list[PairMatch]:
    """
    在字符串中查找成对的标记

    对于相同的开始和结束标记（如 **），会将找到的标记按顺序两两配对。
    例如：第1个和第2个配对，第3个和第4个配对，以此类推。

    :param line: 要搜索的字符串
    :param marker: 要匹配的标记，如 "**"

    :return: 匹配到的成对标记列表
    """
    matches = []
    positions = []

    # 找到所有标记的位置
    start = 0
    while True:
        pos = line.find(marker, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + len(marker)

    # 将位置两两配对（第1个和第2个，第3个和第4个，...）
    for i in range(0, len(positions) - 1, 2):
        open_pos = positions[i]
        close_pos = positions[i + 1]
        matches.append(
            PairMatch(
                marker=marker,
                open_start=open_pos,
                open_end=open_pos + len(marker),
                close_start=close_pos,
                close_end=close_pos + len(marker),
            )
        )

    return matches


def remove_spaces_around_paired_markers(line: str, matches: list[PairMatch]) -> str:
    """
    移除成对标记内侧的空格

    对于每一对标记：
    - 移除开始标记后面的空格（内侧）
    - 移除结束标记前面的空格（内侧）

    从后往前处理每一对标记，避免修改字符串后索引变化的问题。
    对于每一对，先处理结束标记前的空格，再处理开始标记后的空格。

    :param line: 要处理的字符串
    :param matches: 成对标记的匹配列表

    :return: 处理后的字符串
    """
    if not matches:
        return line

    # 按开始位置从后往前排序，确保修改不影响前面的索引
    sorted_matches = sorted(matches, key=lambda m: m.open_start, reverse=True)

    result = line
    for match in sorted_matches:
        # 先处理结束标记前面的空格
        space_count = 0
        pos = match.close_start
        while pos - space_count - 1 >= 0 and result[pos - space_count - 1] == " ":
            space_count += 1
        if space_count > 0:
            result = result[: pos - space_count] + result[pos:]

        # 再处理开始标记后面的空格
        # 注意：删除close前的空格不影响open_end的位置（因为在前面）
        space_count = 0
        pos = match.open_end
        while pos + space_count < len(result) and result[pos + space_count] == " ":
            space_count += 1
        if space_count > 0:
            result = result[:pos] + result[pos + space_count :]

    return result


def post_process_paired_markers(line: str) -> str:
    """
    后处理：移除成对标记内侧的多余空格

    目前支持的标记：
    - ** (Markdown粗体)

    这个函数会按顺序处理多个标记类型，每次处理完一个标记类型后，
    将修改后的字符串作为下一个标记类型的输入。

    :param line: 要处理的字符串

    :return: 处理后的字符串
    """
    # 可以扩展到其他标记，如 "()", "[]", "<>" 等
    markers_to_process = ["**"]

    for marker in markers_to_process:
        matches = find_pair_markers(line, marker)
        line = remove_spaces_around_paired_markers(line, matches)

    return line


def _process_last_special_char(line: str, tokens: list[str], char: str):
    try:
        if line.rstrip()[-1] == char:
            tokens.append("")
    except IndexError:
        pass


def handle_dou_hao(line: str) -> str:
    """
    中文逗号 ， → 英文逗号 ,
    并在逗号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("，") if token.strip()]
    _process_last_special_char(line, tokens, "，")
    return ", ".join(tokens).strip()


def handle_dun_hao(line: str) -> str:
    """
    中文顿号 、 → 英文逗号 ,
    并在逗号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("、") if token.strip()]
    _process_last_special_char(line, tokens, "、")
    return ", ".join(tokens).strip()


def handle_ju_hao(line: str) -> str:
    """
    中文句号 。 → 英文句号 .
    并在句号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("。") if token.strip()]
    _process_last_special_char(line, tokens, "。")
    return ". ".join(tokens).strip()


def handle_mao_hao(line: str) -> str:
    """
    中文冒号 ： → 英文冒号 :
    并在冒号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("：") if token.strip()]
    _process_last_special_char(line, tokens, "：")
    return ": ".join(tokens).strip()


def handle_fen_hao(line: str) -> str:
    """
    中文分号 ； → 英文分号 ;
    并在分号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("；") if token.strip()]
    _process_last_special_char(line, tokens, "；")
    return "; ".join(tokens).strip()


def handle_wen_hao(line: str) -> str:
    """
    中文问号 ？ → 英文问号 ?
    并在问号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("？") if token.strip()]
    _process_last_special_char(line, tokens, "？")
    return "? ".join(tokens).strip()


def handle_exclamation(line: str) -> str:
    """
    中文感叹号 ！ → 英文感叹号 !
    并在感叹号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("！") if token.strip()]
    _process_last_special_char(line, tokens, "！")
    return "! ".join(tokens).strip()


def handle_zuo_kuo_hao(line: str) -> str:
    """
    中文左括号 （ → 英文左括号 (
    并在左括号前添加一个空格
    """
    tokens = [token.strip() for token in line.split("（") if token.strip()]
    return " (".join(tokens).strip()


def handle_you_kuo_hao(line: str) -> str:
    """
    中文右括号 ） → 英文右括号 )
    并在右括号后添加一个空格. 但如果右括号之后是一个特殊标点符号, 则不添加空格.
    """
    tokens = [token.strip() for token in line.split("）") if token.strip()]
    new_tokens = list()
    for ith, token in enumerate(tokens):
        new_tokens.append(token)
        try:
            next_token = tokens[ith + 1]
            if next_token[0] in ",.:;?!":
                new_tokens.append(")")
            else:
                new_tokens.append(") ")
        except IndexError:
            break
    try:
        if line.rstrip()[-1] == "）":
            new_tokens.append(")")
    except IndexError:
        pass
    return "".join(new_tokens).strip()


def handle_zuo_shuang_yin_hao(line: str) -> str:
    """
    中文左双引号 (U+201C) → 英文左双引号 "
    并在左双引号前添加一个空格
    """
    tokens = [token.strip() for token in line.split(LQ) if token.strip()]
    return ' "'.join(tokens).strip()


def handle_you_shuang_yin_hao(line: str) -> str:
    """
    中文右双引号 (U+201D) → 英文右双引号 "
    并在右双引号后添加一个空格. 但如果右双号之后是一个特殊标点符号, 则不添加空格.
    """
    tokens = [token.strip() for token in line.split(RQ) if token.strip()]
    new_tokens = list()
    for ith, token in enumerate(tokens):
        new_tokens.append(token)
        try:
            next_token = tokens[ith + 1]
            if next_token[0] in ",.:;?!)":
                new_tokens.append('"')
            else:
                new_tokens.append('" ')
        except IndexError:
            break
    try:
        if line.rstrip()[-1] == RQ:
            new_tokens.append('"')
    except IndexError:
        pass
    return "".join(new_tokens).strip()


def handle_consecutive_punctuation(line: str) -> str:
    """
    处理连续的2-3个相同的中文标点符号

    连续的中文标点应该被视为一个整体，直接转换为对应数量的英文标点，不在中间添加空格。
    例如：
    - 。。。 → ...
    - ？？？ → ???
    - ！！！ → !!!

    :param line: 要处理的字符串
    :return: 处理后的字符串
    """
    # 定义中文标点到英文标点的映射
    punctuation_map = {
        '。': '.',
        '？': '?',
        '！': '!',
    }

    # 处理每种标点的连续情况（2-3个）
    for chinese_punct, english_punct in punctuation_map.items():
        # 匹配2-3个连续的相同标点
        pattern = f'{re.escape(chinese_punct)}{{2,3}}'

        def replace_func(match):
            # 将连续的中文标点替换为相同数量的英文标点
            count = len(match.group())
            return english_punct * count

        line = re.sub(pattern, replace_func, line)

    return line


def handle_space_between_chinese_and_english(line: str) -> str:
    """
    Add space between Chinese and English characters/numbers/punctuation.
    Goes through character by character and maintains two consecutive characters.
    If one is an ASCII character (a-z, A-Z, 0-9, or certain ASCII punctuation) and the other is non-ASCII, add space between them.

    Special rules:
    - Closing punctuation (,.!?;:)) should NOT have space before them
    - Opening punctuation (([{"') should NOT have space after them
    - Closing quotes (determined by context) can have space after them
    """
    if not line:
        return line

    result = []
    prev_char = None

    # Punctuation that should stay close to preceding text (no space before)
    closing_punctuation = ",.!?;:)]}"
    # Punctuation that should stay close to following text (no space after)
    # This includes opening brackets and left quotes
    opening_punctuation = "([{\""

    # Track whether we're inside quotes (simple toggle)
    inside_quotes = False

    for current_char in line:
        # Check if we need to add space between prev_char and current_char
        if prev_char is not None:
            # Check character types
            prev_is_english = prev_char.isalpha() and ord(prev_char) < 128
            current_is_english = current_char.isalpha() and ord(current_char) < 128
            prev_is_number = prev_char.isdigit()
            current_is_number = current_char.isdigit()
            prev_is_non_ascii = ord(prev_char) >= 128
            current_is_non_ascii = ord(current_char) >= 128
            # Check for ASCII punctuation (excluding space and common separators)
            prev_is_ascii_punct = ord(prev_char) < 128 and not prev_char.isalnum() and prev_char not in " \t\n"
            current_is_closing_punct = current_char in closing_punctuation

            # Special handling for quotes: check if previous quote is a closing quote
            # A quote is closing if it comes after alphanumeric characters or non-ASCII chars
            prev_is_closing_quote = (prev_char == '"' and
                                    len(result) >= 2 and
                                    (result[-2].isalnum() or ord(result[-2]) >= 128))

            # Check if current char is a quote and determine if it's opening or closing
            # Use quote state tracking: if we're not inside quotes, it's opening; otherwise closing
            if current_char == '"':
                current_is_opening_quote = not inside_quotes
                current_is_closing_quote_char = inside_quotes
            else:
                current_is_opening_quote = False
                current_is_closing_quote_char = False

            # Opening punctuation, but exclude closing quotes
            # Note: quotes in opening_punctuation are treated as opening ONLY when followed by content
            prev_is_opening_punct = prev_char in opening_punctuation and not prev_is_closing_quote

            # Add space in the following cases:
            should_add_space = False

            # 1. Between English letter and non-ASCII character, example: "Eng中文"
            if prev_is_english and current_is_non_ascii:
                should_add_space = True
            # 2. Between non-ASCII character and English letter, example: "中文Eng"
            # BUT NOT after opening punctuation/quotes
            elif prev_is_non_ascii and current_is_english and not prev_is_opening_punct:
                should_add_space = True
            # 3. Between number and non-ASCII character, example: "100中文"
            elif prev_is_number and current_is_non_ascii:
                should_add_space = True
            # 4. Between non-ASCII character and number, example: "中文100"
            # BUT NOT after opening punctuation/quotes
            elif prev_is_non_ascii and current_is_number and not prev_is_opening_punct:
                should_add_space = True
            # 5. Between ASCII punctuation and non-ASCII character
            # BUT NOT after opening punctuation like ( or opening quotes
            elif prev_is_ascii_punct and current_is_non_ascii and not prev_is_opening_punct:
                should_add_space = True
            # 6. Between non-ASCII character and ASCII letter
            # Example: '中文A' should add space
            # BUT NOT before opening quotes
            elif prev_is_non_ascii and prev_char not in " " and current_char.isalpha() and ord(current_char) < 128 and not current_is_opening_quote:
                should_add_space = True
            # 7. Between non-ASCII character and opening quote, example: '从"' -> '从 "'
            elif prev_is_non_ascii and current_is_opening_quote:
                should_add_space = True

            # Actually add the space if conditions met
            # Don't add before closing punctuation or closing quotes
            if should_add_space and not current_is_closing_punct and not current_is_closing_quote_char:
                result.append(" ")

        result.append(current_char)
        prev_char = current_char

        # Update quote state
        if current_char == '"':
            inside_quotes = not inside_quotes

    return "".join(result)


def handle_everything(line: str) -> str:
    """
    对单行文本应用全部规则，返回规范化后的行

    :param line: 原始行
    :return: 规范化后的行
    """
    # First, handle consecutive punctuation (2-3 of the same type)
    # This must be done before individual punctuation handling
    line = handle_consecutive_punctuation(line)
    # Then handle individual punctuation marks
    line = handle_dou_hao(line)
    line = handle_dun_hao(line)
    line = handle_ju_hao(line)
    line = handle_mao_hao(line)
    line = handle_fen_hao(line)
    line = handle_wen_hao(line)
    line = handle_exclamation(line)
    line = handle_zuo_kuo_hao(line)
    line = handle_you_kuo_hao(line)
    line = handle_zuo_shuang_yin_hao(line)
    line = handle_you_shuang_yin_hao(line)
    # Add spaces between Chinese and English after all punctuation conversions
    line = handle_space_between_chinese_and_english(line)
    # Post-process to remove spaces inside paired markers
    line = post_process_paired_markers(line)
    return line


def process(text: str) -> str:
    """
    对整段文本逐行应用规则

    :param text: 原始文本
    :return: 规范化后的文本
    """
    lines = text.splitlines()
    new_lines = [handle_everything(line) for line in lines]
    return "\n".join(new_lines)


def lint_file(input_path: Path, output_path: Path) -> bool:
    """
    读取一个 Markdown 文件，应用标点规则，写到 output_path

    :param input_path: 输入文件路径
    :param output_path: 输出文件路径（等于 input_path 时即原地覆盖）

    :return: 若规范化后的内容和输入不同则返回 True，否则返回 False
    """
    original = input_path.read_text(encoding="utf-8")
    # splitlines() 会丢弃行尾换行，这里保留文件末尾是否有换行的信息
    trailing_newline = original.endswith("\n")
    processed = process(original)
    if trailing_newline and not processed.endswith("\n"):
        processed += "\n"

    changed = processed != original
    output_path.write_text(processed, encoding="utf-8")
    return changed


def check_file(input_path: Path) -> bool:
    """
    只检查一个 Markdown 文件是否符合规范，不写入任何文件

    :param input_path: 输入文件路径

    :return: 若文件需要修改则返回 True，否则返回 False
    """
    original = input_path.read_text(encoding="utf-8")
    trailing_newline = original.endswith("\n")
    processed = process(original)
    if trailing_newline and not processed.endswith("\n"):
        processed += "\n"
    return processed != original


def _run_file(input_path: Path, output_path: Path | None, check: bool) -> int:
    """
    执行 file 子命令：处理单个文件

    :param input_path: 输入文件路径
    :param output_path: 可选的输出文件路径（None 表示原地覆盖）
    :param check: 是否只检查不写入

    :return: 进程退出码（0 成功；--check 且需要修改时 1；输入不是文件时 2）
    """
    if not input_path.is_file():
        print(f"error: not a file: {input_path}")
        return 2

    if check:
        if output_path is not None:
            print("note: --check is set, ignoring output path")
        changed = check_file(input_path)
        print(f"{'would reformat' if changed else 'ok'}: {input_path}")
        return 1 if changed else 0

    target = output_path if output_path is not None else input_path
    changed = lint_file(input_path, target)
    if target == input_path:
        print(f"{'reformatted' if changed else 'ok'}: {input_path}")
    else:
        print(f"wrote: {target} (from {input_path})")
    return 0


def _run_batch(inputs: list[str], check: bool) -> int:
    """
    执行 batch 子命令：循环处理多个文件，每个都原地覆盖（或只检查）

    批量模式没有单独的输出路径参数，因为多个输入无法对应一个输出；
    每个文件各自原地处理，本质上就是对 file 单文件逻辑的一个循环。

    :param inputs: 输入文件路径列表
    :param check: 是否只检查不写入

    :return: 进程退出码（有文件缺失返回 2；--check 且任一文件需要修改返回 1；否则 0）
    """
    any_missing = False
    any_changed = False
    for name in inputs:
        path = Path(name)
        if not path.is_file():
            print(f"skip (not a file): {path}")
            any_missing = True
            continue
        if check:
            changed = check_file(path)
            print(f"{'would reformat' if changed else 'ok'}: {path}")
        else:
            changed = lint_file(path, path)
            print(f"{'reformatted' if changed else 'ok'}: {path}")
        any_changed = any_changed or changed

    if any_missing:
        return 2
    if check and any_changed:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    """
    命令行入口：把中文标点规范化为英文标点

    采用子命令模式：

    - file 子命令处理单个文件。第 1 个位置参数是输入文件，默认原地覆盖；
      第 2 个可选位置参数是输出文件，写到别处而不动输入。
    - batch 子命令处理多个文件。位置参数是一串输入文件，每个都原地覆盖。

    两个子命令都支持 --check：只检查不写任何文件，需要修改时返回码为 1。
    file 模式下带 --check 会忽略输出路径。

    :param argv: 命令行参数（默认读取 sys.argv）
    :return: 进程退出码
    """
    parser = argparse.ArgumentParser(
        description="Normalize Chinese punctuation to English in Markdown files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    file_parser = subparsers.add_parser(
        "file",
        help="Process a single file (optionally to a different output path).",
    )
    file_parser.add_argument(
        "input",
        help="Input .md file. Overwritten in place unless an output path is given.",
    )
    file_parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Optional output path. Write here instead of overwriting the input. "
             "Ignored when --check is set.",
    )
    file_parser.add_argument(
        "--check",
        action="store_true",
        help="Only check, do not write any file (exit 1 if the input would change).",
    )

    batch_parser = subparsers.add_parser(
        "batch",
        help="Process many files, each overwritten in place.",
    )
    batch_parser.add_argument(
        "inputs",
        nargs="+",
        help="One or more .md files. Each is overwritten in place.",
    )
    batch_parser.add_argument(
        "--check",
        action="store_true",
        help="Only check, do not write any file (exit 1 if any input would change).",
    )

    args = parser.parse_args(argv)

    if args.command == "file":
        output = Path(args.output) if args.output is not None else None
        return _run_file(Path(args.input), output, args.check)
    if args.command == "batch":
        return _run_batch(args.inputs, args.check)
    parser.error(f"unknown command: {args.command}")  # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())
