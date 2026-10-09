"""Build responsive HTML editions from the LaTeX sources.

Requires pandoc and beautifulsoup4. Run from any directory:
    python scripts/build_paper_html.py
"""

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import subprocess

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Paper:
    source: str
    number: str
    title: str
    subtitle: str
    date: str
    description: str
    edition_label: str


PAPERS = (
    Paper(
        "disorder_potential_search_note_v2.tex",
        "01",
        "Disorder Potential and the Cost of Search",
        "A balance law and a separation by disorder location",
        "October 4, 2026",
        "The full mobile-friendly HTML edition of Disorder Potential and the Cost of Search.",
        "paper 01 / 02",
    ),
    Paper(
        "experiments/n9-potential-distribution/potential_across_random_permutations.tex",
        "N",
        "Potential Across Random Permutations",
        "A companion note on when disorder budgets help search",
        "October 9, 2026",
        "Exact permutation counts and general bounds explain when a disorder budget helps search.",
        "companion note",
    ),
    Paper(
        "search-under-a-disorder-budget/search_under_a_disorder_budget.tex",
        "02",
        "Search Under a Disorder Budget",
        "Preprocessing, repeated queries, and adaptive indexing",
        "October 9, 2026",
        "The full mobile-friendly HTML edition of Search Under a Disorder Budget.",
        "paper 02 / 02",
    ),
    Paper(
        "search-under-query-entropy/search_under_query_entropy.tex",
        "03",
        "Search Under Disorder and Query Entropy",
        "A two-budget note on repeated comparison search",
        "October 8, 2026",
        "The full mobile-friendly HTML edition of Search Under Disorder and Query Entropy.",
        "work in progress",
    ),
)


def pandoc(source: str, *, filename: Path | None = None) -> str:
    command = ["pandoc", "-f", "latex", "-t", "html5", "--mathjax", "--wrap=none"]
    if filename is not None:
        command.append(str(filename))
    result = subprocess.run(
        command,
        input=None if filename is not None else source,
        capture_output=True,
        check=True,
        encoding="utf-8",
        cwd=ROOT,
    )
    return result.stdout


def bibliography_entries(tex: str) -> list[tuple[str, str]]:
    block = re.search(
        r"\\begin\{thebibliography\}\{[^}]+\}(.*?)\\end\{thebibliography\}",
        tex,
        re.DOTALL,
    )
    if not block:
        return []
    text = block.group(1)
    matches = list(re.finditer(r"\\bibitem\{([^}]+)\}", text))
    return [
        (match.group(1), text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)].strip())
        for index, match in enumerate(matches)
    ]


