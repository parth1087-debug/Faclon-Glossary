"""Builds io-vision/index.html (I/O Vision: computer vision use cases for plants).

Run from anywhere:  python3 src/io-vision/build_page.py

Sources, all in this folder:
  content.json   All page content:
                   hero          {title, headline, tagline, pillars[], img, alt}
                   categories[]  {id, name, short}           order sets the filter chips and sections
                   use_cases[]   {id, cat (category id), name (catalogue name), title (detail title),
                                  sub (one-line subtitle), feat (what it detects),
                                  problem[], solution[], impact[] [title, text],
                                  img (asset name), alt}
                                 A use case with empty problem/solution/impact shows its summary only.
                   projects[]    {customer, uses[] (use case ids), sub, usecase, how[] [label, text],
                                  buckets[] (size classes, optional), benefits, stats[] [value, label],
                                  imgs[] [asset name, caption]}
  assets/        JPG images referenced by name in content.json, embedded as data URIs

Source: Faclon "Vision Use Cases" deck (I/O Vision). Edit content.json and re-run; the page is
regenerated in full. Counts in the hero are computed from the lists.
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
OUT = ROOT / "io-vision" / "index.html"
C = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
E = html.escape


def img(name):
    return "data:image/jpeg;base64," + base64.b64encode((HERE / "assets" / f"{name}.jpg").read_bytes()).decode()


CATS = C["categories"]
CAT = {c["id"]: c for c in CATS}
UCS = C["use_cases"]
UC = {u["id"]: u for u in UCS}
PROJ = C["projects"]
deployed = {}
for p in PROJ:
    for u in p["uses"]:
        deployed.setdefault(u, []).append(p["customer"])
cameras = next((s[0] for p in PROJ for s in p["stats"] if s[1] == "Cameras"), None)

# ---------- hero ----------
H = C["hero"]
pillars = "".join(f"<li>{E(p)}</li>" for p in H["pillars"])
cat_counts = {c["id"]: sum(1 for u in UCS if u["cat"] == c["id"]) for c in CATS}

# ---------- categories overview ----------
ICON = {
    "conveyors": '<path d="M3 15h18M5 15l2-5h10l2 5"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "safety": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="m9 12 2 2 4-4"/>',
    "road": '<path d="M9 3 6 21M15 3l3 18M12 5v3M12 11v3M12 17v2"/>',
    "process": '<rect x="3" y="4" width="7" height="7" rx="1"/><rect x="14" y="13" width="7" height="7" rx="1"/><path d="M10 7.5h4a2 2 0 0 1 2 2V13"/>',
    "quality": '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5M8.5 11l2 2 3-3.5"/>',
    "thermal": '<path d="M10 14V5a2 2 0 1 1 4 0v9a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
}


def icon(cid, size=22):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[cid]}</svg>')


cat_tiles = "".join(
    f'<a class="ct" href="#uc" data-jump="{c["id"]}"><span class="ci">{icon(c["id"])}</span>'
    f'<b>{E(c["name"])}</b><span class="cn">{cat_counts[c["id"]]} use case{"s" if cat_counts[c["id"]] != 1 else ""}</span>'
    f'<ul>{"".join(f"<li>{E(u["name"])}</li>" for u in UCS if u["cat"] == c["id"])}</ul></a>'
    for c in CATS
)

# ---------- use case cards ----------
def uc_card(u):
    cat = CAT[u["cat"]]
    q = " ".join([u["name"], u["title"], u["sub"], u["feat"], cat["name"], *u["problem"], *u["solution"],
                  *[" ".join(i) for i in u["impact"]], *deployed.get(u["id"], [])]).lower()
    dep = "".join(f'<span class="dep">Deployed · {E(c)}</span>' for c in deployed.get(u["id"], []))
    if u["problem"]:
        prob = "".join(f"<li>{E(x)}</li>" for x in u["problem"])
        sol = "".join(f"<li>{E(x)}</li>" for x in u["solution"])
        imp = "".join(f'<div class="im"><b>{E(t)}</b><p>{E(d)}</p></div>' for t, d in u["impact"])
        more = (f'<details><summary>Problem, solution and impact</summary><div class="dt">'
                f'<div class="ps"><span class="lab red">Problem</span><ul class="bl">{prob}</ul></div>'
                f'<div class="ps"><span class="lab">Solution</span><ul class="bl">{sol}</ul></div>'
                f'<div class="ps"><span class="lab grn">Operational impact</span><div class="ims">{imp}</div></div>'
                f'</div></details>')
    else:
        more = ""
    return (f'<article class="uc" id="uc-{u["id"]}" data-cat="{u["cat"]}" data-q="{E(q)}">'
            f'<figure><img src="{img(u["img"])}" alt="{E(u["alt"])}"></figure>'
            f'<div class="ub"><span class="uk">{icon(u["cat"], 14)}{E(cat["name"])}</span>'
            f'<h3>{E(u["name"])}</h3><p class="us">{E(u["sub"])}</p>'
            f'<p class="uf"><span>Detects</span>{E(u["feat"])}</p>{dep}</div>{more}</article>')


uc_cards = "".join(uc_card(u) for u in UCS)
chips = (f'<button type="button" class="chip on" data-cat="all" aria-pressed="true">All <span>{len(UCS)}</span></button>'
         + "".join(f'<button type="button" class="chip" data-cat="{c["id"]}" aria-pressed="false">{E(c["short"])} '
                   f'<span>{cat_counts[c["id"]]}</span></button>' for c in CATS))


# ---------- projects ----------
def project(p, i):
    stats = "".join(f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in p["stats"])
    uses = "".join(f'<a href="#uc-{u}">{E(UC[u]["name"])}</a>' for u in p["uses"])
    how = "".join(f'<li><b>{E(t)}</b><p>{E(d)}</p></li>' for t, d in p["how"])
    buckets = ("<div class=\"bk\"><span class=\"lab\">Size buckets</span><div class=\"bks\">"
               + "".join(f"<span>{E(b)}</span>" for b in p["buckets"]) + "</div></div>") if p["buckets"] else ""
    imgs = p["imgs"]
    if len(imgs) == 1:
        pics = f'<figure class="pf one"><img src="{img(imgs[0][0])}" alt="{E(imgs[0][1])}"><figcaption>{E(imgs[0][1])}</figcaption></figure>'
    else:
        pics = "".join(f'<figure class="pf{" wide" if j == 2 and len(imgs) == 3 and p["buckets"] else ""}">'
                       f'<img src="{img(n)}" alt="{E(c)}"><figcaption>{E(c)}</figcaption></figure>'
                       for j, (n, c) in enumerate(imgs))
    return (f'<article class="pj{" rev" if i % 2 else ""}"><div class="pt">'
            f'<div class="eyebrow">Relevant project</div><h3>{E(p["customer"])}</h3><p class="psub">{E(p["sub"])}</p>'
            + (f'<div class="pst">{stats}</div>' if stats else "")
            + f'<div class="puc"><span class="lab">Use case</span><p>{E(p["usecase"])}</p></div>'
            f'<ul class="how">{how}</ul>{buckets}'
            f'<div class="pben"><span class="lab grn">Benefits</span><p>{E(p["benefits"])}</p></div>'
            f'<div class="puses"><span class="lab">Use cases on this page</span><div>{uses}</div></div>'
            f'</div><div class="pics n{len(imgs)}">{pics}</div></article>')


projects = "".join(project(p, i) for i, p in enumerate(PROJ))

CSS = """
:root{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--red:#B5452F;--redBg:#FBEEEB;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#fff;scroll-padding-top:24px}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
table{font-variant-numeric:tabular-nums}
ul{list-style:none}
img{max-width:100%;display:block}
button{font:inherit}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}
h1,h2,h3{letter-spacing:-.015em;line-height:1.2;text-wrap:balance}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
section{padding:72px 0}
section.panel{background:var(--bg)}
h2{font-size:clamp(26px,3.4vw,36px);font-weight:700;margin:8px 0 10px}
.sub{color:var(--ink2);font-size:17px;max-width:700px;margin-bottom:34px}
.lab{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);margin-bottom:6px}
.lab.red{color:var(--red)}.lab.grn{color:var(--green)}

