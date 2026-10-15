"""Builds energy-management/index.html (Energy Management on I/O Sense).

Run from anywhere:  python3 src/energy-management/build_page.py
Content lives in content.json next to this script; edit it and re-run, the page is regenerated in full.
  title / tagline / lede : hero text          pillars : the three hero promises
  kpis        : [{v: value, l: label}] shown in the hero strip
  benefit_cats: {key: label} filter chips      benefits : [{t: title, c: category key, d: description}]
  architecture: {example, cloud, onprem}; each option has label, intro, chain [{t, d, hub?}],
                power, dss_title, dss [items], optional outputs [items],
                diagram (asset name of the full drawing) and diagram_cap
  modules     : [{id, n: name, s: subtitle, d: description, p: [points], img?: asset name, cap?: caption,
                 full?: true to span the full width when there is no screenshot}]
  drill       : [{t, d}] the I/O Matrix drill-down levels, in order
  showcase    : [{img, t, d}] large screenshots with a short explanation
  customers   : customer names only (no sites or meter counts: the source slide is confidential)
  contacts    : [{n, ph, tel, e}]
Screenshots live in assets/ as JPGs and are embedded as data URIs so the page stays self-contained.
"""
import base64
import html
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))
from cta import CTA_BUTTONS  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "energy-management" / "index.html"
D = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape


def img(name, alt, cls="", lazy=True):
    data = base64.b64encode((HERE / "assets" / f"{name}.jpg").read_bytes()).decode()
    return f'<img class="{cls}" src="data:image/jpeg;base64,{data}" alt="{E(alt)}"{' loading="lazy"' if lazy else ''} decoding="async">'


# ---------- benefits ----------
cats = D["benefit_cats"]
chips = [f'<button class="chip" type="button" data-c="" aria-pressed="true">All<i>{len(D["benefits"])}</i></button>']
for k, label in cats.items():
    n = sum(1 for b in D["benefits"] if b["c"] == k)
    chips.append(f'<button class="chip" type="button" data-c="{k}" aria-pressed="false">{E(label)}<i>{n}</i></button>')
benefits = "".join(
    f'<article class="ben" data-c="{b["c"]}"><span class="bcat">{E(cats[b["c"]])}</span>'
    f'<h3>{E(b["t"])}</h3><p>{E(b["d"])}</p></article>'
    for b in D["benefits"]
)

# ---------- showcase ----------
showcase = "".join(
    f'<figure class="show"><div class="shot">{img(s["img"], s["t"])}</div>'
    f'<figcaption><h3>{E(s["t"])}</h3><p>{E(s["d"])}</p></figcaption></figure>'
    for s in D["showcase"]
)


# ---------- architecture ----------
def arch_panel(key, a):
    nodes = []
    for i, c in enumerate(a["chain"]):
        if i:
            nodes.append('<span class="arrow" aria-hidden="true">→</span>')
        nodes.append(f'<div class="node{" hub" if c.get("hub") else ""}"><em>{i + 1:02d}</em>'
                     f'<b>{E(c["t"])}</b><span>{E(c["d"])}</span></div>')
    dss = "".join(f"<li>{E(x)}</li>" for x in a["dss"])
    outs = ""
    if a.get("outputs"):
        outs = '<div class="outs">' + "".join(f"<span>{E(x)}</span>" for x in a["outputs"]) + "</div>"
    return (f'<div class="arch-panel" id="arch-{key}" data-k="{key}">'
            f'<h3 class="arch-h">{E(a["label"])} deployment</h3><p class="arch-intro">{E(a["intro"])}</p>'
            f'<div class="chain">{"".join(nodes)}</div>'
            f'<div class="arch-foot"><div class="dss"><b>{E(a["dss_title"])}</b><ul>{dss}</ul>{outs}</div>'
            f'<p class="power">{E(a["power"])}. {E(D["architecture"]["example"])}; the same pattern repeats for every substation.</p></div>'
            + diagram(a) + '</div>')


