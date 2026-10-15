"""Builds power-plant-ai/index.html (Advisory Agents + Automated Process Control page).

Run from anywhere:  python3 src/power-plant-ai/build_page.py
Edit the AGENTS and APC lists below to change content; the page is regenerated in full.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "power-plant-ai" / "index.html"

# ======================= ADVISORY AGENTS =======================
AGENTS = [
 ("Visibility Agent", "Plant head · Efficiency cell", "eye",
  ["Live DCS tags, energy meters and lab results against HMBD design, shift targets and golden bands",
   "Net / gross heat rate, boiler and turbine efficiency, APC, condenser vacuum, O<sub>2</sub>/CO, emissions margins",
   "First-principles heat balance of the steam cycle, calibrated to live data"],
  ["One live KPI view for the unit, replacing scattered DCS screens and spreadsheets",
   "Heat-rate gap split into named losses (vacuum, dry flue gas, unburnt carbon, APH leakage, spray, heaters, APC) in kcal/kWh and ₹",
   "Deviation alerts with the loss already quantified",
   "Prompt-to-dashboard: ask a question, get the trend or chart"],
  "Why is NHR 38 kcal/kWh above design on night shift?",
  "Two-thirds of the gap is condenser back pressure (CT cells 3 and 5 off at higher wet bulb) and the rest is excess O<sub>2</sub> running 0.8% above the band since the coal source changed."),
 ("Reporting Agent", "Shift in-charge · Management · Compliance", "doc",
  ["DCS and historian data, lab (LIMS) results, energy meters, shift logs and maintenance records",
   "Report templates the plant already uses (shift, daily, monthly MIS, efficiency tests)"],
  ["Shift handover, daily generation and monthly MIS reports drafted automatically",
   "Emissions compliance summaries (SO<sub>2</sub>, NOx, SPM) with exceedance explanations",
   "Efficiency and energy-audit reports with loss attribution",
   "New reports built from a plain-language request, not a ticket to IT"],
  "Make the October performance report for Unit 2 in the usual format.",
  "Drafted: generation, PLF, NHR vs target, APC breakdown, top five losses with ₹ impact, outages with causes and emissions compliance. Two lab values flagged as missing for your review."),
 ("Operations Agent", "Control room operators · Shift in-charge", "gauge",
  ["Combustion: O<sub>2</sub>, CO, NOx, FEGT, windbox and draft pressures, bed temperatures (FBC)",
   "Coal quality from lab and inferred GCV, mill DP, classifier, PF fineness",
   "Steam temperatures and SH/RH spray, condenser vacuum, CT and CW operation, auxiliary loading"],
  ["Ranked setpoint recommendations: excess O<sub>2</sub>, mill classifier and DP, burner tilt, CT fan cells, CW pump combination",
   "Daily coal blend advice for operations and procurement",
   "Which auxiliaries to run at the current load: BFPs, fans, CW pumps",
   "Limestone and SCR/SNCR reagent dosing advice to hold emissions at least cost"],
  "Load is coming down to 70% for the IEX window. What should I change?",
  "Take BFP-B off and carry load on A and C, which are closer to their design curves. Drop CT cells to four. Bring excess O<sub>2</sub> to 3.6%. The expected effect on APC and NHR is shown with each step."),
 ("Maintenance Agent", "Maintenance · Reliability engineers", "wrench",
  ["Vibration spectra, bearing temperatures and motor current on mills, BFPs, ID/FD/PA fans, CW pumps, crushers and conveyors",
   "Section-wise heat-exchange index, APH leakage, HP/LP heater TTD and DCA, ESP field behaviour",
   "Generator winding and cooler temperatures, water and steam chemistry"],
  ["Failure warnings 2–8 weeks ahead with remaining-useful-life estimates",
   "A prioritized work list ranked by risk and ₹ impact, with draft CMMS work orders",
   "Condition-based schedules for soot blowing, ESP, heater and APH seal maintenance",
   "Condenser tube-leak and chemistry-excursion alerts before tube damage sets in"],
  "What should I plan for the shutdown next month?",
  "Eight jobs ranked by risk: PA fan-B bearing (outer-race defect, about 5 weeks of life), APH radial seals (leakage up from 7% to 11%), HP heater-6 (TTD +4 °C)..."),
 ("Breakdown & RCA Agent", "Operations · Maintenance · Plant head", "alert",
  ["Sequence of events, alarms and trip logs, and DCS trends before and after the event",
   "Past failures, RCA reports, maintenance history and OEM manuals linked to the asset",
   "Process and design limits from the ontology"],
  ["Ranked probable root causes with confidence and the evidence trail behind each",
   "A safe restart checklist and what to watch during restart",
   "Recurrence check: has this happened before, and what fixed it?",
   "Every RCA written back to the knowledge base so the next one is faster"],
  "Unit tripped on drum level low at 02:14. Why?",
  "Most likely BFP-A recirculation valve stuck open (82% confidence): discharge flow fell 9 s before the drum-level dip while the motor current held. The same valve was logged in May. Evidence and trends are attached."),
 ("Design Improvement Agent", "Efficiency cell · Projects · Technical services", "pencil",
  ["Long-run performance versus design for every major section and auxiliary",
   "Pump and fan efficiency curves re-traced from operating data",
   "Recurring failures, chronic losses and digital-twin what-if simulations"],
  ["Modification cases: APH seal upgrade, heater retubing, VFD retrofit, pump re-impelling, insulation, CT fill replacement",
   "Each case sized in kcal/kWh, MW, ₹/year and payback",
   "What-if simulation before capex: coal change, extraction change, an asset out of service",
   "An ROI-ranked improvement list for the annual budget"],
  "Is a VFD on ID fan-A worth it?",
  "At your load profile (61% of hours below 80% MCR) the fan runs on the damper most of the year. Estimated saving and payback are shown against three years of operating data."),
 ("Plant Knowledge Co-pilot", "Every role · New joiners", "chat",
  ["OEM manuals, SOPs, P&amp;IDs, HMBD, shift logs and past RCAs, all linked to the asset in the ontology",
   "Live and historical plant data"],
  ["Instant, cited answers to operating and maintenance questions",
   "Step-by-step procedures pulled from the plant’s own SOPs",
   "Faster onboarding, so senior-operator know-how stays in the plant",
   "Works in English and in the regional language"],
  "What is the startup sequence for BFP-C after maintenance?",
  "From SOP-OP-117 (rev 4): 12 steps, with interlocks to check before each one. BFP-C’s last startup note warns about the balancing line vent."),
]

ICONS = {
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "doc": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
 "gauge": '<path d="M12 14l4-4"/><path d="M3.3 17a9 9 0 1 1 17.4 0"/>',
 "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
 "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/>',
 "pencil": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
}
def icon(k):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

def agent_card(i, a):
    name, who, ic, ana, prov, q, ans = a
    al = "".join(f"<li>{x}</li>" for x in ana)
    pl = "".join(f"<li>{x}</li>" for x in prov)
    return f"""
