"""Builds coal-mining-ai-use-case-map/index.html (AI & IoT use-case roadmap for coal mining).

Run from anywhere:  python3 src/coal-mining-ai-use-case-map/build_page.py

Content lives in content.json next to this script:
  hero        {eyebrow, title, kicker, lede}
  unit        label for every ₹ value          note   the indicative-savings footnote
  modes[]     {id, name}  deployment modes: opencast, underground, both
  domains[]   {id, name}  operational domains, in page order
  use_cases[] {n number, d domain id, t title, v indicative savings in ₹ Cr per MTPA,
               m mode id, sense (what is measured), analyse (what the analytics find),
               act (what people receive), solves (problem addressed)}
  cta         {title, text}
Domain totals, the grand total and the counts are computed from use_cases[], so they always
match the cards. Edit the JSON and re-run; the page is regenerated in full.

Source: Faclon "Coal Mining Use Cases" roadmap (AI & IoT use-case roadmap, mining operations).
"""
import html
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))
from cta import CTA_BUTTONS  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "coal-mining-ai-use-case-map" / "index.html"
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape

UCS = C["use_cases"]
DOMS = C["domains"]
MODES = {m["id"]: m["name"] for m in C["modes"]}


def cr(v):
    s = f"{v:.2f}".rstrip("0")
    return "₹" + (s + "0" if s.endswith(".") else s) + " Cr"


dom_total = {d["id"]: round(sum(u["v"] for u in UCS if u["d"] == d["id"]), 2) for d in DOMS}
dom_count = {d["id"]: sum(1 for u in UCS if u["d"] == d["id"]) for d in DOMS}
TOTAL = round(sum(u["v"] for u in UCS), 2)
MAXD = max(dom_total.values())
DNAME = {d["id"]: d["name"] for d in DOMS}

ICON = {
    "fleet": '<path d="M3 16V9h9l3 4h4a2 2 0 0 1 2 2v1"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M12 9V6H6"/>',
    "material": '<path d="M3 15h18M5 15l2-5h10l2 5"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "fixed": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
    "processing": '<path d="M8 3h8M9 3v6l-5 9a2 2 0 0 0 1.8 3h12.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M6.5 15h11"/>',
    "energy": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "safety": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="m9 12 2 2 4-4"/>',
    "environment": '<path d="M4 20c0-8 6-14 16-16-1 10-7 16-15 16"/><path d="M4 20 14 10"/>',
}


def icon(d, size=20):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[d]}</svg>')


# ---------- value by domain ----------
bars = "".join(
    f'<button type="button" class="vb" data-jump="{d["id"]}" aria-label="Show {E(d["name"])} use cases">'
    f'<span class="vn">{icon(d["id"], 16)}<span>{E(d["name"])}<small>{dom_count[d["id"]]} use case{"s" if dom_count[d["id"]] != 1 else ""}</small></span></span>'
    f'<span class="vt"><span class="vf" style="width:{dom_total[d["id"]] / MAXD * 100:.1f}%"></span></span>'
    f'<b>{cr(dom_total[d["id"]])}</b></button>'
    for d in sorted(DOMS, key=lambda d: -dom_total[d["id"]])
)

# ---------- use case cards ----------
def card(u):
    q = " ".join([u["t"], DNAME[u["d"]], MODES[u["m"]], u["sense"], u["analyse"], u["act"], u["solves"]]).lower()
    return (f'<article class="uc" id="uc-{u["n"]}" data-d="{u["d"]}" data-m="{u["m"]}" data-v="{u["v"]}" data-n="{u["n"]}" data-q="{E(q)}">'
            f'<div class="uh"><span class="no">{u["n"]:02d}</span><div class="ut"><span class="dk">{icon(u["d"], 14)}{E(DNAME[u["d"]])}</span>'
            f'<h3>{E(u["t"])}</h3></div><div class="uv"><b>{cr(u["v"])}</b><span>per MTPA</span>'
            f'<em class="md {u["m"]}">{E(MODES[u["m"]])}</em></div></div>'
            f'<ol class="steps"><li><span class="sl s1">Sense</span><p>{E(u["sense"])}</p></li>'
            f'<li><span class="sl s2">Analyse</span><p>{E(u["analyse"])}</p></li>'
            f'<li><span class="sl s3">Act</span><p>{E(u["act"])}</p></li></ol>'
            f'<p class="solves"><span>Solves</span>{E(u["solves"])}</p></article>')


