# Repo conventions

This repo holds Faclon Labs customer-facing solution pages, published with GitHub Pages from `main` / root. The root `index.html` is a landing page listing every solution; each solution lives in its own folder (`/<solution>/`).

## Rules
- Generated files (`index.html`, `<solution>/index.html`, `<solution>/*.pdf`) are never hand-edited. Change the build scripts in `src/` and regenerate.
- The landing page is built by `src/home/build_home.py` from its `SOLUTIONS` list. When a solution page is added, set `live: True` for it there, rebuild, and add a row to the README table.
- Solution pages link back to the landing page with relative `../` links.
- Pages are self-contained HTML: inline CSS and SVG, with Google Fonts (Inter) as the only external dependency. They must work at phone width (~390px) with no horizontal scroll.
- Keep `<meta name="robots" content="noindex">` on every page unless asked otherwise.
- The repo is public. Do not commit internal pricing, deal data or anything marked confidential.
- The site is password-protected. After ANY build, and before committing, run `GLOSSARY_PASSWORD='<password>' python3 src/shared/protect.py` (ask Parth for the password; never commit it or write it into any file). Then run `python3 src/shared/protect.py --check`, which must pass: never push an unprotected `index.html`. Do not change `src/shared/protect_salt.txt`, or everyone's saved login stops working.

## Visual system (shared by all pages)
- Navy bands (`#0B1A30`) for hero and CTA; white body; `#F6F8FB` panels.
- Blue `#3D63F5` = insight, advisory and analytics. Green `#11875F` = control, closed loop and outcomes. Amber = in-progress or DMZ. Muted red = problems or constraints.
- Inter for all text; numbers in tabular figures; uppercase eyebrows with letter-spacing.

## Content rules
- Customer figures must come from approved sources: SPB (100+ RCAs/day, 98.4% accuracy, 20 TPD steam, ₹1 cr/yr), JSW Energy (1,000+ sensors, 15+ failures caught, ₹1.3 cr over 2 yrs), Hindustan Zinc (91 MW, 1 pp APC target), Grasim (175 MW, 5 boilers + 5 turbines), Tata Power Prayagraj. The Faclon Labs Presentation 2026 deck is also an approved source for every customer case it lists (used on /faclon-overview/). The Steam Trap Failure Detection deck is an approved source for its steam trap customer cases: HMEL, Cairn, Grasim, Jubilant Ingrevia (used on /steam-trap-monitoring/). The Condition Based Monitoring deck is an approved source for its vibration-monitoring case studies: JSW Energy, JSW Cements, JSW Steel, Godrej Agrovet, Grasim Pulp and Fibre, Apar Oil, SRF, Marico, DLF (used on /condition-based-monitoring/).
- Example agent conversations are illustrative and must stay labelled as such.
- ₹ values are "up to, per 100 MW per year" and are indicative.
- Platform names: Faclon AI platform, Ontology, I/O Connect (gateway, can sit in OT, DMZ or IT).
- Write in plain language for plant and business readers: describe what a controller or agent does logically, never as mathematical formulas.