/* hero */
.hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;left:-200px;top:-220px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.25),rgba(124,149,255,0) 68%)}
.hero .wrap{position:relative;padding-top:34px;padding-bottom:56px}
.brand{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}
.brand b{color:#fff;letter-spacing:.22em}
.back{display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none}
.back:hover{color:#fff}
.hgrid{display:grid;grid-template-columns:1.25fr .75fr;gap:40px;align-items:center;margin-top:40px}
.hero .prod{font-size:14px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--blue2)}
.hero h1{font-size:clamp(34px,5vw,56px);font-weight:700;margin:12px 0 14px}
.lede{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:640px}
.hpic{border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,.14);box-shadow:0 30px 60px rgba(0,0,0,.35);margin:0}
.hpic img{width:100%;height:420px;object-fit:cover;object-position:center 40%}
.pillars{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,.12);border-radius:12px;overflow:hidden;margin-top:28px}
.pillars li{background:var(--navy2);padding:14px 18px;font-weight:600;font-size:14.5px;color:#E3E9F5}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);margin-top:14px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}
.kp{background:var(--navy2);padding:16px 20px}
.kp b{font-size:28px;display:block}
.kp span{font-size:12.5px;color:#9FB0CC}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.jump a{font-size:13px;color:#D5DEEE;border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:5px 12px;text-decoration:none}
.jump a:hover{border-color:var(--blue2);color:#fff}

/* how */
.flow{display:grid;grid-template-columns:1fr auto 1fr auto 1.15fr auto 1.25fr;align-items:stretch}
.node{border:1px solid var(--line);border-radius:14px;background:#fff;padding:18px;display:flex;flex-direction:column;gap:6px}
.node .k{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.node b{font-size:16px}
.node p{font-size:13.5px;color:var(--ink2)}
.node.core{background:var(--navy);border-color:var(--navy);color:#fff}
.node.core .k{color:var(--blue2)}.node.core p{color:#C5D0E3}
.node.out{border-color:var(--blue);background:var(--blueBg)}
.node.int{border-color:var(--green);background:var(--greenBg)}
.node ul{font-size:13.5px;display:flex;flex-direction:column;gap:3px}
.node.out li:before{content:"→ ";color:var(--blue);font-weight:700}
.node.int li:before{content:"↔ ";color:var(--green);font-weight:700}
.arr{display:flex;align-items:center;justify-content:center;padding:0 8px;color:var(--blue);font-weight:700;font-size:18px}
.flownote{font-size:13px;color:var(--mute);margin-top:14px}

/* categories */
.cts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ct{display:block;border:1px solid var(--line);border-radius:16px;background:#fff;padding:18px 20px;text-decoration:none;color:inherit;transition:border-color .15s,box-shadow .15s}
.ct:hover{border-color:var(--blue);box-shadow:0 10px 26px rgba(15,27,45,.07)}
.ci{display:inline-flex;width:38px;height:38px;border-radius:10px;background:var(--blueBg);color:var(--blue);align-items:center;justify-content:center;margin-bottom:10px}
.ct b{display:block;font-size:16.5px}
.cn{font-size:12.5px;color:var(--mute)}
.ct ul{margin-top:10px;display:flex;flex-wrap:wrap;gap:6px}
.ct li{font-size:12.5px;background:var(--bg);border:1px solid var(--line);border-radius:20px;padding:2px 10px;color:var(--ink2)}

/* catalogue */
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:18px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{border:1px solid var(--line);background:#fff;color:var(--ink2);border-radius:20px;padding:6px 12px;font-size:13.5px;font-weight:500;cursor:pointer}
.chip span{color:var(--mute);font-size:12px;margin-left:2px}
.chip.on{background:var(--navy);border-color:var(--navy);color:#fff}
.chip.on span{color:#9FB0CC}
.search{flex:1 1 240px;position:relative;min-width:0}
.search input{width:100%;font:inherit;font-size:14.5px;padding:9px 12px 9px 34px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--mute)}
input:focus,button:focus-visible,a:focus-visible,summary:focus-visible{outline:2px solid var(--blue);outline-offset:1px}
.count{font-size:13px;color:var(--mute);margin-left:auto}
.ucs{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:start}
.uc{border:1px solid var(--line);border-radius:16px;background:#fff;overflow:hidden;display:flex;flex-direction:column;scroll-margin-top:24px}
.uc:target{border-color:var(--blue);box-shadow:0 0 0 3px var(--blueBg)}
.uc figure{margin:0;background:#0B1A30}
.uc figure img{width:100%;height:190px;object-fit:cover}
.ub{padding:16px 18px 14px;display:flex;flex-direction:column;gap:6px}
.uk{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--blue)}
.uc h3{font-size:17.5px}
.us{font-size:13.5px;color:var(--mute)}
.uf{font-size:14px;color:var(--ink2);border-top:1px solid var(--line);padding-top:8px;margin-top:2px}
.uf span{display:block;font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin-bottom:2px}
.dep{align-self:flex-start;font-size:11.5px;font-weight:600;color:var(--green);background:var(--greenBg);border-radius:20px;padding:2px 10px}
details{border-top:1px solid var(--line);background:var(--bg)}
summary{cursor:pointer;list-style:none;padding:11px 18px;font-size:13.5px;font-weight:600;color:var(--blue);display:flex;justify-content:space-between;align-items:center}
summary::-webkit-details-marker{display:none}
summary:after{content:"+";font-size:18px;line-height:1;font-weight:500}
details[open] summary:after{content:"−"}
.dt{padding:2px 18px 18px;display:flex;flex-direction:column;gap:14px}
.bl{display:flex;flex-direction:column;gap:6px;font-size:13.5px;color:var(--ink2)}
.bl li{padding-left:14px;position:relative}
.bl li:before{content:"";position:absolute;left:0;top:.6em;width:6px;height:6px;border-radius:50%;background:var(--line)}
.ps:first-child .bl li:before{background:#E7B5A9}
.ps:nth-child(2) .bl li:before{background:var(--blue2)}
.ims{display:flex;flex-direction:column;gap:8px}
.im{background:#fff;border:1px solid var(--line);border-left:3px solid var(--green);border-radius:10px;padding:9px 12px}
.im b{font-size:13.5px;display:block}
.im p{font-size:13px;color:var(--ink2)}
.empty{padding:36px;text-align:center;color:var(--mute);border:1px dashed var(--line);border-radius:16px;margin-top:6px}

/* projects */
.pj{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:start;background:#fff;border:1px solid var(--line);border-radius:18px;padding:28px}
.pj+.pj{margin-top:22px}
.pj.rev .pt{order:2}
.pj h3{font-size:28px;margin:6px 0 4px}
.psub{color:var(--mute);font-size:14.5px;margin-bottom:14px}
.pst{display:flex;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-bottom:16px}
.pst div{flex:1;background:#fff;padding:12px 16px}
.pst b{font-size:28px;color:var(--green);display:block;line-height:1.1}
.pst span{font-size:12.5px;color:var(--mute)}
.puc{background:var(--blueBg);border-radius:12px;padding:12px 14px;margin-bottom:14px}
.puc p{font-size:14.5px;color:var(--ink)}
.how{display:flex;flex-direction:column;gap:10px;margin-bottom:14px}
.how li{border-left:3px solid var(--blue);padding-left:12px}
.how b{font-size:14.5px}
.how p{font-size:13.5px;color:var(--ink2)}
.bk{margin-bottom:14px}
.bks{display:flex;flex-wrap:wrap;gap:6px}
.bks span{font-size:12.5px;font-weight:600;border:1px solid var(--line);background:var(--bg);border-radius:8px;padding:3px 9px}
.pben{background:var(--greenBg);border-radius:12px;padding:12px 14px;margin-bottom:14px}
.pben p{font-size:14px;color:var(--ink)}
.puses div{display:flex;flex-wrap:wrap;gap:6px}
.puses a{font-size:12.5px;color:var(--blue);background:#fff;border:1px solid var(--line);border-radius:20px;padding:2px 10px;text-decoration:none}
.puses a:hover{border-color:var(--blue)}
.pics{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.pics.n3:not(:has(.wide)){grid-template-columns:1fr}
.pf{margin:0;border-radius:12px;overflow:hidden;border:1px solid var(--line);background:#fff}
.pf.wide,.pf.one{grid-column:1/-1}
.pf img{width:100%;height:auto}
.pics.n3:not(:has(.wide)) .pf img{height:200px;object-fit:cover}
.pf figcaption{font-size:12.5px;color:var(--mute);padding:8px 12px;border-top:1px solid var(--line)}

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
  .hgrid{grid-template-columns:1fr;gap:28px}
  .hpic img{height:260px}
  .flow{grid-template-columns:1fr}
  .arr{padding:6px 0;transform:rotate(90deg)}
  .cts,.ucs{grid-template-columns:1fr 1fr}
  .kpis{grid-template-columns:1fr 1fr}
  .pj{grid-template-columns:1fr;gap:22px}
  .pj.rev .pt{order:0}
  .count{margin-left:0;width:100%}
}
@media (max-width:640px){
  .wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  section{padding:52px 0}
  .hgrid{margin-top:28px}
  .pillars{grid-template-columns:1fr}
  .cts,.ucs{grid-template-columns:1fr}
  .pj{padding:18px}
  .pics{grid-template-columns:1fr}
}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.bar{display:none}.uc,.pj,.ct{break-inside:avoid}details>*{display:block}}
"""

JS = """
(function(){
  var q=document.getElementById('q'),chips=[].slice.call(document.querySelectorAll('.chip')),
      cards=[].slice.call(document.querySelectorAll('.uc')),count=document.getElementById('count'),
      empty=document.getElementById('empty'),cat='all',TOTAL=cards.length;
  function apply(){
    var term=q.value.trim().toLowerCase(),shown=0;
    cards.forEach(function(c){var ok=(cat==='all'||c.dataset.cat===cat)&&(!term||c.dataset.q.indexOf(term)>-1);c.hidden=!ok;if(ok)shown++});
    count.textContent=shown===TOTAL?'Showing all '+TOTAL+' use cases':'Showing '+shown+' of '+TOTAL+' use cases';
    empty.hidden=!!shown;
  }
  function pick(c){cat=c;chips.forEach(function(b){var on=b.dataset.cat===c;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)});apply()}
  chips.forEach(function(b){b.addEventListener('click',function(){pick(b.dataset.cat)})});
  [].slice.call(document.querySelectorAll('[data-jump]')).forEach(function(a){a.addEventListener('click',function(){q.value='';pick(a.dataset.jump)})});
  [].slice.call(document.querySelectorAll('.puses a')).forEach(function(a){a.addEventListener('click',function(){q.value='';pick('all');var t=document.querySelector(a.getAttribute('href'));if(t){var d=t.querySelector('details');if(d)d.open=true}})});
  q.addEventListener('input',apply);apply();
})();
"""

kp_cam = (f'<div class="kp"><b>{E(cameras)}</b><span>Cameras at one Hindalco site</span></div>' if cameras else
          f'<div class="kp"><b>{sum(1 for u in UCS if u["id"] in deployed)}</b><span>Use cases in production</span></div>')

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>I/O Vision · Faclon Labs</title>
<meta name="description" content="I/O Vision: {len(UCS)} computer vision use cases for plants, from conveyor health and particle size to PPE, road safety, quality inspection and thermal monitoring.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Computer vision · All industries</span></div>
  <a class="back" href="../">← All solutions</a>
  <div class="hgrid">
    <div>
      <div class="prod">{E(H["title"])}</div>
      <h1>{E(H["headline"])}</h1>
      <p class="lede">{E(H["tagline"])}. Cameras already on site, or new optical and thermal ones, feed AI models that watch conveyors, people, vehicles, products and hot processes around the clock and raise an alert the moment something is wrong.</p>
    </div>
    <figure class="hpic"><img src="{img(H["img"])}" alt="{E(H["alt"])}"></figure>
  </div>
  <ul class="pillars">{pillars}</ul>
  <div class="kpis">
    <div class="kp"><b>{len(UCS)}</b><span>Vision AI use cases</span></div>
    <div class="kp"><b>{len(CATS)}</b><span>Areas of the plant</span></div>
    <div class="kp"><b>{len(PROJ)}</b><span>Customer deployments shown</span></div>
    {kp_cam}
  </div>
  <nav class="jump" aria-label="On this page"><a href="#how">How it works</a><a href="#areas">Areas covered</a><a href="#uc">Use cases</a><a href="#projects">Customer deployments</a></nav>
</div></header>

<main>
<section id="how"><div class="wrap">
  <div class="eyebrow">I/O Vision · How it works</div>
  <h2>From a camera frame to an action on the shop floor</h2>
  <p class="sub">Every use case follows the same path. Cameras capture the scene, an AI model trained for that task reads each frame, and the result reaches the people and systems that need to act on it.</p>
  <div class="flow">
    <div class="node"><span class="k">Capture</span><b>Optical and thermal cameras</b><p>Fixed over conveyors, gates, roads, work zones, burners and the sinter bed. Zones and boundaries are configured within each camera view.</p></div>
    <div class="arr" aria-hidden="true">→</div>
    <div class="node core"><span class="k">Faclon</span><b>I/O Vision AI models</b><p>Run on a GPU-enabled server. Detect, segment, classify, track and measure in real time, even in dusty or low-visibility conditions.</p></div>
    <div class="arr" aria-hidden="true">→</div>
    <div class="node out"><span class="k">I/O Sense platform</span><b>Alerts, logs and trends</b><ul><li>Instant alerts to operators and supervisors</li><li>Timestamped event logs with visual evidence</li><li>Dashboards and audit-ready reports</li><li>Trends correlated with process parameters</li></ul></div>
    <div class="arr" aria-hidden="true">→</div>
    <div class="node int"><span class="k">Integrations</span><b>Plant systems</b><ul><li>SCADA / PLC for status and control signals</li><li>CMMS for maintenance workflows</li><li>Quality management systems</li><li>Access control and weighbridge</li><li>ISO 45001-aligned safety systems</li></ul></div>
  </div>
  <p class="flownote">Integrations shown are the ones named across the use cases below; each deployment uses the ones its use cases need.</p>
</div></section>

<section class="panel" id="areas"><div class="wrap">
  <div class="eyebrow">Coverage</div>
  <h2>{len(UCS)} use cases across {len(CATS)} areas of the plant</h2>
  <p class="sub">Pick an area to see its use cases.</p>
  <div class="cts">{cat_tiles}</div>
</div></section>

<section id="uc"><div class="wrap">
  <div class="eyebrow">Use case catalogue</div>
  <h2>What I/O Vision watches for</h2>
  <p class="sub">Each card shows what the system detects. Open it for the problem it solves, how the solution works and the operational impact.</p>
  <div class="bar">
    <div class="chips" role="group" aria-label="Filter by area">{chips}</div>
    <label class="search" for="q">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="q" type="search" placeholder="Search, e.g. helmet, belt tear, number plate, flame" aria-label="Search use cases">
    </label>
    <div class="count" id="count">Showing all {len(UCS)} use cases</div>
  </div>
  <div class="ucs" id="uclist">{uc_cards}</div>
  <div class="empty" id="empty" hidden>No use cases match. Try a word such as “conveyor”, “PPE” or “thermal”.</div>
</div></section>

<section class="panel" id="projects"><div class="wrap">
  <div class="eyebrow" style="color:var(--green)">Customer deployments</div>
  <h2>Running in power, zinc and aluminium plants</h2>
  <p class="sub">Three deployments of I/O Vision: what each customer needed, how the system works on their site and what it delivers.</p>
  {projects}
</div></section>
</main>

<div class="cta"><div class="wrap">
  <div><div class="k">Next step</div><h2>Your digital backbone for operational efficiency and decision intelligence</h2><p>Tell us what you would like your cameras to watch for. We will show you which I/O Vision use cases fit your plant.</p></div>
  {CTA_BUTTONS}
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · I/O Vision</span><span>Computer vision for safer, smarter plants</span></div></div>
<script>{JS}</script>
</body></html>"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
