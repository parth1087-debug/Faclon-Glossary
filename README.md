# Faclon Labs: solution collateral

Customer-facing pages and downloads for Faclon Labs solution lines, published as a static website with GitHub Pages.

**Live site:** https://parth1087-debug.github.io/Power-Plant-AI/

| Solution | Web page | Download |
|---|---|---|
| Power Plant AI | [`/power-plant-ai/`](power-plant-ai/index.html) | [Use-case catalogue (PDF)](power-plant-ai/power-plant-ai-use-case-catalogue.pdf) |

## Layout

```
index.html                     Landing page listing every solution
<solution>/index.html          Generated web page for a solution (do not hand-edit)
<solution>/*.pdf               Generated downloads
src/<solution>/build_*.py      Source of truth: content lives in the Python lists at the top of each script
src/shared/                    Shared assets (logo, badges)
CLAUDE.md                      Conventions for anyone (or any AI assistant) editing this repo
```

## Updating a page

1. Edit the content lists in `src/<solution>/build_page.py` (for example `AGENTS` or `APC` for Power Plant AI).
2. Regenerate:
   ```bash
   python3 src/power-plant-ai/build_page.py           # writes power-plant-ai/index.html
   python3 src/power-plant-ai/build_catalogue_pdf.py  # writes the PDF (needs: pip install playwright && playwright install chromium)
   ```
3. Commit and push. GitHub Pages republishes within a minute or two.

## Adding a new solution

1. Copy `src/power-plant-ai/` to `src/<new-solution>/` and change its content and `OUT` path.
2. Run the build so `<new-solution>/index.html` exists.
3. Add a card for it in the root `index.html` and a row in the table above.

## One-time setup: turn on GitHub Pages

Repository **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, folder = `/ (root)`. Save.

## Notes

- Every page carries `<meta name="robots" content="noindex">`, so it is reachable by link but not listed by search engines. Remove that line from a page to make it searchable.
- The repository is public, so everything committed here (including customer names and figures) can be read by anyone. Keep internal-only material out of it.
- Indicative ₹ values are "up to, per 100 MW per year" and must be re-baselined against each plant's data.
