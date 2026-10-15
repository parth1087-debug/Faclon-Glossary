"""Builds condition-based-monitoring/index.html (Condition Based Monitoring / predictive maintenance).

Run from anywhere:  python3 src/condition-based-monitoring/build_page.py

Sources, all in this folder:
  content.json   All page content:
                   hero          {title, tagline, pillars[]}
                   architecture  {transmits[], analytics[] {t, d}, outputs[]}
                   benefits[]    {v (headline figure, "" for none), t, d}
                   faults[]      fault types detected      assets[]  asset types covered
                   features[]    {img, t, d, alt}          platform screenshots with their description
                   sensor        {img, specs[] [label, value]}
                   gallery[]     {img, c}                  installation photos and captions
                   cases[]       {c customer, p plants text, np plant count, a assets, s sensors,
                                  d asset description, n issues found (e.g. "130+"), i example issues}
  assets/        JPG images referenced by name in content.json, embedded as data URIs

Source: Faclon "Condition Based Monitoring" deck. Edit content.json and re-run; the page is
regenerated in full. Totals in the hero and case-study band are computed from cases[].
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
OUT = ROOT / "condition-based-monitoring" / "index.html"
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape


def img(name):
    return "data:image/jpeg;base64," + base64.b64encode((HERE / "assets" / f"{name}.jpg").read_bytes()).decode()


def num(n):
    return f"{n:,}"


cases = C["cases"]
T_PLANTS = sum(c["np"] for c in cases)
T_ASSETS = sum(c["a"] for c in cases)
T_SENSORS = sum(c["s"] for c in cases)
T_ISSUES = sum(int(c["n"].rstrip("+")) for c in cases)
ISSUES_LABEL = f"{T_ISSUES // 50 * 50}+" if T_ISSUES >= 100 else f"{T_ISSUES}+"

# ---------- sections ----------
pillars = "".join(f"<li>{E(p)}</li>" for p in C["hero"]["pillars"])

A = C["architecture"]
transmits = "".join(f"<span>{E(x)}</span>" for x in A["transmits"])
analytics = "".join(f'<div class="an"><b>{E(x["t"])}</b><p>{E(x["d"])}</p></div>' for x in A["analytics"])
outputs = "".join(f"<li>{E(x)}</li>" for x in A["outputs"])
assets_short = " · ".join(C["assets"][:6])

benefits = "".join(
    f'<article class="ben{" fig" if b["v"] else ""}">'
    + (f'<div class="bv">{E(b["v"])}</div>' if b["v"] else "")
    + f'<h3>{E(b["t"])}</h3><p>{E(b["d"])}</p></article>'
    for b in C["benefits"]
)
faults = "".join(f"<li>{E(f)}</li>" for f in C["faults"])
assets = "".join(f"<li>{E(a)}</li>" for a in C["assets"])

features = "".join(
    f'<div class="feat{" rev" if i % 2 else ""}"><div class="ftxt"><div class="eyebrow">I/O Sense platform</div>'
    f'<h3>{E(f["t"])}</h3><p>{E(f["d"])}</p></div>'
    f'<figure class="shot"><img src="{img(f["img"])}" alt="{E(f["alt"])}"></figure></div>'
    for i, f in enumerate(C["features"])
)

specs = "".join(f"<tr><th>{E(k)}</th><td>{E(v)}</td></tr>" for k, v in C["sensor"]["specs"])

gallery = "".join(
    f'<figure class="g{" wide" if i == 0 else ""}"><img src="{img(g["img"])}" alt="{E(g["c"])}">'
    f'<figcaption>{E(g["c"])}</figcaption></figure>'
    for i, g in enumerate(C["gallery"])
)


def case_card(c):
    q = " ".join([c["c"], c["p"], c["d"], c["i"]]).lower()
    issues = "".join(f"<li>{E(x.strip())}</li>" for x in c["i"].split(","))
    return (f'<article class="case" data-name="{E(c["c"])}" data-a="{c["a"]}" data-s="{c["s"]}" '
            f'data-n="{int(c["n"].rstrip("+"))}" data-q="{E(q)}">'
            f'<div class="ch"><div><h3>{E(c["c"])}</h3><span class="pl">{E(c["p"])}</span></div>'
            f'<div class="cm"><div><b>{num(c["a"])}</b><span>Assets</span></div>'
            f'<div><b>{num(c["s"])}</b><span>Sensors</span></div>'
            f'<div class="iss"><b>{E(c["n"])}</b><span>Issues found</span></div></div></div>'
            f'<div class="cb"><div><span class="lab">Assets monitored</span><p>{E(c["d"])}</p></div>'
            f'<div><span class="lab red">Issues identified, e.g.</span><ul class="il">{issues}</ul></div></div>'
            f'</article>')


case_cards = "".join(case_card(c) for c in cases)

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--red:#B5452F;--redBg:#FBEEEB;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:24px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
ul{list-style:none}
img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3{letter-spacing:-.015em;line-height:1.2;text-wrap:balance}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
section{padding:72px 0}
section.panel{background:var(--bg)}
h2{font-size:clamp(26px,3.4vw,36px);font-weight:700;margin:8px 0 10px}
.sub{color:var(--ink2);font-size:17px;max-width:680px;margin-bottom:34px}

.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.32),rgba(124,149,255,0) 68%)}
.hero .wrap{position:relative;padding-top:34px;padding-bottom:56px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hero h1{font-size:clamp(36px,5.6vw,60px);font-weight:700;margin:52px 0 14px;max-width:820px}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:700px}
.pillars{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,.12);border-radius:12px;overflow:hidden;margin-top:30px;max-width:900px}
.pillars li{background:var(--navy2);padding:14px 18px;font-weight:600;font-size:14.5px;color:#E3E9F5}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:14px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:28px;display:block}
.kp span{font-size:12.5px;color:#9FB0CC}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.jump a{font-size:13px;color:#D5DEEE;border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:5px 12px;text-decoration:none}
.jump a:hover{border-color:var(--blue2);color:#fff}

/* architecture */
.archfig{margin:0 0 30px;border:1px solid var(--line);border-radius:16px;background:#fff;padding:18px 18px 12px;box-shadow:0 12px 32px rgba(15,27,45,.06)}
.archfig img{width:100%;height:auto}
.archfig .zoom{display:block;cursor:zoom-in}
.archfig figcaption{display:flex;justify-content:space-between;gap:12px;font-size:12.5px;color:var(--mute);border-top:1px solid var(--line);margin-top:12px;padding-top:10px}
.archfig figcaption span{color:var(--blue);font-weight:600}
.steph{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-bottom:12px}
.lbx{display:none}
.archfig:target{position:fixed;inset:0;z-index:50;margin:0;border:0;border-radius:0;background:#0B1A30;overflow:auto;padding:56px 16px 16px}
.archfig:target img{background:#fff;border-radius:10px;padding:10px;min-width:900px;max-width:1600px;margin:0 auto}
.archfig:target .zoom{cursor:default}
.archfig:target figcaption{display:none}
.archfig:target .lbx{display:block;position:fixed;top:10px;right:18px;color:#fff;font-size:38px;line-height:1;text-decoration:none}
@media (min-width:1001px){.archfig figcaption span{display:none}.archfig .zoom{cursor:zoom-in}}
.flow{display:grid;grid-template-columns:1.1fr auto 1fr auto .8fr auto 1.2fr auto 1.3fr;align-items:stretch;gap:0}
.node{border:1px solid var(--line);border-radius:14px;background:#fff;padding:16px;display:flex;flex-direction:column;gap:6px}
.node .k{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.node b{font-size:15.5px}
.node p{font-size:13px;color:var(--ink2)}
.node.core{background:var(--navy);border-color:var(--navy);color:#fff}
.node.core .k{color:var(--blue2)}
.node.core p{color:#C5D0E3}
.node.out{border-color:var(--blue);background:var(--blueBg)}
.node.out ul{font-size:13px;color:var(--ink);display:flex;flex-direction:column;gap:3px}
.node.out li:before{content:"→ ";color:var(--blue);font-weight:700}
.arr{display:flex;align-items:center;justify-content:center;padding:0 6px;color:var(--blue);font-weight:700}
.arr small{display:block;font-size:10.5px;letter-spacing:.08em;color:var(--mute);text-align:center}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
.chips span{font-size:11.5px;font-weight:600;border-radius:20px;padding:2px 9px;background:var(--blueBg);color:var(--blue)}
.analytics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}
.an{border:1px solid var(--line);border-radius:14px;padding:16px 18px;background:#fff;border-top:3px solid var(--blue)}
.an b{display:block;font-size:15.5px;margin-bottom:4px}
.an p{font-size:13.5px;color:var(--ink2)}

/* benefits */
.bens{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.ben{border:1px solid var(--line);border-radius:16px;padding:22px;background:#fff}
.ben.fig{border-top:4px solid var(--green)}
.bv{font-size:44px;font-weight:700;color:var(--green);line-height:1;margin-bottom:10px;letter-spacing:-.02em}
.ben h3{font-size:18px;margin-bottom:6px}
.ben p{color:var(--ink2);font-size:14.5px}
.note{font-size:12.5px;color:var(--mute);font-style:italic;margin-top:16px}

/* faults */
.fa{display:grid;grid-template-columns:1.5fr 1fr;gap:20px}
.box{border:1px solid var(--line);border-radius:16px;padding:22px;background:#fff}
.box h3{font-size:18px;margin-bottom:4px}
.box .hint{font-size:13px;color:var(--mute);margin-bottom:14px}
.flist{display:flex;flex-wrap:wrap;gap:8px}
.flist li{font-size:13.5px;border:1px solid #EFD4CC;background:var(--redBg);color:#7A2E1F;border-radius:20px;padding:5px 12px}
.alist li{border-color:var(--line);background:var(--bg);color:var(--ink)}
.flist li.more{background:#fff;border-style:dashed;color:var(--mute);font-style:italic}

/* features */
.feat{display:grid;grid-template-columns:1fr 1.6fr;gap:36px;align-items:center}
.feat+.feat{margin-top:56px}
.feat.rev .ftxt{order:2}
.ftxt h3{font-size:24px;margin:8px 0 10px}
.ftxt p{color:var(--ink2)}
.shot{border-radius:14px;overflow:hidden;border:1px solid var(--line);box-shadow:0 18px 40px rgba(15,27,45,.10);background:#fff}

/* sensor */
.sensor{display:grid;grid-template-columns:.8fr 1.4fr;gap:36px;align-items:start}
.sph{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;display:flex;flex-direction:column;align-items:center;gap:14px}
.sph img{max-width:300px;width:100%}
.sph .chips span{background:var(--bg);color:var(--ink2)}
table.spec{width:100%;border-collapse:collapse;font-size:14px;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.spec th,.spec td{text-align:left;padding:9px 14px;border-bottom:1px solid var(--line);vertical-align:top}
.spec tr:last-child th,.spec tr:last-child td{border-bottom:0}
.spec th{font-weight:600;color:var(--mute);width:42%;font-size:13px}

/* gallery */
.gal{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.g{border-radius:14px;overflow:hidden;background:#000;position:relative;margin:0}
.g.wide{grid-column:span 2}
.g img{width:100%;height:260px;object-fit:cover;object-position:center 75%}
.g figcaption{position:absolute;left:0;right:0;bottom:0;padding:22px 14px 10px;font-size:13px;color:#fff;background:linear-gradient(transparent,rgba(11,26,48,.85))}

/* cases */
.totals{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-bottom:22px}
.totals div{background:#fff;padding:14px 18px}
.totals b{font-size:26px;display:block;color:var(--green)}
.totals span{font-size:12.5px;color:var(--mute)}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:16px}
.search{flex:1 1 260px;position:relative;min-width:0}
.search input{width:100%;font:inherit;font-size:14.5px;padding:9px 12px 9px 34px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--mute)}
select{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);max-width:100%}
input:focus,select:focus,a:focus-visible{outline:2px solid var(--blue);outline-offset:1px}
.count{font-size:13px;color:var(--mute);margin-left:auto}
.cases{display:flex;flex-direction:column;gap:12px}
.case{border:1px solid var(--line);border-radius:16px;background:#fff;overflow:hidden}
.ch{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center;padding:16px 20px;background:#fff}
.ch h3{font-size:19px}
.pl{font-size:13px;color:var(--mute)}
.cm{display:flex;gap:22px}
.cm div{text-align:right;line-height:1.15}
.cm b{font-size:20px;display:block}
.cm span{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute)}
.cm .iss b{color:var(--green)}
.cb{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:14px 20px 18px;background:var(--bg);border-top:1px solid var(--line);font-size:14px;color:var(--ink2)}
.lab{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);margin-bottom:4px}
.lab.red{color:var(--red)}
.il{display:flex;flex-wrap:wrap;gap:6px}
.il li{font-size:12.5px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:2px 10px;color:var(--ink)}
.empty{padding:36px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:16px}

.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta .k{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue2)}
.cta h2{font-size:30px;margin:6px 0 8px;max-width:640px}
.cta p{color:#C5D0E3;max-width:600px}
.acts{display:flex;flex-wrap:wrap;gap:10px}
.btn{background:var(--blue);color:#fff;font-weight:600;padding:12px 22px;border-radius:10px;text-decoration:none;white-space:nowrap}
.btn.ghost{background:transparent;border:1px solid rgba(255,255,255,.3)}
.btn:hover,.btn:focus-visible{filter:brightness(1.1)}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:1000px){
  .flow{grid-template-columns:1fr;gap:0}
  .arr{padding:6px 0;transform:none}
  .arr .ah{display:inline-block;transform:rotate(90deg)}
  .arr small{display:inline;margin-left:8px}
  .analytics{grid-template-columns:1fr 1fr}
  .bens{grid-template-columns:1fr 1fr}
  .fa,.feat,.sensor{grid-template-columns:1fr}
  .feat.rev .ftxt{order:0}
  .kpis{grid-template-columns:1fr 1fr}
  .totals{grid-template-columns:repeat(3,1fr)}
  .count{margin-left:0;width:100%}
}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  section{padding:52px 0}
  .hero h1{margin-top:38px}
  .pillars{grid-template-columns:1fr}
  .analytics,.bens{grid-template-columns:1fr}
  .gal{grid-template-columns:1fr}.g.wide{grid-column:auto}.g img{height:220px}
  .totals{grid-template-columns:1fr 1fr}
  .cb{grid-template-columns:1fr;gap:12px}
  .ch{flex-direction:column;align-items:flex-start}
  .cm{width:100%;justify-content:space-between}.cm div{text-align:left}
  .spec th{width:46%}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.bar{display:none}.case,.ben,.an,.feat{break-inside:avoid}}
"""