def convert_body(paper: Paper) -> tuple[str, str]:
    source_path = ROOT / paper.source
    tex = source_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(pandoc("", filename=source_path), "html.parser")

    # The HTML page supplies its own title block, navigation, and metadata.
    title_block = soup.find("div", class_="center")
    if title_block is None:
        raise ValueError(f"Missing title block: {source_path}")
    title_block.decompose()

    main_paper = paper.number == "01"
    for heading in soup.find_all(["h1", "h4"]):
        if main_paper:
            heading.name = "h2" if heading.name == "h1" else "h3"
        else:
            heading.name = "h2"

    first_paragraph = soup.find("p")
    if first_paragraph and first_paragraph.strong and first_paragraph.strong.get_text(strip=True) == "Abstract.":
        first_paragraph["class"] = ["abstract"]

    entries = bibliography_entries(tex)
    numbers = {key: index + 1 for index, (key, _) in enumerate(entries)}
    for citation in soup.select("span.citation"):
        keys = citation.get("data-cites", "").split()
        if not keys or any(key not in numbers for key in keys):
            raise ValueError(f"Unresolved citation in {source_path}: {keys}")
        group = soup.new_tag("span", attrs={"class": "citation"})
        for index, key in enumerate(keys):
            if index:
                group.append(" ")
            link = soup.new_tag("a", href=f"#ref-{key}", attrs={"class": "citation-link"})
            link.string = f"[{numbers[key]}]"
            group.append(link)
        citation.replace_with(group)

    labels = re.findall(r"\\label\{(eq:[^}]+)\}", tex)
    equation_numbers = {label: number for number, label in enumerate(labels, start=1)}
    seen_labels = set()
    for display in soup.select("span.math.display"):
        match = re.search(r"\\label\{(eq:[^}]+)\}", display.get_text())
        if match:
            label = match.group(1)
            display["id"] = label
            display.string = display.get_text().replace(match.group(0), rf"\tag{{{equation_numbers[label]}}}")
            seen_labels.add(label)
    if seen_labels != set(labels):
        raise ValueError(f"Equation anchors missing in {source_path}: {set(labels) - seen_labels}")
    for link in soup.select('a[data-reference-type="eqref"]'):
        label = link.get("data-reference")
        if label not in equation_numbers:
            raise ValueError(f"Unresolved equation reference in {source_path}: {label}")
        link.string = f"({equation_numbers[label]})"

    for table in soup.find_all("table"):
        headers = [heading.get_text(" ", strip=True) for heading in table.select("thead th")]
        for row in table.select("tbody tr"):
            for index, cell in enumerate(row.find_all("td")):
                if index < len(headers):
                    cell["data-label"] = headers[index]

    old_bibliography = soup.find("div", class_="thebibliography")
    if entries:
        if old_bibliography is None:
            raise ValueError(f"Missing converted bibliography in {source_path}")
        section = soup.new_tag("section", id="references", attrs={"class": "references"})
        heading = soup.new_tag("h2", id="references-heading")
        heading.string = "References"
        section.append(heading)
        ordered = soup.new_tag("ol")
        for key, entry_tex in entries:
            item = soup.new_tag("li", id=f"ref-{key}")
            rendered = BeautifulSoup(pandoc(entry_tex), "html.parser")
            paragraph = rendered.find("p")
            if paragraph:
                for child in list(paragraph.contents):
                    item.append(child.extract())
            else:
                for child in list(rendered.contents):
                    item.append(child.extract())
            ordered.append(item)
        section.append(ordered)
        old_bibliography.replace_with(section)
    elif old_bibliography:
        raise ValueError(f"Unexpected bibliography in {source_path}")

    section_links = []
    for heading in soup.find_all("h2"):
        anchor = heading.get("id")
        if anchor:
            section_links.append(
                f'<li><a href="#{escape(anchor, quote=True)}">{escape(heading.get_text(" ", strip=True))}</a></li>'
            )
    toc = ""
    if section_links:
        toc = (
            '<nav class="toc" aria-label="paper contents"><details>'
            '<summary>on this page</summary><ol>'
            + "".join(section_links)
            + "</ol></details></nav>"
        )

    body = "".join(str(node) for node in soup.contents)
    return toc, body


def build(paper: Paper) -> Path:
    toc, body = convert_body(paper)
    source = Path(paper.source)
    output = ROOT / source.with_suffix(".html")
    prefix = "../" * len(source.parent.parts) if source.parent != Path(".") else "./"
    title = escape(paper.title)
    subtitle = escape(paper.subtitle)
    page = f"""<!doctype html>
<!-- Generated from {escape(paper.source)} by scripts/build_paper_html.py. -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#080808">
  <meta name="description" content="{escape(paper.description, quote=True)}">
  <title>{title} — jonathan r. landers</title>
  <link rel="stylesheet" href="{prefix}paper.css">
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"></script>
</head>
<body id="top">
  <a class="skip" href="#paper-body">skip to paper</a>
  <div class="frame">
    <header class="masthead">
      <a class="brand" href="{prefix}index.html" aria-label="disorder and search, home"><img class="brand-icon" src="{prefix}ninja-mark.svg" alt="" aria-hidden="true">disorder / search</a>
      <nav aria-label="paper links">
        <a href="{prefix}index.html#papers">papers and note</a>
        <a href="./{source.stem}.pdf">pdf</a>
        <a href="./{source.name}">latex</a>
      </nav>
    </header>
    <main>
      <header class="paper-hero">
        <p class="eyebrow">{escape(paper.edition_label)} &nbsp;·&nbsp; html edition</p>
        <h1>{title}</h1>
        <p class="subtitle">{subtitle}</p>
        <p class="byline">Jonathan R. Landers &nbsp;·&nbsp; {escape(paper.date)}</p>
        <nav class="paper-actions" aria-label="other formats">
          <a href="./{source.stem}.pdf">read the pdf ↗</a>
          <a href="./{source.name}">latex source ↗</a>
        </nav>
      </header>
      <article class="paper-body" id="paper-body">
        {toc}
        {body}
      </article>
    </main>
    <footer class="footer">
      <p>jonathan r. landers · 2026</p>
      <a href="#top">back to top ↑</a>
    </footer>
  </div>
</body>
</html>
"""
    output.write_text(page, encoding="utf-8")
    return output


if __name__ == "__main__":
    for paper in PAPERS:
        path = build(paper)
        print(path.relative_to(ROOT))
