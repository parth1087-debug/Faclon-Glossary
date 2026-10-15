"""Builds steam-trap-monitoring/index.html (Steam Trap Failure Detection).

Run from anywhere:  python3 src/steam-trap-monitoring/build_page.py
Content lives in content.json next to this script; edit it and re-run. Fields:
  hero          {title, lede, kpis[] {value, label}}
  why[]         {t title, d text, o: true to colour it as an outcome (green)}
  failures[]    {n number, t name, sig temperature signature, d what happens, impact}
  business_case {note, lines[] {line, traps, leaking, loss, steam (MT/yr), save (₹ lakh/yr)},
                 total (₹ lakh/yr), assumptions[] [label, text], plus[] other benefits}
  install[]     {t title, points[]}
  platform[]    feature list;  views[] {t, d} dashboard views
  node[] / gateway[]  hardware specification lines
  cases[]       {logo (file stem in src/faclon-overview/assets), customer, site, metric,
                 metric_label, d, ongoing: true for deployments in progress}
  contact       {name, phone, tel, email, web}
Customer logos are read from src/faclon-overview/assets/ and embedded as data URIs.
"""
import base64
import html
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))
from cta import CTA_BUTTONS  # noqa: E402

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagrams  # noqa: E402  inline SVG architecture diagrams

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "steam-trap-monitoring" / "index.html"
ASSETS = ROOT / "src" / "faclon-overview" / "assets"
D = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape


def logo(stem):
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg")):
        p = ASSETS / f"{stem}.{ext}"
        if p.exists():
            return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
    raise FileNotFoundError(stem)


def lakh(v):
    return f"₹{v:.2f} L"


# ---------- sections ----------
h = D["hero"]
kpis = "".join(f'<div class="kp"><b>{E(k["value"])}</b><span>{E(k["label"])}</span></div>' for k in h["kpis"])

why = "".join(
    f'<article class="why{" o" if w.get("o") else ""}"><h3>{E(w["t"])}</h3><p>{E(w["d"])}</p></article>'
    for w in D["why"])


def gauge(sig):
    """Two-thermometer badge: which side of the trap gives the failure away."""
    hi_out = "outlet" in sig.lower()
    def side(name, on, up):
        cls = "on" if on else ""
        arrow = ("▲ High" if up else "▼ Low") if on else "Normal"
        return f'<div class="th {cls}{" up" if up else ""}"><small>{name}</small><b>{arrow}</b></div>'
    return (f'<div class="gauge">{side("Inlet", not hi_out, False)}'
            f'<svg viewBox="0 0 64 28" width="64" height="28" aria-hidden="true"><path d="M0 14h18M46 14h18" stroke="currentColor" stroke-width="3"/>'
            f'<rect x="18" y="4" width="28" height="20" rx="6" fill="none" stroke="currentColor" stroke-width="2.5"/></svg>'
            f'{side("Outlet", hi_out, True)}</div>')


fails = "".join(
    f'<article class="fail"><div class="fail-top"><span class="num">{f["n"]}</span><h3>{E(f["t"])}</h3></div>'
    f'{gauge(f["sig"])}<p>{E(f["d"])}</p><div class="impact"><b>Impact</b>{E(f["impact"])}</div></article>'
    for f in D["failures"])

bc = D["business_case"]
mx = max(l["save"] for l in bc["lines"])
bars = "".join(
    f'<div class="brow"><span class="bl">{E(l["line"])}</span>'
    f'<div class="btrack"><div class="bfill" style="width:{l["save"] / mx * 100:.1f}%"></div></div>'
    f'<span class="bv">{lakh(l["save"])}</span></div>' for l in bc["lines"])
rows = "".join(
    f'<tr><th scope="row">{E(l["line"])}</th><td>{l["traps"]}</td><td>{l["leaking"]}</td><td>{E(l["loss"])}</td>'
    f'<td>{l["steam"]} MT</td><td class="g">{lakh(l["save"])}</td></tr>' for l in bc["lines"])
assum = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in bc["assumptions"])
plus = "".join(f"<li>{E(p)}</li>" for p in bc["plus"])

FIGS = [diagrams.header_install(), diagrams.hx_install()]
install = "".join(
    f'<article class="inst"><h3>{E(i["t"])}</h3><figure class="fig">{FIGS[n]}</figure><p class="swipe">Swipe sideways to see the whole diagram →</p><ol>'
    + "".join(f"<li>{E(p)}</li>" for p in i["points"]) + "</ol></article>" for n, i in enumerate(D["install"]))

