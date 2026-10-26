#!/usr/bin/env python3
"""Build the Gentle Fitness Pack.

Looks through src/sheets/ for HTML sheets, wraps each one with the shared
getting-started page and stylesheet, and renders an unbranded PDF into
printables/ using WeasyPrint.

Usage:
    python3 build.py               # build every sheet
    python3 build.py wake-up-stretch   # build a single sheet by name
"""

import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SHEETS = SRC / "sheets"
OUT = ROOT / "printables"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def wrap(title: str, css: str, getting_started: str, body: str) -> str:
    """Assemble one full HTML document: getting-started page, then the sheet."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} — Gentle Movement Pack</title>
<meta name="description" content="Free printable gentle-movement sheet. Education only; never exercise prescription.">
<style>
{css}
</style>
</head>
<body>
{getting_started}
{body}
</body>
</html>
"""


def build_sheet(title: str, sheet_path: Path, css: str, getting_started: str, out_dir: Path) -> Path:
    html = wrap(title=title, css=css, getting_started=getting_started, body=read(sheet_path))
    out_pdf = out_dir / f"{sheet_path.stem}.pdf"
    HTML(string=html, base_url=str(SRC)).write_pdf(out_pdf)
    return out_pdf


def main(argv: list[str]) -> int:
    css_path = SRC / "styles.css"
    gs_path = SRC / "getting-started.html"
    for required in (css_path, gs_path):
        if not required.exists():
            print(f"Missing required source: {required.relative_to(ROOT)}", file=sys.stderr)
            return 2

    sheets = sorted(SHEETS.glob("*.html"))
    if not sheets:
        print(f"No sheets found in {SHEETS.relative_to(ROOT)}", file=sys.stderr)
        return 2

    wanted = [a for a in argv[1:] if not a.startswith("-")] or None
    if wanted:
        wanted = [w.lower() for w in wanted]
        sheets = [s for s in sheets if s.stem in wanted or s.stem.lower() in wanted]
        missing = [
            w for w in wanted if w not in {s.stem for s in SHEETS.glob("*.html")}
        ]
        if missing:
            print(f"No sheet named: {', '.join(missing)}", file=sys.stderr)
            return 2

    OUT.mkdir(exist_ok=True)
    css = read(css_path)
    getting_started = read(gs_path)

    built: list[Path] = []
    for sheet in sheets:
        title = sheet.stem.replace("-", " ").title()
        pdf = build_sheet(title, sheet, css, getting_started, OUT)
        built.append(pdf)
        print(f"built {pdf.relative_to(ROOT)}")

    print(f"\n{len(built)} PDF(s) in printables/ — unbranded, offline, no signups.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
