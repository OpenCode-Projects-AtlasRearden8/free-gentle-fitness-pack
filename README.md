# Gentle Fitness Pack

Free printable pages for moving gently at any size and any energy level. Seven
sheets, one build script, zero signups, zero tracking. The sheets work the
moment they leave the printer.

Brought to you by **Asdale Dynamics, LLC** — the LLC behind *The Massive AI
Manual* and dylanasdale.github.io, which explains AI "like a friend would" and
publishes plain-English guides and practical, tested tools. Gentle Fitness Pack
is a healthcare-adjacent education aid: it teaches ideas about everyday
movement; it never prescribes exercise, medication, or anything medical.

## What's inside

Every PDF opens with a kind getting-started page, then the sheet itself, and
carries the same reminder in small print on **every** page: this material is
education only, never exercise prescription — go only if your doctor or
physical therapist has cleared you to move, and stop if anything hurts.

| PDF | Use it when |
| --- | --- |
| `wake-up-stretch.pdf` | Six easy moves, five unhurried minutes, before your coffee cools |
| `chair-exercises.pdf` | Two pages of fully seated movement for the lowest-energy days |
| `mileage-log.pdf` | Walk and count *anything* — lampposts, songs, blocks — and jot it down |
| `balance-practice.pdf` | Everyday steadiness, practiced within arm's reach of something sturdy |
| `water-tracker.pdf` | A gentle sip tally; your cup, your amounts, no quota |
| `rest-day-permission.pdf` | The official-looking slip that says resting counts |
| `movement-bingo.pdf` | A monthly card of tiny wins; any five in a row counts |

## Rebuild the PDFs yourself

Requires Python 3.9+ with WeasyPrint (`pip install weasyprint`).

```bash
python3 build.py                 # builds every sheet into printables/
python3 build.py wake-up-stretch # or just one sheet
python3 -m pytest tests/         # verifies every PDF builds and is valid
```

## How the sources work

- `src/styles.css` — the shared print stylesheet. The cleared-reminder lives in
  the `@page` footer here, so it appears automatically on every rendered page.
- `src/getting-started.html` — the welcome page included as page 1 of every PDF.
- `src/sheets/*.html` — one file per printable, plain HTML/CSS, easy to edit.
- `printables/` — the finished, unbranded PDFs: no logos, no company names,
  nothing to administer.

## Who this is for

Anyone who has ever felt talked down to by a fitness plan. Big bodies, tired
bodies, wobbly days, by-choice rest days — the pack assumes all of it and adds
nothing to prove. Print one page or all of them. Nothing is collected, nothing
is tracked, and nothing needs an account.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Asdale Dynamics, LLC.
Published as an education-only resource; it is not medical advice.