def diagram(a):
    if not a.get("diagram"):
        return ""
    return (f'<figure class="diagram"><figcaption><b>{E(a["label"])} architecture</b><span>{E(a["diagram_cap"])}</span></figcaption>'
            f'<div class="dg-scroll" tabindex="0" role="region" aria-label="{E(a["label"])} architecture diagram">'
            f'{img(a["diagram"], a["label"] + " architecture: " + a["diagram_cap"], lazy=False)}</div>'
            f'<p class="dg-hint">Swipe sideways to see the full diagram</p></figure>')


A = D["architecture"]
arch = arch_panel("cloud", A["cloud"]) + arch_panel("onprem", A["onprem"])


# ---------- modules ----------
def module(m, i):
    pts = "".join(f"<li>{E(p)}</li>" for p in m["p"])
    shot = ""
    if m.get("img"):
        shot = f'<figure class="mshot">{img(m["img"], m["cap"])}<figcaption>{E(m["cap"])}</figcaption></figure>'
    cls = " wide" if m.get("img") else (" full" if m.get("full") else "")
    return (f'<article class="mod{cls}" id="m-{m["id"]}">'
            f'<div class="mod-top"><em>{i + 1:02d}</em><div><h3>{E(m["n"])}</h3><span>{E(m["s"])}</span></div></div>'
            f'<p class="mod-d">{E(m["d"])}</p><ul class="pts">{pts}</ul>{shot}</article>')


modules = "".join(module(m, i) for i, m in enumerate(D["modules"]))
modnav = "".join(f'<a href="#m-{m["id"]}">{E(m["n"])}</a>' for m in D["modules"])
drill = "".join(
    f'<li><em>Level {i + 1}</em><b>{E(x["t"])}</b><span>{E(x["d"])}</span></li>' for i, x in enumerate(D["drill"])
)

customers = "".join(f"<li>{E(c)}</li>" for c in D["customers"])
pillars = "".join(f"<li>{E(p)}</li>" for p in D["pillars"])
kpis = "".join(f'<div class="kp"><b>{E(k["v"])}</b><span>{E(k["l"])}</span></div>' for k in D["kpis"])
contacts = "".join(
    f'<div class="ct"><b>{E(c["n"])}</b><a href="tel:{E(c["tel"])}">{E(c["ph"])}</a>'
    f'<a href="mailto:{E(c["e"])}">{E(c["e"])}</a></div>'
    for c in D["contacts"]
)

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FDF3E3;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:24px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
ul{list-style:none}img{display:block;max-width:100%;height:auto}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3{letter-spacing:-.015em;line-height:1.2;text-wrap:balance}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}