JS = """
(function(){
  var q=document.getElementById('q'),sort=document.getElementById('sort'),list=document.getElementById('caselist'),
      count=document.getElementById('count'),empty=document.getElementById('empty'),
      orig=[].slice.call(list.children),TOTAL=orig.length;
  function apply(){
    var term=q.value.trim().toLowerCase(),k=sort.value,kids=orig.slice(),shown=0;
    if(k==='name')kids.sort(function(a,b){return a.dataset.name.localeCompare(b.dataset.name)});
    else if(k!=='default')kids.sort(function(a,b){return b.dataset[k]-a.dataset[k]});
    kids.forEach(function(c){var ok=!term||c.dataset.q.indexOf(term)>-1;c.hidden=!ok;if(ok)shown++;list.appendChild(c)});
    count.textContent=shown===TOTAL?'Showing all '+TOTAL+' customers':'Showing '+shown+' of '+TOTAL+' customers';
    empty.hidden=!!shown;
  }
  q.addEventListener('input',apply);sort.addEventListener('change',apply);apply();
})();
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Condition Based Monitoring · Faclon Labs</title>
<meta name="description" content="Wireless tri-axial vibration sensors and the I/O Sense platform detect 50+ common faults across pumps, motors, fans, gearboxes and more, with automated diagnostics and maintenance recommendations.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Predictive maintenance · Rotating equipment</span></div>
  <a class="back" href="../">← All solutions</a>
  <h1>{E(C["hero"]["title"])}</h1>
  <p class="lede">{E(C["hero"]["tagline"])}. Wireless tri-axial vibration sensors on every critical machine, with the I/O Sense platform turning the signals into fault diagnoses and recommended actions for the maintenance team.</p>
  <ul class="pillars">{pillars}</ul>
  <div class="kpis">
    <div class="kp"><b>50+</b><span>Common problems identified</span></div>
    <div class="kp"><b>{len(cases)}</b><span>Customers in case studies</span></div>
    <div class="kp"><b>{num(T_ASSETS)}</b><span>Assets monitored</span></div>
    <div class="kp"><b>{num(T_SENSORS)}</b><span>Sensors installed</span></div>
  </div>
  <nav class="jump" aria-label="On this page"><a href="#how">How it works</a><a href="#benefits">Benefits</a><a href="#faults">Faults &amp; assets</a><a href="#platform">Platform</a><a href="#sensor">Sensor</a><a href="#installs">Installations</a><a href="#cases">Case studies</a></nav>
</div></header>

<main>
<section id="how"><div class="wrap">
  <div class="eyebrow">Predictive maintenance · Architecture</div>
  <h2>From the machine to a maintenance decision</h2>
  <p class="sub">Sensors are fixed to each machine and send readings over Wi-Fi. The data reaches the I/O Sense Digitization Suite over 4G, where it is checked, analysed and turned into alerts, reports and dashboards.</p>
  <figure class="archfig" id="arch"><a href="#how" class="lbx" aria-label="Close enlarged diagram">×</a><a href="#arch" class="zoom" aria-label="Enlarge architecture diagram"><img src="{img(A["img"])}" alt="{E(A["alt"])}"></a>
    <figcaption>Predictive maintenance architecture<span>Tap to enlarge</span></figcaption></figure>
  <h3 class="steph">Step by step</h3>
  <div class="flow">
    <div class="node"><span class="k">Assets</span><b>Rotating equipment</b><p>{E(assets_short)} and more</p></div>
    <div class="arr"><span class="ah">→</span></div>
    <div class="node"><span class="k">Sensors</span><b>Tri-axial vibration sensors</b><p>Wi-Fi-enabled transmission of</p><div class="chips">{transmits}</div></div>
    <div class="arr"><span class="ah">→</span></div>
    <div class="node"><span class="k">Network</span><b>Wi-Fi router</b><p>One router serves a group of sensors</p></div>
    <div class="arr"><span class="ah">→</span><small>4G</small></div>
    <div class="node core"><span class="k">Faclon</span><b>I/O Sense Digitization Suite</b><p>Analytics | Automation | AI</p></div>
    <div class="arr"><span class="ah">→</span></div>
    <div class="node out"><span class="k">Faclon I/O Sense Platform</span><ul>{outputs}</ul></div>
  </div>
  <div class="analytics">{analytics}</div>
</div></section>

<section class="panel" id="benefits"><div class="wrap">
  <div class="eyebrow" style="color:var(--green)">Predictive maintenance · Benefits</div>
  <h2>What plants gain</h2>
  <p class="sub">Machines stay available for longer, failures are caught early, and maintenance teams spend their time fixing problems rather than collecting readings.</p>
  <div class="bens">{benefits}</div>
  <p class="note">Benefit figures are indicative and depend on each plant’s assets and maintenance baseline.</p>
</div></section>

<section id="faults"><div class="wrap">
  <div class="eyebrow">Coverage</div>
  <h2>50+ common problems identified, across a variety of assets</h2>
  <p class="sub">Each fault leaves its own pattern in the vibration, temperature and noise of a machine. The platform recognises these patterns and names the likely fault.</p>
  <div class="fa">
    <div class="box"><h3>Problems identified</h3><p class="hint">50+ common problems, including</p><ul class="flist">{faults}<li class="more">And many more</li></ul></div>
    <div class="box"><h3>Assets covered</h3><p class="hint">Works across a variety of rotating assets</p><ul class="flist alist">{assets}<li class="more">And many more</li></ul></div>
  </div>
</div></section>

<section class="panel" id="platform"><div class="wrap">
  <div class="eyebrow">I/O Sense platform key features</div>
  <h2>Diagnoses and actions, not just data</h2>
  <p class="sub">Every monitored asset carries a risk level, the fault found and the recommended solution, with the full vibration spectrum one click away.</p>
  {features}
</div></section>

<section id="sensor"><div class="wrap">
  <div class="eyebrow">Hardware</div>
  <h2>Sensor details</h2>
  <p class="sub">A compact sensor that measures vibration on three axes, temperature and noise, built for harsh plant conditions.</p>
  <div class="sensor">
    <div class="sph"><img src="{img(C["sensor"]["img"])}" alt="Faclon tri-axial vibration sensor, a small black cube with a cable">
      <div class="chips"><span>IP67</span><span>78 g</span><span>0.2 Hz to 6 kHz</span><span>Stud or magnetic mount</span></div></div>
    <table class="spec"><tbody>{specs}</tbody></table>
  </div>
</div></section>

<section class="panel" id="installs"><div class="wrap">
  <div class="eyebrow">In the field</div>
  <h2>Installation images</h2>
  <p class="sub">Sensors are mounted directly on bearing housings, casings and drive ends, with no change to the machine.</p>
  <div class="gal">{gallery}</div>
</div></section>

<section id="cases"><div class="wrap">
  <div class="eyebrow" style="color:var(--green)">Case studies</div>
  <h2>Running across power, cement, steel, process and buildings</h2>
  <p class="sub">Deployments by customer: the plants covered, how many assets and sensors, which machines, and the issues the system found.</p>
  <div class="totals">
    <div><b>{len(cases)}</b><span>Customers</span></div>
    <div><b>{T_PLANTS}</b><span>Plants</span></div>
    <div><b>{num(T_ASSETS)}</b><span>Assets</span></div>
    <div><b>{num(T_SENSORS)}</b><span>Sensors</span></div>
    <div><b>{ISSUES_LABEL}</b><span>Issues identified</span></div>
  </div>
  <div class="bar">
    <label class="search" for="q">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Search customer, machine or fault, e.g. ID fan, soft foot" aria-label="Search case studies">
    </label>
    <select id="sort" aria-label="Order">
      <option value="default">Default order</option><option value="s">Most sensors</option><option value="a">Most assets</option><option value="n">Most issues found</option><option value="name">Customer A–Z</option>
    </select>
    <div class="count" id="count">Showing all {len(cases)} customers</div>
  </div>
  <div class="cases" id="caselist">{case_cards}</div>
  <div class="empty" id="empty" hidden>No case studies match. Try a machine such as “pump” or a fault such as “bearing”.</div>
</div></section>
</main>

<div class="cta"><div class="wrap">
  <div><div class="k">Next step</div><h2>Your digital backbone for operational efficiency and decision intelligence</h2><p>Tell us which machines matter most in your plant. We will show you what condition-based monitoring can catch on them.</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Condition Based Monitoring</span><span>Predictive maintenance for rotating equipment</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
