"""Builds pulp-paper-ai-use-case-map/index.html (AI use-case catalog for an integrated pulp & paper mill).

Run from anywhere:  python3 src/pulp-paper-ai-use-case-map/build_page.py
Content lives in use_cases.json next to this script: process areas -> process units -> use cases.
  s     : process area name       area : true when units have no process flow / inputs (Utilities, Cross-Cutting)
  n     : process unit name       f    : process flow steps
  rm / ut / out / q : raw material / input, utility input, output, quality parameters
  t     : use case title          k    : "ai" (AI Advisory), "cv" (Vision AI) or "fd" (Foundation)
  v     : indicative value, up to ₹ cr per MTPA of paper; null for the foundation layer
  loc   : critical locations (maximum impact)      locLabel : heading for loc (default "Critical locations")
  d     : what Faclon does        p    : problems addressed        kpi : KPIs tracked
Edit the JSON and re-run; the page is regenerated in full.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "pulp-paper-ai-use-case-map" / "index.html"
DATA = json.loads((HERE / "use_cases.json").read_text(encoding="utf-8"))
E = html.escape

KIND = {"ai": ("AI Advisory", "soft sensors, optimization, setpoint advisory"),
        "cv": ("Vision AI", "camera-based detection & condition monitoring"),
        "fd": ("Foundation", "IT-OT data layer enabling everything else")}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def num(v):
    return f"{int(v) if float(v).is_integer() else v}"


def uc_card(u, p, s):
    locs = ""
    if u.get("loc"):
        locs = (f'<div class="locs"><b>{E(u.get("locLabel", "Critical locations"))} · maximum impact</b><ul>'
                + "".join(f"<li>{E(l)}</li>" for l in u["loc"]) + "</ul></div>")
    does = "".join(f"<li>{E(x)}</li>" for x in u["d"])
    probs = "".join(f"<li>{E(x)}</li>" for x in u["p"])
    kpis = "".join(f"<li>{E(x)}</li>" for x in u["kpi"])
    search = " ".join([u["t"], KIND[u["k"]][0], *u["d"], *u["p"], *u["kpi"], *u.get("loc", []),
                       p["n"], p.get("q", ""), p.get("rm", ""), p.get("out", ""), s["s"]]).lower()
    if u["v"] is None:
        val = '<div class="val fd">Platform<small>layer</small></div>'
    else:
        val = f'<div class="val">₹{num(u["v"])} cr<small>up to / MTPA</small></div>'
    return (f'<article class="card k-{u["k"]}" data-v="{u["v"] or 0}" data-k="{u["k"]}" data-q="{E(search)}">'
            f'<div class="card-top"><div><span class="kind">{KIND[u["k"]][0]}</span><h4>{E(u["t"])}</h4></div>{val}</div>'
            f'{locs}<div class="does"><b>What Faclon does</b><ul>{does}</ul></div>'
            f'<div class="pk"><div class="probs"><b>Problems addressed</b><ul>{probs}</ul></div>'
            f'<div class="kpil"><b>KPIs tracked</b><ul>{kpis}</ul></div></div></article>')


def process_block(p, s):
    flow = ""
    if p.get("f"):
        flow = '<div class="flow">' + "<i>→</i>".join(f"<b>{E(x)}</b>" for x in p["f"]) + "</div>"
    rows = [("Input", p.get("rm")), ("Utility", p.get("ut")), ("Output", p.get("out")), ("Quality", p.get("q"))]
    io = "".join(
        f'<span class="tag{" qp" if l == "Quality" else ""}">{l}</span><span>{E(v)}</span>' for l, v in rows if v
    )
    io = f'<div class="io">{io}</div>' if io else ""
    cards = "".join(uc_card(u, p, s) for u in p["uc"])
    return (f'<div class="proc"><div class="proc-head"><div class="proc-top"><h3>{E(p["n"])}</h3>{flow}</div>'
            f'{io}</div><div class="cards">{cards}</div></div>')


sections_html, rail, options, bars = [], [], [], []
n_proc = n_uc = 0
kinds = {"ai": 0, "cv": 0, "fd": 0}
area_vals = []
for s in DATA:
    s["_v"] = sum(u["v"] or 0 for p in s["procs"] for u in p["uc"])
    area_vals.append(s["_v"])
grand = sum(area_vals)
vmax = max(area_vals)
for i, s in enumerate(DATA):
    total = sum(len(p["uc"]) for p in s["procs"])
    n_uc += total
    n_proc += len(s["procs"])
    for p in s["procs"]:
        for u in p["uc"]:
            kinds[u["k"]] += 1
    units = f'{len(s["procs"])} unit{"s" if len(s["procs"]) > 1 else ""}'
    sid = slug(s["s"])
    sections_html.append(
        f'<section class="section" id="{sid}" data-total="{total}" data-meta="{units}">'
        f'<div class="sec-head"><h2><em>{i + 1:02d}</em>{E(s["s"])}</h2>'
        f'<span class="meta">{units} · {total} use cases · up to ₹{num(s["_v"])} cr / MTPA</span></div>'
        + "".join(process_block(p, s) for p in s["procs"]) + "</section>")
    rail.append(f'<a href="#{sid}">{E(s["s"])}<i>{total}</i></a>')
    options.append(f'<option value="{sid}">{i + 1:02d}  {E(s["s"])}</option>')
    bars.append(f'<a class="brow" href="#{sid}"><span class="bn"><em>{i + 1:02d}</em>{E(s["s"])}</span>'
                f'<span class="bt"><span class="bf" style="width:{s["_v"] / vmax * 100:.1f}%"></span></span>'
                f'<span class="bv">₹{num(s["_v"])}<small> cr</small></span><span class="bc">{total} use case{"s" if total > 1 else ""}</span></a>')

assert (n_uc, n_proc, len(DATA), grand) == (40, 21, 10, 204), (n_uc, n_proc, len(DATA), grand)

mix = "".join(
    f'<div class="mix-i k-{k}"><b>{kinds[k]}</b><span><strong>{KIND[k][0]}</strong> {E(KIND[k][1])}</span></div>'
    for k in ("ai", "cv", "fd"))

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FBF3E6;
--red:#B5452F;--redBg:#FBEFEC;--violet:#7A4FD6;--violetBg:#F2EDFC;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:80px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
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
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:740px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:34px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:30px;display:block;line-height:1.2}
.kp b small{font-size:15px;font-weight:600;margin-left:2px}
.kp span{font-size:12.5px;color:#9FB0CC}
.kp.hl{background:var(--blue)}
.kp.hl span{color:#DCE3FF}
.kfoot{font-size:12.5px;color:#9FB0CC;margin-top:10px}
.proof{margin-top:22px;display:flex;flex-wrap:wrap;gap:8px 22px;align-items:center;font-size:14px;color:#E4EAF5;padding:14px 18px;border-radius:12px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08)}
.proof b{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue2);font-weight:700}
.proof span{font-weight:600}

.ov{padding-top:56px;padding-bottom:12px}
.ov h2{font-size:28px;margin:6px 0 20px}
.cca{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cca div{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.cca em{font-style:normal;font-size:11.5px;font-weight:700;letter-spacing:.14em;color:var(--blue)}
.cca h3{font-size:18px;margin:6px 0 8px}
.cca p{font-size:14px;color:var(--ink2)}
.ov-grid{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:28px;margin-top:34px}
.ov-grid h3{font-size:19px;margin-bottom:12px}
.chart{border:1px solid var(--line);border-radius:14px;padding:8px 6px}
.brow{display:grid;grid-template-columns:170px minmax(0,1fr) 68px 92px;gap:12px;align-items:center;padding:7px 12px;border-radius:8px;text-decoration:none;color:var(--ink)}
.brow:hover{background:var(--bg)}
.bn{font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bn em{font-style:normal;font-size:11px;color:var(--mute);margin-right:8px;font-weight:600}
.bt{height:10px;background:var(--bg);border-radius:6px;overflow:hidden}
.bf{display:block;height:100%;background:var(--green);border-radius:6px}
.bv{text-align:right;font-weight:700;color:var(--green)}
.bv small{font-weight:500;font-size:11px}
.bc{font-size:12px;color:var(--mute);text-align:right}
.btot{display:flex;justify-content:space-between;margin:6px 6px 2px;padding:12px;border-radius:10px;background:var(--navy);color:#fff;font-weight:700}
.btot span:last-child{color:#7FD8B2}
.mix{display:flex;flex-direction:column;gap:10px}
.mix-i{display:flex;gap:16px;align-items:center;border:1px solid var(--line);border-radius:14px;padding:14px 18px}
.mix-i b{font-size:34px;line-height:1;min-width:46px;color:var(--blue)}
.mix-i.k-cv b{color:var(--violet)}.mix-i.k-fd b{color:var(--amber)}
.mix-i span{font-size:14px;color:var(--ink2)}
.mix-i strong{color:var(--ink)}
.howto{margin-top:10px;background:var(--bg);border-radius:14px;padding:14px 18px;font-size:13.5px;color:var(--ink2)}
.howto b{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--blue);margin-bottom:4px}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);margin-top:40px;border-top:1px solid var(--line)}
.bar .wrap{padding-top:12px;padding-bottom:12px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.search{flex:1 1 240px;position:relative;min-width:0}
.search input{width:100%;font:inherit;font-size:14.5px;padding:9px 12px 9px 34px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--mute)}
select{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);max-width:100%}
input:focus,select:focus,button:focus-visible,a:focus-visible{outline:2px solid var(--blue);outline-offset:1px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden;max-width:100%}
.seg button{font:inherit;font-size:13.5px;padding:8px 12px;border:0;background:#fff;color:var(--ink2);cursor:pointer;border-right:1px solid var(--line);white-space:nowrap}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--blueBg);color:var(--blue);font-weight:600}
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
.tag.qp{background:var(--blueBg);border-color:#D6DEFF;color:var(--blue)}
.cards{padding:16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}
.card{border:1px solid var(--line);border-top:3px solid var(--blue);border-radius:14px;padding:16px 18px;display:flex;flex-direction:column;gap:14px;min-width:0;background:#fff}
.card.k-cv{border-top-color:var(--violet)}.card.k-fd{border-top-color:var(--amber)}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.card h4{font-size:16px;font-weight:700;line-height:1.3;margin-top:6px}
.kind{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);background:var(--blueBg);border-radius:20px;padding:2px 9px}
.k-cv .kind{color:var(--violet);background:var(--violetBg)}.k-fd .kind{color:var(--amber);background:var(--amberBg)}
.val{flex:none;text-align:right;line-height:1.1;font-size:19px;font-weight:700;color:var(--green);white-space:nowrap}
.val small{display:block;font-size:10.5px;font-weight:500;color:var(--mute);margin-top:3px}
.val.fd{color:var(--amber);font-size:15px}
.card b{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin-bottom:5px}
.card li{position:relative;padding-left:14px;font-size:13.5px;color:var(--ink2);line-height:1.45;margin-bottom:4px}
.card li:before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:#C3CCDA}
.does b{color:var(--blue)}.does li{color:var(--ink)}.does li:before{background:var(--blue2)}
.pk{display:grid;grid-template-columns:1fr 1fr;gap:12px;border-top:1px solid var(--line);padding-top:12px}
.probs b{color:var(--red)}.probs li:before{background:#E0A898;border-radius:1px;width:6px;height:2px;top:9px}
.kpil b{color:var(--green)}.kpil li:before{background:#8FD0B4}
.pk li{font-size:12.5px}
.locs{background:var(--amberBg);border-radius:10px;padding:10px 12px}
.locs b{color:var(--amber)}
.locs li{font-size:13px}.locs li:before{background:#D9B47A;border-radius:1px;height:2px;top:9px}
.empty{padding:40px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:16px}
.note{font-size:12.5px;color:var(--mute);font-style:italic;margin-top:-8px}

.cta{background:var(--navy);color:#fff}
.cta .wrap{padding-top:56px;padding-bottom:56px}
.cta h2{font-size:32px;margin:6px 0 10px}
.cta h2 em{font-style:normal;color:var(--blue2)}
.cta p{color:#C5D0E3;max-width:720px}
.steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:28px}
.steps3 div{border:1px solid rgba(255,255,255,.12);background:var(--navy2);border-radius:14px;padding:18px 20px}
.steps3 em{font-style:normal;font-size:26px;font-weight:700;color:var(--blue2)}
.steps3 h3{font-size:17px;margin:4px 0 4px}
.steps3 p{font-size:14px}
.cta-row{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;margin-top:28px}
.btn{background:var(--blue);color:#fff;font-weight:600;padding:12px 22px;border-radius:10px;text-decoration:none;white-space:nowrap}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:980px){.ov-grid{grid-template-columns:1fr}}
@media (max-width:900px){.main{grid-template-columns:1fr}.rail{display:none}.kpis{grid-template-columns:1fr 1fr}.count{margin-left:0;width:100%}.cca,.steps3{grid-template-columns:1fr}}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  .hero .eyebrow{margin-top:36px}.cards{grid-template-columns:1fr;padding:12px}.sec-head h2{font-size:23px}
  .brow{grid-template-columns:minmax(0,1fr) 62px;row-gap:4px}.bt{grid-column:1/-1;grid-row:2}.bc{display:none}
  .pk{grid-template-columns:1fr}.seg{width:100%}.seg button{flex:1;padding:7px 4px;font-size:12.5px}
  .bar .wrap{gap:8px;padding-top:10px;padding-bottom:10px}.search{flex-basis:100%}.search input{padding-top:8px;padding-bottom:8px}
  #sec,#sort{flex:1 1 0;min-width:0;padding:7px 8px;font-size:13px}.count{display:none}
  .proc-head{padding:14px 14px}.io{grid-template-columns:1fr;gap:2px}.io span:not(.tag){margin-bottom:6px}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.bar,.rail{display:none}.main{grid-template-columns:1fr}.card,.proc-head{break-inside:avoid}}
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
      s.querySelectorAll('.proc').forEach(function(p){
        var m=0;
        p.querySelectorAll('.card').forEach(function(c){
          var ok=inSec&&(!kind||c.dataset.k===kind)&&(!term||c.dataset.q.indexOf(term)>-1);
          c.hidden=!ok;if(ok)m++;
        });
        p.hidden=!m;n+=m;
      });
      s.hidden=!n;shown+=n;
      var t=+s.dataset.total,meta=s.querySelector('.meta');
      if(!meta._o)meta._o=meta.textContent;
      meta.textContent=n===t?meta._o:s.dataset.meta+' · '+n+' of '+t+' use cases';
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
""" % n_uc

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Pulp &amp; Paper AI Use Case Map · Faclon Labs</title>
<meta name="description" content="{n_uc} deployable AI use cases across the integrated pulp &amp; paper mill, from wood yard to winder, with indicative value per MTPA of paper.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Industrial AI · Operating layer for plant autonomy</span></div>
  <a class="back" href="../">← All solutions</a>
  <div class="eyebrow">Industry brief · Pulp &amp; paper manufacturing</div>
  <h1>An AI use-case catalog for the <em>integrated pulp &amp; paper mill</em></h1>
  <p class="lede">Forty deployable AI use cases mapped across the full mill, wood yard to winder, plus chemical recovery, utilities and cross-cutting reliability. Each one turns disconnected plant data into continuous intelligence and action, with the value at stake quantified per million tonnes of annual paper capacity.</p>
  <div class="kpis">
    <div class="kp"><b>{n_uc}</b><span>Deployable AI use cases</span></div>
    <div class="kp"><b>{len(DATA)}</b><span>Process areas, end to end</span></div>
    <div class="kp"><b>{n_proc}</b><span>Distinct process units</span></div>
    <div class="kp hl"><b>₹{num(grand)}<small>cr</small></b><span>Value at stake / MTPA</span></div>
  </div>
  <p class="kfoot">Up to ₹{num(grand)} crore per MTPA of annual value identified across the mill · indicative, per million tonnes / annum of paper.</p>
  <div class="proof"><b>Proven at scale</b><span>400+ factories</span><span>100k+ assets connected</span><span>10B+ data points / day</span><span>↑20%+ OEE</span><span>↓80% unplanned downtime</span></div>
