"""Builds it-ot-integration/index.html (IT-OT Integration reference architecture).

Run from anywhere:  python3 src/it-ot-integration/build_page.py
Content lives in content.json next to this script; the architecture drawing is in
diagram.py. Edit either and re-run. content.json fields:
  hero            {lede, kpis[] {value, label}}
  key_points[]    short statements shown beside the drawing
  platforms[]     {name, level, status Core|Optional, color, role, notes}
  scope[]         {area, in, out};  scope_note
  vlans[]         [vlan, name, carries, present on];  vlan_note
  nat[]           [where, direction, what is translated];  nat_note
  routing[]       [device, default gateway, static / connected routes]
  firewalls[]     {id, name, sub, rules[] [#, source, destination, service, action, notes]};  fw_note
  flows[]         {t, steps[], alt[] optional extra step chains, rules, d}
  design_rules[]  [title, text]
  considerations[] [item, why it matters, status]  (status drives the filter chips)
  protocols[]     [protocol, typical devices, transport, converter, information required, host-side changes];  protocol_note
  hosts[]         [area, target host system, typical protocols];  hosts_note
  open_items[]    [question, what it decides]
  contact         {name, phone, tel, email, web}
The page names no customer and no equipment vendor; keep it that way.
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import diagram  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "it-ot-integration" / "index.html"
D = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")


def act(a):
    cls = "ok" if a == "Allow" else ("req" if "request" in a else "no")
    return f'<span class="act {cls}">{E(a)}</span>'


def table(head, rows, cls=""):
    th = "".join(f"<th>{E(h)}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


h = D["hero"]
kpis = "".join(f'<div class="kp"><b>{E(k["value"])}</b><span>{E(k["label"])}</span></div>' for k in h["kpis"])
keyp = "".join(f"<li>{E(k)}</li>" for k in D["key_points"])

plats = "".join(
    f'<article class="plat c-{E(p["color"])}{" opt" if p["status"] == "Optional" else ""}">'
    f'<div class="ptop"><h3>{E(p["name"])}</h3><span class="st {"core" if p["status"] == "Core" else "opt"}">{E(p["status"])}</span></div>'
    f'<div class="lvl">{E(p["level"])}</div><p class="role">{E(p["role"])}</p><p>{E(p["notes"])}</p></article>'
    for p in D["platforms"])


def chain(steps):
    return '<ol class="chain">' + "".join(f"<li><span>{E(x)}</span></li>" for x in steps) + "</ol>"


flows = "".join(
    f'<article class="flow"><div class="fh"><span class="fn">{i}</span><h3>{E(f["t"])}</h3><span class="rl">Rules {E(f["rules"])}</span></div>'
    + chain(f["steps"]) + "".join(chain(a) for a in f.get("alt", []))
    + f'<p>{E(f["d"])}</p></article>'
    for i, f in enumerate(D["flows"], 1))

rules = "".join(f'<article class="rule"><h3>{E(a)}</h3><p>{E(b)}</p></article>' for a, b in D["design_rules"])

vl = table(["VLAN", "Name", "Carries", "Present on"],
           [[f"<b>{E(a)}</b>", E(b), E(c), E(d)] for a, b, c, d in D["vlans"]], "t-vlan")
nat = table(["Where", "Direction", "What is translated"], [[f"<b>{E(a)}</b>", E(b), E(c)] for a, b, c in D["nat"]])
rt = table(["Device", "Default gateway", "Static / connected routes"], [[f"<b>{E(a)}</b>", E(b), E(c)] for a, b, c in D["routing"]])

fw_tabs = '<button class="chip on" data-fw="all">All firewalls</button>' + "".join(
    f'<button class="chip" data-fw="{E(f["id"])}">{E(f["name"])}</button>' for f in D["firewalls"])
fw_blocks = "".join(
    f'<div class="fwb" data-fw="{E(f["id"])}"><h3>{E(f["name"])} <small>{E(f["sub"])}</small></h3>'
    + table(["#", "Source", "Destination", "Service", "Action", "Notes"],
            [[f"<b>{E(r[0])}</b>", E(r[1]), E(r[2]), E(r[3]), act(r[4]), E(r[5])] for r in f["rules"]], "t-fw")
    + "</div>" for f in D["firewalls"])

statuses = []
for c in D["considerations"]:
    if c[2] not in statuses:
        statuses.append(c[2])
add_chips = f'<button class="chip on" data-st="all">All · {len(D["considerations"])}</button>' + "".join(
    f'<button class="chip" data-st="{slug(s)}">{E(s)} · {sum(1 for c in D["considerations"] if c[2] == s)}</button>' for s in statuses)
adds = "".join(
    f'<li class="add" data-st="{slug(c[2])}"><span class="an">{i}</span><div><b>{E(c[0])}</b><p>{E(c[1])}</p></div>'
    f'<span class="sts s-{slug(c[2])}">{E(c[2])}</span></li>'
    for i, c in enumerate(D["considerations"], 1))

prot = table(["Protocol", "Typical devices", "Transport · port", "Converter", "Information required", "Host-side changes · licences"],
             [[f"<b>{E(r[0])}</b>", E(r[1]), E(r[2]), E(r[3]), E(r[4]), E(r[5])] for r in D["protocols"]], "t-prot")

scope = "".join(
    f'<div class="sc"><div class="sa">{E(r["area"])}</div><div class="si"><small>In scope</small>{E(r["in"])}</div>'
    f'<div class="so"><small>Not in scope</small>{E(r["out"])}</div></div>' for r in D["scope"])

hosts = table(["#", "Area", "Target host system", "Typical protocol · interface"],
              [[str(i), E(a), f"<b>{E(b)}</b>", E(c)] for i, (a, b, c) in enumerate(D["hosts"], 1)])
opens = table(["#", "Question", "What it decides"],
              [[str(i), E(a), E(b)] for i, (a, b) in enumerate(D["open_items"], 1)])

ct = D["contact"]
NAV = [("architecture", "Architecture"), ("platforms", "Faclon platforms"), ("flows", "Traffic flows"),
       ("rules", "Design rules"), ("network", "VLAN · NAT · routing"), ("firewalls", "Firewall rules"),
       ("protocols", "Protocols"), ("added", "Considerations"), ("scope", "Scope"), ("survey", "Site survey")]
nav = "".join(f'<a href="#{i}">{E(t)}</a>' for i, t in NAV)

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FDF3E3;
--red:#B5452F;--redBg:#FBEDEA;--purple:#7B4FE0;--purpleBg:#F3EEFE;--slate:#2A3340;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:64px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
ul,ol{list-style:none}
button{font:inherit;cursor:pointer}
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
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:760px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:36px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:24px;display:block;line-height:1.25}
.kp:nth-child(4) b{color:#6FD3A8}
.kp span{font-size:12.5px;color:#9FB0CC}

.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;gap:4px;overflow-x:auto;padding-top:10px;padding-bottom:10px;scrollbar-width:none}
.nav .wrap::-webkit-scrollbar{display:none}
.nav a{flex:none;font-size:13.5px;color:var(--ink2);text-decoration:none;padding:6px 11px;border-radius:8px}
.nav a:hover,.nav a.cur{background:var(--blueBg);color:var(--blue)}
a:focus-visible,button:focus-visible{outline:2px solid var(--blue);outline-offset:1px}

section{padding:64px 0 8px}
.sh{max-width:780px;margin-bottom:26px}
.sh h2{font-size:clamp(26px,3.2vw,34px);font-weight:700;margin:8px 0 10px}
.sh p{color:var(--ink2);font-size:16px}
h3.sub{font-size:18px;margin:30px 0 12px}
.note{font-size:13px;color:var(--mute);margin-top:10px}

/* architecture */
.fig{margin:0;border:1px solid var(--line);border-radius:16px;background:#fff;padding:10px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.fig svg{display:block;width:100%;height:auto;min-width:980px}
.fig figcaption{font-size:12.5px;color:var(--mute);padding:8px 6px 2px}
.swipe{display:none;font-size:12px;color:var(--mute);margin:0 0 10px}
.legend{display:flex;flex-wrap:wrap;gap:8px 18px;margin:14px 0 0;font-size:12.5px;color:var(--ink2)}
.legend span{display:inline-flex;align-items:center;gap:7px}
.legend i{display:inline-block;width:22px;height:12px;border-radius:3px}
.keyp{margin-top:22px;display:grid;grid-template-columns:1fr 1fr;gap:10px 28px}
.keyp li{position:relative;padding-left:20px;font-size:14px;color:var(--ink2)}
.keyp li:before{content:"";position:absolute;left:2px;top:8px;width:8px;height:8px;border-radius:2px;background:var(--blue)}

.ad text{font-family:Inter,system-ui,sans-serif;fill:var(--ink2);font-size:11.5px}
.ad .a-tt{font-weight:600;fill:var(--ink);font-size:13px}
.ad .a-pt{font-weight:700;font-size:15px;fill:var(--ink)}
.ad .a-sm{font-size:11.5px;fill:var(--ink2)}
.ad .a-eb{font-size:11px;font-weight:700;letter-spacing:.12em;fill:var(--mute)}
.ad .a-lv{font-size:11px;font-weight:600;fill:var(--blue)}
.ad .a-mini{font-size:10px;font-weight:700;letter-spacing:.1em;fill:var(--mute)}
.ad .a-mb{fill:#4A5A70}
.ad .a-halo{paint-order:stroke;stroke:#F6F8FB;stroke-width:6px;stroke-linejoin:round}
.ad .a-cn{font-size:11.5px;fill:var(--ink2);font-weight:500}
.ad .a-badge{font-size:9.5px;font-weight:700;letter-spacing:.08em;fill:#fff}
.ad .a-bust{font-size:11px;font-weight:700;letter-spacing:.12em;fill:#fff}
.ad .a-ag{fill:var(--purple)}
.ad .a-band{fill:#FBFCFE;stroke:var(--line);stroke-width:1.2}
.ad .a-cons{fill:#fff}
.ad .a-l5{fill:#F4F7FD;stroke:#D6E0F4}
.ad .a-dmz{fill:#FFF9EF;stroke:#F1DDB7}
.ad .a-field{fill:#F6F8FB}
.ad .a-box{fill:#fff;stroke:#B9C3D2;stroke-width:1.2}
.ad .a-pill{fill:#fff;stroke:#9AA7BB;stroke-width:1.2}
.ad .a-dash{stroke-dasharray:5 4}
.ad .a-dash2{stroke-dasharray:6 4}
.ad .a-plat{stroke-width:2}
.ad .a-p-green{fill:#EAF6F1;stroke:var(--green)}
.ad .a-p-purple{fill:var(--purpleBg);stroke:var(--purple)}
.ad .a-p-navy{fill:#E9EDF6;stroke:#1E3A70}
.ad .a-p-blue{fill:var(--blueBg);stroke:var(--blue)}
.ad .a-p-dark{fill:#EDEFF2;stroke:var(--slate)}
.ad .a-ioc{fill:#FDF0DA;stroke:var(--amber);stroke-width:2.2}
.ad .a-fw{fill:#FBEDEA;stroke:var(--red);stroke-width:1.6}
.ad .a-sw{fill:#EEF2F8;stroke:#7D8CA3;stroke-width:1.2}
.ad .a-dev{fill:#fff;stroke:#5B6778;stroke-width:1.2}
.ad .a-liu{fill:#FDF3E3;stroke:#E0A54B;stroke-width:1.2}
.ad .a-ctl{fill:#fff;stroke:#D6E0F4;stroke-dasharray:4 4}
.ad .a-bus{fill:var(--navy)}
.ad .a-core{fill:var(--green)}
.ad .a-opt{fill:var(--purple)}
.ad .a-add{fill:var(--amber)}
.ad .a-ln{stroke:#8A97AA;stroke-width:1.4}
.ad .a-bl{stroke:var(--navy);stroke-width:2}
.ad .a-tr{stroke:#5B6778;stroke-width:3}
.ad .a-of{stroke:#E0701B;stroke-width:2.2}
.ad .a-up{stroke:var(--blue);stroke-width:2.4}
.ad .a-uph{fill:var(--blue)}

/* platforms */
.plats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.plat{border:1px solid var(--line);border-top:4px solid var(--c,var(--blue));border-radius:14px;padding:16px 18px;min-width:0}
.plat.opt{border-top-style:dashed}
.c-slate{--c:var(--amber)}.c-blue{--c:var(--blue)}.c-green{--c:var(--green)}.c-dark{--c:var(--slate)}.c-navy{--c:#1E3A70}.c-purple{--c:var(--purple)}
.ptop{display:flex;justify-content:space-between;align-items:center;gap:8px}
.plat h3{font-size:18px;color:var(--c)}
.st{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;border-radius:20px;padding:2px 9px}
.st.core{background:var(--greenBg);color:var(--green)}.st.opt{background:var(--purpleBg);color:var(--purple)}
.lvl{font-size:12px;color:var(--mute);margin-top:2px}
.plat .role{font-weight:600;color:var(--ink);margin:10px 0 6px;font-size:14px}
.plat p{font-size:13.5px;color:var(--ink2)}

/* flows */
.flows{display:grid;grid-template-columns:minmax(0,1fr);gap:12px}
.flow{border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.fh{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.fn{width:26px;height:26px;border-radius:50%;background:var(--blueBg);color:var(--blue);font-weight:700;font-size:13px;display:grid;place-items:center;flex:none}
.flow h3{font-size:17px}
.rl{margin-left:auto;font-size:12px;color:var(--mute);font-weight:600}
.chain{display:flex;flex-wrap:wrap;gap:6px 0;align-items:center;margin-bottom:8px}
.chain li{display:inline-flex;align-items:center}
.chain span{font-size:13px;background:var(--bg);border-radius:8px;padding:5px 10px;color:var(--ink)}
.chain li+li:before{content:"→";color:var(--blue);margin:0 7px;font-weight:700}
.flow p{font-size:13.5px;color:var(--ink2)}

/* design rules */
.rules{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.rule{background:var(--bg);border-radius:14px;padding:16px 18px}
.rule h3{font-size:15.5px;margin-bottom:6px}
.rule p{font-size:13.5px;color:var(--ink2)}

/* tables */
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:9px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:0}
thead th{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);background:var(--bg);font-weight:700}
td{color:var(--ink2)}td b{color:var(--ink)}
.t-fw,.t-prot{min-width:900px}.t-vlan{min-width:640px}
.act{display:inline-block;font-size:11.5px;font-weight:700;border-radius:20px;padding:2px 9px;white-space:nowrap}
.act.ok{background:var(--greenBg);color:var(--green)}.act.no{background:var(--redBg);color:var(--red)}.act.req{background:var(--amberBg);color:var(--amber)}
.fwb{margin-top:22px}.fwb h3{font-size:18px;margin-bottom:10px}.fwb h3 small{font-size:13px;color:var(--mute);font-weight:500;margin-left:6px}
.fwb[hidden]{display:none}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{border:1px solid var(--line);background:#fff;color:var(--ink2);border-radius:20px;padding:6px 14px;font-size:13px}
.chip.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.nets{display:grid;grid-template-columns:minmax(0,1fr);gap:4px}

/* considerations */
.adds{display:flex;flex-direction:column;gap:8px;margin-top:16px}
.add{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:14px;align-items:start;border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.add[hidden]{display:none}
.an{font-weight:700;color:var(--mute);font-size:13px;padding-top:2px}
.add b{font-size:14.5px}.add p{font-size:13.5px;color:var(--ink2);margin-top:2px}
.sts{font-size:11.5px;font-weight:600;border-radius:20px;padding:3px 10px;white-space:nowrap;background:var(--blueBg);color:var(--blue)}
.s-recommended{background:var(--greenBg);color:var(--green)}.s-site-survey{background:var(--amberBg);color:var(--amber)}
.s-option{background:var(--bg);color:var(--ink2)}.s-applied{background:var(--blueBg);color:var(--blue)}
.s-if-optional-modules-are-taken{background:var(--purpleBg);color:var(--purple)}
.count{font-size:13px;color:var(--mute);margin-top:10px}

/* scope */
.scope{display:flex;flex-direction:column;gap:10px}
.sc{display:grid;grid-template-columns:140px minmax(0,1.3fr) minmax(0,1fr);gap:14px;border:1px solid var(--line);border-radius:14px;padding:14px 18px;font-size:13.5px;color:var(--ink2)}
.sa{font-weight:700;color:var(--ink);font-size:14.5px}
.sc small{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:3px}
.si small{color:var(--green)}.so small{color:var(--red)}

.cta{background:var(--navy);color:#fff;margin-top:64px}
.cta .wrap{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}
.cta h2{font-size:30px;margin:6px 0 8px}
.cta p{color:#C5D0E3;max-width:620px}
.contact{display:flex;flex-direction:column;gap:8px;min-width:0}
.btn{background:var(--blue);color:#fff;font-weight:600;padding:12px 22px;border-radius:10px;text-decoration:none;text-align:center}
.btn.ghost{background:transparent;border:1px solid rgba(255,255,255,.25)}
.foot{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}
.foot .wrap{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}
.foot a{color:inherit;text-decoration:none}
.disc{font-size:12.5px;color:var(--mute);margin-top:22px;max-width:820px}

@media (max-width:1000px){
  .plats{grid-template-columns:1fr 1fr}.rules{grid-template-columns:1fr 1fr}.kpis{grid-template-columns:1fr 1fr}
}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  .hero h1{margin-top:40px}.kp b{font-size:20px}
  section{padding-top:48px}
  .swipe{display:block}.fig svg{min-width:900px}
  .plats,.rules,.keyp{grid-template-columns:minmax(0,1fr)}
  .sc{grid-template-columns:minmax(0,1fr);gap:8px}
  .add{grid-template-columns:24px minmax(0,1fr)}.add .sts{grid-column:2;justify-self:start}
  .rl{margin-left:0;width:100%}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.nav,.chips{display:none}.fwb[hidden],.add[hidden]{display:block!important}.plat,.rule,.flow,.add{break-inside:avoid}}
"""

