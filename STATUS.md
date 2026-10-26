# STATUS

## What was built

**Gentle Fitness Pack v1.0** — a free, offline, zero-signup printable pack for
moving gently at any size or energy level. Seven HTML/CSS sheets build into
unbranded PDFs via one script (`build.py`, WeasyPrint). Every PDF opens with
the kind getting-started page and carries the education-only cleared-reminder
in small print on every rendered page (implemented in the `@page` footer of
`src/styles.css`, plus a visible reminder card on each sheet).

Sheets (all in `printables/`):

1. `wake-up-stretch.pdf` — five-minute wake-up stretch card
2. `chair-exercises.pdf` — chair-exercise pages (Page A + Page B)
3. `mileage-log.pdf` — walk-and-count mileage log
4. `balance-practice.pdf` — balance-practice sheet
5. `water-tracker.pdf` — water-sip tracker
6. `rest-day-permission.pdf` — rest-day permission slip
7. `movement-bingo.pdf` — monthly movement-bingo card

Tone is beginner-friendly and non-condescending (size- and energy-neutral
wording throughout), consistent with Asdale Dynamics, LLC's "explain it like a
friend would" style. The PDFs themselves are unbranded (no company name, no
logo); branding lives only in README/STATUS/LICENSE.

## How to run it

```bash
python3 build.py                 # build every sheet into printables/
python3 build.py <sheet-name>    # rebuild a single sheet
python3 -m pytest tests/         # run the verification tests
```

Requires Python 3.9+ and WeasyPrint (`pip install weasyprint`); tests also use
`pytest` and `pypdf`.

## Verification results

- Full rebuild from an empty `printables/`: all 7 PDFs generated (16–24 KB each).
- Single-sheet rebuild (`python3 build.py water-tracker`): works, exit 0.
- Test suite: **20 passed** (builds every sheet, verifies `%PDF` header +
  `%%EOF` trailer, >= 2 pages parsed by `pypdf`, document titles, the
  getting-started page first, the education/prescription/doctor reminders on
  every sheet, and that no branding string reaches the PDF sources).
- Pages visually spot-checked via image render (getting-started, bingo,
  permission slip, water tracker, chair page A): layout, fillable boxes,
  checkboxes, and footers all render correctly on letter size.
- No secrets, API keys, or personal data anywhere in the repo.

## Known gaps

- Single shared getting-started page is included in every PDF; the per-sheet
  focus line on that page is generic rather than sheet-specific.
- Print layout is tuned for letter; A4 prints fine but pages are not
  A4-optimized (slightly different margins).
- No accessibility-tagged PDFs (content is plain text and easily readable, but
  WeasyPrint output is not screen-reader tagged).
- Bingo card content is fixed per month (a blank "Month of ___" line, same 25
  squares each month).
- Copyright/if-asked: MIT LICENSE copyright line is
  `Copyright (c) 2026 Asdale Dynamics, LLC`; Asdale Dynamics, LLC is credited
  in README.md and not in the PDFs (kept unbranded by design).

## Publishing

Not published anywhere. Repository is local-only; no remote, no pushes.
