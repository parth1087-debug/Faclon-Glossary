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
src/admin/index.html           Source of the User Manager (built into admin/index.html by protect.py)
src/shared/protect.py          Encrypts pages and builds the User Manager
users.json                     User list (written by the User Manager; encrypted keyrings)
src/shared/                    Shared assets
CLAUDE.md                      Conventions for anyone (or any AI assistant) editing this repo
```

## Updating pages

```bash
python3 src/home/build_home.py                     # writes index.html
python3 src/power-plant-ai/build_page.py           # writes power-plant-ai/index.html
python3 src/steel-ai-use-case-map/build_page.py    # writes steel-ai-use-case-map/index.html (content in use_cases.json)
python3 src/faclon-overview/build_page.py         # writes faclon-overview/index.html (content in content.json)
python3 src/steam-trap-monitoring/build_page.py   # writes steam-trap-monitoring/index.html (content in content.json, diagrams in diagrams.py)
python3 src/bus-bar-monitoring/build_page.py      # writes bus-bar-monitoring/index.html (content in content.json, photos in assets/)
python3 src/energy-management/build_page.py       # writes energy-management/index.html (content in content.json, screenshots in assets/)
python3 src/condition-based-monitoring/build_page.py  # writes condition-based-monitoring/index.html (content in content.json)
python3 src/power-plant-ai/build_catalogue_pdf.py  # writes the PDF (needs: pip install playwright && playwright install chromium)
```

Then pull `main` and password-protect the regenerated pages (the admin password is not stored in this repo):

```
git pull origin main
GLOSSARY_PASSWORD='<admin password>' python3 src/shared/protect.py   # encrypts pages, refreshes users.json, builds admin/
python3 src/shared/protect.py --check                                # must pass before you commit
```

Commit and push. GitHub Pages republishes within a minute or two.

## Adding a new solution

1. Copy `src/power-plant-ai/` to `src/<new-solution>/`, change its content and set `OUT` to `<new-solution>/index.html`.
2. Run its build so `<new-solution>/index.html` exists.
3. In `src/home/build_home.py`, set `"live": True` for that solution (or add it to `SOLUTIONS`), then rebuild the landing page.
4. Add a row to the table above.

## Notes

- **Access control.** Visitors sign in with a username and password and see only the solutions shared with them; other pages show a "No access" screen. Sign in as `admin` with the admin password to see everything.
- **User Manager** at [`/admin/`](admin/index.html): add, edit and remove users, pick their solutions, then **Publish**, which commits `users.json` to `main` (needs a fine-grained GitHub token with Contents: Read and write on this repo, saved once per browser; without one it offers a download to upload by hand). Changes are live in about a minute.
- How it works: each page is AES-encrypted with its own key, derived from the admin password. Each user's entry in `users.json` is a keyring holding only their pages' keys, locked with their own password. Removing a user or a solution takes effect on their next page load.
- Limits: this protects the published pages only. The sources in `src/` and the PDFs are readable by anyone with the link to this public repo or file. Someone who deliberately copied their page keys before being removed could still read those pages; to cut that off completely, change the admin password and recreate users.
- Every page carries `<meta name="robots" content="noindex">`, so it is reachable by link but not listed by search engines.
- The repository is public, so everything committed here (including customer names and figures) can be read by anyone. Keep internal-only material out of it.
- Indicative ₹ values are "up to, per 100 MW per year" and must be re-baselined against each plant's data.
