# Faclon Labs: solution pages

Customer-facing pages for Faclon Labs solution lines, published as a static website with GitHub Pages.

**Live site:** https://parth1087-debug.github.io/Faclon-Glossary/

| Solution | Page | Download |
|---|---|---|
| Power Plant AI | [`/power-plant-ai/`](power-plant-ai/index.html) | [Use-case catalogue (PDF)](power-plant-ai/power-plant-ai-use-case-catalogue.pdf) |
| Faclon Labs Overview | [`/faclon-overview/`](faclon-overview/index.html) | |
| Steel AI Use Case Map | [`/steel-ai-use-case-map/`](steel-ai-use-case-map/index.html) | |
| Steam Trap Failure Detection | [`/steam-trap-monitoring/`](steam-trap-monitoring/index.html) | |
| Bus Bar Monitoring | [`/bus-bar-monitoring/`](bus-bar-monitoring/index.html) | |
| Energy Management | [`/energy-management/`](energy-management/index.html) | |
| Condition Based Monitoring | [`/condition-based-monitoring/`](condition-based-monitoring/index.html) | |

## Layout

```
index.html                     Landing page listing every solution (generated)
<solution>/index.html          Page for one solution (generated; do not hand-edit)
<solution>/*.pdf               Generated downloads
src/home/build_home.py         Source of truth for the landing page: edit the SOLUTIONS list
src/<solution>/build_*.py      Source of truth for each solution page
src/shared/                    Shared assets
CLAUDE.md                      Conventions for anyone (or any AI assistant) editing this repo
```

## Updating pages

```bash
python3 src/home/build_home.py                     # writes index.html
python3 src/power-plant-ai/build_page.py           # writes power-plant-ai/index.html
python3 src/steel-ai-use-case-map/build_page.py    # writes steel-ai-use-case-map/index.html (content in use_cases.json)
python3 src/faclon-overview/build_page.py         # writes faclon-overview/index.html (content in content.json)
python3 src/steam-trap-monitoring/build_page.py   # writes steam-trap-monitoring/index.html (content in content.json)
python3 src/bus-bar-monitoring/build_page.py      # writes bus-bar-monitoring/index.html (content in content.json, photos in assets/)
python3 src/energy-management/build_page.py       # writes energy-management/index.html (content in content.json, screenshots in assets/)
python3 src/condition-based-monitoring/build_page.py  # writes condition-based-monitoring/index.html (content in content.json)
python3 src/power-plant-ai/build_catalogue_pdf.py  # writes the PDF (needs: pip install playwright && playwright install chromium)
```

Commit and push. GitHub Pages republishes within a minute or two.

## Adding a new solution

1. Copy `src/power-plant-ai/` to `src/<new-solution>/`, change its content and set `OUT` to `<new-solution>/index.html`.
2. Run its build so `<new-solution>/index.html` exists.
3. In `src/home/build_home.py`, set `"live": True` for that solution (or add it to `SOLUTIONS`), then rebuild the landing page.
4. Add a row to the table above.

## Notes

- Every page carries `<meta name="robots" content="noindex">`, so it is reachable by link but not listed by search engines.
- The repository is public, so everything committed here (including customer names and figures) can be read by anyone. Keep internal-only material out of it.
- Indicative ₹ values are "up to, per 100 MW per year" and must be re-baselined against each plant's data.