.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.32),rgba(124,149,255,0) 68%)}
.hero:after{content:"";position:absolute;left:-160px;bottom:-260px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(17,135,95,.22),rgba(17,135,95,0) 68%)}
.hero .wrap{position:relative;z-index:1;padding-top:34px;padding-bottom:56px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hero .eyebrow{color:var(--blue2);margin-top:52px;display:block}
.hero h1{font-size:clamp(38px,6vw,64px);font-weight:700;margin:12px 0 10px}
.tag-line{font-size:clamp(18px,2.2vw,24px);font-weight:600;color:#DCE4F5;max-width:760px}
.lede{font-size:clamp(15.5px,1.7vw,18px);color:#B9C6DD;max-width:720px;margin-top:14px}
.pillars{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.pillars li{font-size:14px;font-weight:500;padding:8px 14px 8px 30px;border-radius:30px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);position:relative}
.pillars li:before{content:"";position:absolute;left:13px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:#3DD39B}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:34px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:28px;display:block}
.kp:first-child b{color:#3DD39B}
.kp span{font-size:12.5px;color:#9FB0CC;display:block;line-height:1.4;margin-top:2px}

.jump{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.jump .wrap{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;padding-top:8px;padding-bottom:8px}
.jump .wrap::-webkit-scrollbar{display:none}
.jump a{flex:none;font-size:14px;font-weight:500;color:var(--ink2);text-decoration:none;padding:7px 12px;border-radius:8px}
.jump a:hover{background:var(--bg);color:var(--ink)}

section.band{padding:64px 0}
section.band.alt{background:var(--bg)}
.sh{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.sh h2{font-size:clamp(26px,3.2vw,34px);font-weight:700;margin-top:6px}
.sh p{color:var(--ink2);max-width:620px;margin-top:8px}

.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px}
.chip{font:inherit;font-size:14px;padding:7px 12px;border:1px solid var(--line);border-radius:30px;background:#fff;color:var(--ink2);cursor:pointer;display:inline-flex;gap:8px;align-items:center}
.chip i{font-style:normal;font-size:12px;color:var(--mute)}
.chip[aria-pressed="true"]{background:var(--greenBg);border-color:var(--green);color:var(--green)}
.chip[aria-pressed="true"] i{color:var(--green)}
button:focus-visible,a:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.count{font-size:13px;color:var(--mute);margin-bottom:16px}
.bens{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.ben{border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fff;border-top:3px solid var(--green)}
.bcat{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--green)}
.ben h3{font-size:17px;margin:6px 0 6px}
.ben p{font-size:14px;color:var(--ink2)}

.shows{display:grid;gap:28px}
.show{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:28px;align-items:center}
.show:nth-child(even) .shot{order:2}
.shot{border-radius:14px;overflow:hidden;border:1px solid var(--line);box-shadow:0 12px 32px -18px rgba(11,26,48,.35);background:#fff}
.show h3{font-size:22px;margin-bottom:8px}
.show p{color:var(--ink2)}
.illus{font-size:12.5px;color:var(--mute);font-style:italic;margin-top:22px}

.tabs{display:inline-flex;padding:4px;background:#fff;border:1px solid var(--line);border-radius:12px;gap:4px;margin-bottom:22px}
.tab{font:inherit;font-size:14.5px;font-weight:600;padding:8px 18px;border:0;border-radius:9px;background:transparent;color:var(--ink2);cursor:pointer}
.tab[aria-selected="true"]{background:var(--navy);color:#fff}
.arch-panel+.arch-panel{margin-top:40px}
.js .arch-panel+.arch-panel{margin-top:0}
.js .arch-h{display:none}
.arch-h{font-size:20px;margin-bottom:6px}
.arch-intro{color:var(--ink2);margin-bottom:18px;max-width:720px}
.chain{display:flex;align-items:stretch;gap:8px}
.node{flex:1 1 0;min-width:0;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:4px}
.node em{font-style:normal;font-size:11px;font-weight:700;letter-spacing:.12em;color:var(--mute)}
.node b{font-size:15px;line-height:1.3}
.node span{font-size:13px;color:var(--ink2);line-height:1.45}
.node.hub{background:var(--blue);border-color:var(--blue);color:#fff}
.node.hub em,.node.hub span{color:#DCE3FF}
.arrow{flex:none;align-self:center;color:var(--blue);font-weight:700}
.arch-foot{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;margin-top:16px;align-items:start}
.dss{background:var(--navy);color:#fff;border-radius:12px;padding:18px 20px}
.dss b{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue2)}
.dss ul{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:6px 18px;margin-top:10px;font-size:14px}
.dss li{padding-left:14px;position:relative;color:#DCE4F5}
.dss li:before{content:"";position:absolute;left:0;top:9px;width:6px;height:6px;border-radius:2px;background:var(--blue2)}
.outs{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px;padding-top:12px;border-top:1px solid rgba(255,255,255,.12)}
.outs span{font-size:12.5px;padding:4px 10px;border-radius:20px;background:rgba(124,149,255,.18);color:#fff}
.diagram{margin-top:22px;border:1px solid var(--line);border-radius:14px;background:#fff;overflow:hidden}
.diagram figcaption{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:14px 18px;border-bottom:1px solid var(--line);background:var(--bg)}
.diagram figcaption b{font-size:15px}
.diagram figcaption span{font-size:13px;color:var(--mute)}
.dg-scroll{overflow-x:auto;padding:14px}
.dg-scroll img{width:100%;min-width:0}
.dg-hint{display:none;font-size:12px;color:var(--mute);padding:0 18px 12px}
.power{font-size:13.5px;color:var(--ink2);background:var(--amberBg);border-left:3px solid var(--amber);border-radius:8px;padding:12px 14px}

.modnav{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:20px}
.modnav a{font-size:13px;color:var(--blue);text-decoration:none;padding:5px 10px;border-radius:20px;background:var(--blueBg)}
.mods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.mod{border:1px solid var(--line);border-radius:16px;padding:20px 22px;background:#fff;display:flex;flex-direction:column;gap:12px}
.mod.wide{grid-column:1/-1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);column-gap:28px;align-items:start}
.mod.wide>*{grid-column:1}
.mod.full{grid-column:1/-1}
.mod.full .pts{display:grid;grid-template-columns:1fr 1fr;gap:6px 28px}
.mod.wide .mshot{grid-column:2;grid-row:1/span 3}
.mod-top{display:flex;gap:14px;align-items:flex-start}
.mod-top em{font-style:normal;font-size:13px;font-weight:700;letter-spacing:.12em;color:var(--blue);padding-top:4px}
.mod-top h3{font-size:20px}
.mod-top span{font-size:13px;color:var(--mute)}
.mod-d{color:var(--ink)}
.pts{display:flex;flex-direction:column;gap:6px;font-size:14px;color:var(--ink2)}
.pts li{padding-left:16px;position:relative}
.pts li:before{content:"";position:absolute;left:0;top:9px;width:7px;height:2px;background:var(--blue)}
.mshot img{border-radius:10px;border:1px solid var(--line)}
.mshot figcaption{font-size:12.5px;color:var(--mute);margin-top:6px}
.drill{margin-top:28px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px}
.drill h3{font-size:17px}
.drill p{font-size:14px;color:var(--ink2);margin-top:4px}
.drill ol{list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:16px;counter-reset:l}
.drill li{background:var(--bg);border-radius:10px;padding:12px 14px;position:relative;border-left:3px solid var(--blue)}
.drill li:nth-child(2){border-color:#5B7BF7}.drill li:nth-child(3){border-color:#7C95FF}.drill li:nth-child(4){border-color:#A8B8FF}
.drill em{font-style:normal;font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
.drill b{display:block;font-size:15px;margin-top:2px}
.drill span{font-size:13px;color:var(--mute)}

.custs{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.custs li{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 18px;font-weight:600;font-size:15px;display:flex;align-items:center;min-height:64px}

.cta{background:var(--navy);color:#fff}
.cta .wrap{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:32px;padding-top:56px;padding-bottom:56px;align-items:center}
.cta h2{font-size:30px;margin:6px 0 8px}
.cta p{color:#C5D0E3;max-width:560px}
.cts{display:grid;gap:12px}
.ct{background:var(--navy2);border-radius:12px;padding:14px 18px;display:flex;flex-direction:column;gap:2px}
.ct b{font-size:15px}
.ct a{color:#C5D0E3;text-decoration:none;font-size:14px;overflow-wrap:anywhere}
.ct a:hover{color:#fff}
.btn{display:inline-block;margin-top:18px;background:var(--blue);color:#fff;font-weight:600;padding:11px 20px;border-radius:10px;text-decoration:none}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:980px){
  .chain{flex-direction:column}.arrow{transform:rotate(90deg)}
  .arch-foot,.show,.mod.wide,.cta .wrap{grid-template-columns:1fr}
  .show:nth-child(even) .shot{order:0}
  .mod.wide .mshot{grid-column:1;grid-row:auto}
  .mods{grid-template-columns:1fr}.mod.full .pts{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}
  .drill ol{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){
  .dg-scroll img{width:880px;max-width:none}.dg-hint{display:block}
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  section.band{padding:44px 0}.hero .eyebrow{margin-top:36px}
  .bens{grid-template-columns:1fr}.drill ol{grid-template-columns:1fr}
  .kp{padding:14px}.kp b{font-size:24px}
  .tabs{display:flex}.tab{flex:1}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.jump,.tabs,.chips{display:none}.ben,.mod,.node,.show{break-inside:avoid}}
"""

JS = """
(function(){
  document.documentElement.classList.add('js');
  var chips=document.querySelectorAll('.chip'),bens=document.querySelectorAll('.ben'),count=document.getElementById('bcount');
  function filt(c){
    var n=0;
    bens.forEach(function(b){var ok=!c||b.dataset.c===c;b.hidden=!ok;if(ok)n++});
    chips.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.c===c)});
    count.textContent=n===bens.length?'Showing all '+n+' benefits':'Showing '+n+' of '+bens.length+' benefits';
  }
  chips.forEach(function(x){x.addEventListener('click',function(){filt(x.dataset.c)})});
  var tabs=document.querySelectorAll('.tab'),panels=document.querySelectorAll('.arch-panel');
  function show(k){
    panels.forEach(function(p){p.hidden=p.dataset.k!==k});
    tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.k===k)});
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.k)})});
  document.querySelector('.tabs').hidden=false;
  show('cloud');filt('');
})();
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Energy Management · Faclon Labs</title>
<meta name="description" content="Plant-wide energy management on I/O Sense: meters to decisions, with dashboards, alerts, reports and drill-down analysis.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Energy Management · I/O Sense</span></div>
  <a class="back" href="../">← All solutions</a>
  <span class="eyebrow">Plant-wide energy intelligence</span>
  <h1>{E(D["title"])}</h1>
  <p class="tag-line">{E(D["tagline"])}</p>
  <p class="lede">{E(D["lede"])}</p>
  <ul class="pillars">{pillars}</ul>
  <div class="kpis">{kpis}</div>
</div></header>

<nav class="jump" aria-label="On this page"><div class="wrap">
  <a href="#benefits">Benefits</a><a href="#in-action">In action</a><a href="#architecture">Architecture</a><a href="#platform">Platform modules</a><a href="#customers">Customers</a><a href="#contact">Contact</a>
</div></nav>

<section class="band" id="benefits"><div class="wrap">
  <div class="sh"><div><span class="eyebrow" style="color:var(--green)">What it delivers</span><h2>Ten ways metered energy data pays back</h2>
  <p>From the monthly bill down to a single feeder, each benefit comes from measured data rather than estimates.</p></div></div>
  <div class="chips" role="group" aria-label="Filter benefits">{"".join(chips)}</div>
  <div class="count" id="bcount" aria-live="polite">Showing all {len(D["benefits"])} benefits</div>
  <div class="bens">{benefits}</div>
</div></section>

<section class="band alt" id="in-action"><div class="wrap">
  <div class="sh"><div><span class="eyebrow">In action</span><h2>What plant teams see every shift</h2></div></div>
  <div class="shows">{showcase}</div>
  <p class="illus">Screens are for representation purposes only.</p>
</div></section>

<section class="band" id="architecture"><div class="wrap">
  <div class="sh"><div><span class="eyebrow">Architecture</span><h2>From meter to decision, in the cloud or on premise</h2>
  <p>Standard energy meters on RS485 Modbus feed industrial gateways in each substation. Choose where the platform runs; the meters and panels stay the same.</p></div></div>
  <div class="tabs" role="tablist" aria-label="Deployment option" hidden>
    <button class="tab" type="button" role="tab" data-k="cloud" aria-selected="true">{E(A["cloud"]["label"])}</button>
    <button class="tab" type="button" role="tab" data-k="onprem" aria-selected="false">{E(A["onprem"]["label"])}</button>
  </div>
  {arch}
</div></section>

<section class="band alt" id="platform"><div class="wrap">
  <div class="sh"><div><span class="eyebrow">I/O Sense platform</span><h2>Eight modules, configured without code</h2>
  <p>Everything from user access to custom KPIs is set up by your own team through the interface.</p></div></div>
  <div class="modnav">{modnav}</div>
  <div class="mods">{modules}</div>
  <div class="drill"><h3>I/O Matrix drill-down, from incomer to machine</h3><p>Start at the plant total and click down to the feeder that is driving a deviation.</p><ol>{drill}</ol></div>
</div></section>

<section class="band" id="customers"><div class="wrap">
  <div class="sh"><div><span class="eyebrow" style="color:var(--green)">Customers</span><h2>{E(D["customers_note"])}</h2>
  <p>Live, multi-site deployments for leading Indian manufacturers and energy companies.</p></div></div>
  <ul class="custs">{customers}</ul>
</div></section>

<div class="cta" id="contact"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Your digital backbone</div><h2>Start with the meters you already have</h2>
  <p>We're here as your digital backbone to drive operational efficiency and decision intelligence. Talk to us about connecting your substations and seeing your first dashboards.</p>
  <div style="margin-top:18px">{CTA_BUTTONS}</div></div>
  <div class="cts">{contacts}</div>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Energy Management</span><span>Powered by I/O Sense</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
