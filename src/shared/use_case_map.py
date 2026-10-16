"""Shared builder for industry AI use-case map pages (aluminium, copper, refinery, solar, ...).

Each industry folder (src/<slug>/) has a short build_page.py that calls build(CFG) and a
use_cases.json with the content. Edit the JSON and re-run that folder's build_page.py.

use_cases.json: a list of plant sections, in plant-flow order:
  s      : section name
  procs  : unit processes, each:
    n                    unit process name
    f                    process flow steps (optional)
    rm / ut / out / q    raw material, utility input, output, quality parameters (optional)
    uc                   use cases, each:
      t      title                      k     "ai" (AI Advisory), "cv" (Vision AI) or "fd" (Foundation)
      v      indicative value, up to ₹ crore (null when the source gives none)
      basis  what v is quoted per, e.g. "MTPA aluminium" or "100 MW per year" (null with v)
      vq     qualifier shown after the value, e.g. "risk-adjusted" (optional)
      vt     text shown instead of a value, e.g. "Enabler for all other use cases" (optional)
      loc    critical locations, maximum impact (optional)
      d      what Faclon does           p     problems addressed         kpi   KPIs tracked
      calc   how the value is estimated (optional, shown in a fold-out)
      tier   priority tier 1-3, 1 = start here (optional; the tier filter is hidden when no use case has one)

CFG (dict) keys:
  slug, title (page <title> and short name), sector (brand line), eyebrow, h1 (HTML allowed),
  lede, primary (main value basis, e.g. "MTPA aluminium"), basis_note (plain words for the note),
  area ("plant section" / "process area"), search (placeholder), examples (3 tuples for the
  Connect / Contextualise / Act row: (heading, text)), cta (paragraph), flow_word ("Plant flow order").
Section, page and hero totals are computed from the JSON, so they always match the cards. Values
quoted on a basis other than `primary` (downstream products) are totalled separately, never added in.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cta import CTA_BUTTONS  # noqa: E402

E = html.escape
KIND = {"ai": ("AI Advisory", "soft sensors, optimisation and setpoint advisory"),
        "cv": ("Vision AI", "camera-based detection and condition monitoring"),
        "fd": ("Foundation", "the IT-OT data layer every other use case runs on")}
TIER = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def num(v):
    v = round(float(v), 2)
    return f"{int(v) if v.is_integer() else v}"


def short(basis):
    """'MTPA aluminium' -> '/ MTPA aluminium'; '100 MW per year' -> '/ 100 MW / yr'."""
    return "/ " + basis.replace(" per year", " / yr")


def totals(items):
    t = {}
    for u in items:
        if u.get("v") is not None:
            t[u["basis"]] = t.get(u["basis"], 0) + u["v"]
    return t


def build(cfg, data_path, out_path):
    DATA = json.loads(Path(data_path).read_text(encoding="utf-8"))
    P = cfg["primary"]
    allu = [u for s in DATA for p in s["procs"] for u in p["uc"]]
    has_val = any(u.get("v") is not None for u in allu)
    has_tier = any(u.get("tier") for u in allu)
    n_uc, n_proc = len(allu), sum(len(s["procs"]) for s in DATA)
    kinds = {k: sum(1 for u in allu if u["k"] == k) for k in KIND}
    tiers = {t: sum(1 for u in allu if u.get("tier") == t) for t in TIER}
    grand = totals(allu)
    gp = grand.get(P, 0)
    others = {b: v for b, v in grand.items() if b != P}

    def val_html(u):
        if u.get("v") is not None:
            sub = "up to " + short(u["basis"]) + (f" · {u['vq']}" if u.get("vq") else "")
            return f'<div class="val">₹{num(u["v"])} cr<small>{E(sub)}</small></div>'
        if u["k"] == "fd":
            return '<div class="val fd">Platform<small>enabler</small></div>'
        return ""

    def card(u, p, s):
        locs = ""
        if u.get("loc"):
            locs = ('<div class="locs"><b>Critical locations · maximum impact</b><ul>'
                    + "".join(f"<li>{E(x)}</li>" for x in u["loc"]) + "</ul></div>")
        li = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)
        calc = (f'<details class="calc"><summary>How the value is estimated</summary><p>{E(u["calc"])}</p></details>'
                if u.get("calc") else "")
        tier = (f'<span class="tier t{u["tier"]}">{TIER[u["tier"]]}</span>' if u.get("tier") else "")
        q = " ".join([u["t"], KIND[u["k"]][0], *u["d"], *u["p"], *u["kpi"], *u.get("loc", []), u.get("calc", ""),
                      p["n"], p.get("q", ""), p.get("rm", ""), p.get("out", ""), s["s"]]).lower()
        return (f'<article class="card k-{u["k"]}" data-v="{u.get("v") or 0}" data-k="{u["k"]}" data-t="{u.get("tier") or 0}" data-q="{E(q)}">'
                f'<div class="card-top"><div><div class="chips"><span class="kind">{KIND[u["k"]][0]}</span>{tier}</div>'
                f'<h4>{E(u["t"])}</h4></div>{val_html(u)}</div>'
                + (f'<p class="vt">{E(u["vt"])}</p>' if u.get("vt") and u["k"] != "fd" else "")
                + f'{locs}<div class="does"><b>What Faclon does</b><ul>{li(u["d"])}</ul></div>'
                f'<div class="pk"><div class="probs"><b>Problems addressed</b><ul>{li(u["p"])}</ul></div>'
                f'<div class="kpil"><b>KPIs tracked</b><ul>{li(u["kpi"])}</ul></div></div>{calc}</article>')

    def proc_block(p, s):
        flow = ('<div class="flow">' + "<i>→</i>".join(f"<b>{E(x)}</b>" for x in p["f"]) + "</div>") if p.get("f") else ""
        rows = [("Input", p.get("rm")), ("Utility", p.get("ut")), ("Output", p.get("out")), ("Quality", p.get("q"))]
        io = "".join(f'<span class="tag{" qp" if l == "Quality" else ""}">{l}</span><span>{E(v)}</span>' for l, v in rows if v)
        return (f'<div class="proc"><div class="proc-head"><div class="proc-top"><h3>{E(p["n"])}</h3>{flow}</div>'
                + (f'<div class="io">{io}</div>' if io else "") + '</div><div class="cards">'
                + "".join(card(u, p, s) for u in p["uc"]) + "</div></div>")

    def val_text(t):
        parts = []
        if t.get(P):
            parts.append(f"₹{num(t[P])} cr {short(P)}")
        parts += [f"₹{num(v)} cr {short(b)}" for b, v in t.items() if b != P]
        return " · ".join(parts)

    secs, rail, opts, bars = [], [], [], []
    svals = []
    for s in DATA:
        items = [u for p in s["procs"] for u in p["uc"]]
        t = totals(items)
        svals.append((s, items, t, sum(t.values())))
    vmax = max([x[3] for x in svals] + [1])
    cmax = max(len(x[1]) for x in svals)
    for i, (s, items, t, tsum) in enumerate(svals):
        n = len(items)
        units = f'{len(s["procs"])} unit{"s" if len(s["procs"]) > 1 else ""}'
        sid = slug(s["s"])
        vt = val_text(t)
        secs.append(f'<section class="section" id="{sid}" data-total="{n}" data-meta="{units}">'
                    f'<div class="sec-head"><h2><em>{i + 1:02d}</em>{E(s["s"])}</h2>'
                    f'<span class="meta">{units} · {n} use case{"s" if n != 1 else ""}' + (f" · up to {vt}" if vt else "") + "</span></div>"
                    + "".join(proc_block(p, s) for p in s["procs"]) + "</section>")
        rail.append(f'<a href="#{sid}">{E(s["s"])}<i>{n}</i></a>')
        opts.append(f'<option value="{sid}">{i + 1:02d}  {E(s["s"])}</option>')
        if has_val:
            pv, ov = t.get(P, 0), sum(v for b, v in t.items() if b != P)
            if pv:
                label = f'₹{num(pv)}<small> cr</small>'
                bar = f'<span class="bf" style="width:{pv / vmax * 100:.1f}%"></span>'
                if ov:
                    bar += f'<span class="bf alt" style="width:{ov / vmax * 100:.1f}%"></span>'
                    label += '<small class="plus">+</small>'
            elif ov:
                label = f'₹{num(ov)}<small> cr*</small>'
                bar = f'<span class="bf alt" style="width:{ov / vmax * 100:.1f}%"></span>'
            else:
                label, bar = "<small>enabler</small>", ""
            bars.append(f'<a class="brow" href="#{sid}"><span class="bn"><em>{i + 1:02d}</em>{E(s["s"])}</span>'
                        f'<span class="bt">{bar}</span><span class="bv">{label}</span>'
                        f'<span class="bc">{n} use case{"s" if n > 1 else ""}</span></a>')
        else:
            bars.append(f'<a class="brow" href="#{sid}"><span class="bn"><em>{i + 1:02d}</em>{E(s["s"])}</span>'
                        f'<span class="bt"><span class="bf blue" style="width:{n / cmax * 100:.1f}%"></span></span>'
                        f'<span class="bv b">{n}</span><span class="bc">{units}</span></a>')

    other_note = ""
    if others:
        other_note = ("Sections marked * or + also carry use cases valued per MTPA of their own product (" +
                      "; ".join(f"₹{num(v)} cr {short(b)}" for b, v in others.items()) +
                      "). These are shown separately and not added to the total.")
    mix = "".join(f'<div class="mix-i k-{k}"><b>{kinds[k]}</b><span><strong>{KIND[k][0]}</strong> · {E(KIND[k][1])}</span></div>'
                  for k in KIND if kinds[k])
    tier_mix = ""
    if has_tier:
        tier_mix = ('<div class="tiers">' + "".join(
            f'<div class="tm t{t}"><b>{tiers[t]}</b><span>{TIER[t]}</span></div>' for t in TIER if tiers[t]) +
            '</div><p class="tnote">Tier 1 use cases are the highest priority: the best mix of value and ease of '
            'deployment, and the natural place to start.</p>')

    if has_val:
        kp4 = f'<div class="kp hl"><b>₹{num(gp)}<small>cr</small></b><span>Value at stake {E(short(P))}</span></div>'
        kfoot = (f'<p class="kfoot">Up to ₹{num(gp)} crore {E(short(P))} of indicative annual value across the plant'
                 + ((" · plus " + "; ".join(f"₹{num(v)} cr {E(short(b))}" for b, v in others.items())) if 0 < len(others) <= 2
                    else (" · plus downstream use cases quoted per MTPA of their own product" if others else ""))
                 + ".</p>")
        chart_h = f"Value at stake by {cfg['area']}"
        btot = f'<div class="btot"><span>Total identified · {n_uc} use cases</span><span>₹{num(gp)} cr {E(short(P))}</span></div>'
        note = (f"All figures are indicative and subject to mutual agreement. Values are an upper bound, in ₹ crore "
                f"{cfg['basis_note']}.")
        sort_opt = '<option value="value">Highest value first</option>'
    else:
        kp4 = f'<div class="kp hl"><b>{kinds["cv"]}</b><span>Vision AI use cases</span></div>'
        kfoot = f'<p class="kfoot">{E(cfg.get("novalue_hero", "Value is sized for each site in a short assessment of its own data."))}</p>'
        chart_h = f"Use cases by {cfg['area']}"
        btot = f'<div class="btot"><span>Total</span><span>{n_uc} use cases</span></div>'
        note = cfg.get("novalue_note", "Value is sized per site: a 4–6 week assessment turns these use cases into a costed, prioritised plan.")
        sort_opt = ""
    tier_seg = ""
    if has_tier:
        tier_seg = ('<div class="seg" id="tierf" role="group" aria-label="Priority tier"><button type="button" data-t="" aria-pressed="true">All tiers</button>'
                    + "".join(f'<button type="button" data-t="{t}" aria-pressed="false">{TIER[t]}</button>' for t in TIER if tiers[t]) + "</div>")
    howto = ("Each unit process lists its inputs, process flow and quality parameters, followed by use-case cards. Every card states "
             "what Faclon does, the operating problems it removes and the KPIs it moves"
             + (", with the value at stake as an upper bound and how that value is estimated" if has_val else "")
             + (". The tier badge shows where to start." if has_tier else "."))
    ex = "".join(f'<div><em>{i + 1:02d} · {w}</em><h3>{E(h)}</h3><p>{E(t)}</p></div>'
                 for i, (w, (h, t)) in enumerate(zip(("Connect", "Contextualise", "Act"), cfg["examples"])))

    CSS = (Path(__file__).with_name("use_case_map.css").read_text(encoding="utf-8"))
    JS = (Path(__file__).with_name("use_case_map.js").read_text(encoding="utf-8")).replace("__TOTAL__", str(n_uc))
    t_esc = E(cfg["title"])
    HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t_esc} · Faclon Labs</title>
<meta name="description" content="{E(cfg['description'])}">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<header class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>{E(cfg['sector'])}</span></div>
  <a class="back" href="../">← All solutions</a>
  <div class="eyebrow">{E(cfg['eyebrow'])}</div>
  <h1>{cfg['h1']}</h1>
  <p class="lede">{E(cfg['lede'])}</p>
  <div class="kpis">
    <div class="kp"><b>{n_uc}</b><span>AI use cases</span></div>
    <div class="kp"><b>{len(DATA)}</b><span>{E(cfg['area'].capitalize())}s, end to end</span></div>
    <div class="kp"><b>{n_proc}</b><span>Unit processes</span></div>
    {kp4}
  </div>
  {kfoot}
  <div class="proof"><b>Proven at scale</b><span>400+ factories</span><span>100k+ assets connected</span><span>10B+ data points / day</span><span>↑20%+ OEE</span><span>↓80% unplanned downtime</span></div>
</div></header>

<section class="wrap ov">
  <div class="eyebrow">Executive overview</div>
  <h2>{"Where the value sits" if has_val else "Where AI fits across the plant"}, and how Faclon unlocks it</h2>
  <div class="cca">{ex}</div>
  <div class="ov-grid">
    <div>
      <h3>{E(chart_h)}</h3>
      <div class="chart">{"".join(bars)}{btot}</div>
      {f'<p class="onote">{E(other_note)}</p>' if other_note else ''}
    </div>
    <div>
      <h3>Use-case mix</h3>
      <div class="mix">{mix}</div>
      {tier_mix}
      <div class="howto"><b>How to read each use case</b>{howto}</div>
    </div>
  </div>
</section>

<div class="bar"><div class="wrap">
  <label class="search" for="q">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="{E(cfg['search'])}" aria-label="Search use cases">
  </label>
  <select id="sec" aria-label="{E(cfg['area'].capitalize())}"><option value="">All {E(cfg['area'])}s</option>{"".join(opts)}</select>
  <select id="sort" aria-label="Order"><option value="chain">{E(cfg.get('flow_word', 'Plant flow order'))}</option>{sort_opt}</select>
  <div class="seg" id="kind" role="group" aria-label="Use-case type">
    <button type="button" data-k="" aria-pressed="true">All</button>{"".join(f'<button type="button" data-k="{k}" aria-pressed="false">{KIND[k][0]}</button>' for k in KIND if kinds[k])}
  </div>
  {tier_seg}
  <div class="count" id="count">Showing all {n_uc} use cases</div>
</div></div>

<div class="wrap main">
  <nav class="rail" aria-label="{E(cfg['area'].capitalize())}s">{"".join(rail)}</nav>
  <main>
    <p class="note">{E(note)}</p>
    {"".join(secs)}
    <div class="empty" id="empty" hidden>No use cases match these filters. Try a broader term, or clear the filters.</div>
  </main>
</div>

<div class="cta"><div class="wrap">
  <div class="eyebrow" style="color:var(--blue2)">Next step</div>
  <h2>Explore a focused pilot</h2>
  <p>{E(cfg['cta'])}</p>
  <div class="steps3">
    <div><em>1</em><h3>Connect</h3><p>We tap existing DCS, PLC, lab and camera data: no rip-and-replace.</p></div>
    <div><em>2</em><h3>Prove</h3><p>A live dashboard and a first quantified value unlock inside 4–6 weeks.</p></div>
    <div><em>3</em><h3>Scale</h3><p>A plant-wide rollout plan with shared models and value targets for each area.</p></div>
  </div>
  <div class="cta-row"><p style="font-size:13px">Faclon Labs Pvt Ltd · The operating layer for industrial autonomy. All terms are indicative and subject to mutual agreement.</p>{CTA_BUTTONS}</div>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../">← All solutions</a> · Faclon Labs · {t_esc}</span><span>{E(cfg['sector'])}</span></div></div>
<script>{JS}</script>
</body></html>"""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(HTML, encoding="utf-8")
    print("wrote", out_path, len(HTML), "bytes ·", n_uc, "use cases ·", ", ".join(f"₹{num(v)} cr {b}" for b, v in grand.items()) or "no values")
    return {"use_cases": n_uc, "sections": len(DATA), "units": n_proc, "totals": grand, "kinds": kinds, "tiers": tiers}