</div></header>

<section class="wrap ov">
  <div class="eyebrow">Executive overview</div>
  <h2>Where the value sits, and how Faclon unlocks it</h2>
  <div class="cca">
    <div><em>01 · Connect</em><h3>One data fabric across the mill</h3><p>I/O Connect ingests DCS, PLC, lab, ERP and camera streams into a unified namespace: no rip-and-replace, no per-project data plumbing.</p></div>
    <div><em>02 · Contextualize</em><h3>Models tuned to the process</h3><p>Deepsense builds soft sensors and kinetic models (kappa, brightness, H-factor, heat rate) that fill the gaps between slow lab samples.</p></div>
    <div><em>03 · Act</em><h3>Advisories into the control room</h3><p>Bruce AI turns predictions into location-tagged alerts and setpoint advisories operators can act on, with the value tracked per tonne.</p></div>
  </div>
  <div class="ov-grid">
    <div>
      <h3>Value at stake by process area</h3>
      <div class="chart">{"".join(bars)}
        <div class="btot"><span>Total identified · {n_uc} use cases</span><span>₹{num(grand)} cr / MTPA</span></div>
      </div>
    </div>
    <div>
      <h3>Use-case mix</h3>
      <div class="mix">{mix}</div>
      <div class="howto"><b>How to read each use case</b>Each process unit lists its inputs, process flow and quality parameters, followed by use-case cards. Every card states what Faclon does, the operating problems it removes, the KPIs it moves, and the value at stake, quantified as an upper bound per MTPA of paper capacity.</div>
    </div>
  </div>
