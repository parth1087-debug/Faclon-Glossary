"""Builds cement-ai-use-case-map/index.html (AI & IoT use-case catalogue for cement plants).

Run from anywhere:  python3 src/cement-ai-use-case-map/build_page.py
Content lives in use_cases.json next to this script: plant areas -> use cases.
  s   : plant area name
  t   : use case title
  k   : "ai" (AI advisory), "cv" (Vision AI), "iot" (IoT sensing) or "fd" (data platform)
  v   : [low, high] indicative savings in ₹ Cr per MTPA of cement per year; null when the source gives none
  d   : what it does              p : problems addressed
Edit the JSON and re-run; the page is regenerated in full.
"""
import html
import json
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))
from cta import CTA_BUTTONS  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "cement-ai-use-case-map" / "index.html"
DATA = json.loads((HERE / "use_cases.json").read_text(encoding="utf-8"))
E = html.escape

KIND = {"ai": "AI Advisory", "cv": "Vision AI", "iot": "IoT Sensing", "fd": "Platform"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def num(v):
    return f"{int(v) if float(v).is_integer() else v}"


def rng(v):
    return f"₹{num(v[0])}–{num(v[1])} Cr"


ALL = [u for s in DATA for u in s["uc"]]
VALS = [u["v"] for u in ALL if u["v"]]
LO, HI = min(v[0] for v in VALS), max(v[1] for v in VALS)
N_UC = len(ALL)
COUNTS = {k: sum(1 for u in ALL if u["k"] == k) for k in KIND}
assert (N_UC, len(DATA), LO, HI) == (27, 9, 0.15, 7), (N_UC, len(DATA), LO, HI)


def uc_card(u, s):
    does = "".join(f"<li>{E(x)}</li>" for x in u["d"])
    probs = "".join(f"<li>{E(x)}</li>" for x in u["p"])
    search = " ".join([u["t"], KIND[u["k"]], *u["d"], *u["p"], s["s"]]).lower()
    if u["v"]:
        a, b = (x / HI * 100 for x in u["v"])
        val = (f'<div class="val">{rng(u["v"])}<small>per MTPA · per year</small></div>')
        meter = (f'<div class="meter" aria-hidden="true"><span style="left:{a:.1f}%;width:{max(b - a, 1.5):.1f}%"></span></div>')
        hi = u["v"][1]
    else:
        val = '<div class="val fd">Platform<small>enables the other use cases</small></div>'
        meter, hi = "", 0
    return (f'<article class="card k-{u["k"]}" data-v="{hi}" data-k="{u["k"]}" data-q="{E(search)}">'
            f'<div class="card-top"><div><span class="kind">{KIND[u["k"]]}</span><h4>{E(u["t"])}</h4></div>{val}</div>'
            f'{meter}<div class="cols"><div class="does"><b>What it does</b><ul>{does}</ul></div>'
            f'<div class="probs"><b>Problem addressed</b><ul>{probs}</ul></div></div></article>')


sections, rail, options, chips = [], [], [], []
for i, s in enumerate(DATA):
    sid = slug(s["s"])
    n = len(s["uc"])
    label = f'{n} use case{"s" if n > 1 else ""}'
    sections.append(
        f'<section class="section" id="{sid}" data-total="{n}"><div class="sec-head">'
        f'<h2><em>{i + 1:02d}</em>{E(s["s"])}</h2><span class="meta" data-o="{label}">{label}</span></div>'
        f'<div class="cards">{"".join(uc_card(u, s) for u in s["uc"])}</div></section>')
    rail.append(f'<a href="#{sid}">{E(s["s"])}<i>{n}</i></a>')
    options.append(f'<option value="{sid}">{i + 1:02d}  {E(s["s"])}</option>')
    chips.append(f'<a href="#{sid}"><em>{i + 1:02d}</em>{E(s["s"])}<i>{n}</i></a>')

seg = '<button type="button" data-k="" aria-pressed="true">All</button>' + "".join(
    f'<button type="button" data-k="{k}" aria-pressed="false">{v}</button>' for k, v in KIND.items())

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FBF3E6;
--red:#B5452F;--violet:#7A4FD6;--violetBg:#F2EDFC;--teal:#0E7C8C;--tealBg:#E4F4F6;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:80px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
ul{list-style:none}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4{letter-spacing:-.015em;line-height:1.2;text-wrap:balance}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}

