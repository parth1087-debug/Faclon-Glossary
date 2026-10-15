"""Builds steel-ai-use-case-map/index.html (AI use case map for the steel value chain).

Run from anywhere:  python3 src/steel-ai-use-case-map/build_page.py
Content lives in use_cases.json next to this script: sections -> processes -> use cases.
  s     : section name            area : true for the cross-cutting section (areas, not processes)
  n     : process / area name     f    : process steps     rm / ut / out / k : inputs, utilities, output, KPIs
  t     : use case title          v    : indicative value in ₹ cr per MTPA
  u     : "alloy" when the value is per MTPA alloy (default steel)
  cv    : 1 for Computer Vision   loc  : critical locations
  b     : [analyses, predicts, delivers]; null skips a line
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
OUT = ROOT / "steel-ai-use-case-map" / "index.html"
DATA = json.loads((HERE / "use_cases.json").read_text(encoding="utf-8"))
E = html.escape


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fmt_v(v):
    return f"₹{int(v) if float(v).is_integer() else v} cr"


def uc_card(u, p, s):
    labels = ["Analyses", "Predicts", "Delivers"]
    steps = "".join(
        f'<li><span>{labels[i]}</span><div>{E(x)}</div></li>' for i, x in enumerate(u["b"]) if x
    )
    locs = ""
    if u.get("loc"):
        locs = ('<div class="locs"><b>Critical locations · maximum impact</b><ul>'
                + "".join(f"<li>{E(l)}</li>" for l in u["loc"]) + "</ul></div>")
    search = " ".join([u["t"], *[x for x in u["b"] if x], *u.get("loc", []),
                       p["n"], p.get("k", ""), p.get("rm", ""), p.get("out", ""), s["s"]]).lower()
    cv = '<span class="cv">Computer Vision</span>' if u.get("cv") else ""
    return (f'<article class="card" data-v="{u["v"]}" data-cv="{1 if u.get("cv") else 0}" '
            f'data-q="{E(search)}"><div class="card-top"><div><h4>{E(u["t"])}</h4>{cv}</div>'
            f'<div class="val">{fmt_v(u["v"])}<small>/ MTPA {E(u.get("u", "steel"))}</small></div></div>'
            f'{locs}<ul class="steps">{steps}</ul></article>')


def process_block(p, s):
    flow = ""
    if p.get("f"):
        flow = '<div class="flow">' + "<i>→</i>".join(f"<b>{E(x)}</b>" for x in p["f"]) + "</div>"
    rows = [("RM", p.get("rm")), ("Utility", p.get("ut")), ("Output", p.get("out")), ("KPIs", p.get("k"))]
    io = "".join(
        f'<span class="tag{" kpi" if l == "KPIs" else ""}">{l}</span><span>{E(v)}</span>' for l, v in rows if v
    )
    io = f'<div class="io">{io}</div>' if io else ""
    cards = "".join(uc_card(u, p, s) for u in p["uc"])
    return (f'<div class="proc"><div class="proc-head"><div class="proc-top"><h3>{E(p["n"])}</h3>{flow}</div>'
            f'{io}</div><div class="cards">{cards}</div></div>')


sections_html, rail, options = [], [], []
n_proc = n_uc = n_cv = 0
for i, s in enumerate(DATA):
    total = sum(len(p["uc"]) for p in s["procs"])
    n_uc += total
    n_cv += sum(1 for p in s["procs"] for u in p["uc"] if u.get("cv"))
    n_proc += len(s["procs"])
    kind = "areas" if s.get("area") else ("processes" if len(s["procs"]) > 1 else "process")
    sid = slug(s["s"])
    sections_html.append(
        f'<section class="section" id="{sid}" data-total="{total}" data-meta="{len(s["procs"])} {kind}">'
        f'<div class="sec-head"><h2><em>{i + 1:02d}</em>{E(s["s"])}</h2>'
        f'<span class="meta">{len(s["procs"])} {kind} · {total} use cases</span></div>'
        + "".join(process_block(p, s) for p in s["procs"]) + "</section>")
    rail.append(f'<a href="#{sid}">{E(s["s"])}<i>{total}</i></a>')
    options.append(f'<option value="{sid}">{i + 1:02d}  {E(s["s"])}</option>')

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--red:#B5452F;color-scheme:light}
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
.hero .wrap{position:relative;padding-top:34px;padding-bottom:56px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hero h1{font-size:clamp(34px,5.2vw,56px);font-weight:700;margin:56px 0 18px;max-width:820px}
.hero h1 em{font-style:normal;color:var(--blue2)}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:700px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:36px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:28px;display:block}
.kp span{font-size:12.5px;color:#9FB0CC}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar .wrap{padding-top:12px;padding-bottom:12px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.search{flex:1 1 260px;position:relative;min-width:0}
.search input{width:100%;font:inherit;font-size:14.5px;padding:9px 12px 9px 34px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--mute)}
select{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);max-width:100%}
input:focus,select:focus,button:focus-visible,a:focus-visible{outline:2px solid var(--blue);outline-offset:1px}
.toggle{display:inline-flex;align-items:center;gap:8px;font:inherit;font-size:14px;padding:8px 12px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink2);cursor:pointer}
.toggle[aria-pressed="true"]{background:var(--blueBg);border-color:var(--blue);color:var(--blue)}
.count{font-size:13px;color:var(--mute);margin-left:auto}

.main{display:grid;grid-template-columns:200px minmax(0,1fr);gap:32px;padding-top:32px;padding-bottom:72px}
.rail{position:sticky;top:calc(env(safe-area-inset-top,0px) + 80px);align-self:start;display:flex;flex-direction:column;gap:2px}
.rail a{display:flex;justify-content:space-between;gap:8px;text-decoration:none;color:var(--ink2);font-size:14px;padding:6px 10px;border-radius:8px}
.rail a:hover{background:var(--bg);color:var(--ink)}
.rail a i{font-style:normal;font-size:12px;color:var(--mute)}
.rail a.dim{opacity:.35}

.section{margin-bottom:40px}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap;padding-bottom:12px;border-bottom:2px solid var(--ink)}
.sec-head h2{font-size:28px;font-weight:700}
.sec-head h2 em{font-style:normal;font-size:13px;font-weight:700;letter-spacing:.14em;color:var(--blue);margin-right:12px;vertical-align:middle}
.sec-head .meta{font-size:13px;color:var(--mute)}
.proc{margin-top:18px;border:1px solid var(--line);border-radius:16px;overflow:hidden}
.proc-head{background:var(--bg);padding:16px 20px;display:flex;flex-direction:column;gap:10px}
.proc-top{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline}
.proc-top h3{font-size:19px;font-weight:700}
.flow{display:flex;flex-wrap:wrap;gap:4px;align-items:center;font-size:13px;color:var(--ink2)}
.flow b{font-weight:500}
.flow i{font-style:normal;color:var(--blue)}
.io{display:grid;grid-template-columns:auto minmax(0,1fr);gap:6px 12px;font-size:13.5px;color:var(--ink2)}
.tag{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:2px 7px;border-radius:5px;background:#fff;border:1px solid var(--line);color:var(--mute);justify-self:start;align-self:start;margin-top:1px}
.tag.kpi{background:var(--greenBg);border-color:#CDE9DC;color:var(--green)}
.cards{padding:16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}
.card{border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:flex;flex-direction:column;gap:12px;min-width:0;background:#fff}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.card h4{font-size:16px;font-weight:700;line-height:1.3}
.cv{display:inline-block;font-size:11px;font-weight:600;color:var(--blue);background:var(--blueBg);border-radius:20px;padding:2px 9px;margin-top:6px}
.val{flex:none;text-align:right;line-height:1.1}
.val{font-size:18px;font-weight:700;color:var(--green);white-space:nowrap}
.val small{display:block;font-size:10.5px;font-weight:500;color:var(--mute);margin-top:2px}
.steps{display:flex;flex-direction:column;gap:7px;font-size:13.5px;color:var(--ink2)}
.steps li{display:grid;grid-template-columns:72px minmax(0,1fr);gap:8px;line-height:1.45}
.steps li span{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);padding-top:2px}
.steps li:last-child span{color:var(--blue)}
.steps li:last-child div{color:var(--ink)}
.locs{font-size:13px;background:var(--bg);border-radius:10px;padding:10px 12px}
.locs b{display:block;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:4px}
.locs li{color:var(--ink2);padding:2px 0 2px 14px;position:relative}
.locs li:before{content:"";position:absolute;left:0;top:10px;width:6px;height:2px;background:#C9B48F}
.empty{padding:40px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:16px}
.note{font-size:12.5px;color:var(--mute);font-style:italic;margin-top:-8px}

.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta h2{font-size:30px;margin:6px 0 8px}
.cta p{color:#C5D0E3;max-width:600px}
.btn{background:var(--blue);color:#fff;font-weight:600;padding:12px 22px;border-radius:10px;text-decoration:none;white-space:nowrap}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:900px){.main{grid-template-columns:1fr}.rail{display:none}.kpis{grid-template-columns:1fr 1fr}.count{margin-left:0;width:100%}}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  .hero h1{margin-top:40px}.cards{grid-template-columns:1fr;padding:12px}.sec-head h2{font-size:23px}
  .steps li{grid-template-columns:1fr;gap:0}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.bar,.rail{display:none}.main{grid-template-columns:1fr}.card,.proc-head{break-inside:avoid}}
"""