JS = """
(function(){
  var links=[].slice.call(document.querySelectorAll('.nav a'));
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('cur',a.getAttribute('href')==='#'+e.target.id)})}
    })},{rootMargin:'-45% 0px -50% 0px'});
    links.forEach(function(a){var s=document.querySelector(a.getAttribute('href'));if(s)io.observe(s)});
  }
  function chips(sel,attr,items,after){
    var bs=[].slice.call(document.querySelectorAll(sel+' .chip'));
    bs.forEach(function(b){b.addEventListener('click',function(){
      bs.forEach(function(x){x.classList.toggle('on',x===b)});
      var v=b.getAttribute(attr),n=0;
      [].slice.call(document.querySelectorAll(items)).forEach(function(el){
        var show=v==='all'||el.getAttribute(attr)===v;el.hidden=!show;if(show)n++;
      });
      if(after)after(n);
    })});
  }
  chips('#fwchips','data-fw','.fwb');
  var cnt=document.getElementById('addcount');
  chips('#addchips','data-st','.add',function(n){cnt.textContent='Showing '+n+' of '+document.querySelectorAll('.add').length});
})();
"""

legend_items = [("#EAF6F1;border:2px solid #11875F", "Core Faclon platform"),
                ("#F3EEFE;border:2px dashed #7B4FE0", "Optional Faclon module"),
                ("#FDF0DA;border:2px solid #C77A12", "I/O Connect (DMZ gateway)"),
                ("#FBEDEA;border:1.5px solid #B5452F", "Firewall"),
                ("#EEF2F8;border:1.5px solid #7D8CA3", "Switch"),
                ("#fff;border:1.5px dashed #B9C3D2", "Converter, only where needed"),
                ("#E0701B;height:3px", "Fibre run (OFC star)"),
                ("#3D63F5;height:3px", "Data moves up, outbound only")]