features = "".join(f"<li>{E(p)}</li>" for p in D["platform"])
views = "".join(f'<article class="view"><h3>{E(v["t"])}</h3><p>{E(v["d"])}</p></article>' for v in D["views"])
node = "".join(f"<li>{E(x)}</li>" for x in D["node"])
gw = "".join(f"<li>{E(x)}</li>" for x in D["gateway"])

cases = "".join(
    f'<article class="case"><div class="clogo"><img src="{logo(c["logo"])}" alt="{E(c["customer"])}"></div>'
    f'<div class="cbody"><div class="chead"><h3>{E(c["customer"])}</h3><span class="site">{E(c["site"])}</span>'
    f'{"<span class=pill>Ongoing</span>" if c.get("ongoing") else ""}</div><p>{E(c["d"])}</p></div>'
    f'<div class="cmet"><b>{E(c["metric"])}</b><span>{E(c["metric_label"])}</span></div></article>'
    for c in D["cases"])

ct = D["contact"]

NAV = [("how", "How it works"), ("failures", "Failure modes"), ("why", "Why Faclon"), ("value", "Business case"),
       ("install", "Installation"), ("platform", "Platform"), ("hardware", "Hardware"), ("customers", "Customers")]
nav = "".join(f'<a href="#{i}">{E(t)}</a>' for i, t in NAV)

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FDF3E3;--red:#B5452F;--redBg:#FBEDEA;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:64px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
ul,ol{list-style:none}
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
.hero h1{font-size:clamp(34px,5.2vw,56px);font-weight:700;margin:56px 0 18px;max-width:860px}
.hero h1 em{font-style:normal;color:var(--blue2)}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:720px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:36px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:26px;display:block;line-height:1.25}
.kp:nth-child(1) b,.kp:nth-child(3) b{color:#6FD3A8}
.kp span{font-size:12.5px;color:#9FB0CC}

.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:10px;padding-bottom:10px;scrollbar-width:none}
.nav .wrap::-webkit-scrollbar{display:none}
.nav a{flex:none;font-size:13.5px;color:var(--ink2);text-decoration:none;padding:6px 11px;border-radius:8px}
.nav a:hover,.nav a.cur{background:var(--blueBg);color:var(--blue)}
a:focus-visible{outline:2px solid var(--blue);outline-offset:1px}

section{padding:64px 0 8px}
.sh{max-width:760px;margin-bottom:28px}
.sh h2{font-size:clamp(26px,3.2vw,34px);font-weight:700;margin:8px 0 10px}
.sh p{color:var(--ink2);font-size:16px}

/* how it works */
.flowx{display:grid;grid-template-columns:1.2fr auto 1fr auto 1.3fr;align-items:stretch;gap:0}
.fx{border:1px solid var(--line);border-radius:16px;padding:18px 20px;background:#fff}
.fx.cloud{background:var(--navy);color:#fff;border-color:var(--navy)}
.fx small{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.fx.cloud small{color:var(--blue2)}
.fx h3{font-size:18px;margin:4px 0 6px}
.fx p{font-size:13.5px;color:var(--ink2)}
.fx.cloud p{color:#C5D0E3}
.link{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 10px;min-width:110px;text-align:center}
.link b{font-size:12px;font-weight:700;color:var(--blue)}
.link span{font-size:11.5px;color:var(--mute)}
.link i{display:block;width:100%;height:2px;margin:6px 0;background:repeating-linear-gradient(90deg,var(--blue) 0 6px,transparent 6px 11px);position:relative}
.link i:after{content:"";position:absolute;right:-2px;top:-4px;border:5px solid transparent;border-left:7px solid var(--blue)}
.dcs{margin:12px 0 0 auto;width:min(100%,520px);border:1px dashed #B9C6E8;border-radius:12px;padding:12px 16px;font-size:13.5px;color:var(--ink2);background:var(--blueBg)}
.dcs b{color:var(--blue)}
.feat{margin-top:22px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.feat li{background:var(--bg);border-radius:10px;padding:10px 12px;font-size:13.5px;color:var(--ink2);display:flex;gap:8px;align-items:flex-start}
.feat li:before{content:"";flex:none;width:7px;height:7px;border-radius:50%;background:var(--blue);margin-top:7px}

/* failure modes */
.fails{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.fail{border:1px solid var(--line);border-radius:16px;padding:18px;display:flex;flex-direction:column;gap:12px;min-width:0}
.fail-top{display:flex;align-items:center;gap:10px}
.num{flex:none;width:28px;height:28px;border-radius:50%;background:var(--redBg);color:var(--red);font-weight:700;font-size:13px;display:grid;place-items:center}
.fail h3{font-size:18px}
.fail p{font-size:13.5px;color:var(--ink2)}
.gauge{display:flex;align-items:center;justify-content:space-between;gap:6px;background:var(--bg);border-radius:12px;padding:10px 12px;color:#9AA7BB}
.th{display:flex;flex-direction:column;min-width:0}
.th:last-child{text-align:right}
.th small{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.th b{font-size:13.5px;color:var(--mute);font-weight:600}
.th.on b{color:var(--blue)}
.th.on.up b{color:var(--red)}
.impact{margin-top:auto;font-size:13px;color:var(--ink2);border-top:1px solid var(--line);padding-top:10px}
.impact b{display:block;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin-bottom:2px}
.rule{margin-top:16px;font-size:13.5px;color:var(--ink2);background:var(--bg);border-radius:12px;padding:12px 16px}

/* why */
.whys{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.why{border:1px solid var(--line);border-top:3px solid var(--blue);border-radius:14px;padding:18px 20px}
.why.o{border-top-color:var(--green)}
.why h3{font-size:17px;margin-bottom:8px}
.why p{font-size:13.5px;color:var(--ink2)}

/* business case */
.bc{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:20px;align-items:start}
.panel{background:var(--bg);border-radius:16px;padding:22px}
.total small{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.total b{display:block;font-size:44px;line-height:1.1;color:var(--green);margin:4px 0 2px}
.total span{font-size:13.5px;color:var(--ink2)}
.bars{margin-top:20px;display:flex;flex-direction:column;gap:10px}
.brow{display:grid;grid-template-columns:90px minmax(0,1fr) 78px;gap:10px;align-items:center;font-size:13.5px}
.bl{color:var(--ink2)}
.btrack{height:14px;background:#fff;border-radius:7px;overflow:hidden}
.bfill{height:100%;background:var(--green);border-radius:7px}
.bv{text-align:right;font-weight:700;color:var(--green)}
.plus{margin-top:20px;font-size:13.5px;color:var(--ink2)}
.plus b{display:block;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin-bottom:6px}
.plus li{padding:3px 0 3px 18px;position:relative}
.plus li:before{content:"+";position:absolute;left:2px;color:var(--green);font-weight:700}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:520px}
th,td{padding:10px 12px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap}
thead th{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);background:var(--bg);font-weight:700;white-space:normal;vertical-align:bottom}
th[scope=row],thead th:first-child{text-align:left}
td.g{color:var(--green);font-weight:700}
tfoot td,tfoot th{border-bottom:0;font-weight:700}
tfoot td.g{font-size:15px}
.note{font-size:12.5px;color:var(--mute);margin-top:12px}
dl.as{margin-top:16px;display:grid;gap:8px}
dl.as div{display:grid;grid-template-columns:170px minmax(0,1fr);gap:12px;font-size:13.5px}
dl.as dt{color:var(--mute);font-weight:600}
dl.as dd{color:var(--ink2)}

/* install */
.insts{display:grid;grid-template-columns:minmax(0,1fr);gap:18px}
.inst ol{display:grid!important;grid-template-columns:1fr 1fr;gap:10px 28px}
.inst{border:1px solid var(--line);border-radius:16px;padding:20px 22px}
.inst h3{font-size:18px;margin-bottom:12px}
.inst ol{counter-reset:s;display:flex;flex-direction:column;gap:10px}
.inst li{counter-increment:s;position:relative;padding-left:34px;font-size:14px;color:var(--ink2)}
.inst li:before{content:counter(s);position:absolute;left:0;top:0;width:22px;height:22px;border-radius:6px;background:var(--blueBg);color:var(--blue);font-size:12px;font-weight:700;display:grid;place-items:center}

/* platform */
.views{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.view{background:var(--bg);border-radius:14px;padding:18px 20px}
.view h3{font-size:16px;margin-bottom:6px}
.view p{font-size:13.5px;color:var(--ink2)}

/* hardware */
.hw{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.spec{border:1px solid var(--line);border-radius:16px;padding:20px 22px}
.spec h3{font-size:18px;margin:4px 0 12px}
.spec li{font-size:14px;color:var(--ink2);padding:7px 0;border-top:1px solid var(--line)}
.spec li:first-child{border-top:0}

/* customers */
.cases{display:flex;flex-direction:column;gap:12px}
.case{display:grid;grid-template-columns:120px minmax(0,1fr) 170px;gap:20px;align-items:center;border:1px solid var(--line);border-radius:16px;padding:16px 20px}
.clogo{height:64px;display:grid;place-items:center}
.clogo img{max-width:110px;max-height:60px;object-fit:contain}
.chead{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin-bottom:4px}
.chead h3{font-size:17px}
.site{font-size:13px;color:var(--mute)}
.pill{font-size:11px;font-weight:600;color:var(--amber);background:var(--amberBg);border-radius:20px;padding:2px 9px}
.case p{font-size:14px;color:var(--ink2)}
.cmet{text-align:right}
.cmet b{display:block;font-size:26px;line-height:1.1;color:var(--green)}
.cmet span{font-size:12.5px;color:var(--mute)}

.cta{background:var(--navy);color:#fff;margin-top:64px}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta h2{font-size:30px;margin:6px 0 8px}
.cta p{color:#C5D0E3;max-width:600px}
.contact{display:flex;flex-direction:column;gap:8px;min-width:0}
.btn{background:var(--blue);color:#fff;font-weight:600;padding:12px 22px;border-radius:10px;text-decoration:none;text-align:center}
.btn.ghost{background:transparent;border:1px solid rgba(255,255,255,.25)}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}

/* architecture diagrams */
.fig{margin:0;border:1px solid var(--line);border-radius:16px;background:#fff;padding:12px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.fig svg{display:block;width:100%;height:auto;min-width:680px}
.fig figcaption{font-size:12.5px;color:var(--mute);padding:6px 6px 0}
.inst .fig{background:var(--bg);border:0;margin-bottom:16px}
.dg text{font-family:Inter,system-ui,sans-serif;fill:var(--ink2);font-size:13px}
.dg .b{font-weight:600;fill:var(--ink)}
.dg .eb{font-size:10.5px;font-weight:700;letter-spacing:.12em;fill:var(--mute)}
.dg .eb.a,.dg .a{fill:var(--blue)}
.dg .o{fill:#C25A0E}.dg .bl{fill:#2F6FB5}.dg .m{fill:var(--mute);font-size:12px}
.dg .v{writing-mode:vertical-rl;font-size:12px;fill:#2F4F8F}
.dg .dots{font-size:22px;fill:var(--mute);font-weight:700}
.dg .pipe{fill:none;stroke:#8A97AA;stroke-width:6;stroke-linejoin:round}
.dg .pipe.thin{stroke-width:4}
.dg .hdrl{stroke-width:8}
.dg .insul{fill:none;stroke:#F2E2B0;stroke-width:22;stroke-linejoin:round}
.dg .hdr{fill:#C9D1DC}.dg .hl{fill:var(--ink);font-weight:600}
.dg .well{fill:#C9D1DC}
.dg .trap rect{fill:#5B6778}.dg .trap line{stroke:#5B6778;stroke-width:4}
.dg .valve path{fill:#fff;stroke:#2F6FB5;stroke-width:2.5}.dg .valve line{stroke:#2F6FB5;stroke-width:2.5}.dg .valve .hdl{stroke:#C0392B;stroke-width:4}
.dg .lead{fill:none;stroke-width:3}.dg .lead.li{stroke:#E0701B}.dg .lead.lo{stroke:#4A8FE0}
.dg .rtd.ri{fill:#E0701B}.dg .rtd.ro{fill:#4A8FE0}
.dg .nbox{fill:#9FC8B6;stroke:#4E8A72;stroke-width:2}.dg .nface{fill:#E8F1EC;stroke:#4E8A72;stroke-width:2}
.dg .ant{stroke:#2A3340;stroke-width:3;stroke-linecap:round}
.dg .wave{fill:none;stroke:var(--mute);stroke-width:1.6}
.dg .gbox{fill:#9FC8B6;stroke:#4E8A72;stroke-width:2}.dg .gt{fill:#173A2C;font-weight:700;font-size:13px}.dg .gt.s{font-weight:500;font-size:11.5px}
.dg .cbox{fill:var(--navy)}.dg .ct{fill:#fff;font-weight:700;font-size:15px}.dg .cs{fill:var(--blue2);font-size:12px}
.dg .radio{fill:none;stroke:#E0701B;stroke-width:2.2;stroke-dasharray:2 6;stroke-linecap:round}
.dg .flow{fill:none;stroke:var(--blue);stroke-width:2.2}.dg .flow.dash{stroke-dasharray:6 5}.dg .flow.g{stroke:var(--mute);stroke-width:1.6}
.dg .data{fill:none;stroke:#E0701B;stroke-width:2.2}
.dg .opt{fill:var(--blueBg);stroke:#B9C6E8;stroke-dasharray:5 4}
.dg .out{fill:var(--greenBg);stroke:#CDE9DC}
.dg .pillar{fill:#B9CCF0}
.dg .bldg{fill:#EEF1F6;stroke:#9AA7BB;stroke-width:2}.dg .win{stroke:#B9C6E8;stroke-width:8}.dg .mast{stroke:#2A3340;stroke-width:3}
.dg .hx{fill:#fff;stroke:#2A3340;stroke-width:2.5}.dg .coil{fill:none;stroke:#2A3340;stroke-width:2.5}
.dg .tag{fill:#fff;stroke:#6B7A90;stroke-width:2}
.dg .sys{fill:#fff;stroke:#2A3340;stroke-width:1.6}
.arch{margin-bottom:8px}
.swipe{display:none;font-size:12px;color:var(--mute);margin:-8px 0 14px}
.flowx,.dcs{display:none}

@media (max-width:1000px){
  .flowx{grid-template-columns:minmax(0,1fr)}.link{flex-direction:row;gap:10px;padding:10px 0;min-width:0}
  .link i{width:2px;height:28px;margin:0;order:-1;background:repeating-linear-gradient(180deg,var(--blue) 0 6px,transparent 6px 11px)}
  .link i:after{right:-4px;top:auto;bottom:-6px;border:5px solid transparent;border-top:7px solid var(--blue)}
  .dcs{margin-left:0}
  .fails{grid-template-columns:1fr 1fr}.feat{grid-template-columns:1fr 1fr}.whys,.views{grid-template-columns:1fr 1fr}
  .bc{grid-template-columns:minmax(0,1fr)}.kpis{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  .hero h1{margin-top:40px}.kp b{font-size:21px}
  .arch{display:none}.flowx{display:grid}.dcs{display:block}.inst ol{grid-template-columns:1fr}.swipe{display:block}
  .fig svg{min-width:640px}
  section{padding-top:48px}
  .fails,.feat,.whys,.views,.insts,.hw{grid-template-columns:minmax(0,1fr)}
  .case{grid-template-columns:1fr;gap:10px}.clogo{justify-content:start;height:48px}.cmet{text-align:left}
  dl.as div{grid-template-columns:1fr;gap:0}
  .brow{grid-template-columns:80px minmax(0,1fr) 70px}
  .total b{font-size:38px}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.nav{display:none}.fail,.why,.case,.spec,.inst,.view{break-inside:avoid}}
"""

JS = """
(function(){
  var links=[].slice.call(document.querySelectorAll('.nav a'));
  if(!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('cur',a.getAttribute('href')==='#'+e.target.id)})}
  })},{rootMargin:'-45% 0px -50% 0px'});
  links.forEach(function(a){var s=document.querySelector(a.getAttribute('href'));if(s)io.observe(s)});
})();
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Steam Trap Failure Detection · Faclon Labs</title>
<meta name="description" content="Wireless, temperature-based steam trap failure detection: leaking, flooding, choking and non-operational traps caught in real time, with ROI in under a year.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Steam trap monitoring · Process industries</span></div>
  <a class="back" href="../">← All solutions</a>
  <h1>Steam Trap <em>Failure Detection</em></h1>
  <p class="lede">{E(h["lede"])}</p>
  <div class="kpis">{kpis}</div>
</div></header>

<nav class="nav" aria-label="Sections"><div class="wrap">{nav}</div></nav>

<main>
<section id="how"><div class="wrap">
  <div class="sh"><div class="eyebrow">How it works</div><h2>From the trap to an alert, with no cables</h2>
  <p>A battery node on each trap reads its inlet and outlet temperature and radios it to a gateway. The gateway sends it to the I/O Sense cloud, where every trap gets a live status, a diagnosis and its steam loss.</p></div>
  <figure class="fig arch">{diagrams.architecture()}<figcaption>System architecture. Header traps need no DCS connection; process data is an optional input.</figcaption></figure>
  <div class="flowx">
    <div class="fx"><small>On each trap</small><h3>Steam trap node</h3><p>Battery powered, conformally coated, flameproof enclosure, 2 temperature sensors on inlet and outlet.</p></div>
    <div class="link" aria-hidden="true"><b>Wireless LoRa</b><i></i><span>up to 1,000 m</span></div>
    <div class="fx"><small>At height, in the open</small><h3>Gateway</h3><p>Receives up to 30 trap nodes and buffers data locally.</p></div>
    <div class="link" aria-hidden="true"><b>4G</b><i></i><span>SIM uplink</span></div>
    <div class="fx cloud"><small>Analytics · Automation · AI</small><h3>I/O Sense Cloud</h3><p>Failure diagnosis, steam loss and saving, alerts, reports and maintenance logging.</p></div>
  </div>
  <div class="dcs"><b>Optional · DCS / Historian / API.</b> Key process parameters (control valve, header pressure, header temperature, steam flow, condensate temperature) let the algorithm run on real-time baselines. Not mandatory.</div>
  <ul class="feat">{features}</ul>
</div></section>

<section id="failures"><div class="wrap">
  <div class="sh"><div class="eyebrow">Types of failure detected</div><h2>The four ways a trap wastes steam or hurts the process</h2>
  <p>Each trap is judged against the saturated steam temperature. Which side of the trap is off, and in which direction, tells the failure apart.</p></div>
  <div class="fails">{fails}</div>
  <p class="rule"><b>The rule of thumb:</b> a high outlet temperature indicates leaking; a low inlet temperature indicates flooding, a non-operational trap or choking. On heat exchangers, control valve position sets the inlet baseline dynamically.</p>
</div></section>

<section id="why"><div class="wrap">
  <div class="sh"><div class="eyebrow">Steam trap management</div><h2>Why temperature-only, wireless monitoring</h2></div>
  <div class="whys">{why}</div>
</div></section>

<section id="value"><div class="wrap">
  <div class="sh"><div class="eyebrow">Business case per 100 traps</div><h2>Steam savings from catching leaks in a day, not 45</h2>
  <p>{E(bc["note"])}</p></div>
  <div class="bc">
    <div class="panel">
      <div class="total"><small>Total annual savings · indicative</small><b>{lakh(bc["total"])}</b><span>per year, per 100 traps, from leaking traps alone</span></div>
      <div class="bars">{bars}</div>
      <div class="plus"><b>On top of the steam savings</b><ul>{plus}</ul></div>
    </div>
    <div>
      <div class="tw"><table>
        <thead><tr><th>Pressure line</th><th>Traps</th><th>Leaking traps</th><th>Avg steam loss per trap</th><th>Steam saved / yr</th><th>Savings / yr</th></tr></thead>
        <tbody>{rows}</tbody>
        <tfoot><tr><th scope="row">Total</th><td>100</td><td>10</td><td></td><td>{sum(l["steam"] for l in bc["lines"]):,} MT</td><td class="g">{lakh(bc["total"])}</td></tr></tfoot>
      </table></div>
      <dl class="as">{assum}</dl>
      <p class="note">Values are indicative, in ₹ lakh per year per 100 traps, using the assumptions above; they are re-baselined against each plant’s trap count, pressures and steam cost.</p>
    </div>
  </div>
</div></section>

<section id="install"><div class="wrap">
  <div class="sh"><div class="eyebrow">Installation</div><h2>Two installation patterns</h2>
  <p>Header traps need only the node and gateway. Heat exchanger traps can also draw on DCS or historian data to baseline the trap against the live process.</p></div>
  <div class="insts">{install}</div>
</div></section>

<section id="platform"><div class="wrap">
  <div class="sh"><div class="eyebrow">I/O Sense platform</div><h2>What the maintenance team sees</h2></div>
  <div class="views">{views}</div>
</div></section>

<section id="hardware"><div class="wrap">
  <div class="sh"><div class="eyebrow">Hardware</div><h2>Built for hydrocarbon Zone 1 and all weather</h2></div>
  <div class="hw">
    <div class="spec"><div class="eyebrow">Node device</div><h3>Steam trap node</h3><ul>{node}</ul></div>
    <div class="spec"><div class="eyebrow">Gateway · ST-110</div><h3>LoRa to 4G gateway</h3><ul>{gw}</ul></div>
  </div>
</div></section>

<section id="customers"><div class="wrap">
  <div class="sh"><div class="eyebrow">Customer cases</div><h2>Running in refineries, upstream oil and chemicals</h2></div>
  <div class="cases">{cases}</div>
</div></section>
</main>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Your digital backbone for operational efficiency</div><h2>Start with a pilot on your traps</h2><p>Begin with a header of up to 30 traps on one gateway, see the failures and steam loss it surfaces, then scale across the plant.</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · Steam Trap Failure Detection</span><span>Steam trap monitoring for process industries</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
