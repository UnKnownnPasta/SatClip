"""Rebuild archive/index.csv and the catalog section of archive/README.md
from the front matter of archive/papers/*.md.

Run from the repo root:  python tools/build_index.py
Every paper file must carry: id, title, year, venue, category, era, link, takeaway.
"""
import csv
import glob
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(ROOT, "archive", "papers")
FIELDS = ["id", "title", "year", "venue", "category", "era", "link", "takeaway"]
START, END = "<!-- CATALOG:START -->", "<!-- CATALOG:END -->"


def front_matter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        raise ValueError(f"no front matter in {path}")
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            v = v.strip()
            if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                v = v[1:-1]
            data[k.strip()] = v
    missing = [f for f in FIELDS if not data.get(f)]
    if missing:
        raise ValueError(f"{os.path.basename(path)} missing {missing}")
    data["file"] = os.path.basename(path)
    return data


def main():
    rows = [front_matter(p) for p in sorted(glob.glob(os.path.join(PAPERS, "*.md")))]
    ids = [r["id"] for r in rows]
    dup = [i for i, c in Counter(ids).items() if c > 1]
    if dup:
        raise SystemExit(f"duplicate ids: {dup}")
    titles = Counter(r["title"].lower() for r in rows)
    dupt = [t for t, c in titles.items() if c > 1]
    if dupt:
        raise SystemExit(f"duplicate titles: {dupt}")

    with open(os.path.join(ROOT, "archive", "index.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "title", "year", "venue", "category", "era", "link", "takeaway"])
        for r in rows:
            w.writerow([r[k] for k in FIELDS])

    cats = Counter(r["category"] for r in rows)
    lines = [START, "", f"Total papers: **{len(rows)}**", ""]
    lines.append("| Category | Count |")
    lines.append("|---|---|")
    for c, n in sorted(cats.items()):
        lines.append(f"| {c} | {n} |")
    for c in sorted(cats):
        lines += ["", f"### {c}", "", "| ID | Paper | Year | Era | Takeaway for SatClip |", "|---|---|---|---|---|"]
        for r in rows:
            if r["category"] == c:
                title = r["title"].replace("|", "/")
                lines.append(
                    f"| {r['id']} | [{title}](papers/{r['file']}) ([source]({r['link']})) | {r['year']} | {r['era']} | {r['takeaway'].replace('|', '/')} |"
                )
    lines += ["", END]
    readme_path = os.path.join(ROOT, "archive", "README.md")
    readme = open(readme_path, encoding="utf-8").read()
    pre, rest = readme.split(START, 1)
    _, post = rest.split(END, 1)
    open(readme_path, "w", encoding="utf-8").write(pre + "\n".join(lines) + post)
    print(f"indexed {len(rows)} papers: {dict(sorted(cats.items()))}")


if __name__ == "__main__":
    main()
