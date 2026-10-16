"""Builds spb-closed-loop-soot-blowing/index.html: the SPB AI closed-loop soot blowing case study.

Run from anywhere:  python3 src/spb-closed-loop-soot-blowing/build_page.py
Content lives in content.json next to this script (from the ISB Case Study SPB v2 deck), one key per section:
  hero         eyebrow, title, sub, stats [[value, label]]
  arch         principles [[title, text]], legend [[kind, text]]; the network diagram itself is drawn below (ARCH)
  estimation   steps [[title, text]], note [lead, text]
  decision     objective, constraints [..], overrides [[trigger, action]], note
  safety       checks [[check, condition, persistence]], failsafe [..]
  dashboard    img (file name without .jpg in assets/, embedded as a data URI), title, alt
  performance  tiles [[value, label, colour b|g|""]], steam / sgr bar charts, note
  compare      rows [[parameter, before, after, delta]], note
  savings      tiles [[value, label]], lines [[line, calculation, result]], note
  validation   blocks [[title, text, accent b|r|n]], next
Edit the JSON and re-run; the page is regenerated in full.
"""
import base64
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src" / "shared"))
from cta import CTA_BUTTONS  # noqa: E402

OUT = ROOT / "spb-closed-loop-soot-blowing" / "index.html"
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape


def img(name):
    return "data:image/jpeg;base64," + base64.b64encode((HERE / "assets" / f"{name}.jpg").read_bytes()).decode()


def head(eyebrow, title, sub=""):
    s = f'<p class="sub">{E(sub)}</p>' if sub else ""
    return f'<div class="eyebrow">{E(eyebrow)}</div><h2>{E(title)}</h2>{s}'


def note(n, cls=""):
    return f'<div class="note {cls}"><b>{E(n[0])}</b> {E(n[1])}</div>'


h = C["hero"]
hero_stats = "".join(f'<div class="kp"><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in h["stats"])

# ---------- architecture diagram (drawn from the deck's Solution and Network Architecture slide) ----------
ARCH = """
<div class="net" role="img" aria-label="Network architecture: control network, OT South firewall, industrial DMZ and APC zone, OT North firewall, IT network, IT perimeter firewall, Faclon Cloud">
  <div class="nrow top">
    <div class="nbox"><b>Faclon Cloud</b></div>
    <span class="harr">←</span>
    <div class="nbox"><b>Manual lab entry</b><small>web form, direct to cloud</small></div>
    <div class="nbox rem"><b>Vendor / Faclon engineer</b><small>named account, MFA</small></div>
  </div>
  <div class="fw"><span></span><b>IT Perimeter firewall</b><span></span></div>
  <div class="zone it"><div class="zl"><b>IT network — Level 4</b><small>carries plant data in transit; no historian, collector or application component of this project resides here</small></div>
    <div class="nbox rem"><b>Remote access VPN</b><small>IT-owned, accounts issued by IT</small></div></div>
  <div class="fw"><span>outbound MQTT only</span><b>OT North firewall</b><span>1 inbound rule</span></div>
  <div class="mid">
    <div class="zone dmz"><div class="zl"><b>Industrial DMZ — Level 3.5</b></div>
      <div class="pair">
        <div class="nbox"><b>Data collector and historian</b><small>OPC UA client to the DCS<br>local store and forward buffer</small></div>
        <div class="nbox rem"><b>Jump host</b><small>second, separate authentication<br>all sessions recorded<br>credentials separate from corporate</small></div>
      </div></div>
    <div class="zone apc"><div class="zl"><b>APC zone</b></div>
      <div class="nbox wr"><b>APC execution engine</b><small>reads tags, writes setpoints<br>no default route — no path north<br>tuned from the jump host only</small></div></div>
  </div>
  <div class="flows"><span class="f-data">↓ OPC UA read</span><span class="f-rem">↓ RDP, scoped per account</span><span class="f-wr">↓ OPC UA read + write</span></div>
  <div class="fw"><span>no default route</span><b>OT South firewall</b><span>no inbound sessions into OT</span></div>
  <div class="zone ctl"><div class="zl"><b>Power plant control network — Levels 0–2</b></div>
    <div class="pair"><div class="nbox"><b>DCS controllers and HMI</b><small>vendor owned and supported</small></div>
    <div class="nbox"><b>OPC UA server</b><small>inside the control network</small></div></div></div>
</div>"""
legend = "".join(f'<span class="lg {k}"><i></i>{E(t)}</span>' for k, t in C["arch"]["legend"])
principles = "".join(f'<div class="pr"><h3>{E(t)}</h3><p>{E(x)}</p></div>' for t, x in C["arch"]["principles"])

es = C["estimation"]
est_steps = "".join(f'<div class="stp"><i>{i}</i><h3>{E(t)}</h3><p>{E(x)}</p></div>' for i, (t, x) in enumerate(es["steps"], 1))

d = C["decision"]
cons = "".join(f"<li>{E(x)}</li>" for x in d["constraints"])
ovr = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in d["overrides"])

