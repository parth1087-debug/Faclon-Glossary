# Faclon Labs: solution pages

Customer-facing pages for Faclon Labs solution lines, published as a static website with GitHub Pages.

**Live site:** https://parth1087-debug.github.io/Faclon-Glossary/

| Solution | Page | Download |
|---|---|---|
| Power Plant AI | [`/power-plant-ai/`](power-plant-ai/index.html) | |
| Faclon Labs Overview | [`/faclon-overview/`](faclon-overview/index.html) | |
| Steel AI Use Case Map | [`/steel-ai-use-case-map/`](steel-ai-use-case-map/index.html) | |
| AI Closed-Loop Soot Blowing | [`/ai-closed-loop-soot-blowing/`](ai-closed-loop-soot-blowing/index.html) | |
| Cement AI Use Case Map | [`/cement-ai-use-case-map/`](cement-ai-use-case-map/index.html) | |
| Pulp & Paper AI Use Case Map | [`/pulp-paper-ai-use-case-map/`](pulp-paper-ai-use-case-map/index.html) | |
| Coal Mining AI Use Case Map | [`/coal-mining-ai-use-case-map/`](coal-mining-ai-use-case-map/index.html) | |
| Aluminium Use Cases | [`/aluminium-use-cases/`](aluminium-use-cases/index.html) | |
| Copper Use Cases | [`/copper-use-cases/`](copper-use-cases/index.html) | |
| Pulp & Fibre Use Cases | [`/pulp-fibre-use-cases/`](pulp-fibre-use-cases/index.html) | |
| Refinery & Petrochemicals Use Cases | [`/refinery-petrochemicals-use-cases/`](refinery-petrochemicals-use-cases/index.html) | |
| Chemicals Use Cases | [`/chemicals-use-cases/`](chemicals-use-cases/index.html) | |
| Agrochemicals Use Cases | [`/agrochemicals-use-cases/`](agrochemicals-use-cases/index.html) | |
| Solar Use Cases | [`/solar-use-cases/`](solar-use-cases/index.html) | |
| Battery Energy Storage Use Cases | [`/bess-use-cases/`](bess-use-cases/index.html) | |
| Steam Trap Failure Detection | [`/steam-trap-monitoring/`](steam-trap-monitoring/index.html) | |
| Bus Bar Monitoring | [`/bus-bar-monitoring/`](bus-bar-monitoring/index.html) | |
| Energy Management | [`/energy-management/`](energy-management/index.html) | |
| Condition Based Monitoring | [`/condition-based-monitoring/`](condition-based-monitoring/index.html) | |
| IT-OT Integration | [`/it-ot-integration/`](it-ot-integration/index.html) | |
| I/O Vision | [`/io-vision/`](io-vision/index.html) | |

## Layout

```
index.html                     Landing page listing every solution (generated)
<solution>/index.html          Page for one solution (generated; do not hand-edit)
<solution>/*.pdf               Generated downloads
src/home/build_home.py         Source of truth for the landing page: edit the SOLUTIONS list
src/<solution>/build_*.py      Source of truth for each solution page
src/admin/index.html           Source of the User Manager (built into admin/index.html by protect.py)
src/shared/protect.py          Encrypts pages, renders their PDFs and builds the User Manager (needs: pip install playwright && playwright install chromium)
readme/index.html              Read me guide for signed-in users (generated; not a solution, can't be downloaded)
src/readme/build_page.py       Source of the Read me
src/connector/                 Source of the Claude connector for contributors (built into connector/ by protect.py)
connector/                     Claude connector downloads: .mcpb for Claude Desktop, single .js for Claude Code (generated)
src/shared/page_tools.js       Signed-in bar and Download dialog injected into every unlocked page
<solution>/page-pdf.bin        Encrypted one-page PDF of that solution (generated)
users.json                     User list (written by the User Manager; encrypted keyrings)
src/shared/                    Shared assets
CLAUDE.md                      Conventions for anyone (or any AI assistant) editing this repo
```

## Updating pages

