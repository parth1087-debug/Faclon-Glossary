# Repo conventions

This repo holds Faclon Labs customer-facing solution pages, published with GitHub Pages from `main` / root. The root `index.html` is a landing page listing every solution; each solution lives in its own folder (`/<solution>/`).

## Rules
- Generated files (`index.html`, `<solution>/index.html`, `<solution>/*.pdf`) are never hand-edited. Change the build scripts in `src/` and regenerate.
- The landing page is built by `src/home/build_home.py` from its `SOLUTIONS` list. When a solution page is added, set `live: True` for it there, rebuild, and add a row to the README table.
- Solution pages link back to the landing page with relative `../` links.
- Pages are self-contained HTML: inline CSS and SVG, with Google Fonts (Inter) as the only external dependency. They must work at phone width (~390px) with no horizontal scroll.
- Keep `<meta name="robots" content="noindex">` on every page unless asked otherwise.
- The repo is public. Do not commit internal pricing, deal data or anything marked confidential.
- The site is password-protected per user. After ANY build, and before committing, run `GLOSSARY_PASSWORD='<admin password>' python3 src/shared/protect.py` (ask Parth for the admin password; never commit it or write it into any file). Then run `python3 src/shared/protect.py --check`, which must pass: never push an unprotected `index.html`.
- `protect.py` encrypts each page with its own key, refreshes the solution list in `users.json` and builds `admin/index.html` (the User Manager) from `src/admin/index.html` + `src/shared/auth_core.js`. Edit those sources, never `admin/index.html`.
- `users.json` holds the user list and is written by the User Manager straight to `main`. Never edit or reorder its `users` array by hand. Always pull `main` right before running `protect.py`, and if `users.json` conflicts in a merge, keep `main`'s `users` array.
- `protect.py` also renders each changed solution page to one continuous PDF page (`src/shared/pagepdf.py`, Playwright + Chromium, Inter from `src/shared/fonts/`) and stores it encrypted as `<solution>/page-pdf.bin` for the in-page Download button. Never hand-edit those files.
- The signed-in bar and Download dialog (PDF of this page, or one offline HTML file of chosen solutions) come from `src/shared/page_tools.js`. Edit that source and re-run `protect.py`.
- Global Read/Download switches per solution live in `users.json` `policy` (set in the User Manager's Solution access panel). Read off removes that page's key from every keyring and the vault; Download off removes its PDF key (`HMAC(master, "pdf:"+slug)`) from keyrings and `dvault`. `protect.py` keeps `vault`/`dvault` in line with `policy`; ring-building logic exists in both `auth_core.js` (`buildRing`) and `protect.py` (`build_ring`) and must stay identical.
- Per-user rights (User Manager): **Can download** (off = no PDF key in the ring, no `da` for super users, Download button hidden) and **Contributor** (ring gets the contrib key `HMAC(master,"contrib")`).
- Contributor uploads: a contributor's browser commits `<slug>/index.html` (gate copied from an existing page, `D.up:1`, page key `HMAC(contrib key, "page:"+slug)`) and registers it in `users.json` (`solutions`, `uploads[slug].meta` encrypted card text, `vault[slug]` locked to the super-user ECDH key `spub`). Uploaded pages render in a sandboxed iframe. They have no build script in `src/`; `protect.py` adopts them as they are (re-wraps the gate, renders their PDF, converts the vault entry). Never delete or rewrite an uploaded page's folder unless Parth asks. Contributors publish with the token in `users.json` `contrib.tok` (encrypted with the contrib key).
- A new solution page is visible only to admin until Parth ticks it for users in the User Manager.
- Exception: super users ("Super user" switch in the User Manager) see every page, including new ones, through the `vault` in `users.json`. `protect.py` adds each new page to the vault; never edit it by hand.
- Do not change `src/shared/protect_salt.txt` or the admin password: either one changes every page key, which logs everyone out and means every user has to be recreated.

## Visual system (shared by all pages)
- Navy bands (`#0B1A30`) for hero and CTA; white body; `#F6F8FB` panels.
- Blue `#3D63F5` = insight, advisory and analytics. Green `#11875F` = control, closed loop and outcomes. Amber = in-progress or DMZ. Muted red = problems or constraints.
- Inter for all text; numbers in tabular figures; uppercase eyebrows with letter-spacing.

## Content rules
- Customer figures must come from approved sources: SPB (100+ RCAs/day, 98.4% accuracy, 20 TPD steam, ₹1 cr/yr), JSW Energy (1,000+ sensors, 15+ failures caught, ₹1.3 cr over 2 yrs), Hindustan Zinc (91 MW, 1 pp APC target), Grasim (175 MW, 5 boilers + 5 turbines), Tata Power Prayagraj. The Faclon Labs Presentation 2026 deck is also an approved source for every customer case it lists (used on /faclon-overview/). The Steam Trap Failure Detection deck is an approved source for its steam trap customer cases: HMEL, Cairn, Grasim, Jubilant Ingrevia (used on /steam-trap-monitoring/). The Condition Based Monitoring deck is an approved source for its vibration-monitoring case studies: JSW Energy, JSW Cements, JSW Steel, Godrej Agrovet, Grasim Pulp and Fibre, Apar Oil, SRF, Marico, DLF (used on /condition-based-monitoring/). The Vision Use Cases (I/O Vision) deck is an approved source for its customer deployments: JSW Energy (lignite particle size analysis), Hindustan Zinc (belt, tray and shuttle conveyor monitoring), Hindalco (200 cameras, 98% accuracy) (used on /io-vision/).
- Example agent conversations are illustrative and must stay labelled as such.
- ₹ values are "up to, per 100 MW per year" and are indicative.
- Platform names: Faclon AI platform, Ontology, I/O Connect (gateway, can sit in OT, DMZ or IT).
- Write in plain language for plant and business readers: describe what a controller or agent does logically, never as mathematical formulas.