.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.32),rgba(124,149,255,0) 68%)}
.hero .wrap{position:relative;padding-top:34px;padding-bottom:48px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hero .eyebrow{color:var(--blue2);margin-top:48px}
.hero h1{font-size:clamp(32px,5vw,54px);font-weight:700;margin:12px 0 18px;max-width:860px}
.hero h1 em{font-style:normal;color:var(--blue2)}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:760px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:34px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:30px;display:block;line-height:1.2}
.kp span{font-size:12.5px;color:#9FB0CC}
.kp.hl b{color:#7FD9B3}
.areas{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.areas a{display:inline-flex;gap:8px;align-items:center;font-size:13.5px;color:#E4EAF5;text-decoration:none;padding:6px 12px;border-radius:20px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04)}
.areas a:hover{border-color:var(--blue2)}
.areas em{font-style:normal;font-size:11px;color:#8798B8}
.areas i{font-style:normal;font-size:12px;color:var(--blue2);font-weight:600}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar .wrap{padding-top:12px;padding-bottom:12px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.search{flex:1 1 220px;position:relative;min-width:0}
.search input{width:100%;font:inherit;font-size:14.5px;padding:9px 12px 9px 34px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--mute)}
select{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);max-width:100%}
input:focus,select:focus,button:focus-visible,a:focus-visible{outline:2px solid var(--blue);outline-offset:1px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden;max-width:100%}
.seg button{font:inherit;font-size:13.5px;padding:8px 11px;border:0;background:#fff;color:var(--ink2);cursor:pointer;border-right:1px solid var(--line);white-space:nowrap}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--blueBg);color:var(--blue);font-weight:600}
.count{font-size:13px;color:var(--mute);margin-left:auto}

.main{display:grid;grid-template-columns:190px minmax(0,1fr);gap:32px;padding-top:32px;padding-bottom:72px}
.rail{position:sticky;top:calc(env(safe-area-inset-top,0px) + 80px);align-self:start;display:flex;flex-direction:column;gap:2px}
.rail a{display:flex;justify-content:space-between;gap:8px;text-decoration:none;color:var(--ink2);font-size:14px;padding:6px 10px;border-radius:8px}
.rail a:hover{background:var(--bg);color:var(--ink)}
.rail a i{font-style:normal;font-size:12px;color:var(--mute)}
.rail a.dim{opacity:.35}
.note{font-size:12.5px;color:var(--mute);font-style:italic;margin-bottom:8px}

.section{margin-bottom:40px}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap;padding-bottom:12px;border-bottom:2px solid var(--ink);margin-bottom:16px}
.sec-head h2{font-size:28px;font-weight:700}
.sec-head h2 em{font-style:normal;font-size:13px;font-weight:700;letter-spacing:.14em;color:var(--blue);margin-right:12px;vertical-align:middle}
.sec-head .meta{font-size:13px;color:var(--mute)}
.cards{display:grid;grid-template-columns:1fr;gap:14px}
.card{border:1px solid var(--line);border-left:4px solid var(--blue);border-radius:14px;padding:18px 20px;display:flex;flex-direction:column;gap:12px;min-width:0;background:#fff}
.card.k-cv{border-left-color:var(--violet)}.card.k-iot{border-left-color:var(--teal)}.card.k-fd{border-left-color:var(--amber)}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}
.card h4{font-size:17.5px;font-weight:700;line-height:1.3;margin-top:6px}
.kind{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);background:var(--blueBg);border-radius:20px;padding:2px 9px}
.k-cv .kind{color:var(--violet);background:var(--violetBg)}.k-iot .kind{color:var(--teal);background:var(--tealBg)}.k-fd .kind{color:var(--amber);background:var(--amberBg)}
.val{flex:none;text-align:right;line-height:1.1;font-size:20px;font-weight:700;color:var(--green);white-space:nowrap}
.val small{display:block;font-size:10.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin-top:4px}
.val.fd{color:var(--amber);font-size:16px}
.meter{position:relative;height:6px;border-radius:4px;background:var(--bg)}
.meter span{position:absolute;top:0;height:100%;border-radius:4px;background:var(--green);opacity:.85}
.cols{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:22px}
.card b{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px}
.card li{position:relative;padding-left:15px;font-size:13.5px;line-height:1.5;margin-bottom:5px}
.does b{color:var(--blue)}.does li{color:var(--ink)}
.does li:before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--blue2)}
.probs b{color:var(--red)}.probs li{color:var(--ink2)}
.probs li:before{content:"";position:absolute;left:0;top:10px;width:7px;height:2px;background:#E0A898}
.empty{padding:40px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:16px}

.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta h2{font-size:30px;margin:6px 0 8px}
.cta p{color:#C5D0E3;max-width:640px}
.btn{background:var(--blue);color:#fff;font-weight:600;padding:12px 22px;border-radius:10px;text-decoration:none;white-space:nowrap}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:900px){.main{grid-template-columns:1fr}.rail{display:none}.kpis{grid-template-columns:1fr 1fr}.count{margin-left:0;width:100%}}
@media (max-width:720px){.cols{grid-template-columns:1fr;gap:12px}}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  .hero .eyebrow{margin-top:36px}.sec-head h2{font-size:23px}.card{padding:16px}
  .card-top{flex-direction:column;gap:6px}.val{text-align:left}
  .bar .wrap{gap:8px;padding-top:10px;padding-bottom:10px}.search{flex-basis:100%}.search input{padding-top:8px;padding-bottom:8px}
  #sec,#sort{flex:1 1 0;min-width:0;padding:7px 8px;font-size:13px}.count{display:none}
  .seg{width:100%}.seg button{flex:1;padding:7px 2px;font-size:12px}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.bar,.rail{display:none}.main{grid-template-columns:1fr}.card{break-inside:avoid}}
"""

JS = """
(function(){
  var q=document.getElementById('q'),sec=document.getElementById('sec'),sort=document.getElementById('sort'),
      count=document.getElementById('count'),empty=document.getElementById('empty'),
      rail=document.querySelectorAll('.rail a'),kb=document.querySelectorAll('#kind button'),kind='',TOTAL=%d;
  document.querySelectorAll('.cards').forEach(function(c){c._orig=[].slice.call(c.children)});
  function apply(){
    var term=q.value.trim().toLowerCase(),shown=0;
    document.querySelectorAll('.cards').forEach(function(c){
      var kids=c._orig.slice();
      if(sort.value==='value')kids.sort(function(a,b){return b.dataset.v-a.dataset.v});
      kids.forEach(function(k){c.appendChild(k)});
    });
    document.querySelectorAll('.section').forEach(function(s,i){
      var n=0,inSec=!sec.value||sec.value===s.id;
      s.querySelectorAll('.card').forEach(function(c){
        var ok=inSec&&(!kind||c.dataset.k===kind)&&(!term||c.dataset.q.indexOf(term)>-1);
        c.hidden=!ok;if(ok)n++;
      });
      s.hidden=!n;shown+=n;
      var t=+s.dataset.total,m=s.querySelector('.meta');
      m.textContent=n===t?m.dataset.o:n+' of '+t+' use cases';
      rail[i].querySelector('i').textContent=n;rail[i].classList.toggle('dim',!n);
    });
    count.textContent=shown===TOTAL?'Showing all '+TOTAL+' use cases':'Showing '+shown+' of '+TOTAL+' use cases';
    empty.hidden=!!shown;
  }
  q.addEventListener('input',apply);sort.addEventListener('change',apply);
  sec.addEventListener('change',function(){apply();window.scrollTo({top:document.querySelector('.bar').offsetTop})});
  kb.forEach(function(b){b.addEventListener('click',function(){
    kind=b.dataset.k;kb.forEach(function(x){x.setAttribute('aria-pressed',x===b)});apply();
  })});
  apply();
})();
""" % N_UC

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Cement AI Use Case Map · Faclon Labs</title>
<meta name="description" content="{N_UC} AI and IoT use cases across the cement value chain, from mines and crushing to pyroprocessing, grinding, utilities and reliability, with indicative savings per MTPA.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Solution catalogue · Cement manufacturing</span></div>
  <a class="back" href="../">← All solutions</a>
  <div class="eyebrow">Solution catalogue · Cement manufacturing</div>
  <h1>AI &amp; IoT use cases for <em>cement plants</em></h1>
  <p class="lede">A catalogue of AI and IoT use cases spanning the full cement value chain, from mines and crushing through pyroprocessing, grinding, utilities and plant-wide reliability. Each is mapped to the problem it solves and its indicative annual savings per MTPA of cement.</p>
  <div class="kpis">
    <div class="kp"><b>{N_UC}</b><span>Use cases</span></div>
    <div class="kp"><b>{len(DATA)}</b><span>Plant areas</span></div>
    <div class="kp"><b>{COUNTS["cv"]}</b><span>Vision AI use cases</span></div>
    <div class="kp hl"><b>₹{num(LO)}–{num(HI)} Cr</b><span>Savings / MTPA / yr, per use case</span></div>
  </div>
  <nav class="areas" aria-label="Plant areas">{"".join(chips)}</nav>
</div></header>

<div class="bar"><div class="wrap">
  <label class="search" for="q">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="Search use cases, e.g. SHC, free lime, belt, WHRS" aria-label="Search use cases">
  </label>
  <select id="sec" aria-label="Plant area"><option value="">All plant areas</option>{"".join(options)}</select>
  <select id="sort" aria-label="Order"><option value="chain">Value chain order</option><option value="value">Highest savings first</option></select>
  <div class="seg" id="kind" role="group" aria-label="Use-case type">{seg}</div>
  <div class="count" id="count">Showing all {N_UC} use cases</div>
</div></div>

<div class="wrap main">
  <nav class="rail" aria-label="Plant areas">{"".join(rail)}</nav>
  <main>
    <p class="note">Savings are indicative ranges in ₹ Cr per MTPA of cement per year. The green bar on each card shows its range on a common scale up to ₹{num(HI)} Cr.</p>
    {"".join(sections)}
    <div class="empty" id="empty" hidden>No use cases match these filters. Try a broader term such as “kiln” or “energy”, or clear the filters.</div>
  </main>
</div>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">From catalogue to plant outcome</div><h2>Start with your plant’s data</h2><p>Faclon’s industrial AI operating layer connects, contextualises and acts on plant data from mine to cement mill, turning these use cases into measurable savings in fuel, power, quality and uptime.</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Cement AI Use Case Map</span><span>Industrial AI for cement</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
