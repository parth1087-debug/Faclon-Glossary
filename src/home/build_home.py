"""Builds index.html, the landing page that lists every Faclon solution.

Run from anywhere:  python3 src/home/build_home.py
To add a solution or make one live, edit the SOLUTIONS list below and re-run.
A solution with "live": True becomes a clickable card linking to /<slug>/.
"""
import html
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))
from cta import CTA_BUTTONS  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "index.html"
E = html.escape

# ======================= SOLUTIONS =======================
# slug   : folder name, so the page lives at /<slug>/index.html
# accent : "blue" (insight, analytics) or "green" (control, outcomes)
# live   : True once /<slug>/index.html exists; False shows a "Coming soon" card
# links  : extra downloads shown on live cards, as (label, file inside the slug folder)
# cat    : landing-page group, an id from CATS. users.json "cats" (set at upload or in the User Manager)
#          overrides it on the live site; protect.py copies it there for pages that have none.
#          blurb is kept for reference but no longer shown on cards.
# Mirror of CATS in src/shared/auth_core.js and protect.py
CATS = [("core", "Core documents"), ("solution", "Solution documents"), ("maps", "Industry use case maps"),
        ("cases", "Case studies"), ("technical", "Technical documents"), ("others", "Others")]

SOLUTIONS = [
    {
        "slug": "faclon-overview",
        "cat": "core",
        "name": "Faclon Labs Overview",
        "sector": "Company",
        "accent": "blue",
        "live": True,
        "blurb": "Who we are, the AI-native stack, an example industrial AI architecture, 25+ use cases "
                 "and 37 customer cases across power, metals, process and manufacturing plants.",
        "tags": ["8-layer AI-native stack", "25+ use cases", "37 customer cases"],
        "links": [],
    },
    {
        "slug": "power-plant-ai",
        "cat": "solution",
        "name": "Power Plant AI",
        "sector": "Power",
        "accent": "green",
        "live": True,
        "blurb": "Advisory Agents and Automated Process Control for boilers, turbines and auxiliaries "
                 "in captive and utility power plants.",
        "tags": ["6 Advisory Agents", "8 APC applications", "CFBC · AFBC · PF"],
        "links": [],
    },
    {
        "slug": "ai-closed-loop-soot-blowing",
        "cat": "cases",
        "name": "AI Closed-Loop Soot Blowing",
        "sector": "Boilers · Pulp & paper",
        "accent": "green",
        "live": True,
        "blurb": "Zone-by-zone soot estimation and a constrained scheduler that blows only where it pays, "
                 "behind a 9-point safety gate. Paper mill case study: 30% less soot-blowing steam.",
        "tags": ["−28.8 t/day steam", "9-point safety gate", "Paper mill case study"],
        "links": [],
    },
    {
        "slug": "steel-ai-use-case-map",
        "cat": "maps",
        "name": "Steel AI Use Case Map",
        "sector": "Metals",
        "accent": "blue",
        "live": True,
        "blurb": "70 AI use cases across every section of a steel plant, from mining and iron making to "
                 "rolling, finishing and utilities, with indicative value per MTPA.",
        "tags": ["10 plant sections", "70 use cases", "28 Vision AI"],
        "links": [],
    },
    {
        "slug": "cement-ai-use-case-map",
        "cat": "maps",
        "name": "Cement AI Use Case Map",
        "sector": "Cement",
        "accent": "blue",
        "live": True,
        "blurb": "27 AI and IoT use cases across the cement value chain, from mines and crushing to pyro, "
                 "grinding, utilities and reliability, with indicative savings per MTPA.",
        "tags": ["9 plant areas", "27 use cases", "₹0.15–7 Cr / MTPA / yr"],
        "links": [],
    },
    {
        "slug": "pulp-paper-ai-use-case-map",
        "cat": "maps",
        "name": "Pulp & Paper AI Use Case Map",
        "sector": "Pulp & Paper",
        "accent": "blue",
        "live": True,
        "blurb": "40 deployable AI use cases across the integrated pulp & paper mill, from wood yard to winder, "
                 "with up to ₹204 cr per MTPA of value at stake.",
        "tags": ["10 process areas", "40 use cases", "11 Vision AI"],
        "links": [],
    },
    {
        "slug": "coal-mining-ai-use-case-map",
        "cat": "maps",
        "name": "Coal Mining AI Use Case Map",
        "sector": "Mining",
        "accent": "blue",
        "live": True,
        "blurb": "13 AI and IoT use cases across the coal mine, from haulage and washery to gas, safety and "
                 "environment, for opencast and underground operations, with indicative savings per MTPA.",
        "tags": ["7 domains", "13 use cases", "₹7.45 Cr / MTPA"],
        "links": [],
    },
    {
        "slug": "aluminium-use-cases",
        "cat": "maps",
        "name": "Aluminium Use Cases",
        "sector": "Metals",
        "accent": "blue",
        "live": True,
        "blurb": "62 AI use cases across the integrated aluminium plant, from bauxite and Bayer refining to potlines, casthouse, rolling and extrusion, with indicative value per MTPA.",
        "tags": ["8 plant sections", "62 use cases", "₹175.5 Cr / MTPA aluminium"],
        "links": [],
    },
    {
        "slug": "copper-use-cases",
        "cat": "maps",
        "name": "Copper Use Cases",
        "sector": "Metals",
        "accent": "blue",
        "live": True,
        "blurb": "46 AI use cases across the copper smelter and refinery, from concentrate blending and smelting to electrorefining, acid plant and rod mill, with indicative value per MTPA.",
        "tags": ["10 plant sections", "46 use cases", "₹183 Cr / MTPA copper"],
        "links": [],
    },
    {
        "slug": "pulp-fibre-use-cases",
        "cat": "maps",
        "name": "Pulp & Fibre Use Cases",
        "sector": "Pulp & Fibre",
        "accent": "blue",
        "live": True,
        "blurb": "47 AI use cases across dissolving pulp and viscose staple fibre, from wood yard to spinning, chemical recovery and utilities, with indicative value per MTPA.",
        "tags": ["10 process areas", "47 use cases", "₹152 Cr / MTPA fibre"],
        "links": [],
    },
    {
        "slug": "refinery-petrochemicals-use-cases",
        "cat": "maps",
        "name": "Refinery & Petrochemicals Use Cases",
        "sector": "Oil & Gas",
        "accent": "blue",
        "live": True,
        "blurb": "56 AI use cases across the refinery and petrochemical complex, from crude selection and distillation to FCC, hydrocracker, steam cracker and polymers, with indicative value per MMTPA.",
        "tags": ["13 process areas", "56 use cases", "₹229 Cr / MMTPA crude"],
        "links": [],
    },
    {
        "slug": "chemicals-use-cases",
        "cat": "maps",
        "name": "Chemicals Use Cases",
        "sector": "Chemicals",
        "accent": "blue",
        "live": True,
        "blurb": "28 AI use cases for batch and continuous chemical plants, from golden batch and reactor yield to distillation energy, solvent recovery, utilities, effluent and safety.",
        "tags": ["8 plant areas", "28 use cases", "Golden batch · solvent recovery"],
        "links": [],
    },
    {
        "slug": "agrochemicals-use-cases",
        "cat": "maps",
        "name": "Agrochemicals Use Cases",
        "sector": "Chemicals",
        "accent": "blue",
        "live": True,
        "blurb": "35 AI use cases for crop protection manufacturing, from technical synthesis and solvent recovery to SC, EC and granule formulation, small-pack filling, ZLD and campaign planning.",
        "tags": ["9 plant areas", "35 use cases", "Synthesis · formulation · packing"],
        "links": [],
    },
    {
        "slug": "solar-use-cases",
        "cat": "maps",
        "name": "Solar Use Cases",
        "sector": "Renewables",
        "accent": "blue",
        "live": True,
        "blurb": "10 AI use cases for utility-scale solar, from soiling and string losses to inverters, forecasting, the substation and site security, with indicative value per 100 MW.",
        "tags": ["6 plant areas", "10 use cases", "₹11.5 Cr / 100 MW / yr"],
        "links": [],
    },
    {
        "slug": "bess-use-cases",
        "cat": "maps",
        "name": "Battery Energy Storage Use Cases",
        "sector": "Renewables",
        "accent": "blue",
        "live": True,
        "blurb": "7 AI use cases for battery energy storage, from cell anomaly early warning and state of health to revenue-optimal dispatch, with indicative value per 100 MWh.",
        "tags": ["5 system areas", "7 use cases", "₹11.8 Cr / 100 MWh / yr"],
        "links": [],
    },
    {
        "slug": "bus-bar-monitoring",
        "cat": "solution",
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
        "slug": "condition-based-monitoring",
        "cat": "solution",
        "name": "Condition Based Monitoring",
        "sector": "All industries",
        "accent": "blue",
        "live": True,
        "blurb": "Wireless tri-axial vibration sensors and the I/O Sense platform catch faults in pumps, "
                 "motors, fans and gearboxes early, with automated diagnostics and recommended actions.",
        "tags": ["50+ faults detected", "Tri-axial vibration sensors", "9 customer deployments"],
        "links": [],
    },
    {
        "slug": "it-ot-integration",
        "cat": "technical",
        "name": "IT-OT Integration",
        "sector": "All industries",
        "accent": "blue",
        "live": True,
        "blurb": "A reference architecture for bringing plant data into the Faclon platforms safely: segmented "
                 "field networks, a two-firewall industrial DMZ with I/O Connect, and outbound-only upload to UDF.",
        "tags": ["Two-firewall IDMZ", "Read-only · outbound only", "IEC 62443 aligned"],
        "links": [],
    },
    {
        "slug": "io-vision",
        "cat": "solution",
        "name": "I/O Vision",
        "sector": "Computer vision",
        "accent": "blue",
        "live": True,
        "blurb": "Computer vision for safer, smarter plants: conveyor health, particle size, PPE and site "
                 "safety, vehicle tracking, surface defects and thermal monitoring, with real-time alerts.",
        "tags": ["21 use cases", "6 plant areas", "3 customer deployments"],
        "links": [],
    },
    {
        "slug": "metals-ai",
        "cat": "solution",
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
        "cat": "solution",
        "name": "Energy Management",
        "sector": "All industries",
        "accent": "blue",
        "live": True,
        "blurb": "Plant-wide energy monitoring on I/O Sense, from meters to dashboards, alerts, reports and "
                 "drill-downs from the main incomer to each machine feeder.",
        "tags": ["10 benefits", "Cloud or on-premise", "12 enterprise customers"],
        "links": [],
    },
    {
        "slug": "steam-trap-monitoring",
        "cat": "solution",
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
        "cat": "solution",
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
        "cat": "solution",
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
  <article class="card live {accent}" data-slug="{E(s['slug'])}" data-cat="{E(s['cat'])}">
    <a class="main" href="{E(s['slug'])}/">
      <div class="top"><span class="sec">{E(s['sector'])}</span><span class="pill on">Live</span></div>
      <h3>{E(s['name'])}</h3>
      {tags_html}
      <span class="open">Open solution →</span>
    </a>
    {f'<div class="extra">{extra}</div>' if extra else ''}
  </article>"""
    return f"""
  <article class="card soon {accent}" aria-disabled="true" data-slug="{E(s['slug'])}" data-cat="{E(s['cat'])}">
    <div class="main">
      <div class="top"><span class="sec">{E(s['sector'])}</span><span class="pill">Coming soon</span></div>
      <h3>{E(s['name'])}</h3>
      {tags_html}
    </div>
  </article>"""


live = [s for s in SOLUTIONS if s["live"]]
soon = [s for s in SOLUTIONS if not s["live"]]
# "Coming soon" cards are hidden for now; set SHOW_COMING_SOON = True to list them again.
SHOW_COMING_SOON = False
shown = live + (soon if SHOW_COMING_SOON else [])


def group(cid, label):
    inner = "".join(card(s) for s in shown if s["cat"] == cid)
    return f"""
  <section class="grp" data-cat="{cid}" data-label="{E(label)}">
    <h3 class="gh"><button type="button" aria-expanded="true"><span class="chev" aria-hidden="true"></span><span class="gl">{E(label)}</span><span class="n"></span></button></h3>
    <div class="grid">{inner}
    </div>
  </section>"""


groups = "".join(group(c, l) for c, l in CATS)

# Groups: expand/collapse each or all (all open on load), search by name, sector, tags or group.
# Cards hidden by access (style.display none, page_tools.js) or moved between groups are picked up
# by the observer, so empty groups disappear and counts stay right.
SCRIPT = r"""<script>
(function(){
  var box=document.getElementById('groups');if(!box)return;
  var groups=[].slice.call(box.querySelectorAll('.grp')),q=document.getElementById('q'),none=document.getElementById('none');
  var low=function(x){return String(x||'').toLowerCase()};
  function text(c){var o='';['h3','.sec','.tags','.fa-ver'].forEach(function(k){c.querySelectorAll(k).forEach(function(e){o+=' '+e.textContent})});return low(o)}
  function refresh(){
    var t=low(q&&q.value).trim(),total=0;
    groups.forEach(function(g){
      var n=0,lab=low(g.getAttribute('data-label'));
      g.querySelectorAll('article.card').forEach(function(c){
        var allowed=c.style.display!=='none',ok=allowed&&(!t||lab.indexOf(t)>=0||text(c).indexOf(t)>=0);
        c.classList.toggle('nomatch',allowed&&!ok);if(ok)n++;
      });
      g.hidden=!n;g.classList.toggle('searching',!!t);
      var e=g.querySelector('.n');if(e&&e.textContent!==String(n))e.textContent=n;total+=n;
    });
    if(none){none.hidden=!(t&&!total);var w=none.querySelector('b');if(w)w.textContent=q.value.trim()}
  }
  function setOpen(g,on){g.classList.toggle('closed',!on);g.querySelector('.gh button').setAttribute('aria-expanded',on?'true':'false')}
  groups.forEach(function(g){g.querySelector('.gh button').addEventListener('click',function(){setOpen(g,g.classList.contains('closed'))})});
  var ea=document.getElementById('ea'),ca=document.getElementById('ca');
  if(ea)ea.onclick=function(){groups.forEach(function(g){setOpen(g,true)})};
  if(ca)ca.onclick=function(){groups.forEach(function(g){setOpen(g,false)})};
  if(q){q.addEventListener('input',refresh);q.addEventListener('keydown',function(e){if(e.key==='Escape'){q.value='';refresh()}})}
  var pend=0;function soon(){if(pend)return;pend=1;(window.requestAnimationFrame||setTimeout)(function(){pend=0;refresh()})}
  if(window.MutationObserver)groups.forEach(function(g){new MutationObserver(soon).observe(g.querySelector('.grid'),{childList:true,subtree:true,attributes:true,attributeFilter:['style']})});
  /* moves a card to its group (used by the signed-in tools and the offline viewer) */
  window.faGroups={refresh:refresh,place:function(card,cat){var g=box.querySelector('.grp[data-cat="'+cat+'"]')||box.querySelector('.grp[data-cat="others"]');if(g&&card.parentNode!==g.querySelector('.grid'))g.querySelector('.grid').appendChild(card)}};
  refresh();
})();
</script>"""

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
body{{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}}
table{{font-variant-numeric:tabular-nums}}
.wrap{{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}}
h1,h2,h3{{letter-spacing:-.015em;line-height:1.2}}
.eyebrow{{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}}

.hero{{background:var(--navy);color:#fff;position:relative;overflow:hidden}}
.hero:before{{content:"";position:absolute;right:-180px;top:-220px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.3),rgba(124,149,255,0) 68%)}}
.hero .wrap{{position:relative;padding-top:34px;padding-bottom:56px}}
.brand{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC}}
.brand b{{color:#fff;letter-spacing:.22em}}
.hero h1{{font-size:clamp(34px,5.4vw,56px);font-weight:700;margin:72px 0 18px;max-width:800px;text-wrap:balance}}
.hero h1 em{{font-style:normal;color:var(--blue2)}}
.lede{{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:660px}}
.sectors{{display:flex;flex-wrap:wrap;gap:8px;margin-top:30px}}
.btn:hover,.btn:focus-visible{{filter:brightness(1.1)}}
.navlink{{color:#fff;text-decoration:none;letter-spacing:.12em;font-weight:600}}
.navlink:hover{{color:var(--blue2)}}
.menu{{display:flex;gap:22px;flex-wrap:wrap}}
#solutions{{scroll-margin-top:24px}}
.sectors span{{font-size:13px;color:#D5DEEE;border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:4px 12px}}

main .wrap{{padding-top:56px;padding-bottom:80px}}
h2{{font-size:32px;font-weight:700;margin:8px 0 10px}}
.sub{{color:var(--ink2);font-size:17px;max-width:640px;margin-bottom:32px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-flow:dense;gap:18px}}
.card{{border:1px solid var(--line);border-radius:16px;background:#fff;display:flex;flex-direction:column;overflow:hidden;position:relative}}
.card:before{{content:"";position:absolute;left:0;top:0;right:0;height:4px;background:var(--line)}}
.card.live.g:before{{background:var(--green)}} .card.live.b:before{{background:var(--blue)}}
.card .main{{display:flex;flex-direction:column;padding:22px 20px 18px;flex:1;color:inherit;text-decoration:none}}
.card.live{{grid-column:{"span 2" if SHOW_COMING_SOON else "auto"};transition:border-color .15s,box-shadow .15s}}
.card.live:hover,.card.live:focus-within{{border-color:#C9D3E3;box-shadow:0 10px 28px rgba(15,27,45,.08)}}
.card .main:focus-visible{{outline:2px solid var(--blue);outline-offset:-4px;border-radius:14px}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}}
.sec{{font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}}
.pill{{font-size:11.5px;font-weight:600;border-radius:20px;padding:3px 10px;background:var(--bg);color:var(--mute);white-space:nowrap}}
.pill.on{{background:var(--greenBg);color:var(--green)}}
.card.b .pill.on{{background:var(--blueBg);color:var(--blue)}}
.card h3{{font-size:21px;font-weight:700;margin-bottom:6px}}
.card.live h3{{font-size:22px}}
.card.soon h3{{color:var(--ink2)}}
.card.soon p{{color:var(--mute)}}
.tags{{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}}
.tags span{{font-size:12px;font-weight:600;border-radius:20px;padding:3px 10px;border:1px solid var(--line);color:var(--ink2)}}
.open{{margin-top:auto;padding-top:16px;font-weight:600;font-size:14.5px;color:var(--green)}}
.card.b .open{{color:var(--blue)}}
.extra{{border-top:1px solid var(--line);background:var(--bg);padding:12px 22px;display:flex;flex-wrap:wrap;gap:16px}}
.card.nomatch{{display:none}}
.tools{{position:sticky;top:0;z-index:3;background:#fff;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 0;margin-bottom:8px;border-bottom:1px solid var(--line)}}
.srch{{position:relative;flex:1 1 320px;max-width:460px}}
.srch svg{{position:absolute;left:13px;top:50%;width:18px;height:18px;transform:translateY(-50%);fill:none;stroke:var(--mute);stroke-width:2;stroke-linecap:round}}
.srch input{{width:100%;font:inherit;font-size:15px;padding:11px 14px 11px 40px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);outline:none}}
.srch input:focus{{border-color:var(--blue);background:#fff}}
.all{{display:flex;gap:8px}}
.all button{{font:inherit;font-size:13.5px;font-weight:600;color:var(--blue);background:var(--blueBg);border:0;border-radius:9px;padding:9px 13px;cursor:pointer;white-space:nowrap}}
.all button:hover,.all button:focus-visible{{filter:brightness(.97)}}
.none{{color:var(--ink2);font-size:15px;padding:28px 0}}
.grp{{margin-top:18px}}
.gh{{margin:0 0 12px;font-size:inherit}}
.gh button{{display:flex;align-items:center;gap:10px;width:100%;text-align:left;font:inherit;font-size:19px;font-weight:700;letter-spacing:-.01em;color:var(--ink);background:none;border:0;border-radius:8px;padding:10px 4px;cursor:pointer}}
.gh button:focus-visible{{outline:2px solid var(--blue);outline-offset:2px}}
.chev{{width:9px;height:9px;border-right:2px solid var(--mute);border-bottom:2px solid var(--mute);transform:rotate(45deg) translate(-2px,-2px);transition:transform .15s;flex:none}}
.grp.closed .chev{{transform:rotate(-45deg)}}
.n{{font-size:12.5px;font-weight:600;color:var(--mute);background:var(--bg);border-radius:20px;padding:2px 9px}}
.grp.closed:not(.searching) .grid{{display:none}}
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
  .grid{{grid-template-columns:1fr}} .card.live{{grid-column:auto}} .card.live h3{{font-size:20px}}
  .tools{{gap:8px}} .srch{{flex-basis:100%;max-width:none}} .gh button{{font-size:17px}}
  .hero h1{{margin-top:48px}} main .wrap{{padding-top:44px;padding-bottom:56px}} h2{{font-size:26px}}
}}
</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><b>Faclon Labs</b><nav class="menu"><a class="navlink" href="readme/">Read me</a><a class="navlink" href="faclon-overview/">About Faclon Labs →</a></nav></div>
  <h1>Industrial AI that turns plant data into <em>better operations</em></h1>
  <p class="lede">Solutions built on the Faclon AI platform for heavy industry: connecting plant systems, giving every team clear insight, and closing the loop on control.</p>
  <div class="sectors"><span>Cement</span><span>Metals</span><span>Power</span><span>Paper</span><span>Chemicals</span><span>Discrete manufacturing</span></div>
</div></header>

<main><div class="wrap">
  <div class="eyebrow" id="solutions">Solutions</div>
  <h2>Explore a solution</h2>
  <p class="sub">Each solution has its own page with the use cases, architecture and customer results.</p>
  <div class="tools" role="search">
    <div class="srch"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="Search solutions" aria-label="Search solutions" autocomplete="off"></div>
    <div class="all"><button type="button" id="ea">Expand all</button><button type="button" id="ca">Collapse all</button></div>
  </div>
  <p class="none" id="none" hidden>No solutions match “<b></b>”.</p>
  <div id="groups">{groups}
  </div>
</div></main>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Talk to us</div><h2>Start with your plant’s data</h2><p>Tell us which plant and which problem. We will show you which solution fits and what it can be worth.</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span>Faclon Labs</span><span>Industrial AI solutions</span></div></div>
{SCRIPT}
</body></html>"""

OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
