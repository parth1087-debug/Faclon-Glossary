# Repo conventions

This repo holds Faclon Labs customer-facing solution collateral, published with GitHub Pages from `main` / root.

## Rules
- Generated files (`<solution>/index.html`, `<solution>/*.pdf`) are never hand-edited. Change the build script in `src/<solution>/` and regenerate.
- Each solution lives in its own folder with an `index.html`, so its URL is `/<solution>/`. Add a card to the root `index.html` and a row to the README table whenever a solution is added.
- Pages are self-contained HTML: inline CSS and SVG, with Google Fonts (Inter) as the only external dependency. They must work at phone width (~390px) with no horizontal scroll.
- Keep `<meta name="robots" content="noindex">` on every page unless asked otherwise.
- The repo is public. Do not commit internal pricing, deal data or anything marked confidential.

## Visual system (shared by all pages)
- Navy bands (`#0B1A30`) for hero and CTA; white body; `#F6F8FB` panels.
- Blue `#3D63F5` = insight, advisory and analytics. Green `#11875F` = control, closed loop and outcomes. Amber = in-progress or DMZ. Muted red = problems or constraints.
- Inter for all text; numbers in tabular figures; uppercase eyebrows with letter-spacing.

## Content rules
- Customer figures must come from approved sources: SPB (100+ RCAs/day, 98.4% accuracy, 20 TPD steam, ₹1 cr/yr), JSW Energy (1,000+ sensors, 15+ failures caught, ₹1.3 cr over 2 yrs), Hindustan Zinc (91 MW, 1 pp APC target), Grasim (175 MW, 5 boilers + 5 turbines), Tata Power Prayagraj.
- Example agent conversations are illustrative and must stay labelled as such.
- ₹ values are "up to, per 100 MW per year" and are indicative.
- Platform names: Faclon AI platform, Ontology, I/O Connect (gateway, can sit in OT, DMZ or IT).
- Write in plain language for plant and business readers: describe what a controller or agent does logically, never as mathematical formulas.