JS = """
(function(){
  var q=document.getElementById('q'),sec=document.getElementById('sec'),sort=document.getElementById('sort'),
      cvb=document.getElementById('cvOnly'),count=document.getElementById('count'),empty=document.getElementById('empty'),
      rail=document.querySelectorAll('.rail a'),cv=false,TOTAL=%d;
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
      s.querySelectorAll('.proc').forEach(function(p){
        var m=0;
        p.querySelectorAll('.card').forEach(function(c){
          var ok=inSec&&(!cv||c.dataset.cv==='1')&&(!term||c.dataset.q.indexOf(term)>-1);
          c.hidden=!ok;if(ok)m++;
        });
        p.hidden=!m;n+=m;
      });
      s.hidden=!n;shown+=n;
      var t=+s.dataset.total;
      s.querySelector('.meta').textContent=s.dataset.meta+' · '+(n===t?t:n+' of '+t)+' use cases';
      rail[i].querySelector('i').textContent=n;rail[i].classList.toggle('dim',!n);
    });
    count.textContent=shown===TOTAL?'Showing all '+TOTAL+' use cases':'Showing '+shown+' of '+TOTAL+' use cases';
    empty.hidden=!!shown;
  }
  q.addEventListener('input',apply);sort.addEventListener('change',apply);
  sec.addEventListener('change',function(){apply();window.scrollTo({top:document.querySelector('.bar').offsetTop})});
  cvb.addEventListener('click',function(){cv=!cv;cvb.setAttribute('aria-pressed',cv);apply()});
  apply();
})();
""" % n_uc

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Steel AI Use Case Map · Faclon Labs</title>
<meta name="description" content="{n_uc} AI use cases across the steel manufacturing value chain, from mining to finishing, with indicative value per MTPA.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>AI use case map · Steel manufacturing value chain</span></div>
  <a class="back" href="../">← All solutions</a>
  <h1>AI use cases for <em>every section</em> of a steel plant</h1>
  <p class="lede">Mapped across the steel value chain, from mine to finished coil. Each process shows its inputs, output and KPIs. Each use case shows what it analyses, what it predicts, and the advisory or detection it delivers, with indicative value per MTPA.</p>
  <div class="kpis">
    <div class="kp"><b>{len(DATA)}</b><span>Plant sections</span></div>
    <div class="kp"><b>{n_proc}</b><span>Unit processes &amp; areas</span></div>
    <div class="kp"><b>{n_uc}</b><span>AI use cases</span></div>
    <div class="kp"><b>{n_cv}</b><span>Computer Vision use cases</span></div>
  </div>
