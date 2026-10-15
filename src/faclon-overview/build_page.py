"""Builds faclon-overview/index.html, the Faclon Labs company overview (from the 2026 deck).

Run from anywhere:  python3 src/faclon-overview/build_page.py

Sources, all in this folder:
  template.html  Page layout, styles and script. Placeholders:
                   {{name}}          an image from assets/ (name.png or name.jpg), embedded as a data URI
                   <i data-lucide="x"></i>   an icon from icons/x.svg, inlined as SVG
                   <!--CUSTOMERS-->  replaced with the Key Customers section
                   <!--CASES-->      replaced with the Customer Cases section
  content.json   All customer and case content:
                   customers[]   {industry, logos[] {logo, name}}   -> logo wall + industry tabs
                   case_groups[] {id, name}   order of groups in Customer Cases; id "on" = ongoing
                   domains       {id: label}  prod / energy / maint / quality
                   cases[]       {logo, customer, site, title, domains[], ongoing, metrics[] {value, label},
                                  points[] (HTML strings; <b> allowed)}
                                 A case sits in group "on" if ongoing, otherwise in its first domain.
  assets/        Customer logos, team photos, closing photo (PNG/JPG)
  icons/         Lucide icons (ISC licence) used by the template

The output is one self-contained HTML file; Google Fonts (Inter) is the only external request.
"""
import base64
import html
import json
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))
from cta import CTA_BUTTONS  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "faclon-overview" / "index.html"
E = html.escape

content = json.loads((HERE / "content.json").read_text())
t = (HERE / "template.html").read_text()

# ---------- Key Customers ----------
inds = content["customers"]
total = sum(len(i["logos"]) for i in inds)
tabs = f'<button class="tab" data-f="all" aria-pressed="true">All <span>{total}</span></button>'
tiles = ""
for n, ind in enumerate(inds):
    tabs += f'<button class="tab" data-f="i{n}" aria-pressed="false">{E(ind["industry"])} <span>{len(ind["logos"])}</span></button>'
    for lg in ind["logos"]:
        tiles += (f'<figure class="lt" data-g="i{n}"><img src="{{{{{lg["logo"]}}}}}" alt="{E(lg["name"])}">'
                  f'<figcaption>{E(ind["industry"])}</figcaption></figure>')
customers = f"""<!-- 3 -->
<section class="sec alt" id="s3" data-title="Key Customers">
  <div class="wrap">
    <div class="sh rv"><div class="k">Customers</div><h2><b>Key</b> customers</h2><p>A trusted digital partner for industrial plants, commercial buildings and OEMs</p></div>
    <div class="tabs" role="group" aria-label="Filter customers by industry" id="ctabs">{tabs}</div>
    <div class="lwall" id="lwall">{tiles}</div>
  </div>
</section>"""
t = t.replace("<!--CUSTOMERS-->", customers).replace("<!--CTABUTTONS-->", CTA_BUTTONS)

# ---------- Customer Cases ----------
cases = content["cases"]
DOM = content["domains"]
group_of = lambda c: "on" if c["ongoing"] else c["domains"][0]
body, rail, n = "", "", 0
for g in content["case_groups"]:
    items = [c for c in cases if group_of(c) == g["id"]]
    body += f'<h3 class="grp" id="g-{g["id"]}"><span>{E(g["name"])}</span><em>{len(items)} cases</em></h3>'
    sub = ""
    for c in items:
        n += 1
        tags = ('<span class="live">Ongoing</span>' if c["ongoing"] else "") + "".join(
            f"<span>{E(DOM[d])}</span>" for d in c["domains"])
        met = "".join(f'<div><b>{E(m["value"])}</b><span>{E(m["label"])}</span></div>' for m in c["metrics"])
        body += f"""<article class="case" id="c{n}" data-g="{g['id']}">
  <aside class="vside"><div class="vlogo"><img src="{{{{{c['logo']}}}}}" alt="{E(c['customer'])}"></div><div class="vcust">{E(c['customer'])}</div><div class="vsite">{E(c['site'])}</div><div class="vtags">{tags}</div>{f'<div class="vmet">{met}</div>' if met else ''}</aside>
  <div class="vmain"><div class="vhead"><h4>{E(c['title'])}</h4><span class="vct">{n} / {len(cases)}</span></div><ul class="vbul">{''.join('<li>' + p + '</li>' for p in c['points'])}</ul></div>
</article>"""
        sub += f'<a href="#c{n}" data-c="c{n}">{E(c["customer"])}<small>{E(c["title"])}</small></a>'
    rail += (f'<div class="rg" data-g="{g["id"]}"><a class="rt" href="#g-{g["id"]}" data-c="g-{g["id"]}">'
             f'{E(g["name"])}<span>{len(items)}</span></a><div class="rs">{sub}</div></div>')
ongoing = sum(1 for c in cases if c["ongoing"])
case_html = f"""<!-- 9 -->
<section class="sec" id="s9" data-title="Customer Cases" data-cases>
  <div class="wrap">
    <div class="sh rv"><div class="k">Proof in production</div><h2>Customer <b>cases</b></h2><p>{len(cases) - ongoing} implementations across production, energy, maintenance and quality, plus {ongoing} projects underway.</p></div>
    <div class="cwrap">
      <div class="clist">{body}</div>
      <nav class="rail" aria-label="Jump to case"><div class="rail-in"><div class="rail-h">Jump to</div>{rail}</div></nav>
    </div>
  </div>
</section>"""
t = t.replace("<!--CASES-->", case_html).replace("<!--CASEDATA-->", "")


# ---------- images ----------
def uri(name):
    for ext, mime in ((".png", "image/png"), (".jpg", "image/jpeg")):
        f = HERE / "assets" / (name + ext)
        if f.exists():
            return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
    raise SystemExit(f"missing asset: {name}")


t = re.sub(r"\{\{(\w+)\}\}", lambda m: uri(m.group(1)), t)


# ---------- icons ----------
def icon(m):
    pre, name, post = m.groups()
    svg = re.sub(r"<!--.*?-->", "", (HERE / "icons" / f"{name}.svg").read_text(), flags=re.S).strip()
    extra = re.search(r'class="([^"]+)"', pre + post)
    cls = f"lucide lucide-{name}" + (" " + extra.group(1) if extra else "")
    svg = re.sub(r"<svg[^>]*?>", '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" '
                 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
                 f'class="{cls}" aria-hidden="true">', svg, count=1)
    return re.sub(r"\s*\n\s*", "", svg)


t = re.sub(r'<i([^>]*?)data-lucide="([a-z0-9-]+)"([^>]*)></i>', icon, t)
t = t.replace('<script src="https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js"></script>', "")
t = t.replace("try{lucide.createIcons()}catch(e){}", "")
assert 'data-lucide="' not in t and "unpkg" not in t

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Faclon Labs Overview · Faclon Labs</title>
<meta name="description" content="Faclon Labs: data and AI infrastructure for industrial plants. Platform, use cases and customer cases.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head><body>
{t}
</body></html>
"""
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(page)
print(f"wrote {OUT.relative_to(ROOT)} ({len(page) / 1e6:.2f} MB, {len(cases)} cases, {total} logos)")
