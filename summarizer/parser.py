# new_pipc_news_bot/summarizer/parser.py

import re

def parse_summary_text(text, title=""):
    def extract_block(label, text):
        # '**Label:**' 형태로 시작, 다음 '**' 또는 끝까지
        pattern = rf"\*\*{label}:\*\*\s*\n*(.+?)(?=\n\*\*|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    one_line = extract_block("OneLineSummary", text)
    three_line_raw = extract_block("ThreeLineSummary", text)
    key_points_raw = extract_block("KeySummary", text)
    tags_raw = extract_block("tags", text)

    return {
        "title": title,
        "one_line": one_line,
        "three_line": [line.strip("-•* ").strip() for line in three_line_raw.splitlines() if line.strip()],
        "key_points": [line.strip("-•* ").strip() for line in key_points_raw.splitlines() if line.strip()],
        "tags": [tag.strip() for tag in tags_raw.split(",")] if tags_raw else []
    }