legend = "".join(f'<span><i style="background:{s}"></i>{E(l)}</span>' for s, l in legend_items)

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>IT-OT Integration · Faclon Labs</title>
<meta name="description" content="Reference IT-OT integration architecture: segmented field networks, a two-firewall industrial DMZ with I/O Connect, and outbound-only upload to the Faclon platforms in the plant owner's cloud tenancy.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>IT-OT integration · All industries</span></div>
  <a class="back" href="../">← All solutions</a>
  <h1>IT-OT <em>Integration</em></h1>
  <p class="lede">{E(h["lede"])}</p>
  <div class="kpis">{kpis}</div>
</div></header>

<nav class="nav" aria-label="Sections"><div class="wrap">{nav}</div></nav>

<main>
<section id="architecture"><div class="wrap">
  <div class="sh"><div class="eyebrow">Reference architecture</div><h2>From the meter to the Faclon platforms, one layer at a time</h2>
  <p>Field areas sit at the bottom, each on its own fibre run and segment. Data climbs through OT aggregation and an industrial DMZ, where I/O Connect brokers it, then leaves the plant outbound only, over a private link into UDF in the customer's own cloud tenancy. Nothing above the DMZ can reach a controller.</p></div>
  <p class="swipe">Swipe sideways to see the whole drawing →</p>
  <figure class="fig">{diagram.architecture()}<figcaption>Reference drawing, not for construction. Area counts, fibre routes, converter selection and port lists are confirmed by site survey. Field IP addresses are intentionally left out.</figcaption></figure>
  <div class="legend">{legend}</div>
  <ul class="keyp">{keyp}</ul>
