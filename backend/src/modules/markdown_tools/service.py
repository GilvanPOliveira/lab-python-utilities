import html
import re


def inline_markdown_to_html(text: str) -> str:
    escaped = html.escape(text)

    escaped = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.*?)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`(.*?)`", r"<code>\1</code>", escaped)

    return escaped


def markdown_to_html(content: str) -> dict:
    lines = content.splitlines()
    html_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3>{inline_markdown_to_html(stripped[4:])}</h3>")
            continue

        if stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2>{inline_markdown_to_html(stripped[3:])}</h2>")
            continue

        if stripped.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h1>{inline_markdown_to_html(stripped[2:])}</h1>")
            continue

        if stripped.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True

            html_lines.append(f"<li>{inline_markdown_to_html(stripped[2:])}</li>")
            continue

        if in_list:
            html_lines.append("</ul>")
            in_list = False

        html_lines.append(f"<p>{inline_markdown_to_html(stripped)}</p>")

    if in_list:
        html_lines.append("</ul>")

    return {
        "result": "\n".join(html_lines),
    }


def strip_markdown(content: str) -> dict:
    text = content

    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)

    return {
        "result": text.strip(),
    }


def generate_markdown_table(headers: list[str], rows: list[list[str]]) -> dict:
    clean_headers = [header.strip() or "Coluna" for header in headers]

    header_line = "| " + " | ".join(clean_headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(clean_headers)) + " |"

    table_rows = []

    for row in rows:
        normalized_row = row[: len(clean_headers)]

        while len(normalized_row) < len(clean_headers):
            normalized_row.append("")

        table_rows.append("| " + " | ".join(normalized_row) + " |")

    return {
        "result": "\n".join([header_line, separator_line, *table_rows]),
    }


def generate_markdown_list(items: list[str], ordered: bool) -> dict:
    clean_items = [item.strip() for item in items if item.strip()]

    if ordered:
        result = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(clean_items))
    else:
        result = "\n".join(f"- {item}" for item in clean_items)

    return {
        "result": result,
    }
