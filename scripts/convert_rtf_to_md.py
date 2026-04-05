#!/usr/bin/env python3
"""Convert RTF files to Markdown, handling mixed GBK hex escapes and Unicode escapes."""

import os
import re


def parse_rtf_to_text(rtf_content: str) -> str:
    """Parse RTF content and extract readable text with Markdown formatting."""

    text = rtf_content

    # Step 1: Remove nested group blocks (fonttbl, colortbl, etc.)
    for _ in range(10):
        prev = text
        text = re.sub(r'\{\\fonttbl[^{}]*(\{[^{}]*\}[^{}]*)*\}', '', text)
        text = re.sub(r'\{\\colortbl[^{}]*\}', '', text)
        text = re.sub(r'\{\\\*\\expandedcolortbl[^{}]*\}', '', text)
        if text == prev:
            break

    # Step 2: Decode Unicode
    text = re.sub(r'\\uc0\s*', '', text)
    text = re.sub(
        r'\\u(\d+)\s?',
        lambda m: chr(int(m.group(1))) if int(m.group(1)) < 0x110000 else '?',
        text
    )

    # Step 3: Decode GBK hex sequences
    def decode_gbk_sequences(s):
        result = []
        i = 0
        while i < len(s):
            if s[i:i+2] == "\\'" and i + 3 < len(s):
                hex_bytes = bytearray()
                while i < len(s) and s[i:i+2] == "\\'":
                    hex_str = s[i+2:i+4]
                    try:
                        hex_bytes.append(int(hex_str, 16))
                    except ValueError:
                        break
                    i += 4
                try:
                    result.append(hex_bytes.decode('gbk'))
                except (UnicodeDecodeError, ValueError):
                    try:
                        result.append(hex_bytes.decode('latin-1'))
                    except:
                        result.append('?')
            else:
                result.append(s[i])
                i += 1
        return ''.join(result)

    text = decode_gbk_sequences(text)

    # Step 4: Remove RTF header
    text = re.sub(r'\{\\rtf1[^{}\n]*', '', text, count=1)

    # Step 5: Remove all RTF commands
    text = re.sub(r'\\[a-zA-Z]+\d*\s*', '', text)
    text = re.sub(r'\\\*', '', text)

    # Remove braces
    text = text.replace('{', '').replace('}', '')

    # Remove stray backslashes
    text = re.sub(r'\\(?![#*_|`\[\]()!>~$])', '', text)

    # Step 6: Normalize whitespace within each line, then smart-merge lines
    # First collapse all horizontal whitespace
    text = re.sub(r'[ \t]+', ' ', text)

    lines = text.split('\n')
    merged = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            merged.append('')
            continue
        merged.append(stripped)

    # Now do smart line merging
    result = []
    i = 0
    while i < len(merged):
        line = merged[i]

        if line == '':
            result.append('')
            i += 1
            continue

        # Check if this line is part of a table row being built
        if _is_table_fragment(line):
            # Build one table row by collecting fragments
            table_line = line
            while i + 1 < len(merged) and merged[i + 1] != '':
                next_l = merged[i + 1].strip()
                # Stop if next line is a non-table block
                if _is_block_start(next_l) and not next_l.startswith('|'):
                    break
                # If next line starts with | AND current accumulated line
                # ends with |, then next line is a NEW table row - stop
                if next_l.startswith('|') and table_line.rstrip().endswith('|'):
                    break
                # If next line is a separator AND current line ends with |
                if _is_table_separator(next_l) and table_line.rstrip().endswith('|'):
                    break
                # Merge fragments
                if '|' in next_l or _is_table_separator(next_l) or (len(next_l) < 60 and not _is_block_start(next_l)):
                    i += 1
                    table_line += next_l
                else:
                    break
            result.append(table_line)
            i += 1
            continue

        # For non-table lines, check if next line should be merged
        while i + 1 < len(merged) and merged[i + 1] != '':
            next_line = merged[i + 1]

            # Don't merge if next line starts a new structural element
            if _is_block_start(next_line):
                break

            # Don't merge if current line is a block element
            if _is_block_end(line):
                break

            # Don't merge if next line is table content
            if _is_table_fragment(next_line):
                break

            # Don't merge if next line starts with a list marker
            # (but DO merge if it's a continuation like bold text after **)
            if re.match(r'^[-*+]\s', next_line) and not line.endswith('**'):
                break

            # Merge the lines
            line = _merge_two_lines(line, next_line)
            i += 1

        result.append(line)
        i += 1

    text = '\n'.join(result)

    # Step 7: Fix markdown formatting
    # Add space after # for headings: ##Text -> ## Text
    text = re.sub(r'^(#{1,6})([^ #\n])', r'\1 \2', text, flags=re.MULTILINE)

    # Fix bold markers split from content: "- ** \ntext**" -> "- **text**"
    # Pattern: ** followed by newline and then text ending with **
    text = re.sub(r'\*\*\s*\n\s*', '**', text)
    # But we may have broken "**text****text**", fix double **
    # Actually the above is too aggressive. Let's be more targeted:
    # Fix "**\nword" -> "**word" only when ** is at end of line
    # Re-do: just fix lines ending with "**" followed by lines not starting with special chars
    lines2 = text.split('\n')
    fixed = []
    j = 0
    while j < len(lines2):
        l = lines2[j]
        # If line ends with ** and next line has content that should be inside the bold
        if l.rstrip().endswith('**') and j + 1 < len(lines2):
            next_l = lines2[j + 1].strip()
            # If next line looks like it's the bold content (ends with **)
            if next_l and not next_l.startswith('#') and not next_l.startswith('|') and not next_l.startswith('---'):
                fixed.append(l.rstrip() + next_l)
                j += 2
                continue
        fixed.append(l)
        j += 1
    text = '\n'.join(fixed)

    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