</div></section>

<section id="platforms"><div class="wrap">
  <div class="sh"><div class="eyebrow">Faclon platforms in this design</div><h2>Where each platform sits and what it does</h2>
  <p>I/O Connect lives in the industrial DMZ. Everything else runs on the Faclon platform bus inside the customer's tenancy; UDF and Deepsense can also run at the edge.</p></div>
  <div class="plats">{plats}</div>
</div></section>

<section id="flows"><div class="wrap">
  <div class="sh"><div class="eyebrow">Traffic flows</div><h2>Five paths, each through named firewall rules</h2></div>
  <div class="flows">{flows}</div>
</div></section>

<section id="rules"><div class="wrap">
  <div class="sh"><div class="eyebrow">Design rules</div><h2>What keeps the plant safe while the data flows</h2></div>
  <div class="rules">{rules}</div>
</div></section>

<section id="network"><div class="wrap">
  <div class="sh"><div class="eyebrow">Network plan</div><h2>VLANs, NAT and routing</h2>
  <p>Existing field devices keep their addresses and need no configuration change. Overlaps are resolved at each area's NAT switch.</p></div>
  <h3 class="sub">VLAN plan</h3>{vl}<p class="note">{E(D["vlan_note"])}</p>
  <h3 class="sub">NAT schedule</h3>{nat}<p class="note">{E(D["nat_note"])}</p>
  <h3 class="sub">Routing and default gateways</h3>{rt}
