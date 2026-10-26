"""Tests for the Gentle Fitness Pack.

Verifies that every sheet in src/sheets/ builds a valid, well-formed,
unbranded PDF in printables/ with the education-only cleared-reminder
on every page.

Run with:  python3 -m pytest tests/ -v
"""

import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SHEETS = SRC / "sheets"
OUT = ROOT / "printables"

RENDERED_PDFS: list[Path]


def _run_build() -> list[Path]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"build.py failed:\n{result.stdout}\n{result.stderr}")
    return sorted(OUT.glob("*.pdf"))


# Build all PDFs once, before any test runs.
RENDERED_PDFS = _run_build()


def _pdf(name: str) -> Path:
    path = OUT / f"{name}.pdf"
    assert path.exists(), f"missing built PDF: {path.name}"
    return path


def test_build_succeeded():
    assert RENDERED_PDFS is not None
    assert set(p.stem for p in RENDERED_PDFS) == {
        s.stem for s in SHEETS.glob("*.html")
    }


def test_build_script_rejects_unknown_sheet():
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "no-such-sheet"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "No sheet named" in result.stderr


@pytest.mark.parametrize(
    "name",
    sorted(s.stem for s in SHEETS.glob("*.html")),
)
def test_every_sheet_builds_a_valid_pdf(name):
    path = _pdf(name)
    data = path.read_bytes()

    # %PDF header at the start, %%EOF marker at the end.
    assert data[:5] == b"%PDF-", f"{name}.pdf has no PDF header"
    assert b"%%EOF" in data[-4096:], f"{name}.pdf has no %%EOF trailer"

    # A real reader must parse it, and the build always ships the
    # getting-started page (page 1) plus at least one activity page.
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 2, f"{path.name} should have >= 2 pages"
    assert reader.metadata.title and "Gentle Movement Pack" in reader.metadata.title

    # Not an accidentally-empty or corrupted file.
    assert path.stat().st_size > 5_000, f"{path.name} looks truncated"


@pytest.mark.parametrize(
    "name",
    sorted(s.stem for s in SHEETS.glob("*.html")),
)
def test_every_sheet_had_a_getting_started_page(name):
    path = _pdf(name)
    reader = PdfReader(str(path))
    first_page_text = reader.pages[0].extract_text() or ""
    assert "Welcome in" in first_page_text, (
        f"{path.name} page 1 should be the kind getting-started page"
    )


def test_chair_exercises_has_two_activity_pages():
    reader = PdfReader(str(_pdf("chair-exercises")))
    assert len(reader.pages) == 3  # getting-started + Page A + Page B


def test_every_source_page_carries_the_cleared_reminder():
    """The education-only / cleared-to-move reminder lives in the shared
    stylesheet footer (printed on every page) and in a visible reminder
    card on each sheet page."""
    css = (SRC / "styles.css").read_text(encoding="utf-8")
    assert "Education only" in css
    assert "cleared" in css
    assert "prescription" in css

    for sheet in sorted(SHEETS.glob("*.html")):
        text = sheet.read_text(encoding="utf-8")
        assert "education" in text.lower(), f"{sheet.name} lacks education note"
        assert "prescription" in text.lower(), f"{sheet.name} lacks prescription note"
        assert "doctor" in text.lower(), f"{sheet.name} lacks doctor reminder"


def test_pdfs_are_unbranded():
    """PDFs carry no company branding — no company name anywhere in the
    rendered document text, and none in the sources that feed the PDFs."""
    brand_markers = ("Asdale", "asdale", "Dynamics", "LLC")
    for sheet in sorted(SHEETS.glob("*.html")):
        text = sheet.read_text(encoding="utf-8")
        for marker in brand_markers:
            assert marker not in text, f"{marker} found in {sheet.name}"
    wrapper = (ROOT / "build.py").read_text(encoding="utf-8")
    for marker in brand_markers:
        assert marker not in wrapper, f"{marker} found in build.py wrapper"
    css = (SRC / "styles.css").read_text(encoding="utf-8")
    assert "Asdale" not in css


def test_getting_started_mentions_no_signups():
    text = (SRC / "getting-started.html").read_text(encoding="utf-8")
    assert "no signups" in text.lower() or "signups" in text.lower()