def _is_cjk(c):
    """Check if a character is CJK or CJK punctuation."""
    cp = ord(c)
    return (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or
            0x2E80 <= cp <= 0x2EFF or 0x3000 <= cp <= 0x303F or
            0xFF00 <= cp <= 0xFFEF or 0xFE30 <= cp <= 0xFE4F or
            0x3200 <= cp <= 0x32FF or 0xF900 <= cp <= 0xFAFF or
            cp in (0x3001, 0x3002, 0xFF0C, 0xFF1A, 0xFF1B,
                   0xFF08, 0xFF09, 0x300A, 0x300B, 0x3010, 0x3011,
                   0x201C, 0x201D, 0x2018, 0x2019))


def _is_table_fragment(line):
    """Check if a line looks like part of a markdown table."""
    s = line.strip()
    if s.startswith('|'):
        return True
    if re.match(r'^:?-{2,}', s):
        return True
    return False


def _is_complete_table_row(line):
    """Check if a line is a complete table row or separator."""
    s = line.strip()
    # A complete data row: starts with |, ends with |, has multiple cells
    if s.startswith('|') and s.endswith('|') and s.count('|') >= 3:
        return True
    # A complete separator row: |:--|:--|  or |---|---|
    if s.startswith('|') and re.match(r'^\|[\s:]*-{2,}.*\|$', s):
        return True
    # Separator without leading |: :--|:--|:--
    if re.match(r'^[\s:]*-{2,}.*-{2,}\s*$', s) and '|' in s:
        return True
    return False


def _is_table_separator(line):
    """Check if a line is a table separator row like |:--|:--|."""
    s = line.strip()
    return bool(re.match(r'^\|?[\s:]*-{2,}', s))


def _is_table_continuation(line):
    """Check if a line can be part of an ongoing table row."""
    s = line.strip()
    # Contains | (cell separator) or is just text that could be cell content
    # or is a separator fragment
    if '|' in s:
        return True
    if re.match(r'^:?-{2,}', s):
        return True
    # Short text fragments between pipes in a table
    if len(s) < 80 and not _is_block_start(s):
        return True
    return False


def _is_block_start(line):
    """Check if a line starts a new markdown block element."""
    s = line.strip()
    if re.match(r'^#{1,6}[\s]', s) or re.match(r'^#{1,6}[^\s#]', s):
        return True
    if re.match(r'^[-*+]\s', s):
        return True
    if re.match(r'^\d+[\.\)]\s', s):
        return True
    if s.startswith('---') or s.startswith('***') or s.startswith('```'):
        return True
    if s.startswith('>'):
        return True
    return False


def _is_block_end(line):
    """Check if a line is a block element that shouldn't have text appended."""
    s = line.strip()
    if re.match(r'^#{1,6}\s', s):
        return True
    if s.startswith('---') or s.startswith('***'):
        return True
    if re.match(r'^\|.*\|$', s):
        return True
    if re.match(r'^\|?:?-', s):
        return True
    return False


def _merge_two_lines(prev, next_line):
    """Merge two lines with appropriate separator."""
    if not prev:
        return next_line
    last_char = prev[-1]
    first_char = next_line[0] if next_line else ''

    if _is_cjk(last_char) or _is_cjk(first_char):
        return prev + next_line
    elif prev.endswith(' ') or next_line.startswith(' '):
        return prev + next_line
    else:
        return prev + ' ' + next_line


def convert_all():
    """Find all RTF files and convert them to MD."""
    rtf_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.lower().endswith('.rtf'):
                rtf_files.append(os.path.join(root, f))

    rtf_files.sort()
    print(f"Found {len(rtf_files)} RTF files to convert.\n")

    for rtf_path in rtf_files:
        md_path = os.path.splitext(rtf_path)[0] + '.md'
        try:
            with open(rtf_path, 'r', encoding='utf-8', errors='replace') as f:
                rtf_content = f.read()

            md_content = parse_rtf_to_text(rtf_content)
            md_content = md_content.encode('utf-8', errors='replace').decode('utf-8')

            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)

            print(f"✓ {rtf_path} -> {md_path}")
        except Exception as e:
            print(f"✗ {rtf_path}: {e}")

    print(f"\nDone! Converted {len(rtf_files)} files.")


if __name__ == '__main__':
    convert_all()