<article class="agent">
  <header><div class="aic">{icon(ic)}</div><div><h4>{name}</h4><div class="who">{who}</div></div><div class="ano">{i:02d}</div></header>
  <div class="ag-cols">
    <div><div class="lbl">What it analyses</div><ul class="ana">{al}</ul></div>
    <div><div class="lbl prov">What it provides</div><ul class="prov">{pl}</ul></div>
  </div>
  <div class="convo">
    <div class="cq"><span>Ask</span>{q}</div>
    <div class="ca"><span>Agent</span>{ans}</div>
  </div>
</article>"""

agents_html = "".join(agent_card(i + 1, a) for i, a in enumerate(AGENTS))
agent_chips = "".join(f"<div class='chip-ag'>{icon(a[2])}<span>{a[0]}</span></div>" for a in AGENTS)

# ======================= APC APPLICATIONS =======================
# name, applicability, model, CVs, MVs, DVs, logic (how it decides, plain language), benefits, value
APC = [
 ("Combustion & Air–Fuel Ratio Optimization", "All boilers", "MPC",
  ["Excess O<sub>2</sub> (economizer outlet)", "CO", "NOx", "FEGT", "Furnace draft"],
  ["FD / secondary-air damper demand", "PA fan / mill air", "Feeder bias", "OFA dampers"],
  ["Coal GCV and moisture (soft sensor)", "Unit load", "Mill combination"],
  ["Finds the lowest excess O<sub>2</sub> the current coal and load allow before CO starts to rise", "Trims air and feeder bias together to hold that point, while keeping fan power in check", "Backs off at once if CO, NOx or furnace draft approach their limits"],
  ["Holds the lowest safe excess O<sub>2</sub> for the coal being fired", "Lower dry-flue-gas loss and fan power", "CO-breakthrough protection built in"], 4),
 ("Bed Temperature & Multi-Feeder Coal Balancing", "CFBC + AFBC", "MPC",
  ["Zone-wise bed temperatures", "Bed DP / inventory", "Main steam pressure"],
  ["Individual feeder speeds", "Secondary-air dampers", "PA flow", "Bed drain"],
  ["Coal quality and size", "Load demand", "Feeder trips"],
  ["Keeps every bed zone close to its target temperature, with a safe margin below sintering", "Shifts coal between feeders to even out hot and cold zones while holding steam pressure", "Moves feeders and air gradually, so the bed never sees sudden changes"],
  ["Tight, even bed temperature", "Sintering and defluidization risk designed out", "Steadier outlet steam, less attemperation"], 5),
 ("Steam Temperature & Attemperation", "All (RH lever on reheat units)", "MPC",
  ["Main steam temperature", "Hot reheat temperature", "Tube-metal temperatures"],
  ["SH and RH spray valves", "Burner tilt (PF) / bed temperature (FBC)", "Gas bias dampers", "Soot-blow trigger"],
  ["Load ramps", "Fouling state (HEI)", "Mill combination"],
  ["Holds main steam and reheat temperature at design", "Corrects the cause first (burner tilt, gas bias, soot blowing) and uses spray only to trim", "Uses RH spray last because it costs the most heat rate, and keeps tube-metal temperatures within limits"],
  ["Steam held at design, not below it", "Lower spray flow, especially costly RH spray", "Less thermal fatigue at desuperheaters"], 3),
 ("Intelligent Soot Blowing", "All boilers", "MILP scheduler",
  ["Heat-exchange index per section", "Steam temperatures", "Flue gas exit temperature"],
  ["Blow / no-blow command per blower", "Blow sequence and timing"],
  ["Fouling rate per section", "Coal ash and slagging index", "Load"],
  ["Scores each section by how much heat it is losing to fouling", "Blows a section only when the heat recovered is worth more than the steam used and the tube wear caused", "Sequences blows to respect steam-header limits and avoid upsetting steam temperature"],
  ["Blows only the sections that need it", "Less blowing steam and tube erosion", "Restores SH/RH absorption balance"], 5),
 ("Condenser Vacuum, CT & CW Optimization", "All boilers", "LP / MILP",
  ["Condenser back pressure", "CW supply temperature"],
  ["CT fan cells on/off", "Per-cell VFD speed", "CW pump combination", "Vacuum pump duty"],
  ["Ambient wet bulb", "Unit load", "Air ingress"],
  ["Weighs the extra MW from a better vacuum against the power drawn by CT fans and CW pumps", "Picks the fan cells, fan speeds and pump combination that give the highest net MW", "Re-optimizes as wet bulb and load change, and rotates cells for even wear"],
  ["Net MW gain, not just a better vacuum", "Fewer fans in mild weather", "Even wear across cells"], 4),
 ("Auxiliary Load Allocation", "All boilers", "LP",
  ["Total feedwater / air / CW demand met"],
  ["Load share across parallel BFPs, ID/FD/PA fans, CW pumps", "Units in service"],
  ["Unit load", "Re-traced efficiency curve of each unit"],
  ["Uses each pump’s and fan’s efficiency curve, re-traced from plant data", "Splits the required flow so total power drawn is lowest, loading the most efficient units first", "Respects each unit’s minimum and maximum flow and decides which units should be running"],
  ["Efficient units loaded first, degraded ones relieved", "Direct cut in auxiliary power", "Maintenance priorities from the same curves"], 6),
 ("ESP Energy Optimization", "All boilers", "MPC + LP",
  ["Stack SPM"],
  ["Per-field TR-set voltage / current limit", "Rapping sequence"],
  ["Dust loading", "Load", "Coal ash content"],
  ["Predicts stack SPM from dust loading and the behaviour of each field", "Lowers TR-set power field by field while SPM stays safely under the limit", "Adjusts rapping so collection stays steady as fields are trimmed"],
  ["Fields energised only as hard as needed", "Lower ESP power", "SPM compliance held continuously"], 2),
 ("Emissions Reagent Dosing (Limestone · SCR/SNCR)", "CFBC / SCR-SNCR equipped", "MPC + soft sensor",
  ["Stack SO<sub>2</sub>", "Stack NOx", "NH<sub>3</sub> slip"],
  ["Limestone feeder rate", "Urea / ammonia injection rate"],
  ["Coal sulphur and nitrogen", "Bed temperature", "Predicted NOx (ahead of analyser)"],
  ["Predicts SO<sub>2</sub> and NOx from coal and combustion conditions before the analyser sees them", "Doses the minimum limestone and urea / ammonia that keeps emissions inside limits", "Caps ammonia slip to protect the SCR catalyst"],
  ["Compliance at the lowest reagent use", "Less ammonia slip, longer catalyst life", "Better fly-ash quality for sale"], 2),
]

def apc_card(i, a):
    name, app, model, cv, mv, dv, logic, ben, val = a
    def ul(xs): return "".join(f"<li>{x}</li>" for x in xs)
    return f"""