</div></section>

<section id="firewalls"><div class="wrap">
  <div class="sh"><div class="eyebrow">Firewall rules</div><h2>Three firewalls, default deny on each</h2>
  <p>{E(D["fw_note"])}</p></div>
  <div class="chips" id="fwchips">{fw_tabs}</div>
  {fw_blocks}
</div></section>

<section id="protocols"><div class="wrap">
  <div class="sh"><div class="eyebrow">OT protocol support</div><h2>Protocols I/O Connect reads, and what each needs</h2>
  <p>{E(D["protocol_note"])}</p></div>
  {prot}
</div></section>

<section id="added"><div class="wrap">
  <div class="sh"><div class="eyebrow">Design considerations</div><h2>{len(D["considerations"])} items that go beyond the basic brief</h2>
  <p>Recommendations, options and items to settle at site survey.</p></div>
  <div class="chips" id="addchips">{add_chips}</div>
  <p class="count" id="addcount" aria-live="polite">Showing {len(D["considerations"])} of {len(D["considerations"])}</p>
  <ol class="adds">{adds}</ol>
</div></section>

<section id="scope"><div class="wrap">
  <div class="sh"><div class="eyebrow">Scope boundary</div><h2>What this design covers, and what it does not</h2>
  <p>{E(D["scope_note"])}</p></div>
  <div class="scope">{scope}</div>
</div></section>

<section id="survey"><div class="wrap">
  <div class="sh"><div class="eyebrow">Next step</div><h2>Information needed before the site survey</h2></div>
  <h3 class="sub">Open questions</h3>{opens}
  <h3 class="sub">Target host systems</h3>{hosts}<p class="note">{E(D["hosts_note"])}</p>
  <p class="disc">This page describes a reference design. Area counts, fibre routes, converter selection and port lists are subject to site survey for each plant.</p>
</div></section>
</main>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Secure plant data, ready for AI</div><h2>Start with one area and the DMZ</h2><p>Connect one electrical room or machine line through the DMZ into your tenancy, prove the data path and the security controls, then scale area by area and plant by plant.</p></div>
  <div class="contact">
    <a class="btn" href="mailto:{E(ct["email"])}">{E(ct["email"])}</a>
    <a class="btn ghost" href="tel:{E(ct["tel"])}">{E(ct["name"])} · {E(ct["phone"])}</a>
  </div>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · IT-OT Integration</span><span><a href="https://{E(ct["web"])}">{E(ct["web"])}</a></span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
