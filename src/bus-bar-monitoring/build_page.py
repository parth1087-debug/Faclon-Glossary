"""Builds bus-bar-monitoring/index.html (online bus-bar joint temperature monitoring).

Run from anywhere:  python3 src/bus-bar-monitoring/build_page.py
Content lives in content.json next to this script:
  problems[]     {name, desc}           root causes shown in the "Why" section
  consequences[] strings                what those causes lead to
  flow[]         {name, sub, link}      architecture steps, left to right; link = label on the arrow to the next step
  hardware[]     {id, name, short, img, role, specs[[label, value]]}   one tab per device
  screens[]      {name, img, desc}      I/O Sense platform screens, one tab each
  roi            {basis, rows[{metric, label, value}], net{label, value}}   indicative ROI exactly as the deck states it
  install[]      {img, cap}             installation photos
  architecture   labels for the architecture diagram (wide SVG on desktop, tall SVG on phones)
  img            file name (without .jpg) in assets/, embedded as a data URI
Source: Faclon "Bus Bar Monitoring" deck. Edit the JSON and re-run; the page is regenerated in full.
All content is in the HTML; the script only switches tabs (without JS every tab is shown).
"""
import base64
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "bus-bar-monitoring" / "index.html"
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape


def img(name):
    data = base64.b64encode((HERE / "assets" / f"{name}.jpg").read_bytes()).decode()
    return f"data:image/jpeg;base64,{data}"


# ---------- sections ----------
problems = "".join(f'<li><b>{E(p["name"])}</b><span>{E(p["desc"])}</span></li>' for p in C["problems"])
conseq = "".join(f"<li>{E(c)}</li>" for c in C["consequences"])

flow = ""
for i, f in enumerate(C["flow"]):
    arrow = f'<div class="arrow"><span>{E(f["link"])}</span></div>' if f["link"] else ""
    via = f'<small class="via">{E(f["link"])} →</small>' if f["link"] else ""
    flow += (f'<li class="node"><div class="nbox"><em>{i + 1:02d}</em><b>{E(f["name"])}</b>'
             f'<span>{E(f["sub"])}</span>{via}</div>{arrow}</li>')

# ---------- architecture diagram (two SVGs: wide for desktop, tall for phones) ----------
A = C["architecture"]
STRAP, RECV, GW = img("strap"), img("receiver"), img("gateway")