<article class="apc">
  <header>
    <div class="apc-no">{i:02d}</div>
    <div class="apc-t"><h4>{name}</h4><div class="tags"><span class="tag t-model">{model}</span><span class="tag t-app">{app}</span></div></div>
    <div class="apc-v"><b>₹{val:g} cr</b><span>up to, per 100 MW</span></div>
  </header>
  <div class="vars">
    <div class="var cv"><div class="vl">Controlled (CV)</div><ul>{ul(cv)}</ul></div>
    <div class="var mv"><div class="vl">Manipulated (MV)</div><ul>{ul(mv)}</ul></div>
    <div class="var dv"><div class="vl">Disturbance (DV)</div><ul>{ul(dv)}</ul></div>
  </div>
  <div class="obj"><div class="vl">How it decides</div><ul>{ul(logic)}</ul></div>
  <div class="ben">{''.join(f'<span>{b}</span>' for b in ben)}</div>
</article>"""

apc_html = "".join(apc_card(i + 1, a) for i, a in enumerate(APC))

# ---------- squeeze-and-shift SVG ----------
def gauss_path(mu, sd, x0, x1, base, peak_h, sx):
    pts = []
    n = 80
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        y = math.exp(-0.5 * ((x - mu) / sd) ** 2)
        pts.append((sx(x), base - y * peak_h))
    d = f"M{pts[0][0]:.1f},{base} " + " ".join(f"L{px:.1f},{py:.1f}" for px, py in pts) + f" L{pts[-1][0]:.1f},{base} Z"
    return d

W, H = 640, 250
base = 200
sx = lambda x: 40 + (x / 10) * 560
before = gauss_path(4.2, 1.15, 0.6, 7.8, base, 85, sx)
after = gauss_path(6.6, 0.45, 5.0, 8.2, base, 150, sx)
lim_x = sx(8.0)
SVG = f"""<svg viewBox="0 0 {W} {H}" class="ss" role="img" aria-label="Squeeze and shift: APC narrows variability so the target can move closer to the limit">
  <line x1="40" y1="{base}" x2="610" y2="{base}" class="ax"/>
  <path d="{before}" class="before"/>
  <path d="{after}" class="after"/>
  <line x1="{lim_x:.1f}" y1="28" x2="{lim_x:.1f}" y2="{base}" class="lim"/>
  <text x="{lim_x+6:.1f}" y="40" class="tl">Constraint</text>
  <text x="{lim_x+6:.1f}" y="54" class="ts">e.g. CO, metal temp,</text>
  <text x="{lim_x+6:.1f}" y="66" class="ts">SPM limit</text>
  <line x1="{sx(4.2):.1f}" y1="{base}" x2="{sx(4.2):.1f}" y2="{base-85}" class="mean b"/>
  <line x1="{sx(6.6):.1f}" y1="{base}" x2="{sx(6.6):.1f}" y2="{base-150}" class="mean a"/>
  <text x="{sx(4.2):.1f}" y="{base-92}" text-anchor="middle" class="tlb">Operator control</text>
  <text x="{sx(6.6)-8:.1f}" y="{base-158}" text-anchor="end" class="tla">With APC</text>
  <line x1="{sx(4.2):.1f}" y1="{base+20}" x2="{sx(6.6):.1f}" y2="{base+20}" class="shift" marker-end="url(#ar)"/>
  <text x="{(sx(4.2)+sx(6.6))/2:.1f}" y="{base+38}" text-anchor="middle" class="tg">② Shift target toward the limit = ₹ benefit</text>
  <text x="{sx(1.4):.1f}" y="{base-34}" text-anchor="middle" class="ts">① Squeeze</text>
  <text x="{sx(1.4):.1f}" y="{base-20}" text-anchor="middle" class="ts">variability</text>
  <defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="arh"/></marker></defs>
