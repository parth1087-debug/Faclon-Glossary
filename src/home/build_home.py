"""Builds index.html, the landing page that lists every Faclon solution.

Run from anywhere:  python3 src/home/build_home.py
To add a solution or make one live, edit the SOLUTIONS list below and re-run.
A solution with "live": True becomes a clickable card linking to /<slug>/.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "index.html"
E = html.escape

# ======================= SOLUTIONS =======================
# slug   : folder name, so the page lives at /<slug>/index.html
# accent : "blue" (insight, analytics) or "green" (control, outcomes)
# live   : True once /<slug>/index.html exists; False shows a "Coming soon" card
# links  : extra downloads shown on live cards, as (label, file inside the slug folder)
SOLUTIONS = [
    {
        "slug": "faclon-overview",
        "name": "Faclon Labs Overview",
        "sector": "Company",
        "accent": "blue",
        "live": True,
        "blurb": "Who we are, the AI-native stack, an example industrial AI architecture, 25+ use cases "
                 "and 38 customer cases across power, metals, process and manufacturing plants.",
        "tags": ["8-layer AI-native stack", "25+ use cases", "38 customer cases"],
        "links": [],
    },
    {
        "slug": "power-plant-ai",
        "name": "Power Plant AI",
        "sector": "Power",
        "accent": "green",
        "live": True,
        "blurb": "Advisory Agents and Automated Process Control for boilers, turbines and auxiliaries "
                 "in captive and utility power plants.",
        "tags": ["7 Advisory Agents", "8 APC applications", "CFBC · AFBC · PF"],
        "links": [("Use-case catalogue (PDF)", "power-plant-ai-use-case-catalogue.pdf")],
    },
    {
        "slug": "steel-ai-use-case-map",
        "name": "Steel AI Use Case Map",
        "sector": "Metals",
        "accent": "blue",
        "live": True,
        "blurb": "70 AI use cases across every section of a steel plant, from mining and iron making to "
                 "rolling, finishing and utilities, with indicative value per MTPA.",
        "tags": ["10 plant sections", "70 use cases", "28 Computer Vision"],
        "links": [],
    },
    {
        "slug": "bus-bar-monitoring",
        "name": "Bus Bar Monitoring",
        "sector": "Electrical · All industries",
        "accent": "blue",
        "live": True,
        "blurb": "Wireless temperature straps on every critical bus-bar joint, with live alerts, trends "
                 "and reports to catch hot joints before they cause fires or trips.",
        "tags": ["Wireless sensor straps", "Live alerts & trends", "I/O Sense platform"],
        "links": [],
    },
    {
        "slug": "metals-ai",
        "name": "Metals AI",
        "sector": "Metals",
        "accent": "green",
        "live": False,
        "blurb": "Process intelligence and control for steel and metals plants, from kilns and furnaces "
                 "to quality and lab data.",
        "tags": [],
        "links": [],
    },
    {
        "slug": "energy-management",
        "name": "Energy Management",
        "sector": "All industries",
        "accent": "blue",
        "live": False,
        "blurb": "Plant-wide visibility of electricity, fuel, steam and utilities, with consumption tracked "
                 "against production.",
        "tags": [],
        "links": [],
    },
    {
        "slug": "steam-trap-monitoring",
        "name": "Steam Trap Failure Detection",
        "sector": "Process industries",
        "accent": "blue",
        "live": True,
        "blurb": "Wireless, temperature-based monitoring that catches leaking, flooding, choked and isolated "
                 "steam traps in real time, with ROI in under a year.",
        "tags": ["4 failure modes", "Zero cabling · Zone 1", "₹33.92 L / yr per 100 traps"],
        "links": [],
    },
    {
        "slug": "oee-monitoring",
        "name": "OEE Monitoring",
        "sector": "Manufacturing",
        "accent": "blue",
        "live": False,
        "blurb": "Availability, performance and quality tracked live for every machine and line, with "
                 "downtime reasons captured.",
        "tags": [],
        "links": [],
    },
    {
        "slug": "airports",
        "name": "Airports",
        "sector": "Infrastructure",
        "accent": "blue",
        "live": False,
        "blurb": "Connected monitoring of airport utilities and building systems in one view.",
        "tags": [],
        "links": [],
    },
]


def card(s):
    accent = "g" if s["accent"] == "green" else "b"
    tags = "".join(f"<span>{E(t)}</span>" for t in s["tags"])
    tags_html = f'<div class="tags">{tags}</div>' if tags else ""
    if s["live"]:
        extra = "".join(
            f'<a class="dl" href="{E(s["slug"])}/{E(f)}">{E(label)} ↓</a>' for label, f in s["links"]
        )
        return f"""
  <article class="card live {accent}">
    <a class="main" href="{E(s['slug'])}/">
      <div class="top"><span class="sec">{E(s['sector'])}</span><span class="pill on">Live</span></div>
      <h3>{E(s['name'])}</h3>
      <p>{E(s['blurb'])}</p>
      {tags_html}
      <span class="open">Open solution →</span>
    </a>
    {f'<div class="extra">{extra}</div>' if extra else ''}
  </article>"""
    return f"""
  <article class="card soon {accent}" aria-disabled="true">
    <div class="main">
      <div class="top"><span class="sec">{E(s['sector'])}</span><span class="pill">Coming soon</span></div>
      <h3>{E(s['name'])}</h3>
      <p>{E(s['blurb'])}</p>
      {tags_html}
    </div>
  </article>"""


live = [s for s in SOLUTIONS if s["live"]]
soon = [s for s in SOLUTIONS if not s["live"]]
# "Coming soon" cards are hidden for now; set SHOW_COMING_SOON = True to list them again.
SHOW_COMING_SOON = False
cards = "".join(card(s) for s in live + (soon if SHOW_COMING_SOON else []))

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Solutions · Faclon Labs</title>
<meta name="description" content="Faclon Labs industrial AI solutions for power, metals and manufacturing plants.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;color-scheme:light}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{background:#fff}}
body{{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}}
.wrap{{max-width:1080px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}}
h1,h2,h3{{letter-spacing:-.015em;line-height:1.2}}
.eyebrow{{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}}

.hero{{background:var(--navy);color:#fff;position:relative;overflow:hidden}}
.hero:before{{content:"";position:absolute;right:-180px;top:-220px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.3),rgba(124,149,255,0) 68%)}}
.hero .wrap{{position:relative;padding-top:34px;padding-bottom:64px}}
.brand{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC}}
.brand b{{color:#fff;letter-spacing:.22em}}
.hero h1{{font-size:clamp(34px,5.4vw,56px);font-weight:700;margin:72px 0 18px;max-width:800px;text-wrap:balance}}
.hero h1 em{{font-style:normal;color:var(--blue2)}}
.lede{{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:660px}}
.sectors{{display:flex;flex-wrap:wrap;gap:8px;margin-top:30px}}
.heroact{{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}}
.btn.ghost{{background:transparent;border:1px solid rgba(255,255,255,.3)}}
.btn:hover,.btn:focus-visible{{filter:brightness(1.1)}}
.navlink{{color:#fff;text-decoration:none;letter-spacing:.12em;font-weight:600}}
.navlink:hover{{color:var(--blue2)}}
#solutions{{scroll-margin-top:24px}}
.sectors span{{font-size:13px;color:#D5DEEE;border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:4px 12px}}

main .wrap{{padding-top:64px;padding-bottom:80px}}
h2{{font-size:32px;font-weight:700;margin:8px 0 10px}}
.sub{{color:var(--ink2);font-size:17px;max-width:640px;margin-bottom:32px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-flow:dense;gap:18px}}
.card{{border:1px solid var(--line);border-radius:16px;background:#fff;display:flex;flex-direction:column;overflow:hidden;position:relative}}
.card:before{{content:"";position:absolute;left:0;top:0;right:0;height:4px;background:var(--line)}}
.card.live.g:before{{background:var(--green)}} .card.live.b:before{{background:var(--blue)}}
.card .main{{display:flex;flex-direction:column;padding:24px 22px 22px;flex:1;color:inherit;text-decoration:none}}
.card.live{{grid-column:{"span 2" if SHOW_COMING_SOON else "auto"};transition:border-color .15s,box-shadow .15s}}
.card.live:hover,.card.live:focus-within{{border-color:#C9D3E3;box-shadow:0 10px 28px rgba(15,27,45,.08)}}
.card .main:focus-visible{{outline:2px solid var(--blue);outline-offset:-4px;border-radius:14px}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}}
.sec{{font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}}
.pill{{font-size:11.5px;font-weight:600;border-radius:20px;padding:3px 10px;background:var(--bg);color:var(--mute);white-space:nowrap}}
.pill.on{{background:var(--greenBg);color:var(--green)}}
.card.b .pill.on{{background:var(--blueBg);color:var(--blue)}}
.card h3{{font-size:21px;font-weight:700;margin-bottom:6px}}
.card.live h3{{font-size:28px}}
.card p{{color:var(--ink2);font-size:14.5px;max-width:560px}}
.card.soon h3{{color:var(--ink2)}}
.card.soon p{{color:var(--mute)}}
.tags{{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}}
.tags span{{font-size:12px;font-weight:600;border-radius:20px;padding:3px 10px;border:1px solid var(--line);color:var(--ink2)}}
.open{{margin-top:auto;padding-top:20px;font-weight:600;font-size:14.5px;color:var(--green)}}
.card.b .open{{color:var(--blue)}}
.extra{{border-top:1px solid var(--line);background:var(--bg);padding:12px 22px;display:flex;flex-wrap:wrap;gap:16px}}
.dl{{font-size:13.5px;font-weight:600;color:var(--ink2);text-decoration:none}}
.dl:hover,.dl:focus-visible{{color:var(--blue)}}

.cta{{background:var(--navy);color:#fff}}
.cta .wrap{{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;padding-top:48px;padding-bottom:48px}}
.cta h2{{font-size:26px;margin:6px 0 6px}}
.cta p{{color:#C5D0E3;max-width:560px}}
.btn{{display:inline-block;background:var(--blue);color:#fff;text-decoration:none;font-weight:600;border-radius:10px;padding:12px 20px;white-space:nowrap}}
.foot{{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}}
.foot .wrap{{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}}

@media (max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}}}
@media (max-width:640px){{
  .wrap{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
  .grid{{grid-template-columns:1fr}} .card.live{{grid-column:auto}} .card.live h3{{font-size:24px}}
  .hero h1{{margin-top:48px}} main .wrap{{padding-top:44px;padding-bottom:56px}} h2{{font-size:26px}}
}}
</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><b>Faclon Labs</b><a class="navlink" href="faclon-overview/">About Faclon Labs →</a></div>
  <h1>Industrial AI that turns plant data into <em>better operations</em></h1>
  <p class="lede">Solutions built on the Faclon AI platform for heavy industry: connecting plant systems, giving every team clear insight, and closing the loop on control.</p>
  <div class="sectors"><span>Cement</span><span>Metals</span><span>Power</span><span>Paper</span><span>Chemicals</span><span>Discrete manufacturing</span></div>
  <div class="heroact"><a class="btn" href="faclon-overview/">Open Faclon Labs Overview →</a><a class="btn ghost" href="#solutions">Explore solutions ↓</a></div>
</div></header>

<main><div class="wrap">
  <div class="eyebrow" id="solutions">Solutions</div>
  <h2>Explore a solution</h2>
  <p class="sub">Each solution has its own page with the use cases, architecture and customer results.</p>
  <div class="grid">{cards}
  </div>
</div></main>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Talk to us</div><h2>Start with your plant’s data</h2><p>Tell us which plant and which problem. We will show you which solution fits and what it can be worth.</p></div>
  <a class="btn" href="https://www.faclonlabs.com">www.faclonlabs.com</a>
</div></div>
<div class="foot"><div class="wrap"><span>Faclon Labs</span><span>Industrial AI solutions</span></div></div>
</body></html>"""

OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