cards = "".join(card(u) for u in UCS)
chips = (f'<button type="button" class="chip on" data-d="all" aria-pressed="true">All <span>{len(UCS)}</span></button>'
         + "".join(f'<button type="button" class="chip" data-d="{d["id"]}" aria-pressed="false">{E(d["name"])} '
                   f'<span>{dom_count[d["id"]]}</span></button>' for d in DOMS))
mode_counts = {k: sum(1 for u in UCS if u["m"] == k) for k in MODES}

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FDF3E3;--red:#B5452F;--redBg:#FBEEEB;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:24px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
ul,ol{list-style:none}
button{font:inherit;color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3{letter-spacing:-.015em;line-height:1.2;text-wrap:balance}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
section{padding:72px 0}
section.panel{background:var(--bg)}
h2{font-size:clamp(26px,3.4vw,36px);font-weight:700;margin:8px 0 10px}
.sub{color:var(--ink2);font-size:17px;max-width:700px;margin-bottom:30px}
input:focus,button:focus-visible,a:focus-visible{outline:2px solid var(--blue);outline-offset:1px}

/* hero */
.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.3),rgba(124,149,255,0) 68%)}
.hero .wrap{position:relative;padding-top:34px;padding-bottom:56px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hero .eyebrow{color:var(--blue2);margin-top:44px}
.hero h1{font-size:clamp(36px,5.6vw,60px);font-weight:700;margin:12px 0 14px;max-width:860px}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:760px}
.lede b{color:#fff;font-weight:600}
.kpis{display:grid;grid-template-columns:1.3fr 1fr 1fr 1fr;margin-top:30px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:18px 20px}
.kp b{font-size:30px;display:block;line-height:1.15}
.kp.big b{color:#7FD9B3}
.kp span{font-size:12.5px;color:#9FB0CC}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.jump a{font-size:13px;color:#D5DEEE;border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:5px 12px;text-decoration:none}
.jump a:hover{border-color:var(--blue2);color:#fff}

/* value chart */
.vwrap{display:grid;grid-template-columns:1.6fr 1fr;gap:28px;align-items:start}
.vchart{background:#fff;border:1px solid var(--line);border-radius:16px;padding:10px 8px}
.vb{display:grid;grid-template-columns:minmax(0,15rem) 1fr 5.2rem;align-items:center;gap:14px;width:100%;background:none;border:0;border-radius:10px;padding:10px 12px;cursor:pointer;text-align:left}
.vb:hover{background:var(--bg)}
.vn{display:flex;align-items:flex-start;gap:8px;font-weight:600;font-size:14.5px;line-height:1.3}
.vn svg{color:var(--blue);flex:none;margin-top:1px}
.vn small{display:block;font-weight:400;font-size:12px;color:var(--mute);margin-top:2px}
.vt{height:12px;background:var(--bg);border-radius:6px;overflow:hidden}
.vf{display:block;height:100%;background:var(--green);border-radius:6px}
.vb b{font-size:16px;color:var(--green);text-align:right;white-space:nowrap}
.vtot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--line);margin:6px 12px 0;padding:12px 0 6px;font-size:14px;color:var(--mute)}
.vtot b{font-size:18px;color:var(--ink)}
.modes{display:flex;flex-direction:column;gap:12px}
.mbox{border:1px solid var(--line);border-radius:14px;background:#fff;padding:16px 18px}
.mbox h3{font-size:15px;margin-bottom:6px}
.mbox p{font-size:13.5px;color:var(--ink2)}
.mrow{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-top:1px solid var(--line);font-size:14px}
.mrow:first-of-type{border-top:0}
.mrow b{color:var(--green)}

/* pattern */
.pat{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;align-items:stretch}
.pn{border:1px solid var(--line);border-radius:14px;background:#fff;padding:18px}
.pn .k{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.pn b{display:block;font-size:17px;margin:4px 0}
.pn p{font-size:13.5px;color:var(--ink2)}
.pn.s1{border-top:3px solid var(--mute)}.pn.s1 .k{color:var(--mute)}
.pn.s2{border-top:3px solid var(--blue)}.pn.s2 .k{color:var(--blue)}
.pn.s3{border-top:3px solid var(--green)}.pn.s3 .k{color:var(--green)}
.arr{display:flex;align-items:center;justify-content:center;padding:0 10px;color:var(--blue);font-weight:700;font-size:18px}

/* catalogue */
.bar{display:flex;flex-direction:column;gap:12px;margin-bottom:18px}
.row{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip,.seg button{border:1px solid var(--line);background:#fff;color:var(--ink2);border-radius:20px;padding:6px 12px;font-size:13.5px;font-weight:500;cursor:pointer}
.chip span{color:var(--mute);font-size:12px;margin-left:2px}
.chip.on,.seg button.on{background:var(--navy);border-color:var(--navy);color:#fff}
.chip.on span{color:#9FB0CC}
.seg{display:inline-flex;gap:4px;align-items:center;flex-wrap:wrap}
.seg .lb{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin-right:4px}
.search{flex:1 1 240px;position:relative;min-width:0}
.search input{width:100%;font:inherit;font-size:14.5px;padding:9px 12px 9px 34px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--mute)}
select{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);max-width:100%}
.stat{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;background:var(--greenBg);border-radius:12px;padding:10px 16px;font-size:14px}
.stat b{font-size:20px;color:var(--green)}
.stat .cnt{color:var(--mute);font-size:13px}
.ucs{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.uc{border:1px solid var(--line);border-radius:16px;background:#fff;padding:18px 20px;display:flex;flex-direction:column;gap:12px;scroll-margin-top:24px}
.uh{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:start}
.no{font-size:13px;font-weight:700;color:var(--blue);background:var(--blueBg);border-radius:8px;padding:4px 8px}
.dk{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.uc h3{font-size:18px;margin-top:2px}
.uv{text-align:right;line-height:1.2}
.uv b{font-size:22px;color:var(--green);display:block;white-space:nowrap}
.uv span{font-size:11px;color:var(--mute)}
.md{display:block;font-style:normal;font-size:11.5px;font-weight:600;border-radius:20px;padding:2px 9px;margin-top:6px;white-space:nowrap}
.md.opencast{background:var(--amberBg);color:#8A5208}
.md.underground{background:#E4E8F0;color:var(--navy)}
.md.both{background:var(--bg);color:var(--ink2);border:1px solid var(--line)}
.steps{display:flex;flex-direction:column;gap:8px}
.steps li{display:grid;grid-template-columns:4.6rem 1fr;gap:10px;font-size:14px;color:var(--ink2)}
.sl{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding-top:2px}
.sl.s1{color:var(--mute)}.sl.s2{color:var(--blue)}.sl.s3{color:var(--green)}
.solves{font-size:14px;background:var(--redBg);border-radius:10px;padding:9px 12px;color:#5E2417;margin-top:auto}
.solves span{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin-right:8px}
.empty{padding:36px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:16px}
.note{font-size:12.5px;color:var(--mute);font-style:italic;margin-top:16px}

.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta h2{font-size:30px;margin:6px 0 8px;max-width:640px}
.cta p{color:#C5D0E3;max-width:600px}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:1000px){
  .kpis{grid-template-columns:1fr 1fr}
  .vwrap{grid-template-columns:1fr}
  .pat{grid-template-columns:1fr}
  .arr{transform:rotate(90deg);padding:6px 0}
  .ucs{grid-template-columns:1fr}
}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  section{padding:52px 0}
  .vb{grid-template-columns:1fr auto;gap:6px 12px}
  .vt{grid-column:1/-1;grid-row:2}
  .uh{grid-template-columns:auto 1fr}
  .uv{grid-column:1/-1;text-align:left;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
  .uv b{display:inline}
  .md{display:inline-block;margin-top:0}
  .steps li{grid-template-columns:1fr;gap:2px}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.bar{display:none}.uc,.mbox,.pn{break-inside:avoid}}
"""

JS = """
(function(){
  var q=document.getElementById('q'),sort=document.getElementById('sort'),list=document.getElementById('uclist'),
      chips=[].slice.call(document.querySelectorAll('.chip')),modeBtns=[].slice.call(document.querySelectorAll('.seg button')),
      orig=[].slice.call(list.children),sum=document.getElementById('sum'),cnt=document.getElementById('cnt'),
      empty=document.getElementById('empty'),dom='all',mode='all',TOTAL=orig.length;
  function cr(v){var s=(Math.round(v*100)/100).toFixed(2).replace(/0$/,'');return '\\u20b9'+s+' Cr'}
  function apply(){
    var term=q.value.trim().toLowerCase(),k=sort.value,kids=orig.slice(),shown=0,v=0;
    if(k==='v')kids.sort(function(a,b){return b.dataset.v-a.dataset.v});
    kids.forEach(function(c){
      var ok=(dom==='all'||c.dataset.d===dom)&&(mode==='all'||c.dataset.m===mode||c.dataset.m==='both')&&(!term||c.dataset.q.indexOf(term)>-1);
      c.hidden=!ok;if(ok){shown++;v+=parseFloat(c.dataset.v)}list.appendChild(c)});
    sum.textContent=cr(v);
    cnt.textContent=shown===TOTAL?'All '+TOTAL+' use cases':shown+' of '+TOTAL+' use cases';
    empty.hidden=!!shown;
  }
  function pickD(d){dom=d;chips.forEach(function(b){var on=b.dataset.d===d;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)});apply()}
  chips.forEach(function(b){b.addEventListener('click',function(){pickD(b.dataset.d)})});
  modeBtns.forEach(function(b){b.addEventListener('click',function(){mode=b.dataset.m;modeBtns.forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on)});apply()})});
  [].slice.call(document.querySelectorAll('[data-jump]')).forEach(function(b){b.addEventListener('click',function(){q.value='';pickD(b.dataset.jump);document.getElementById('uc').scrollIntoView()})});
  q.addEventListener('input',apply);sort.addEventListener('change',apply);apply();
})();
"""

oc = round(sum(u["v"] for u in UCS if u["m"] in ("opencast", "both")), 2)
ug = round(sum(u["v"] for u in UCS if u["m"] in ("underground", "both")), 2)
H = C["hero"]

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Coal Mining AI Use Case Map · Faclon Labs</title>
<meta name="description" content="{len(UCS)} AI and IoT use cases across {len(DOMS)} coal mining domains, from haulage and washery to safety and environment, with indicative savings of {cr(TOTAL)} per MTPA.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>{E(H["eyebrow"])}</span></div>
  <a class="back" href="../">← All solutions</a>
  <div class="eyebrow">{E(H["kicker"])}</div>
  <h1>{E(H["title"])}</h1>
  <p class="lede">{E(H["lede"])}</p>
  <div class="kpis">
    <div class="kp big"><b>{cr(TOTAL)}</b><span>Total savings potential / MTPA</span></div>
    <div class="kp"><b>{len(UCS)}</b><span>AI use cases mapped</span></div>
    <div class="kp"><b>{len(DOMS)}</b><span>Operational domains</span></div>
    <div class="kp"><b>{len(MODES)}</b><span>Deployment modes</span></div>
  </div>
  <nav class="jump" aria-label="On this page"><a href="#value">Where the value is</a><a href="#pattern">How each use case works</a><a href="#uc">Use cases</a></nav>
</div></header>

<main>
<section id="value"><div class="wrap">
  <div class="eyebrow" style="color:var(--green)">Indicative savings</div>
  <h2>Where the value sits across the mine</h2>
  <p class="sub">Indicative annual savings per MTPA of throughput, by operational domain. Select a domain to see its use cases.</p>
  <div class="vwrap">
    <div class="vchart">{bars}<div class="vtot"><span>All {len(DOMS)} domains</span><b>{cr(TOTAL)} / MTPA</b></div></div>
    <div class="modes">
      <div class="mbox"><h3>Opencast or underground</h3><p>Each use case is marked for opencast mines, underground mines or both. Totals below add every use case that applies.</p>
        <div style="margin-top:8px">
        <div class="mrow"><span>Opencast mine</span><b>{cr(oc)} / MTPA</b></div>
        <div class="mrow"><span>Underground mine</span><b>{cr(ug)} / MTPA</b></div>
        </div></div>
      <div class="mbox"><h3>Biggest single lever</h3><p>Washery yield and media optimisation, at {cr(max(u["v"] for u in UCS))} per MTPA, followed by haulage and dispatch optimisation.</p></div>
    </div>
  </div>
  <p class="note">{E(C["note"])}</p>
</div></section>

<section class="panel" id="pattern"><div class="wrap">
  <div class="eyebrow">How each use case works</div>
  <h2>Sense, analyse, act</h2>
  <p class="sub">Every use case follows the same three steps: data from sensors, cameras or equipment telemetry, analytics that find the loss or the risk, and a live alert or recommendation for the people who can act on it.</p>
  <div class="pat">
    <div class="pn s1"><span class="k">1 · Sense</span><b>Measure what is happening</b><p>Telemetry from HEMM and dumpers, wireless vibration and gas sensors, analysers, energy meters, personnel tags and AI cameras.</p></div>
    <div class="arr" aria-hidden="true">→</div>
    <div class="pn s2"><span class="k">2 · Analyse</span><b>Find the loss or the risk</b><p>Models track cycle times, equipment health, yield, energy per tonne, gas trends, proximity breaches and compliance.</p></div>
    <div class="arr" aria-hidden="true">→</div>
    <div class="pn s3"><span class="k">3 · Act</span><b>Alert the right people</b><p>Live alarms, re-routing prompts, set-point recommendations, automatic stops or trips, dashboards and audit-ready logs.</p></div>
  </div>
</div></section>

<section id="uc"><div class="wrap">
  <div class="eyebrow">Use case roadmap</div>
  <h2>{len(UCS)} AI & IoT use cases</h2>
  <p class="sub">Filter by domain or by your type of mine, search for an asset or problem, or sort by value. The total updates with your selection.</p>
  <div class="bar">
    <div class="chips" role="group" aria-label="Filter by domain">{chips}</div>
    <div class="row">
      <div class="seg" role="group" aria-label="Type of mine"><span class="lb">Mine type</span>
        <button type="button" class="on" data-m="all" aria-pressed="true">All</button>
        <button type="button" data-m="opencast" aria-pressed="false">Opencast</button>
        <button type="button" data-m="underground" aria-pressed="false">Underground</button></div>
      <label class="search" for="q">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input id="q" type="search" placeholder="Search, e.g. tyre, methane, conveyor, washery" aria-label="Search use cases">
      </label>
      <select id="sort" aria-label="Order"><option value="n">Roadmap order</option><option value="v">Highest value first</option></select>
    </div>
    <div class="stat"><span>Indicative savings for this selection: <b id="sum">{cr(TOTAL)}</b> / MTPA</span><span class="cnt" id="cnt">All {len(UCS)} use cases</span></div>
  </div>
  <div class="ucs" id="uclist">{cards}</div>
  <div class="empty" id="empty" hidden>No use cases match. Try “fleet”, “gas” or “dust”.</div>
  <p class="note">{E(C["note"])} Choosing a mine type also includes the use cases that apply to both.</p>
</div></section>
</main>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Next step</div><h2>{E(C["cta"]["title"])}</h2><p>{E(C["cta"]["text"])}</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Coal Mining AI Use Case Map</span><span>Industrial AI for mining operations</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