</svg>"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Power Plant AI · Faclon Labs</title>
<meta name="description" content="Advisory Agents and Automated Process Control for boilers, turbines and auxiliaries.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--navy2:#13264A;
--blue:#3D63F5;--blue2:#7C95FF;--blueBg:#EEF2FF;--green:#11875F;--greenBg:#E5F5EE;--amber:#C77A12;--amberBg:#FFF4E2;--red:#B5452F;--redBg:#FBF1EE;--violet:#6A45D0;--violetBg:#F1ECFD}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{background:#fff}}
body{{font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:#fff;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}}
sub{{font-size:.68em;line-height:0}}
.wrap{{max-width:1080px;margin:0 auto;padding-left:max(28px,env(safe-area-inset-left,0px));padding-right:max(28px,env(safe-area-inset-right,0px))}}
h1,h2,h3,h4{{letter-spacing:-.015em;line-height:1.2}}
.eyebrow{{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}}
section{{padding:72px 0}}
h2{{font-size:32px;font-weight:700;margin:8px 0 12px}}
.sub{{color:var(--ink2);font-size:17px;max-width:720px}}
ul{{list-style:none}}

/* hero */
.hero{{background:var(--navy);color:#fff;position:relative;overflow:hidden}}
.hero:before{{content:"";position:absolute;right:-180px;top:-200px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,rgba(124,149,255,.32),rgba(124,149,255,0) 68%)}}
.hero .wrap{{position:relative;padding-top:34px;padding-bottom:64px}}
.brand{{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9FB0CC;gap:16px;flex-wrap:wrap}}
.brand b{{color:#fff;letter-spacing:.22em}}
.hero h1{{font-size:clamp(34px,5.4vw,58px);font-weight:700;margin:72px 0 18px;max-width:820px}}
.hero h1 em{{font-style:normal;color:var(--blue2)}}
.hero .lede{{font-size:clamp(16px,1.8vw,19px);color:#C5D0E3;max-width:680px}}
.split{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:44px}}
.sp{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:22px 24px;text-decoration:none;color:#fff;display:block;transition:background .15s}}
.sp:hover{{background:rgba(255,255,255,.09)}}
.sp .k{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}}
.sp.a .k{{color:var(--blue2)}} .sp.b .k{{color:#5FD3A6}}
.sp h3{{font-size:22px;margin:8px 0 6px}}
.sp p{{color:#B7C3D8;font-size:14.5px}}
.sp .meta{{margin-top:14px;font-size:13px;color:#fff;opacity:.85}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:16px;border-radius:12px;overflow:hidden;gap:1px;background:rgba(255,255,255,.1)}}
.kp{{background:var(--navy2);padding:16px 20px}}
.kp b{{font-size:26px;display:block}}
.kp span{{font-size:12.5px;color:#9FB0CC}}
.kp.ac b{{color:#F2B256}}

/* part banners */
.part{{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;padding:28px 0 22px;border-bottom:2px solid var(--ink);margin-bottom:8px}}
.part .pn{{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}}
.part h2{{font-size:40px;margin:6px 0 0}}
.partA .pn{{color:var(--blue)}} .partB .pn{{color:var(--green)}}
.part p{{max-width:420px;color:var(--ink2);font-size:15px}}

/* architecture A */
.archA{{display:grid;grid-template-columns:1fr 44px 1.15fr 44px 1fr;margin-top:32px;align-items:stretch}}
.col{{border:1px solid var(--line);border-radius:14px;padding:18px;background:#fff}}
.col h5{{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-bottom:12px;font-weight:700}}
.src{{display:flex;flex-direction:column;gap:8px}}
.src div{{background:var(--bg);border-radius:9px;padding:10px 12px;font-weight:600;font-size:14px}}
.src small{{display:block;font-weight:400;color:var(--mute);font-size:12.5px;margin-top:1px}}
.onto{{background:var(--navy);border-color:var(--navy);color:#fff}}
.onto h5{{color:#9FB0CC}}
.onto .graph{{width:100%;height:auto;display:block;margin:2px 0 10px}}
.onto ul li{{font-size:13.5px;padding:7px 0;border-top:1px solid rgba(255,255,255,.1);color:#D5DEEE}}
.onto ul li b{{color:#fff;font-weight:600}}
.agentsCol{{background:var(--blueBg);border-color:#D6DEFF}}
.chip-ag{{display:flex;align-items:center;gap:9px;background:#fff;border-radius:9px;padding:8px 10px;margin-bottom:6px;font-size:13.5px;font-weight:600}}
.chip-ag svg{{width:17px;height:17px;color:var(--blue);flex:none}}
.arr{{display:flex;align-items:center;justify-content:center}}
.arr svg{{width:30px;height:30px;color:var(--blue)}}
.toPeople{{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:flex-end;font-size:13.5px;color:var(--ink2)}}
.toPeople b{{color:var(--ink);margin-right:4px}}
.toPeople span{{border:1px solid var(--line);border-radius:20px;padding:4px 12px;background:#fff}}

/* how agent works */
.how{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:44px;counter-reset:h}}
.how div{{background:var(--bg);border-radius:12px;padding:16px;position:relative}}
.how div:before{{counter-increment:h;content:counter(h);display:inline-flex;width:24px;height:24px;border-radius:50%;background:var(--blue);color:#fff;font-size:12px;font-weight:700;align-items:center;justify-content:center;margin-bottom:8px}}
.how b{{display:block;font-size:14.5px;margin-bottom:3px}}
.how p{{font-size:13px;color:var(--ink2)}}

/* agent cards */
.agents{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:36px}}
.agent{{border:1px solid var(--line);border-radius:16px;padding:22px;display:flex;flex-direction:column}}
.agent:last-child:nth-child(odd){{grid-column:1/-1;display:grid;grid-template-columns:1.4fr 1fr;column-gap:28px;align-items:start}}
.agent:last-child:nth-child(odd) header{{grid-column:1/-1}}
.agent:last-child:nth-child(odd) .convo{{margin-top:0;border-top:0;padding-top:0}}
.agent header{{display:flex;gap:14px;align-items:center;margin-bottom:16px}}
.aic{{width:42px;height:42px;border-radius:11px;background:var(--blueBg);color:var(--blue);display:flex;align-items:center;justify-content:center;flex:none}}
.aic svg{{width:22px;height:22px}}
.agent h4{{font-size:19px}}
.who{{font-size:13px;color:var(--mute)}}
.ano{{margin-left:auto;font-size:12px;font-weight:700;color:var(--mute);font-variant-numeric:tabular-nums}}
.ag-cols{{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1}}
.lbl{{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-bottom:8px}}
.lbl.prov{{color:var(--blue)}}
.ag-cols li{{font-size:13.5px;color:var(--ink2);padding:5px 0 5px 16px;position:relative;line-height:1.45}}
.ana li:before{{content:"";position:absolute;left:0;top:12px;width:7px;height:2px;background:#AEB9CA}}
.prov li:before{{content:"";position:absolute;left:0;top:10px;width:7px;height:7px;border-radius:50%;background:var(--blue)}}
.prov li{{color:var(--ink)}}
.convo{{margin-top:16px;border-top:1px dashed var(--line);padding-top:14px;font-size:13.5px}}
.convo span{{font-size:10.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;display:block;margin-bottom:3px}}
.cq{{background:var(--bg);border-radius:12px 12px 12px 3px;padding:10px 12px;margin-bottom:8px;font-style:italic;color:var(--ink)}}
.cq span{{color:var(--mute);font-style:normal}}
.ca{{background:var(--blueBg);border-radius:12px 12px 3px 12px;padding:10px 12px;color:var(--ink2);margin-left:28px}}
.ca span{{color:var(--blue)}}
.illus{{font-size:12.5px;color:var(--mute);margin-top:14px;font-style:italic}}

/* APC */
.archB{{margin-top:32px;border:1px solid var(--line);border-radius:16px;overflow:hidden}}
.zone{{display:grid;grid-template-columns:150px 1fr;gap:18px;padding:16px 18px;align-items:center;border-bottom:1px solid var(--line)}}
.zone.ot{{background:#F3F7F5}}
.zone.dmz{{background:#FFF8EC;border-top:2px dashed #E5BE7A;border-bottom:2px dashed #E5BE7A}}
.zone.it{{background:#F4F6FC}}
.zh{{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;display:flex;flex-direction:column;gap:2px}}
.ot .zh{{color:var(--green)}} .dmz .zh{{color:var(--amber)}} .it .zh{{color:var(--blue)}}
.zh small{{font-weight:500;letter-spacing:.04em;text-transform:none;color:var(--mute);font-size:12px}}
.nodes{{display:flex;align-items:stretch;gap:0}}
.node{{background:#fff;border:1px solid var(--line);border-radius:11px;padding:12px 14px;flex:1;font-size:13px;color:var(--ink2)}}
.node b{{display:block;font-size:14.5px;color:var(--ink);margin-bottom:3px}}
.node.ghost{{visibility:hidden}}
.dmz .node,.it .node{{flex:0 0 calc(50% - 8px)}}
.dmz .nodes,.it .nodes{{gap:16px}}
.node.apcn{{border:2px solid var(--green)}}
.node.apcn.alt{{border-style:dashed;background:transparent}}
.node.apcn.alt b{{display:inline}}
.node .pill{{display:inline-block;font-size:10.5px;font-weight:700;background:var(--greenBg);color:var(--green);border-radius:20px;padding:1px 8px;margin-top:6px;margin-left:0}}
.node.apcn.alt .pill{{margin-left:6px}}
.link{{width:34px;flex:none;display:flex;justify-content:center;align-items:center}}
.link svg{{width:30px;height:12px}}
.flows{{display:flex;gap:22px;flex-wrap:wrap;padding:14px 18px;border-top:1px solid var(--line);font-size:13px;color:var(--ink2);background:#fff}}
.flows i{{display:inline-block;width:22px;height:3px;border-radius:2px;vertical-align:middle;margin-right:7px}}
.up i{{background:var(--blue)}} .down i{{background:var(--green)}} .mdl i{{background:var(--amber)}}

.models{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:40px}}
.model{{border:1px solid var(--line);border-radius:14px;padding:20px}}
.model .mt{{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--green)}}
.model h4{{font-size:19px;margin:6px 0 8px}}
.model p{{font-size:14px;color:var(--ink2)}}
.model .use{{margin-top:10px;font-size:13px;color:var(--ink)}}
.model .use b{{color:var(--mute);font-weight:600;font-size:11px;letter-spacing:.1em;text-transform:uppercase;display:block;margin-bottom:2px}}

.objfn{{margin-top:24px;background:var(--navy);color:#fff;border-radius:16px;padding:26px 28px;display:grid;grid-template-columns:1.3fr 1fr;gap:28px}}
.objfn .lead{{color:#C5D0E3;font-size:16px;line-height:1.6;margin-top:12px;max-width:520px}}
.objfn .mt{{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#5FD3A6}}
.terms li{{padding:10px 0;border-top:1px solid rgba(255,255,255,.1);font-size:14px;color:#C5D0E3}}
.terms li:first-child{{border-top:0}}
.terms b{{display:inline-block;width:22px;height:4px;border-radius:2px;vertical-align:middle;margin-right:9px}}
.terms strong{{color:#fff;font-weight:600}}

.apcs{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:36px}}
.apc{{border:1px solid var(--line);border-radius:16px;padding:20px}}
.apc header{{display:flex;gap:12px;align-items:flex-start;margin-bottom:14px}}
.apc-no{{font-size:12px;font-weight:700;color:var(--green);background:var(--greenBg);border-radius:7px;padding:4px 7px;margin-top:2px}}
.apc-t{{flex:1}}
.apc-t h4{{font-size:17.5px;margin-bottom:6px}}
.tags{{display:flex;gap:6px;flex-wrap:wrap}}
.tag{{font-size:11.5px;font-weight:600;border-radius:20px;padding:2px 9px;white-space:nowrap}}
.t-model{{background:var(--greenBg);color:var(--green)}}
.t-app{{border:1px solid var(--line);color:var(--ink2)}}
.apc-v{{text-align:right}}
.apc-v b{{font-size:19px;color:var(--green);display:block;line-height:1.1}}
.apc-v span{{font-size:10.5px;color:var(--mute)}}
.vars{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.var{{border-radius:10px;padding:10px 11px}}
.var.cv{{background:var(--blueBg)}} .var.mv{{background:var(--greenBg)}} .var.dv{{background:var(--bg)}}
.vl{{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:5px}}
.cv .vl{{color:var(--blue)}} .mv .vl{{color:var(--green)}} .dv .vl{{color:var(--mute)}}
.var li{{font-size:12.5px;color:var(--ink2);padding:2px 0;line-height:1.4}}
.obj{{margin-top:10px;border:1px solid var(--line);border-radius:10px;padding:10px 12px}}
.obj .vl{{color:var(--amber)}}
.obj li{{font-size:13px;color:var(--ink);padding:3px 0 3px 16px;position:relative;line-height:1.45}}
.obj li:before{{content:"";position:absolute;left:0;top:10px;width:7px;height:7px;border-radius:50%;background:var(--amber)}}
.ben{{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}}
.ben span{{font-size:12.5px;background:#fff;border:1px solid #CDE9DC;color:#0E6B4C;border-radius:20px;padding:3px 10px}}
.ben span:before{{content:"✓ ";font-weight:700}}

.ssWrap{{display:grid;grid-template-columns:1.25fr 1fr;gap:32px;align-items:center;margin-top:24px}}
.ss{{width:100%;height:auto}}
.ss .ax{{stroke:#AEB9CA;stroke-width:1.5}}
.ss .before{{fill:rgba(181,69,47,.10);stroke:#C9735F;stroke-width:1.8}}
.ss .after{{fill:rgba(17,135,95,.14);stroke:var(--green);stroke-width:2}}
.ss .lim{{stroke:var(--red);stroke-width:2;stroke-dasharray:5 4}}
.ss .mean{{stroke-width:1.2;stroke-dasharray:3 3}}
.ss .mean.b{{stroke:#C9735F}} .ss .mean.a{{stroke:var(--green)}}
.ss text{{font-family:Inter,sans-serif}}
.ss .tl{{font-size:13px;font-weight:700;fill:var(--red)}}
.ss .ts{{font-size:11.5px;fill:var(--mute)}}
.ss .tlb{{font-size:12.5px;font-weight:600;fill:#B05A47}}
.ss .tla{{font-size:12.5px;font-weight:700;fill:var(--green)}}
.ss .tg{{font-size:12.5px;font-weight:600;fill:var(--ink)}}
.ss .shift{{stroke:var(--ink);stroke-width:1.6}}
.ss .arh{{fill:var(--ink)}}
.ssTxt h3{{font-size:24px;margin:6px 0 10px}}
.ssTxt p{{color:var(--ink2);font-size:15px;margin-bottom:10px}}

.safe{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:28px}}
.safe div{{background:var(--bg);border-radius:12px;padding:16px}}
.safe b{{display:block;font-size:14.5px;margin-bottom:4px}}
.safe p{{font-size:13.5px;color:var(--ink2)}}
.path{{display:flex;margin-top:28px;border-radius:12px;overflow:hidden;border:1px solid var(--line)}}
.path div{{flex:1;padding:14px 16px;font-size:13.5px;color:var(--ink2);border-right:1px solid var(--line);background:#fff}}
.path div:last-child{{border:0;background:var(--greenBg)}}
.path b{{display:block;color:var(--ink);font-size:14.5px}}
.path small{{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--green)}}

/* benefits */
.benefits{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:28px}}
.bn{{border-top:3px solid var(--green);padding:14px 2px 0}}
.bn b{{font-size:16px;display:block;margin-bottom:4px}}
.bn p{{font-size:13.5px;color:var(--ink2)}}

/* proof */
.proof{{background:var(--bg)}}
.cases{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}}
.case{{background:#fff;border-radius:14px;padding:20px;border:1px solid var(--line)}}
.case .ct{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.case .cn{{font-size:18px;font-weight:700}}
.case .cx{{font-size:12.5px;color:var(--mute);margin-bottom:12px}}
.case .pt{{font-weight:600;font-size:14.5px;margin-top:12px}}
.case p{{font-size:13.5px;color:var(--ink2)}}
.stat{{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}}
.stat span{{font-size:12.5px;background:var(--blueBg);border-radius:8px;padding:4px 9px;color:var(--ink2)}}
.stat span b{{color:var(--blue);font-size:14px;margin-right:4px}}
.stat span.prog{{background:var(--amberBg);color:var(--amber);font-weight:700;font-size:11px;letter-spacing:.1em;text-transform:uppercase}}
.ptag{{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:2px 8px;border-radius:20px}}
.ptag.ca{{background:var(--blueBg);color:var(--blue)}} .ptag.b{{background:var(--greenBg);color:var(--green)}}

.cta{{background:var(--navy);color:#fff}}
.cta .wrap{{display:flex;justify-content:space-between;align-items:center;gap:28px;padding-top:56px;padding-bottom:56px;flex-wrap:wrap}}
.cta h2{{color:#fff}}
.cta p{{color:#C5D0E3;max-width:560px}}
.btn{{background:var(--blue2);color:#fff;font-weight:700;padding:13px 24px;border-radius:30px;text-decoration:none;white-space:nowrap}}
.foot{{background:var(--navy);color:#6F80A0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid rgba(255,255,255,.08)}}
.foot .wrap{{display:flex;justify-content:space-between;gap:16px;padding-top:18px;padding-bottom:22px;flex-wrap:wrap}}

@media (max-width:900px){{
  .archA{{grid-template-columns:1fr}}
  .arr{{height:36px}} .arr svg{{transform:rotate(90deg)}}
  .how{{grid-template-columns:1fr 1fr}}
  .agents,.apcs{{grid-template-columns:1fr}}
  .agent:last-child:nth-child(odd){{display:flex}} .agent:last-child:nth-child(odd) .convo{{margin-top:16px;border-top:1px dashed var(--line);padding-top:14px}}
  .zone{{grid-template-columns:1fr;gap:10px}} .zh{{flex-direction:row;gap:10px;align-items:baseline}}
  .models,.safe,.cases{{grid-template-columns:1fr}}
  .objfn,.ssWrap{{grid-template-columns:1fr}}
  .benefits{{grid-template-columns:1fr 1fr}}
  .kpis{{grid-template-columns:1fr 1fr}}
  .path{{flex-direction:column}} .path div{{border-right:0;border-bottom:1px solid var(--line)}}
  .part{{flex-direction:column;align-items:flex-start}}
}}
@media (max-width:640px){{
  .wrap{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
  section{{padding:52px 0}}
  h2{{font-size:26px}} .part h2{{font-size:30px}}
  .split{{grid-template-columns:1fr}}
  .ag-cols,.vars{{grid-template-columns:1fr}}
  .how{{grid-template-columns:1fr}}
  .nodes,.dmz .nodes,.it .nodes{{flex-direction:column;gap:8px}} .dmz .node,.it .node{{flex:1}} .node.ghost{{display:none}} .ot .nodes{{gap:0}}
  .link{{width:auto;height:30px;flex-direction:row}} .link svg{{transform:rotate(90deg)}}
  .ca{{margin-left:12px}}
    .benefits{{grid-template-columns:1fr}}
}}
@media print{{ .sp:hover{{background:none}} section{{padding:40px 0}} .agent,.apc,.case{{break-inside:avoid}} }}
</style></head>
<body>

<div class="hero"><div class="wrap">
  <div class="brand"><a href="../" style="color:#fff;text-decoration:none"><b>Faclon Labs</b></a><span>Power Plant AI · Boiler · Turbine · Auxiliaries</span></div>
  <a href="../" style="display:inline-block;margin-top:18px;color:#9FB0CC;font-size:13px;text-decoration:none">← All solutions</a>
  <h1>AI that advises your people <em>and</em> controls your process</h1>
  <p class="lede">Two complementary offerings for captive and utility power plants. Advisory Agents turn plant data into decisions for every team. Automated Process Control writes optimal setpoints back to the DCS, around the clock.</p>
  <div class="split">
    <a class="sp a" href="#agents"><div class="k">Part A</div><h3>Advisory Agents</h3><p>AI agents that analyse plant data through a shared plant ontology and give each team insights, reports, recommendations and root causes.</p><div class="meta">7 agents · humans decide →</div></a>
    <a class="sp b" href="#apc"><div class="k">Part B</div><h3>Automated Process Control</h3><p>Model-predictive and optimization controllers running in the OT network, writing setpoints to the DCS over OPC within safe bounds.</p><div class="meta">8 APC applications · closed loop →</div></a>
  </div>
  <div class="kpis">
    <div class="kp ac"><b>3–5%</b><span>Net heat rate reduction</span></div>
    <div class="kp"><b>98.4%</b><span>Validated RCA recommendation accuracy</span></div>
    <div class="kp"><b>₹1 cr / yr</b><span>Closed-loop soot blowing, 16 MW boiler</span></div>
    <div class="kp"><b>2–8 weeks</b><span>Early warning before equipment failure</span></div>
  </div>
</div></div>

<!-- ================= PART A ================= -->
<div class="wrap" id="agents">
<section>
  <div class="part partA"><div><div class="pn">Part A</div><h2>Advisory Agents</h2></div><p>Agents that read everything the plant knows, reason over it, and tell the right person what to do and why.</p></div>

  <div class="eyebrow" style="margin-top:36px">Architecture</div>
  <h2>Data → Ontology → Agents</h2>
  <p class="sub">Every agent reasons over one shared model of the plant, the ontology. It knows that tag <i>2HFB10CP001</i> is the economizer outlet O<sub>2</sub> of boiler 2, which ID fan it relates to, its design value, and which manual page explains it.</p>

  <div class="archA">
    <div class="col"><h5>Plant data</h5>
      <div class="src">
        <div>DCS / SCADA<small>Real-time process tags, alarms, sequence of events</small></div>
        <div>Historian<small>Years of high-frequency process history</small></div>
        <div>Data platforms<small>Data lake, ERP / CMMS, energy meters</small></div>
        <div>Documents<small>OEM manuals, HMBD, P&amp;IDs, SOPs, shift logs, past RCAs</small></div>
        <div>Lab information<small>LIMS: coal proximate/ultimate &amp; GCV, water chemistry, ash LOI</small></div>
      </div>
    </div>
    <div class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 12h15M14 6l6 6-6 6"/></svg></div>
    <div class="col onto"><h5>Ontology platform</h5>
      <svg class="graph" viewBox="0 0 300 120" aria-hidden="true">
        <g stroke="#4C66A8" stroke-width="1.3">
          <line x1="150" y1="22" x2="70" y2="62"/><line x1="150" y1="22" x2="150" y2="62"/><line x1="150" y1="22" x2="232" y2="62"/>
          <line x1="70" y1="62" x2="34" y2="102"/><line x1="70" y1="62" x2="104" y2="102"/>
          <line x1="150" y1="62" x2="150" y2="102"/><line x1="232" y1="62" x2="206" y2="102"/><line x1="232" y1="62" x2="268" y2="102"/>
          <line x1="104" y1="102" x2="150" y2="102" stroke-dasharray="3 3" stroke="#7C95FF"/>
        </g>
        <g font-family="Inter,sans-serif" font-size="9.5" text-anchor="middle">
          <rect x="114" y="12" width="72" height="20" rx="10" fill="#7C95FF"/><text x="150" y="25.5" fill="#fff" font-weight="700">Unit 2</text>
          <rect x="42" y="52" width="56" height="20" rx="10" fill="#1E3666"/><text x="70" y="65.5" fill="#fff">Boiler</text>
          <rect x="122" y="52" width="56" height="20" rx="10" fill="#1E3666"/><text x="150" y="65.5" fill="#fff">Turbine</text>
          <rect x="204" y="52" width="56" height="20" rx="10" fill="#1E3666"/><text x="232" y="65.5" fill="#fff">Auxiliaries</text>
          <rect x="10" y="92" width="48" height="20" rx="10" fill="#13264A" stroke="#4C66A8"/><text x="34" y="105.5" fill="#C5D0E3">APH</text>
          <rect x="80" y="92" width="48" height="20" rx="10" fill="#13264A" stroke="#4C66A8"/><text x="104" y="105.5" fill="#C5D0E3">O₂ tag</text>
          <rect x="126" y="92" width="48" height="20" rx="10" fill="#13264A" stroke="#4C66A8"/><text x="150" y="105.5" fill="#C5D0E3">HMBD</text>
          <rect x="182" y="92" width="48" height="20" rx="10" fill="#13264A" stroke="#4C66A8"/><text x="206" y="105.5" fill="#C5D0E3">ID fan</text>
          <rect x="244" y="92" width="48" height="20" rx="10" fill="#13264A" stroke="#4C66A8"/><text x="268" y="105.5" fill="#C5D0E3">BFP</text>
        </g>
      </svg>
      <ul>
        <li><b>Asset hierarchy</b>: unit → boiler → APH → radial seal</li>
        <li><b>Tags mapped to assets</b>, with units, ranges and quality</li>
        <li><b>Relationships</b>: feeds, drives, heats, is controlled by</li>
        <li><b>KPIs &amp; physics</b>: heat balance, design curves, limits</li>
        <li><b>Documents &amp; history</b> linked to each asset</li>
      </ul>
    </div>
    <div class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 12h15M14 6l6 6-6 6"/></svg></div>
    <div class="col agentsCol"><h5>Agents</h5>{agent_chips}</div>
  </div>
  <div class="toPeople"><b>Delivered to</b><span>Chat</span><span>Reports</span><span>Alerts</span><span>Dashboards</span><span>CMMS work orders</span><span>Email / WhatsApp</span></div>

  <div class="how">
    <div><b>Trigger</b><p>A KPI deviation, a schedule, an alarm or a question from a user</p></div>
    <div><b>Retrieve context</b><p>Pulls the relevant assets, tags, limits and documents from the ontology</p></div>
    <div><b>Analyse</b><p>Runs physics models, ML models and history comparisons</p></div>
    <div><b>Recommend</b><p>Ranked actions with ₹ impact and the evidence behind each</p></div>
    <div><b>Learn</b><p>Accepted or rejected advice and new RCAs feed back into the knowledge base</p></div>
  </div>

  <div class="eyebrow" style="margin-top:72px">The agents</div>
  <h2>One agent for each job in the plant</h2>
  <p class="sub">Each agent has a clear user, a defined set of data it analyses, and a defined output. All agents share the same ontology, so they agree with each other.</p>
  <div class="agents">{agents_html}</div>
  <p class="illus">Conversations are illustrative and show the shape of agent responses.</p>
</section>
</div>

<!-- ================= PART B ================= -->
<div style="background:linear-gradient(#fff,#FAFCFB)">
<div class="wrap" id="apc">
<section>
  <div class="part partB"><div><div class="pn">Part B</div><h2>Automated Process Control</h2></div><p>Multivariable controllers that hold the plant at its economic optimum every minute, not just when the best operator is on shift.</p></div>

  <div class="eyebrow" style="margin-top:36px;color:var(--green)">Architecture</div>
  <h2>DCS → OPC → APC, inside the OT boundary</h2>
  <p class="sub">The APC engine runs in the OT network or the DMZ, close to the DCS. It reads process values and writes setpoints over OPC. Model training and monitoring happen on the IT side, and only validated models cross the DMZ.</p>

  <div class="archB">
    <div class="zone it"><div class="zh">IT network<small>Level 4</small></div>
      <div class="nodes"><div class="node"><b>Faclon AI platform</b>Model build and retraining on historian data, and APC performance dashboards</div><div class="node ghost"></div></div>
    </div>
    <div class="zone dmz"><div class="zh">DMZ<small>Level 3.5</small></div>
      <div class="nodes"><div class="node"><b>I/O Connect</b>Secure gateway: historian mirror out, validated models in. Firewalled, with no direct IT → DCS path</div><div class="node apcn alt"><b>APC engine</b> can also be hosted here<span class="pill">option</span></div></div>
    </div>
    <div class="zone ot"><div class="zh">OT network<small>Levels 0–3</small></div>
      <div class="nodes">
        <div class="node"><b>Field</b>Dampers, feeders, spray valves, fans, analysers</div><div class="link"><svg viewBox="0 0 30 12"><path d="M0 4h26M22 1l4 3-4 3" fill="none" stroke="#3D63F5" stroke-width="1.6"/><path d="M30 9H4M8 6L4 9l4 3" fill="none" stroke="#11875F" stroke-width="1.6"/></svg></div>
        <div class="node"><b>DCS</b>Base PID control, interlocks, operator HMI with APC ON/OFF</div><div class="link"><svg viewBox="0 0 30 12"><path d="M0 4h26M22 1l4 3-4 3" fill="none" stroke="#3D63F5" stroke-width="1.6"/><path d="M30 9H4M8 6L4 9l4 3" fill="none" stroke="#11875F" stroke-width="1.6"/></svg></div>
        <div class="node"><b>OPC UA / DA server</b>Read PVs, write remote setpoints and biases</div><div class="link"><svg viewBox="0 0 30 12"><path d="M0 4h26M22 1l4 3-4 3" fill="none" stroke="#3D63F5" stroke-width="1.6"/><path d="M30 9H4M8 6L4 9l4 3" fill="none" stroke="#11875F" stroke-width="1.6"/></svg></div>
        <div class="node apcn"><b>APC engine</b>MPC / LP solver, soft sensors, watchdog<span class="pill">Default: OT Level 3</span></div>
      </div>
    </div>
    <div class="flows"><span class="up"><i></i>Process values up (seconds)</span><span class="down"><i></i>Optimal setpoints down to the DCS, within bounds</span><span class="mdl"><i></i>Validated models deployed through the DMZ</span></div>
  </div>

  <div class="eyebrow" style="margin-top:72px;color:var(--green)">Models</div>
  <h2>The right optimizer for each control problem</h2>
  <div class="models">
    <div class="model"><div class="mt">Dynamic · fast</div><h4>Model Predictive Control (MPC)</h4><p>Predicts how each CV will move over the next minutes for every possible MV move. It picks the moves that best meet targets without breaking limits, then repeats every cycle.</p><div class="use"><b>Used for</b>Combustion, bed temperature, steam temperature, ESP, emissions</div></div>
    <div class="model"><div class="mt">Steady-state · economic</div><h4>Linear / Mixed-Integer Programming</h4><p>Finds the cheapest way to meet a demand across many units with on/off and capacity limits. It works from efficiency curves re-traced from plant data.</p><div class="use"><b>Used for</b>Aux load allocation, CT/CW optimization, soot-blowing schedules</div></div>
    <div class="model"><div class="mt">Inference · AI</div><h4>Soft sensors &amp; ML models</h4><p>Estimate what isn’t measured online (coal GCV, PF fineness, NOx ahead of the analyser, fouling) and feed them to the MPC and LP as live inputs.</p><div class="use"><b>Used for</b>Feedforward and disturbance rejection in every application</div></div>
  </div>

  <div class="objfn">
    <div><div class="mt">How every controller decides</div>
      <p class="lead">Every few seconds, each controller looks at where the plant is now, predicts where it is heading, and chooses the next small set of moves. It balances three things, and it never crosses a limit the plant engineers have set.</p>
    </div>
    <ul class="terms">
      <li><b style="background:#9FC0FF"></b><strong>Stay on target.</strong> Keep O<sub>2</sub>, steam temperature, bed temperature and emissions where they should be.</li>
      <li><b style="background:#F2B256"></b><strong>Move gently.</strong> Prefer small, steady valve and damper moves that protect equipment and keep operators’ trust.</li>
      <li><b style="background:#5FD3A6"></b><strong>Run at least cost.</strong> Among the safe options, choose the one that uses the least fuel, spray, auxiliary power or reagent.</li>
    </ul>
  </div>

  <div class="eyebrow" style="margin-top:72px;color:var(--green)">Applications</div>
  <h2>What we control, and what it is worth</h2>
  <p class="sub">For each application: the variables held on target (CV), the handles the APC moves (MV), the disturbances it anticipates (DV), and how it decides each move. Values are indicative, “up to” per 100 MW per year, and are re-baselined against your data.</p>
  <div class="apcs">{apc_html}</div>

  <div class="eyebrow" style="margin-top:72px;color:var(--green)">Why it pays</div>
  <div class="ssWrap">
    <div>{SVG}</div>
    <div class="ssTxt"><h3>Squeeze, then shift</h3>
      <p>Under manual control, operators keep a wide safety margin from every limit because the process swings. APC first <b>squeezes</b> the variability.</p>
      <p>The target can then <b>shift</b> closer to the constraint (lower O<sub>2</sub>, higher steam temperature, less spray) without ever crossing it. The gap between the two averages is the benefit.</p>
    </div>
  </div>

  <div class="benefits">
    <div class="bn"><b>Lower heat rate</b><p>Less dry-gas, unburnt and spray loss; steam held at design</p></div>
    <div class="bn"><b>Lower aux power</b><p>Fans, pumps, CT cells and ESP run only as hard as needed</p></div>
    <div class="bn"><b>Stable operation</b><p>Less variability, faster load-following on IEX ramps, consistent across shifts</p></div>
    <div class="bn"><b>Compliance at least cost</b><p>SO<sub>2</sub>, NOx and SPM held inside limits with minimum reagent</p></div>
  </div>

  <div class="eyebrow" style="margin-top:72px;color:var(--green)">Safety by design</div>
  <h2>The DCS stays in charge</h2>
  <div class="safe">
    <div><b>Operator switch per loop</b><p>Each APC loop has an ON/OFF on the DCS faceplate. The operator can take back control at any moment.</p></div>
    <div><b>Bounded writes</b><p>Setpoints are clamped within engineer-set bands and rate-of-change limits. The APC never writes to final control elements directly.</p></div>
    <div><b>Watchdog fallback</b><p>A heartbeat between the APC and the DCS. If it is lost, the DCS reverts bumplessly to base PID control.</p></div>
    <div><b>DCS interlocks untouched</b><p>Protection, burner management and trips stay in the DCS/BMS. The APC sits above them, never in place of them.</p></div>
    <div><b>Offline validation</b><p>Every controller is tested on the digital twin before go-live.</p></div>
    <div><b>Full audit trail</b><p>Every write, override and switch-off is logged for review by the plant’s C&amp;I team.</p></div>
  </div>
  <div class="path">
    <div><small>Step 1</small><b>Step tests &amp; model ID</b>Plant response identified for each MV</div>
    <div><small>Step 2</small><b>Offline simulation</b>Controller tuned on the digital twin</div>
    <div><small>Step 3</small><b>Advisory mode</b>Recommendations shown, operator applies them</div>
    <div><small>Step 4</small><b>Closed loop</b>Setpoints written in narrow bands, then widened</div>
  </div>
</section>
</div>
</div>

<!-- ================= PROOF ================= -->
<div class="proof"><div class="wrap"><section>
  <div class="eyebrow">Proof</div>
  <h2>Already running in plants</h2>
  <div class="cases">
    <div class="case"><div class="ct"><div class="cn">SPB</div><span class="ptag a">Agents + APC</span></div><div class="cx">21 MW cogeneration · 16 MW recovery boiler</div>
      <div class="pt">Automated RCA Agents</div><p>Flag deviations across boiler, turbine, generator and auxiliaries with root cause and recommendation.</p>
      <div class="stat"><span><b>100+</b>RCAs daily</span><span><b>98.4%</b>accuracy</span></div>
      <div class="pt">Closed-loop soot blowing</div><p>29 soot blowers on the recovery boiler.</p>
      <div class="stat"><span><b>20 TPD</b>steam saved</span><span><b>₹1 cr</b>/ yr</span></div>
      <div class="pt">APC for coal feeding</div><p>7 coal feeders on the AFBC boiler.</p>
      <div class="stat"><span class="prog">In progress</span></div>
    </div>
    <div class="case"><div class="ct"><div class="cn">JSW Energy</div><span class="ptag a">Agents</span></div><div class="cx">Five plants · predictive maintenance</div>
      <div class="pt">Vibration-based condition monitoring</div><p>1,000+ vibration sensors across five plants, cutting unplanned downtime and maintenance cost.</p>
      <div class="stat"><span><b>15+</b>failures caught early</span><span><b>₹1.3 cr</b>over 2 yrs</span></div>
      <div class="pt" style="margin-top:22px">Tata Power · Prayagraj</div><p>Energy meters integrated to benchmark BFPs and ID/FD fans live.</p>
    </div>
    <div class="case"><div class="ct"><div class="cn">Hindustan Zinc · Grasim</div></div><div class="cx">91 MW captive · 175 MW captive (5 boilers, 5 turbines)</div>
      <div class="pt">APC reduction &amp; NHR reduction</div><p>Historian, EMS and lab data integrated. Auxiliary efficiency curves re-traced and run cycles scheduled to load, coal and season. NHR models handle IEX-driven load swings.</p>
      <div class="stat"><span><b>1 pp</b>APC reduction target</span><span class="prog">In progress</span></div>
    </div>
  </div>
</section></div></div>

<div class="cta"><div class="wrap">
  <div><div class="eyebrow" style="color:var(--blue2)">Next step</div><h2>Start with your data</h2><p>Share a sample of DCS, lab and design data. We will return a shortlist of agents and APC applications sized against your plant’s own loss profile, then confirm it on a plant visit.</p></div>
  <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="https://www.faclonlabs.com">www.faclonlabs.com</a><a class="btn" style="background:transparent;border:1.5px solid #7C95FF" href="power-plant-ai-use-case-catalogue.pdf">Use-case catalogue (PDF)</a></div>
</div></div>
<div class="foot"><div class="wrap"><span><a href="../" style="color:inherit;text-decoration:none">← All solutions</a> · Faclon Labs · Power Plant AI</span><span>Advisory Agents · Automated Process Control</span></div></div>
</body></html>"""

OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(HTML), "bytes")
