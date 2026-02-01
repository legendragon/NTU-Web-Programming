from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSIGNMENTS_DIR = ROOT_DIR / "assignments"


def read_first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.replace("# ", "", 1).strip()
    return ""


def read_first_paragraph(text: str) -> str:
    lines = text.splitlines()
    seen_title = False
    for line in lines:
        if line.startswith("# "):
            seen_title = True
            continue
        if not seen_title:
            continue
        if line.strip():
            return line.strip()
    return ""


def get_assignments() -> list[dict[str, str]]:
    if not ASSIGNMENTS_DIR.exists():
        return []
    assignments = []
    for entry in sorted(ASSIGNMENTS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        readme_path = entry / "README.md"
        index_path = entry / "index.html"
        if not index_path.exists():
            continue
        readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
        title = read_first_heading(readme) or entry.name
        description = read_first_paragraph(readme)
        assignments.append(
            {
                "folder": entry.name,
                "title": title,
                "description": description,
            }
        )
    return assignments


def build_index_html(assignments: list[dict[str, str]]) -> str:
    cards = []
    for item in assignments:
        desc = (
            f"<div class=\"card-desc\">{item['description']}</div>"
            if item["description"]
            else ""
        )
        cards.append(
            "\n".join(
                [
                    "        <li class=\"card\">",
                    "          <div>",
                    f"            <div class=\"card-title\">{item['title']}</div>",
                    f"            {desc}" if desc else "",
                    "          </div>",
                    f"          <a class=\"card-link\" href=\"assignments/{item['folder']}/index.html\">open</a>",
                    "        </li>",
                ]
            ).rstrip()
        )
    cards_html = "\n".join(cards)

    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>NTU Web Programming - Assignments</title>
    <style>
      :root {{
        color-scheme: light;
      }}
      body {{
        margin: 0;
        font-family: \"Trebuchet MS\", \"Segoe UI\", sans-serif;
        background: #f6f1e1;
        color: #1b1b1b;
      }}
      .page {{
        max-width: 820px;
        margin: 60px auto 80px;
        padding: 0 20px;
      }}
      h1 {{
        margin: 0 0 10px;
        font-size: 32px;
      }}
      p {{
        margin: 0 0 26px;
        color: #4e4e4e;
      }}
      .list {{
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 14px;
      }}
      .card {{
        background: #ffffff;
        border: 2px solid #d7d7d7;
        border-radius: 14px;
        padding: 16px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
      }}
      .card-title {{
        font-weight: 700;
        font-size: 18px;
      }}
      .card-desc {{
        margin-top: 6px;
        font-size: 13px;
        color: #5a5a5a;
      }}
      .card-link {{
        background: #ff5a58;
        color: #ffffff;
        text-decoration: none;
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }}
      @media (max-width: 560px) {{
        .card {{
          flex-direction: column;
          align-items: flex-start;
        }}
        .card-link {{
          align-self: flex-end;
        }}
      }}
    </style>
  </head>
  <body>
    <main class=\"page\">
      <h1>NTU Web Programming - Assignments</h1>
      <p>Course work collection.</p>

      <ul class=\"list\">
{cards_html}
      </ul>
    </main>
  </body>
</html>
"""


def update_readme(assignments: list[dict[str, str]]) -> None:
    readme_path = ROOT_DIR / "README.md"
    marker_start = "<!-- ASSIGNMENTS:START -->"
    marker_end = "<!-- ASSIGNMENTS:END -->"
    lines = "\n".join(
        [f"- [{item['title']}](assignments/{item['folder']}/)" for item in assignments]
    )
    block = f"{marker_start}\n{lines}\n{marker_end}"

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
    else:
        content = "# NTU Web Programming - Assignments\n\nThis repository collects course assignments.\n\n## Assignments\n\n"

    if marker_start in content and marker_end in content:
        before = content.split(marker_start)[0].rstrip()
        after = content.split(marker_end)[1].lstrip()
        content = f"{before}\n\n{block}\n\n{after}".strip() + "\n"
    else:
        content = f"{content.strip()}\n\n{block}\n"

    if "## GitHub Pages" not in content:
        content += (
            "\n## GitHub Pages\n"
            "After enabling Pages, the site will be available at:\n"
            "- https://legendragon.github.io/NTU-Web-Programming/\n"
        )

    readme_path.write_text(content, encoding="utf-8")


def main() -> None:
    assignments = get_assignments()
    index_html = build_index_html(assignments)
    (ROOT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    update_readme(assignments)
    print(f"Generated index for {len(assignments)} assignment(s).")


if __name__ == "__main__":
    main()