```bash
python3 src/home/build_home.py                     # writes index.html
python3 src/power-plant-ai/build_page.py           # writes power-plant-ai/index.html
python3 src/steel-ai-use-case-map/build_page.py    # writes steel-ai-use-case-map/index.html (content in use_cases.json)
python3 src/ai-closed-loop-soot-blowing/build_page.py   # writes ai-closed-loop-soot-blowing/index.html (content in content.json, screenshot in assets/)
python3 src/cement-ai-use-case-map/build_page.py   # writes cement-ai-use-case-map/index.html (content in use_cases.json)
python3 src/pulp-paper-ai-use-case-map/build_page.py  # writes pulp-paper-ai-use-case-map/index.html (content in use_cases.json)
python3 src/coal-mining-ai-use-case-map/build_page.py  # writes coal-mining-ai-use-case-map/index.html (content in content.json)
python3 src/aluminium-use-cases/build_page.py  # writes aluminium-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/copper-use-cases/build_page.py  # writes copper-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/pulp-fibre-use-cases/build_page.py  # writes pulp-fibre-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/refinery-petrochemicals-use-cases/build_page.py  # writes refinery-petrochemicals-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/chemicals-use-cases/build_page.py  # writes chemicals-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/agrochemicals-use-cases/build_page.py  # writes agrochemicals-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/solar-use-cases/build_page.py  # writes solar-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/bess-use-cases/build_page.py  # writes bess-use-cases/index.html (content in use_cases.json; shared builder src/shared/use_case_map.py)
python3 src/faclon-overview/build_page.py         # writes faclon-overview/index.html (content in content.json)
python3 src/steam-trap-monitoring/build_page.py   # writes steam-trap-monitoring/index.html (content in content.json, diagrams in diagrams.py)
python3 src/bus-bar-monitoring/build_page.py      # writes bus-bar-monitoring/index.html (content in content.json, photos in assets/)
python3 src/energy-management/build_page.py       # writes energy-management/index.html (content in content.json, screenshots in assets/)
python3 src/condition-based-monitoring/build_page.py  # writes condition-based-monitoring/index.html (content in content.json)
python3 src/it-ot-integration/build_page.py      # writes it-ot-integration/index.html (content in content.json, drawing in diagram.py)
python3 src/io-vision/build_page.py                 # writes io-vision/index.html (content in content.json, photos in assets/)
python3 src/readme/build_page.py                    # writes readme/index.html (the Read me guide)
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
- **Renaming a solution.** In the User Manager, **Rename** next to a solution changes the name shown on its landing-page card, in the browser tab, in every user's solution list and in downloads, then **Publish**. **Reset name** goes back to the page's own title. The heading inside the page itself is not changed; edit its build script for that.
- **Solution access switches.** In the User Manager, each solution has a global **Read** and **Download** switch. Read off: no user can open or download it (its key is removed from every keyring). Download off: users can view it, but its PDF key is withheld and download options are hidden. Admin always sees everything, with a label on switched-off cards. Note that a user who can view a page can still save it with their browser; Download off removes the built-in options.
- **User rights.** Per user, in the User Manager: **Can download** (off hides all download options and withholds PDF keys) and **Contributor**.
- **Design guide for contributors:** [`designskill.md`](designskill.md) gives the colours, type, layout, components, writing rules and a starter page, so uploaded pages match the site. It is linked from the Upload dialog and can be handed to an AI assistant as a skill.
- **Contributor uploads.** Contributors get an **Upload** button: they pick a self-contained HTML file, give a title and optional category, description and their name (shown as "Contributed by"). The page is encrypted in their browser and committed straight to `main`, so it is live in about a minute for admin, super users and contributors; the admin assigns it to other users like any solution. Uploaded pages run in a sandboxed frame, have no build script, and get their PDF the next time `protect.py` runs. Contributors publish with a GitHub token the admin sets once under **Contributor GitHub access**; anyone with contributor rights can use it, so give the right only to trusted people.
- **Downloads.** Every signed-in visitor gets a Download button: a PDF of the current page as one continuous page (no page breaks), or one offline HTML file containing the solutions they tick (from the ones shared with them). Downloaded files are not password-protected.
- How it works: each page is AES-encrypted with its own key, derived from the admin password. Each user's entry in `users.json` is a keyring holding only their pages' keys, locked with their own password. Removing a user or a solution takes effect on their next page load.
- Limits: this protects the published pages only. The sources in `src/` and the PDFs are readable by anyone with the link to this public repo or file. Someone who deliberately copied their page keys before being removed could still read those pages; to cut that off completely, change the admin password and recreate users.
- Every page carries `<meta name="robots" content="noindex">`, so it is reachable by link but not listed by search engines.
- The repository is public, so everything committed here (including customer names and figures) can be read by anyone. Keep internal-only material out of it.
- Indicative ₹ values are "up to, per 100 MW per year" and must be re-baselined against each plant's data.