</div></header>

<div class="bar"><div class="wrap">
  <label class="search" for="q">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="Search use cases, KPIs, equipment, e.g. refractory, CSR, tramp metal" aria-label="Search use cases">
  </label>
  <select id="sec" aria-label="Plant section"><option value="">All sections</option>{"".join(options)}</select>
  <select id="sort" aria-label="Order"><option value="chain">Value chain order</option><option value="value">Highest value first</option></select>
  <button class="toggle" id="cvOnly" type="button" aria-pressed="false">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>
    Computer Vision only
  </button>
  <div class="count" id="count">Showing all {n_uc} use cases</div>
</div></div>

<div class="wrap main">
  <nav class="rail" aria-label="Sections">{"".join(rail)}</nav>
  <main>
    <p class="note">Values are indicative, in ₹ crore per MTPA of steel (per MTPA of alloy for ferro alloys), and are re-baselined against each plant’s data.</p>
    {"".join(sections_html)}
    <div class="empty" id="empty" hidden>No use cases match these filters. Try a broader term such as “refractory” or “belt”, or clear the filters.</div>
  </main>
</div>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">From use-case map to plant outcome</div><h2>Start with your plant’s data</h2><p>Faclon’s industrial AI operating layer connects, contextualises and acts on plant data across the steel value chain, turning this map into measurable gains in OEE, yield, energy efficiency and asset availability.</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Steel AI Use Case Map</span><span>Industrial AI operating layer for steel</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