</section>

<div class="bar"><div class="wrap">
  <label class="search" for="q">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="Search use cases, KPIs, equipment, e.g. kappa, felt, steam" aria-label="Search use cases">
  </label>
  <select id="sec" aria-label="Process area"><option value="">All process areas</option>{"".join(options)}</select>
  <select id="sort" aria-label="Order"><option value="chain">Mill flow order</option><option value="value">Highest value first</option></select>
  <div class="seg" id="kind" role="group" aria-label="Use-case type">
    <button type="button" data-k="" aria-pressed="true">All</button><button type="button" data-k="ai" aria-pressed="false">AI Advisory</button><button type="button" data-k="cv" aria-pressed="false">Vision AI</button><button type="button" data-k="fd" aria-pressed="false">Foundation</button>
  </div>
  <div class="count" id="count">Showing all {n_uc} use cases</div>
</div></div>

<div class="wrap main">
  <nav class="rail" aria-label="Process areas">{"".join(rail)}</nav>
  <main>
    <p class="note">All figures are indicative and subject to mutual agreement. Values are an upper bound, in ₹ crore per MTPA (million tonnes / annum) of paper capacity.</p>
    {"".join(sections_html)}
    <div class="empty" id="empty" hidden>No use cases match these filters. Try a broader term such as “steam” or “defect”, or clear the filters.</div>
  </main>
</div>

<div class="cta"><div class="wrap">
  <div class="eyebrow" style="color:var(--blue2)">Next step</div>
  <h2>Explore a <em>focused pilot</em></h2>
  <p>Pick one process area and one KPI from this catalog. Faclon connects the existing instrumentation, stands up a live dashboard, and returns a quantified value-unlock with a mill-wide scale-out plan, typically within a 4–6 week assessment.</p>
  <div class="steps3">
    <div><em>1</em><h3>Connect</h3><p>We tap existing DCS, PLC, lab and camera data: no rip-and-replace.</p></div>
    <div><em>2</em><h3>Prove</h3><p>A live dashboard and first quantified value-unlock inside 4–6 weeks.</p></div>
    <div><em>3</em><h3>Scale</h3><p>A mill-wide rollout plan with shared models and per-area value targets.</p></div>
  </div>
  <div class="cta-row"><p style="font-size:13px">Faclon Labs Pvt Ltd · The operating layer for industrial autonomy. All terms are indicative and subject to mutual agreement.</p><a class="btn" href="https://www.faclon.com">www.faclon.com</a></div>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Pulp &amp; Paper AI Use Case Map</span><span>Industrial AI operating layer for pulp &amp; paper</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