def t(x, y, s, cls="lb", anchor="middle"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{E(s)}</text>'


def cloud(cx, cy, k=1.0):
    return (f'<g transform="translate({cx} {cy}) scale({k})"><path class="cl" d="M-38 18h76a22 22 0 0 0 2-44 '
            f'30 30 0 0 0-57-8 22 22 0 0 0-21 52z"/><path class="ck" d="M-12 2h24M-12 -6h24M-12 10h24"/></g>')


def devices(cx, cy, k=1.0):
    return (f'<g transform="translate({cx} {cy}) scale({k})"><rect class="dv" x="-46" y="-30" width="64" height="42" rx="4"/>'
            f'<path class="dv" d="M-54 16h80l-6 6h-68z"/><rect class="dv" x="28" y="-24" width="24" height="44" rx="5"/>'
            f'<path class="ck" d="M37 14h6"/></g>')


def arrow(x1, y1, x2, y2, mid="ah"):
    return f'<path class="ar" d="M{x1} {y1}L{x2} {y2}" marker-end="url(#{mid})"/>'


DEFS = ('<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        '<path d="M0 0L10 5L0 10z" class="ahf"/></marker></defs>')  # .format(mid=...)

# wide
w = [DEFS.replace('{mid}', 'ah')]
for i, y in enumerate((20, 232)):
    w += [f'<rect class="pn" x="10" y="{y}" width="500" height="188" rx="14"/>',
          t(28, y + 26, f"Panel {i + 1}", "pk", "start"),
          f'<image href="{STRAP}" x="44" y="{y + 40}" width="74" height="133"/>',
          t(170, y + 92, A["straps"], "lb", "start"), t(170, y + 112, A["straps_sub"], "sb", "start"),
          arrow(300, y + 100, 372, y + 100), t(336, y + 90, A["rf"], "sb"),
          f'<image href="{RECV}" x="384" y="{y + 30}" width="94" height="136"/>',
          t(431, y + 182, A["receiver_sub"], "sb"),
          f'<path class="bus" d="M478 {y + 100}H548"/>']
w += ['<path class="bus" d="M548 120V332"/>', f'<text x="538" y="226" class="bl" text-anchor="middle" transform="rotate(-90 538 226)">{E(A["bus"])}</text>',
      arrow(548, 226, 620, 226).replace('M548', 'M552'),
      f'<image href="{GW}" x="628" y="152" width="130" height="154"/>',
      t(693, 330, A["gateway"]), t(693, 349, A["gateway_sub"], "sb"), t(693, 366, A["gateway_cap"], "sb"),
      arrow(768, 226, 848, 226), t(808, 214, A["uplink"], "sb"),
      cloud(935, 226, 1.15), t(935, 286, A["cloud"]), t(935, 304, A["cloud_sub"], "sb"),
      arrow(1012, 226, 1044, 226),
      devices(1104, 226, 1.0), t(1094, 286, A["users"]), t(1094, 304, A["users_sub"], "sb")]
wide = (f'<svg class="arch-h" viewBox="0 0 1180 432" role="img" aria-label="{E(A["title"])}">' + "".join(w) + "</svg>")

# tall
v = [DEFS.replace('{mid}', 'av')]
for i, x in enumerate((6, 186)):
    cx = x + 84
    v += [f'<rect class="pn" x="{x}" y="6" width="168" height="270" rx="12"/>',
          t(x + 12, 26, f"Panel {i + 1}", "pk", "start"),
          f'<image href="{STRAP}" x="{x + 14}" y="36" width="44" height="80"/>',
          t(x + 66, 66, "R · Y · B", "lb", "start"), t(x + 66, 84, "straps", "sb", "start"),
          arrow(cx, 124, cx, 156, 'av'), t(cx + 8, 145, "RF 10 m", "sb", "start"),
          f'<image href="{RECV}" x="{cx - 32}" y="160" width="64" height="93"/>',
          t(cx, 268, A["receiver_sub"], "sb"),
          f'<path class="bus" d="M{cx} 276V304"/>']
v += ['<path class="bus" d="M90 304H270"/>', t(180, 322, A["bus"], "bl"),
      arrow(180, 330, 180, 356, 'av'),
      f'<image href="{GW}" x="128" y="362" width="104" height="123"/>',
      t(180, 506, A["gateway"]), t(180, 524, A["gateway_sub"], "sb"), t(180, 540, A["gateway_cap"], "sb"),
      arrow(180, 552, 180, 586, 'av'),
      cloud(180, 620, 1.1), t(180, 670, A["cloud"]), t(180, 688, A["cloud_sub"], "sb"),
      arrow(180, 700, 180, 732, 'av'),
      devices(185, 772, 1.0), t(180, 822, A["users"]), t(180, 840, A["users_sub"], "sb")]
tall = (f'<svg class="arch-v" viewBox="0 0 360 852" role="img" aria-label="{E(A["title"])}">' + "".join(v) + "</svg>")
arch = f'<figure class="arch">{wide}{tall}</figure>'

hw_tabs, hw_panels = "", ""
for i, h in enumerate(C["hardware"]):
    sel = "true" if i == 0 else "false"
    hw_tabs += (f'<button class="tab" role="tab" id="t-{h["id"]}" aria-controls="p-{h["id"]}" '
                f'aria-selected="{sel}" type="button">{E(h["short"])}</button>')
    specs = "".join(f"<tr><th>{E(k)}</th><td>{E(v)}</td></tr>" for k, v in h["specs"])
    hw_panels += (f'<div class="panel hw" role="tabpanel" id="p-{h["id"]}" aria-labelledby="t-{h["id"]}">'
                  f'<figure class="hwimg"><img src="{img(h["img"])}" alt="{E(h["name"])}" loading="lazy"></figure>'
                  f'<div><div class="eyebrow">{E(h["short"])}</div><h3>{E(h["name"])}</h3><p class="role">{E(h["role"])}</p>'
                  f'<table class="specs"><tbody>{specs}</tbody></table></div></div>')

sc_tabs, sc_panels = "", ""
for i, s in enumerate(C["screens"]):
    sid = f"s{i}"
    sel = "true" if i == 0 else "false"
    sc_tabs += (f'<button class="tab" role="tab" id="t-{sid}" aria-controls="p-{sid}" '
                f'aria-selected="{sel}" type="button">{E(s["name"])}</button>')
    sc_panels += (f'<div class="panel scr" role="tabpanel" id="p-{sid}" aria-labelledby="t-{sid}">'
                  f'<p>{E(s["desc"])}</p><figure class="shot"><img src="{img(s["img"])}" '
                  f'alt="I/O Sense {E(s["name"])} screen" loading="lazy"></figure></div>')

roi = C["roi"]
roi_rows = "".join(
    f'<li><div><b>{E(r["metric"])}</b><span>{E(r["label"])}</span></div><strong>{E(r["value"])}</strong></li>'
    for r in roi["rows"])

install = "".join(
    f'<figure><img src="{img(p["img"])}" alt="{E(p["cap"])}" loading="lazy"><figcaption>{E(p["cap"])}</figcaption></figure>'
    for p in C["install"])

installed_img = img("strap-installed")

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--red:#B5452F;--redBg:#FBEEEA;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:64px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
ul,ol{list-style:none}
img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3{letter-spacing:-.015em;line-height:1.2;text-wrap:balance}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}

.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.32),rgba(124,149,255,0) 68%)}
.hero .wrap{position:relative;padding-top:34px;padding-bottom:56px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hgrid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:40px;align-items:end;margin-top:48px}
.hero h1{font-size:clamp(34px,5vw,54px);font-weight:700;margin:12px 0 18px}
.hero h1 em{font-style:normal;color:var(--blue2)}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:640px}
.hphoto{border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.12)}
.hphoto figcaption{font-size:12px;color:#9FB0CC;background:var(--navy2);padding:8px 12px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:40px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:26px;display:block}
.kp span{font-size:12.5px;color:#9FB0CC}
.kp.g b{color:#7FD6B2}

.jump{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.jump .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:10px;padding-bottom:10px;scrollbar-width:none}
.jump a{flex:none;text-decoration:none;color:var(--ink2);font-size:14px;padding:6px 12px;border-radius:8px}
.jump a:hover{background:var(--bg);color:var(--ink)}

.sec{padding:72px 0}
.sec.alt{background:var(--bg)}
.sh{max-width:720px;margin-bottom:32px}
.sh h2{font-size:clamp(26px,3.4vw,34px);font-weight:700;margin:8px 0 10px}
.sh p{color:var(--ink2);font-size:16.5px}

.why{display:grid;grid-template-columns:minmax(0,1fr) 48px minmax(0,1fr);gap:16px;align-items:stretch}
.causes li{border:1px solid #F0D9D2;background:#fff;border-left:4px solid var(--red);border-radius:12px;padding:14px 16px;margin-bottom:10px}
.causes b{display:block;font-size:16px;color:var(--red)}
.causes span{font-size:14px;color:var(--ink2)}
.to{display:flex;align-items:center;justify-content:center;color:var(--mute);font-size:24px}
.effects{background:var(--navy);color:#fff;border-radius:16px;padding:22px 24px;display:flex;flex-direction:column;justify-content:center}
.effects .eyebrow{color:#F2A58F}
.effects ul{margin-top:12px;display:flex;flex-direction:column;gap:10px}
.effects li{padding-left:18px;position:relative;font-size:16px}
.effects li:before{content:"";position:absolute;left:0;top:9px;width:8px;height:8px;border-radius:50%;background:#F2A58F}
.hence{margin-top:22px;border:1.5px dashed var(--blue);border-radius:14px;padding:16px 20px;font-size:16px;color:var(--ink);background:var(--blueBg)}
.hence b{color:var(--blue)}

.flow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0}
.node{display:flex;align-items:stretch;min-width:0}
.nbox{flex:1;min-width:0;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:6px}
.nbox em{font-style:normal;font-size:11px;font-weight:700;letter-spacing:.14em;color:var(--blue)}
.nbox b{font-size:16px}
.nbox span{font-size:13.5px;color:var(--ink2)}
.node:nth-child(4) .nbox{border-color:#C9D4FB;background:var(--blueBg)}
.via{margin-top:auto;padding-top:8px;border-top:1px dashed var(--line);font-size:12px;font-weight:600;color:var(--blue)}
.arrow{flex:none;width:22px;display:flex;align-items:center;justify-content:center;position:relative}
.arrow:before{content:"";position:absolute;left:4px;right:6px;top:50%;border-top:2px dashed #9DB0F8}
.arrow:after{content:"";position:absolute;right:2px;top:calc(50% - 5px);border:5px solid transparent;border-left-color:var(--blue);border-right:0}
.arrow span{display:none;position:absolute;font-size:10.5px;color:var(--mute);line-height:1.25}
.arch{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;margin-bottom:22px}
.arch svg{display:block;width:100%;height:auto;font-family:Inter,system-ui,sans-serif}
.arch-v{display:none!important;max-width:380px;margin:0 auto}
.arch .pn{fill:var(--bg);stroke:var(--line)}
.arch .pk{font-size:11px;font-weight:700;letter-spacing:.14em;fill:var(--mute);text-transform:uppercase}
.arch .lb{font-size:14px;font-weight:700;fill:var(--ink)}
.arch .sb{font-size:12px;fill:var(--ink2)}
.arch .bl{font-size:12px;font-weight:700;fill:var(--amber)}
.arch .ar{stroke:var(--blue);stroke-width:2;stroke-dasharray:6 5;fill:none}
.arch .ahf{fill:var(--blue)}
.arch .bus{stroke:var(--amber);stroke-width:3;fill:none;stroke-linecap:round}
.arch .cl{fill:var(--blueBg);stroke:var(--blue);stroke-width:2}
.arch .ck{stroke:var(--blue);stroke-width:2;stroke-linecap:round;fill:none}
.arch .dv{fill:#fff;stroke:var(--ink2);stroke-width:2;stroke-linejoin:round}
@media (max-width:760px){.arch-h{display:none!important}.arch-v{display:block!important}.arch{padding:12px}}
.callout{margin-top:22px;font-size:15px;color:var(--ink2)}
.callout b{color:var(--green)}

.tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}
.tab{font:inherit;font-size:14px;font-weight:600;padding:8px 14px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink2);cursor:pointer}
.tab[aria-selected="true"]{background:var(--blueBg);border-color:var(--blue);color:var(--blue)}
.tab:focus-visible,a:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.js .panel[hidden]{display:none}
.panel+.panel{margin-top:28px}
.js .panel+.panel{margin-top:0}
.hw{display:grid;grid-template-columns:300px minmax(0,1fr);gap:32px;align-items:start;border:1px solid var(--line);border-radius:16px;padding:24px;background:#fff}
.hwimg{background:#fff;border-radius:12px;display:flex;justify-content:center}
.hwimg img{max-height:340px;width:auto}
.hw h3{font-size:22px;margin:6px 0 8px}
.role{color:var(--ink2);margin-bottom:14px}
.specs{width:100%;border-collapse:collapse;font-size:14px}
.specs th,.specs td{text-align:left;padding:8px 0;border-top:1px solid var(--line);vertical-align:top}
.specs th{width:38%;font-weight:600;color:var(--mute);padding-right:14px}
.strip{margin-top:22px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:20px;align-items:center}
.strip img{border-radius:12px}
.strip p{color:var(--ink2)}

.scr p{color:var(--ink2);max-width:760px;margin-bottom:14px}
.shot{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 10px 28px rgba(15,27,45,.06)}

.roi{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:32px;align-items:start}
.roibox{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff}
.roibox h3{font-size:14px;font-weight:600;color:var(--ink2);padding:14px 20px;background:var(--bg);border-bottom:1px solid var(--line)}
.roibox li{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 20px;border-bottom:1px solid var(--line)}
.roibox li b{font-size:20px;display:block}
.roibox li span{font-size:13.5px;color:var(--ink2)}
.roibox li strong{font-size:22px;color:var(--green);white-space:nowrap}
.roibox .net{background:var(--greenBg);border-bottom:0}
.roibox .net b{font-size:17px;color:var(--green)}
.roibox .net strong{font-size:28px}
.fine{font-size:12.5px;color:var(--mute);font-style:italic;margin-top:10px}
.gains li{display:flex;gap:12px;align-items:flex-start;padding:12px 0;border-top:1px solid var(--line)}
.gains li:first-child{border-top:0}
.gains i{flex:none;width:28px;height:28px;border-radius:8px;background:var(--greenBg);color:var(--green);display:flex;align-items:center;justify-content:center;font-style:normal;font-weight:700}
.gains b{display:block}
.gains span{color:var(--ink2);font-size:14px}

.gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.gallery figure{border-radius:14px;overflow:hidden;background:#fff;border:1px solid var(--line)}
.gallery img{aspect-ratio:4/3;object-fit:cover;width:100%}
.gallery figcaption{font-size:13px;color:var(--ink2);padding:10px 12px}

.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta h2{font-size:30px;margin:6px 0 8px}
.cta p{color:#C5D0E3;max-width:600px}
.btn{background:var(--blue);color:#fff;font-weight:600;padding:12px 22px;border-radius:10px;text-decoration:none;white-space:nowrap}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:980px){
  .hgrid,.roi{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}
  .flow{grid-template-columns:1fr}
  .node{flex-direction:column}
  .arrow{width:auto;height:46px}
  .arrow:before{left:50%;right:auto;top:4px;bottom:8px;border-top:0;border-left:2px dashed #9DB0F8}
  .arrow:after{left:calc(50% - 4px);right:auto;top:auto;bottom:2px;border:5px solid transparent;border-top-color:var(--blue);border-bottom:0}
  .arrow span{display:block;top:50%;left:calc(50% + 14px);transform:translateY(-50%);white-space:nowrap}
  .via{display:none}
  .why{grid-template-columns:1fr}.to{transform:rotate(90deg);height:24px}
  .hw{grid-template-columns:1fr}.hwimg img{max-height:240px}
  .gallery{grid-template-columns:1fr 1fr}.gallery figure:first-child{grid-column:1/-1}
}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  .hgrid{margin-top:36px}.sec{padding:52px 0}.hw{padding:16px}
  .strip{grid-template-columns:1fr}.gallery{grid-template-columns:1fr}
  .specs th{width:42%}.roibox li strong{font-size:19px}.roibox .net strong{font-size:24px}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.jump{display:none}.panel[hidden]{display:block!important}.hw,.roibox,.gallery figure{break-inside:avoid}}
"""

JS = """
document.documentElement.classList.add('js');
document.querySelectorAll('[role=tablist]').forEach(function(list){
  var tabs=[].slice.call(list.querySelectorAll('[role=tab]'));
  function show(t,focus){
    tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;
      document.getElementById(x.getAttribute('aria-controls')).hidden=!on});
    if(focus)t.focus();
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){show(t)});
    t.addEventListener('keydown',function(e){
      var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;
      if(d){e.preventDefault();show(tabs[(i+d+tabs.length)%tabs.length],true)}
    });
  });
  show(tabs[0]);
});
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Bus Bar Monitoring · Faclon Labs</title>
<meta name="description" content="Online bus-bar health monitoring: wireless temperature straps on every critical joint, live alerts and trends on the I/O Sense platform.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Electrical asset monitoring · Bus bars &amp; panels</span></div>
  <a class="back" href="../">← All solutions</a>
  <div class="hgrid">
    <div>
      <div class="eyebrow" style="color:var(--blue2)">Online bus-bar health monitoring</div>
      <h1>See every critical joint’s temperature, <em>live</em></h1>
      <p class="lede">Wireless sensor straps on each bus-bar joint report temperature every minute. When a joint starts to run hot, the right people get an alert before it turns into a fire, a trip or an unplanned shutdown.</p>
    </div>
    <figure class="hphoto"><img src="{installed_img}" alt="R, Y and B phase sensor straps fitted on bus-bar joints"><figcaption>Phase-coloured sensor straps fitted on bus-bar joints</figcaption></figure>
  </div>
  <div class="kpis">
    <div class="kp"><b>±1 °C</b><span>Sensor accuracy, no calibration</span></div>
    <div class="kp"><b>8–10 yrs</b><span>Replaceable sensor battery</span></div>
    <div class="kp"><b>60</b><span>Sensors per receiver</span></div>
    <div class="kp g"><b>{E(roi["net"]["value"])}</b><span>Indicative net annual return, 30 critical joints</span></div>
  </div>
</div></header>

<nav class="jump" aria-label="On this page"><div class="wrap">
  <a href="#why">Why monitor</a><a href="#how">How it works</a><a href="#hardware">Hardware</a><a href="#platform">Platform</a><a href="#value">Value</a><a href="#installs">Installations</a>
</div></nav>

<main>
<section class="sec" id="why"><div class="wrap">
  <div class="sh"><div class="eyebrow">Why monitor bus bars</div><h2>Joint failures build up quietly, then fail suddenly</h2>
  <p>Most bus-bar faults start at a joint. Periodic manual thermography only catches the problem if someone happens to look on the right day.</p></div>
  <div class="why">
    <ul class="causes">{problems}</ul>
    <div class="to" aria-hidden="true">→</div>
    <div class="effects"><div class="eyebrow">Which leads to</div><ul>{conseq}</ul></div>
  </div>
  <p class="hence">That is why plants need a <b>real-time</b> solution that puts bus-bar temperature data online, so these problems are caught and fixed early.</p>
</div></section>

<section class="sec alt" id="how"><div class="wrap">
  <div class="sh"><div class="eyebrow">How it works</div><h2>From joint to phone in five steps</h2>
  <p>No wiring to the hot side: the straps are battery powered and talk wirelessly to a receiver in the panel.</p></div>
  {arch}
  <ol class="flow">{flow}</ol>
  <p class="callout">Online continuous monitoring with critical alerts helps <b>avert major losses, increase safety and improve the upkeep</b> of electrical operations.</p>
</div></section>

<section class="sec" id="hardware"><div class="wrap">
  <div class="sh"><div class="eyebrow">Hardware</div><h2>Three devices, built for the panel</h2>
  <p>Pick a device to see its specifications.</p></div>
  <div class="tabs" role="tablist" aria-label="Hardware">{hw_tabs}</div>
  {hw_panels}
</div></section>

<section class="sec alt" id="platform"><div class="wrap">
  <div class="sh"><div class="eyebrow">I/O Sense platform</div><h2>One screen for every joint in the plant</h2>
  <p>Live status, alerts, trends and reports for the electrical and maintenance teams, on laptop or mobile.</p></div>
  <div class="tabs" role="tablist" aria-label="Platform screens">{sc_tabs}</div>
  {sc_panels}
</div></section>

<section class="sec" id="value"><div class="wrap">
  <div class="sh"><div class="eyebrow">Value</div><h2>What it is worth</h2>
  <p>An indicative ROI calculation for a plant with 30 critical bus-bar joints.</p></div>
  <div class="roi">
    <div>
      <div class="roibox"><h3>{E(roi["basis"])}</h3><ul>{roi_rows}
        <li class="net"><div><b>{E(roi["net"]["label"])}</b></div><strong>{E(roi["net"]["value"])}</strong></li></ul></div>
      <p class="fine">Indicative values per year, as calculated for 30 critical bus-bar joints. Re-baselined against each plant’s own incident, downtime and insurance data.</p>
    </div>
    <ul class="gains">
      <li><i>1</i><div><b>Fewer major incidents</b><span>A hot joint is flagged while it is still a maintenance job, not a fire or a flashover.</span></div></li>
      <li><i>2</i><div><b>Less unplanned downtime</b><span>Re-tightening and cleaning are planned into a shutdown instead of forced by a trip.</span></div></li>
      <li><i>3</i><div><b>Lower insurance costs</b><span>Continuous, recorded monitoring of critical electrical assets supports a lower risk profile.</span></div></li>
      <li><i>4</i><div><b>Safer, lighter inspections</b><span>Fewer manual thermal rounds near live panels, with every reading logged.</span></div></li>
    </ul>
  </div>
</div></section>

<section class="sec alt" id="installs"><div class="wrap">
  <div class="sh"><div class="eyebrow">Installations</div><h2>In the field</h2>
  <p>Straps fit on the flat, clean surface of the bus bar or lug, one colour per phase.</p></div>
  <div class="gallery">{install}</div>
</div></section>
</main>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Start with your critical joints</div><h2>Put your bus bars online</h2><p>Tell us how many panels and joints matter most. We will size the straps, receivers and gateway and show you what continuous monitoring is worth for your plant.</p></div>
  <a class="btn" href="https://www.faclonlabs.com">www.faclonlabs.com</a>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Bus Bar Monitoring</span><span>Digital backbone for operational efficiency</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