s = C["safety"]
checks = "".join(f'<tr><td class="n">{i}</td><td>{E(a)}</td><td>{E(b)}</td><td class="p">{E(c)}</td></tr>' for i, (a, b, c) in enumerate(s["checks"], 1))
fails = "".join(f"<li>{E(x)}</li>" for x in s["failsafe"])

db = C["dashboard"]

p = C["performance"]
ptiles = "".join(f'<div class="pt {c}"><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l, c in p["tiles"])


def bars(chart, cls, lo=0.0):
    top = max(v for _, _, v in chart["bars"])
    out = []
    for i, (lab, sub, v) in enumerate(chart["bars"]):
        hpct = (v - lo) / (top - lo) * 100 if top > lo else 0
        out.append(f'<div class="bc"><div class="bv {cls if i else "base"}"><em>{(f"{v:.2f}" if v < 10 else f"{v:g}")}</em><span style="height:{hpct:.1f}%"></span></div>'
                   f'<div class="bl">{E(lab)}<small>{E(sub)}</small></div></div>')
    foot = f'<div class="cf">{E(chart["foot"])}</div>' if chart.get("foot") else ""
    return f'<div class="chart"><h4 class="{cls}">{E(chart["title"])}</h4><div class="bars">{"".join(out)}</div>{foot}</div>'


steam_chart = bars(p["steam"], "b")
sgr_chart = bars(p["sgr"], "g", p["sgr"]["axis_from"])

cp = C["compare"]
crow = "".join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td class="dl">{E(dd)}</td></tr>' for a, b, c, dd in cp["rows"])

sv = C["savings"]
stiles = "".join(f'<div class="st{" tot" if i == 2 else ""}"><b>{E(v)}</b><span>{E(l)}</span></div>' for i, (v, l) in enumerate(sv["tiles"]))
slines = "".join(f'<tr><td>{E(a)}</td><td class="calc">{E(b)}</td><td class="res">{E(c)}</td></tr>' for a, b, c in sv["lines"])

va = C["validation"]
vblocks = "".join(f'<div class="vb {k}"><h3>{E(t)}</h3><p>{E(x)}</p></div>' for t, x, k in va["blocks"])

NAV = [("architecture", "Architecture"), ("estimation", "Estimation"), ("decision", "Decision"), ("safety", "Safety"),
       ("live", "Live system"), ("performance", "Performance"), ("savings", "Savings"), ("validation", "Validation")]
nav = "".join(f'<a href="#{i}">{E(t)}</a>' for i, t in NAV)

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--line2:#CDD5E0;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FBF3E6;--red:#B5452F;--redBg:#FBEFEC;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:70px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
ul{list-style:none}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4{letter-spacing:-.015em;line-height:1.2;text-wrap:balance}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
h2{font-size:clamp(26px,3.2vw,34px);font-weight:700;margin:8px 0 6px}
.sub{font-size:16.5px;color:var(--ink2);max-width:820px}
h3{font-size:16.5px;font-weight:700;margin-bottom:6px}
p{color:var(--ink2)}

.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(17,135,95,.32),rgba(17,135,95,0) 68%)}
.hero .wrap{position:relative;padding-top:34px;padding-bottom:52px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand a{color:#fff;text-decoration:none;font-weight:700;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hero .eyebrow{color:#7FD9B3;margin-top:48px}
.hero h1{font-size:clamp(36px,5.4vw,60px);font-weight:700;margin:12px 0 14px;max-width:880px}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:760px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:34px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:30px;display:block;line-height:1.2}
.kp span{font-size:12.5px;color:#9FB0CC}

.jump{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.jump .wrap{display:flex;gap:6px;align-items:center;padding-top:10px;padding-bottom:10px;overflow-x:auto;scrollbar-width:none}
.jump .wrap::-webkit-scrollbar{display:none}
.jump a{flex:none;font-size:13.5px;color:var(--ink2);text-decoration:none;padding:6px 11px;border-radius:8px;white-space:nowrap}
.jump a:hover{background:var(--bg);color:var(--ink)}
.jump a.home{background:var(--blueBg);color:var(--blue);font-weight:600;margin-right:6px}

section{padding:64px 0}
section.alt{background:var(--bg)}
.note{margin-top:22px;padding:14px 18px;border-radius:12px;background:var(--blueBg);border:1px solid #D6DEFF;font-size:14.5px;color:var(--ink)}
.note b{color:var(--blue)}
.note.g{background:var(--greenBg);border-color:#CDE9DC}.note.g b{color:var(--green)}
.note.a{background:var(--amberBg);border-color:#EED9B4}.note.a b{color:var(--amber)}

/* network diagram */
.net{margin-top:28px;border:1px solid var(--line);border-radius:16px;padding:18px;background:#fff;display:flex;flex-direction:column;gap:10px}
.nbox{border:1px solid var(--line2);border-radius:10px;padding:9px 12px;background:#fff;text-align:center;min-width:0}
.nbox b{display:block;font-size:13.5px;font-weight:700}
.nbox small{display:block;font-size:11.5px;color:var(--mute);line-height:1.4;margin-top:2px}
.nbox.rem{border-color:#E1B877;background:#FFFCF6}
.nbox.wr{border-color:#8FD0B4;background:#F4FBF8}
.nrow.top{display:grid;grid-template-columns:1fr auto 1.2fr 1.2fr;gap:12px;align-items:center}
.harr{color:var(--mute);font-size:18px}
.fw{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:center;border:1.5px solid #E4A898;background:var(--redBg);border-radius:10px;padding:7px 14px}
.fw b{font-size:13px;color:var(--red);text-align:center}
.fw span{font-size:11.5px;color:var(--ink2)}.fw span:last-child{text-align:right}
.zone{border-radius:12px;padding:12px 14px;border:1.5px solid var(--line2);background:var(--bg)}
.zone .zl b{display:block;font-size:13.5px;font-weight:700}
.zone .zl small{display:block;font-size:11.5px;color:var(--mute);line-height:1.4}
.zone.it{display:grid;grid-template-columns:1fr 280px;gap:16px;align-items:center}
.zone.dmz{border-color:#9FB2FA;background:#F5F7FF}
.zone.apc{border-color:#8FD0B4;background:#F2FAF6}
.zone.ctl{border-color:#E7CDBE;background:#FBF6F2}
.zone .pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}
.zone .nbox{background:#fff}
.mid{display:grid;grid-template-columns:2fr 1fr;gap:12px}
.mid .zone.apc .nbox{margin-top:10px}
.flows{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;font-size:12px;font-weight:600}
.f-data{color:var(--mute)}.f-rem{color:var(--amber);text-align:center}.f-wr{color:var(--green);text-align:right}
.legend{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:12px;font-size:12.5px;color:var(--ink2)}
.lg i{display:inline-block;width:18px;height:3px;border-radius:2px;margin-right:8px;vertical-align:3px;background:var(--mute)}
.lg.remote i{background:var(--amber)}.lg.write i{background:var(--green)}
.princ{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:28px}
.pr{border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fff;border-top:3px solid var(--blue)}
.pr:last-child{border-top-color:var(--green)}
.pr p{font-size:14.5px}

/* estimation */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:28px;counter-reset:s}
.stp{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px;position:relative}
.stp i{font-style:normal;display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;font-size:13px;margin-bottom:10px}
.stp p{font-size:14px}

/* decision */
.dec{display:grid;grid-template-columns:1fr 1fr 1.25fr;gap:14px;margin-top:28px;align-items:start}
.box{border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fff}
.dec>*,.saf>*,.perf>*{min-width:0}.box{overflow-x:auto}
.box.obj{background:var(--bg)}
.box p{font-size:14.5px}
.dash li{position:relative;padding:4px 0 4px 18px;font-size:14px;color:var(--ink2)}
.dash li:before{content:"";position:absolute;left:0;top:13px;width:9px;height:2px;background:var(--blue)}
table.t{width:100%;border-collapse:collapse;font-size:14px}
table.t th{text-align:left;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);padding:9px 12px;border-bottom:2px solid var(--ink)}
table.t td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink2);line-height:1.45}
table.t td:first-child{color:var(--ink);font-weight:600}
.box h3 small{display:block;font-size:12px;font-weight:500;color:var(--mute);margin-top:2px}

/* safety */
.saf{display:grid;grid-template-columns:1.5fr 1fr;gap:20px;margin-top:28px;align-items:start}
.saf table.t td.n{color:var(--blue);font-weight:700;width:34px}
.saf table.t td.p{white-space:nowrap;color:var(--mute)}
.saf .box{background:var(--greenBg);border-color:#CDE9DC}
.saf .box h3{color:var(--green)}
.saf .dash li:before{background:var(--green)}
.saf .dash li{color:var(--ink)}

/* dashboard */
.shot{margin-top:28px;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 1px 2px rgba(15,27,45,.04),0 12px 32px -18px rgba(15,27,45,.25)}
.shot img{display:block;width:100%;height:auto}
.shot figcaption{font-size:13px;color:var(--mute);padding:10px 16px;border-top:1px solid var(--line)}

/* performance */
.perf{display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:14px;margin-top:28px;align-items:stretch}
.ptiles{display:flex;flex-direction:column;gap:10px}
.pt{border:1px solid var(--line);border-radius:12px;padding:14px 18px;background:#fff}
.pt b{display:block;font-size:30px;line-height:1.15;font-weight:700;letter-spacing:-.02em}
.pt span{font-size:13px;color:var(--ink2)}
.pt.g b{color:var(--green)}
.pt.b{background:var(--blueBg);border-color:#C9D4FF}.pt.b b{color:var(--blue)}
.chart{border:1px solid var(--line);border-radius:14px;padding:18px;background:#fff;display:flex;flex-direction:column}
.chart h4{font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue)}
.chart h4.g{color:var(--green)}
.bars{flex:1;display:flex;gap:22px;align-items:flex-end;justify-content:center;min-height:240px;padding-top:24px;border-bottom:1px solid var(--line2)}
.bc{flex:0 1 120px;display:flex;flex-direction:column;height:100%}
.bv{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center}
.bv em{font-style:normal;font-weight:700;font-size:17px;margin-bottom:6px}
.bv span{display:block;width:100%;border-radius:6px 6px 0 0;background:#AEBBCC}
.bv.b span{background:var(--blue)}.bv.b em{color:var(--blue)}
.bv.g span{background:var(--green)}.bv.g em{color:var(--green)}
.bv.base em{color:var(--ink2)}
.bl{position:relative;top:10px;text-align:center;font-size:12.5px;color:var(--ink2);height:0}
.bl small{display:block;color:var(--mute)}
.cf{margin-top:44px;font-size:12.5px;color:var(--mute);text-align:center}
.bars+.cf{margin-top:44px}
.chart .bars{margin-bottom:46px}
.chart .bars+.cf{margin-top:6px}

/* compare */
.cmpw{margin-top:28px;overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:#fff}
.cmpw table.t th,.cmpw table.t td{padding:13px 16px}
.cmpw table.t td.dl{color:var(--green);font-weight:700;white-space:nowrap}
.cmpw table.t th:nth-child(3){color:var(--blue)}

/* savings */
.stiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:28px}
.st{border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fff}
.st b{display:block;font-size:30px;font-weight:700;color:var(--green);letter-spacing:-.02em;line-height:1.15}
.st span{font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.st.tot{background:var(--navy);border-color:var(--navy)}.st.tot b{color:#7FD9B3}.st.tot span{color:#9FB0CC}
.calcw{margin-top:16px;overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:#fff}
.calcw table.t td.calc{color:var(--ink2)}
.calcw table.t td.res{color:var(--green);font-weight:700;white-space:nowrap;text-align:right}
.calcw table.t th:last-child{text-align:right}

/* validation */
.vgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:28px}
.vb{border:1px solid var(--line);border-left:4px solid var(--blue);border-radius:12px;padding:16px 18px;background:#fff}
.vb.r{border-left-color:var(--red);background:var(--bg)}.vb.n{border-left-color:var(--ink2);background:var(--bg)}
.vb.r h3{color:var(--red)}
.vb p{font-size:14px}
.vgrid .vb:nth-child(4),.vgrid .vb:nth-child(5){grid-column:span 1}
.next{margin-top:16px;display:flex;gap:18px;align-items:center;padding:16px 20px;border-radius:12px;background:var(--blue);color:#fff;font-size:15.5px;font-weight:500}
.next b{flex:none;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:#DCE3FF}

.cta{background:var(--navy);color:#fff}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta .eyebrow{color:var(--blue2)}
.cta h2{color:#fff;margin-bottom:8px}
.cta p{color:#C5D0E3;max-width:600px}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

@media (max-width:1000px){
  .steps{grid-template-columns:1fr 1fr}.dec{grid-template-columns:1fr 1fr}.dec .box:last-child{grid-column:1/-1}
  .saf{grid-template-columns:1fr}.perf{grid-template-columns:1fr 1fr}.perf .ptiles{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr}
  .vgrid{grid-template-columns:1fr 1fr}
}
@media (max-width:760px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  section{padding:48px 0}.kpis{grid-template-columns:1fr 1fr}.hero .eyebrow{margin-top:36px}
  .princ,.steps,.dec,.perf,.perf .ptiles,.stiles,.vgrid{grid-template-columns:1fr}
  .net{padding:12px}.nrow.top{grid-template-columns:1fr}.harr{display:none}
  .fw{grid-template-columns:1fr;text-align:center;gap:2px}.fw span:last-child{text-align:center}
  .zone.it,.mid,.zone .pair,.flows{grid-template-columns:1fr}.flows span{text-align:left!important}
  .next{flex-direction:column;align-items:flex-start;gap:4px}
  .saf table.t td.p{white-space:normal}
  .box{padding:14px}table.t td,table.t th{padding:9px 8px}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.jump{display:none}.box,.pt,.chart,.vb,.stp,.pr{break-inside:avoid}}
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>SPB AI Closed-Loop Soot Blowing · Faclon Labs</title>
<meta name="description" content="Case study: AI closed-loop soot blowing on SPB's 16 MW recovery boiler, with architecture, estimation and decision layers, safety interlocks and certified savings.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../">Faclon Labs</a><span>Case study · Power</span></div>
  <a class="back" href="../">← All solutions</a>
  <div class="eyebrow">{E(h["eyebrow"])}</div>
  <h1>{E(h["title"])}</h1>
  <p class="lede">{E(h["sub"])}</p>
  <div class="kpis">{hero_stats}</div>
</div></header>

<nav class="jump" aria-label="Sections"><div class="wrap"><a class="home" href="../">← All solutions</a>{nav}</div></nav>

<section id="architecture"><div class="wrap">
  {head("Architecture", C["arch"]["title"])}
  {ARCH}
  <div class="legend">{legend}</div>
  <h3 style="margin-top:40px;font-size:20px">{E(C["arch"]["principles_title"])}</h3>
  <div class="princ" style="margin-top:14px">{principles}</div>
</div></section>

<section id="estimation" class="alt"><div class="wrap">
  {head("Estimation layer", es["title"], es["sub"])}
  <div class="steps">{est_steps}</div>
  {note(es["note"], "a")}
</div></section>

<section id="decision"><div class="wrap">
  {head("Decision layer", d["title"], d["sub"])}
  <div class="dec">
    <div class="box obj"><h3>Objective</h3><p>{E(d["objective"])}</p></div>
    <div class="box"><h3>Hard constraints</h3><ul class="dash">{cons}</ul></div>
    <div class="box"><h3>Event-driven overrides</h3><table class="t"><thead><tr><th>Trigger</th><th>Action</th></tr></thead><tbody>{ovr}</tbody></table></div>
  </div>
  {note(d["note"])}
</div></section>

<section id="safety" class="alt"><div class="wrap">
  {head("Safety", s["title"], s["sub"])}
  <div class="saf">
    <div class="box" style="background:#fff;border-color:var(--line)"><table class="t"><thead><tr><th>#</th><th>Check</th><th>Condition</th><th>Persistence</th></tr></thead><tbody>{checks}</tbody></table></div>
    <div class="box"><h3>Fail-safe behaviours</h3><ul class="dash">{fails}</ul></div>
  </div>
</div></section>

<section id="live"><div class="wrap">
  {head("Live system", db["title"])}
  <figure class="shot"><img src="{img(db["img"])}" alt="{E(db["alt"])}" loading="lazy"><figcaption>{E(db["title"])} dashboard</figcaption></figure>
</div></section>

<section id="performance" class="alt"><div class="wrap">
  {head("Results", p["title"], p["sub"])}
  <div class="perf"><div class="ptiles">{ptiles}</div>{steam_chart}{sgr_chart}</div>
  {note(p["note"])}
  <h3 style="margin-top:48px;font-size:22px">{E(cp["title"])}</h3>
  <p class="sub" style="margin-top:4px">{E(cp["sub"])}</p>
  <div class="cmpw"><table class="t"><thead><tr><th>Parameter</th><th>Before (manual)</th><th>After (AI ISB)</th><th>Delta</th></tr></thead><tbody>{crow}</tbody></table></div>
  {note(cp["note"], "g")}
</div></section>

<section id="savings"><div class="wrap">
  {head("Savings", sv["title"], sv["sub"])}
  <div class="stiles">{stiles}</div>
  <div class="calcw"><table class="t"><thead><tr><th>Line</th><th>Calculation</th><th>Result</th></tr></thead><tbody>{slines}</tbody></table></div>
  <div class="note g">{E(sv["note"])}</div>
</div></section>

<section id="validation" class="alt"><div class="wrap">
  {head("Validation", va["title"])}
  <div class="vgrid">{vblocks}</div>
  <div class="next"><b>Next step</b><span>{E(va["next"])}</span></div>
</div></section>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow">Next step</div><h2>Put closed-loop soot blowing on your boiler</h2><p>Faclon reads your existing DCS from outside the control network, learns your boiler from its own history and blows only where it pays.</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · SPB AI Closed-Loop Soot Blowing</span><span>Case study · 16 MW recovery boiler</span></div></div>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
