# Faclon Labs: Power Plant AI

Customer-facing page for Faclon Labs' Power Plant AI offering (Advisory Agents and Automated Process Control), published with GitHub Pages.

**Live page:** https://parth1087-debug.github.io/Power-Plant-AI/

## Layout

```
index.html                               The page (generated; do not hand-edit)
power-plant-ai-use-case-catalogue.pdf    Downloadable catalogue of all 24 use cases (generated)
power-plant-ai/index.html                Redirect so the old /power-plant-ai/ link still works
src/power-plant-ai/build_page.py         Source of truth for the page: edit the AGENTS and APC lists
src/power-plant-ai/build_catalogue_pdf.py Source of truth for the PDF
src/shared/                              Shared assets
CLAUDE.md                                Conventions for anyone (or any AI assistant) editing this repo
```

## Updating the page

1. Edit the content in `src/power-plant-ai/build_page.py`.
2. Regenerate:
   ```bash
   python3 src/power-plant-ai/build_page.py           # writes index.html
   python3 src/power-plant-ai/build_catalogue_pdf.py  # writes the PDF (needs: pip install playwright && playwright install chromium)
   ```
3. Commit and push. GitHub Pages republishes within a minute or two.

## Notes

- The page carries `<meta name="robots" content="noindex">`, so it is reachable by link but not listed by search engines.
- The repository is public, so everything committed here (including customer names and figures) can be read by anyone. Keep internal-only material out of it.
- Indicative ₹ values are "up to, per 100 MW per year" and must be re-baselined against each plant's data.
