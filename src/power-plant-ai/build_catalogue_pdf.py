"""Builds power-plant-ai/power-plant-ai-use-case-catalogue.pdf — one continuous (single tall page) PDF
covering all 24 use cases, customer cases and engagement approach.

Run:  python3 src/power-plant-ai/build_catalogue_pdf.py   (needs: pip install playwright; a Chromium)
"""
import html, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP = Path(__file__).with_name("_catalogue.html")
OUT = ROOT / "power-plant-ai" / "power-plant-ai-use-case-catalogue.pdf"
from playwright.sync_api import sync_playwright

E = html.escape

# ---------------- USE CASES ----------------
# (name, type, applicability, value_cr, bullets[3], problems[])
SECTIONS = [
 ("01", "Overall Efficiency", "Plant-wide view of heat rate and its losses", [
  ("SME Co-pilot", "Analytics", "All boilers", 5, [
    "Benchmarks canonical KPIs live — net/gross heat rate, boiler and turbine efficiency, APC, condenser vacuum, excess O<sub>2</sub>/CO, emissions margins, reliability — against HMBD design, shift target and golden band.",
    "On deviation, cross-references symptoms across boiler, steam cycle, turbine, auxiliaries and emissions to rank probable root causes with confidence scores and cost attribution.",
    "Answers operator queries through a chatbot and issues ranked corrective actions — e.g. <i>“cut excess O<sub>2</sub> from 4.2 to 3.5%”</i>, <i>“address APH radial seal leakage”</i>, <i>“redistribute BFP load to BFP #2”</i>."],
   ["KPI reporting fragmented across dashboards with no unified view", "Operators don’t know which lever to pull when a KPI drifts", "Diagnostic know-how is tribal and retires with senior operators", "Boiler and turbine teams troubleshoot in silos"]),
  ("Digital Twin Simulation", "Analytics", "All boilers", 4, [
    "First-principles heat and mass balance of the steam cycle, built from HMBD and OEM design data and continuously calibrated to live DCS and lab data.",
    "Splits the NHR gap versus design into named losses — condenser vacuum, dry flue gas, unburnt carbon, APH leakage, spray, heater performance, APC — each in kcal/kWh and ₹/year.",
    "Simulates what-ifs before touching the plant: coal blends, IEX-driven load ramps, an asset out of service, extraction changes. Sweeps setpoints for the feasible optimum at each load and validates closed-loop strategies offline before any setpoint reaches the DCS."],
   ["Heat rate gap known only as a single number", "Golden bands set from historical best bake in existing inefficiency", "No safe way to test a control strategy before it touches the DCS"]),
 ]),
 ("02", "Process Control", "Closed-loop and advisory control of combustion, steam and emissions", [
  ("Multi-Feeder Coal Load Balancing + Bed Temperature Stabilization", "Closed-loop APC", "CFBC + AFBC", 5, [
    "Analyses bed temperature distribution and pressure drop, individual feeder rates, secondary air pattern, outlet steam stability and live coal quality.",
    "Detects bed swings and feeder-level firing imbalance — the coupled bed-and-feeder problem that operator control treats as separate loops.",
    "Pushes closed-loop bias setpoints to feeders and secondary air dampers, holding bed temperature tight and preventing sintering and defluidization. A stable bed steadies outlet steam temperature and cuts reliance on attemperation."],
   ["Bed temperature swings drive efficiency loss and sintering risk", "Multi-feeder coordination is manual and skill-dependent", "Coal quality variability destabilizes the bed", "Sintering and defluidization cause forced outages"]),
  ("Air-Fuel Ratio Optimizer", "Closed-loop APC", "All boilers", 4, [
    "Analyses flue gas O<sub>2</sub> at economizer outlet, CO, NOx, FEGT, live coal quality and load.",
    "Predicts the safe minimum excess O<sub>2</sub> setpoint for current coal and load — the efficiency that safety-margin setpoints leave on the table.",
    "Pushes coordinated setpoints to fan demand, dampers and feeder rates, holding optimal O<sub>2</sub> with live CO-breakthrough protection."],
   ["Plants run safety-margin excess O<sub>2</sub>", "CO/O<sub>2</sub> trade-off left to operator judgment", "Weak multivariate coordination across PA/FD fans, dampers and feeders", "Coal quality changes cause excess-air swings"]),
  ("Attemperation Optimization", "Closed-loop APC", "All (RH spray lever on reheat units)", 3, [
    "Analyses main steam and hot reheat temperature, SH/RH spray flow and valve position, degrees of superheat, section-wise SH/RH absorption, burner tilt (PF) or bed temperature (FBC), excess O<sub>2</sub> and soot-blowing state.",
    "Separates spray genuinely needed for tube-metal protection from spray masking correctable upstream imbalance — fouling profile, air distribution, burner tilt, mill combination.",
    "Corrects upstream levers first and trims spray only for residual control — cutting spray flow (especially costlier RH spray) and thermal fatigue at desuperheaters and outlet headers."],
   ["Spray used as the primary steam temperature controller", "RH spray’s far larger heat-rate penalty is invisible to operators", "Steam held below design to preserve spray margin", "Attemperation masks upstream fouling and mill imbalance"]),
  ("Condenser–Cooling Tower Vacuum Optimizer", "Advisory", "All boilers", 4, [
    "Analyses turbine exhaust enthalpy and back pressure, condenser TTD, CW supply/return temperatures, ambient wet bulb, load and air ingress.",
    "Predicts the optimal trade-off between vacuum gain and the aux-power penalty of CT fans, CW pumps and vacuum pumps as ambient and load shift.",
    "Advises CT fan cells ON, CW pump combination, header pressure trim, per-cell VFD speed and vacuum-pump duty cycle."],
   ["Vacuum below design is a direct output loss", "CW and CT operation static regardless of ambient/load", "Air ingress hidden until significant", "All CT cells run in mild weather"]),
  ("Mill Fineness & PF Granulometry Optimization", "Advisory", "PF + SC + USC", 3, [
    "Analyses PF fineness, classifier setpoint, mill DP, outlet temperature, live coal particle size from computer vision and inferred grindability.",
    "Predicts mill power versus fineness target per coal type, including the LOI penalty from coarse particles.",
    "Advises classifier speed and mill DP to hold target fineness at minimum specific energy, each mill tuned to its coal source."],
   ["Coarse PF raises LOI and unburnt carbon loss", "Classifier settings rarely re-tuned", "Over-fineness wastes mill power", "Grindability variability ignored"]),
  ("Multi-Coal Blend Advisory", "Analytics", "Multi-source coal", 3, [
    "Analyses stockpile inventory by source, cost economics, coal quality, boiler behaviour per source and forward dispatch.",
    "Predicts combustion, slagging, emissions, mill capacity and cost per kcal delivered for each candidate blend.",
    "Issues a daily, explainable blend recommendation for joint operations and procurement — advisory, not auto-execute."],
   ["Multiple sources with widely varying quality and cost", "Blending decided weekly, not daily", "Operability constraints learned by experience, not modeled", "Cheap coals can cause expensive operating problems"]),
  ("Limestone Dosing & SO<sub>2</sub> Capture Optimization", "Advisory", "CFBC only", 2, [
    "Analyses live stack SO<sub>2</sub>, coal sulphur, bed temperature and limestone feeder rate against in-bed sulfation chemistry.",
    "Predicts SO<sub>2</sub> capture efficiency across Ca:S ratios, including bed-temperature effects on kinetics.",
    "Advises feeder setpoint to hold stack SO<sub>2</sub> in band at minimum Ca:S — cutting limestone use and improving fly-ash quality for cement sale."],
   ["Limestone overdosed against SO<sub>2</sub> spikes", "Compliance margins tightening under new norms", "Coal sulphur varies cargo to cargo", "Excess limestone hurts fly-ash sale value"]),
  ("Furnace Draft & Windbox Pressure Balancing", "Advisory", "All boilers", 2, [
    "Analyses furnace draft at multiple points, windbox pressure across burner elevations (PF) or distributor-plate DP across bed sections (CFBC/AFBC), fan currents and damper positions.",
    "Detects draft instability and windbox bias causing uneven combustion or non-uniform fluidization.",
    "Provides coordinated fan-demand and damper trim for stable draft and uniform windbox pressure, with anticipatory adjustment on load ramps."],
   ["Draft swings cause inefficient combustion and emission spikes", "Windbox imbalance across burners", "Damper coordination driven by habit", "Slow load-following from manual fan adjustment"]),
  ("NOx Prediction & SCR/SNCR Reagent Optimization", "Advisory", "SCR/SNCR equipped", 2, [
    "Models NOx formation upstream of the stack analyzer from burner conditions, FEGT, excess O<sub>2</sub>, combustion staging and coal nitrogen.",
    "Predicts NOx before the analyzer registers it, enabling anticipatory rather than reactive dosing.",
    "Advises injection rate and stoichiometric ratio to hold compliance at lower reagent use, limiting ammonia slip and extending catalyst life."],
   ["NOx limits tightening", "Reagent dosed conservatively", "Ammonia slip degrades expensive SCR catalyst", "Manual reagent control is reactive"]),
  ("Bed Material Inventory & Cyclone Performance", "Analytics", "CFBC only", 1.5, [
    "Analyses bed pressure profile, cyclone DP, loop-seal pressure drop, bed makeup rate and refractory hotspot signatures.",
    "Detects attrition exceeding makeup, cyclone efficiency loss from refractory wear, and loop-seal blockages disrupting solids return.",
    "Advises bed makeup, schedules cyclone refractory inspection and warns early of recirculation issues that would otherwise force an outage."],
   ["Attrition silent until performance degrades", "Cyclone refractory wear hidden inside the vessel", "Loop-seal blockages cause sudden inventory loss", "Bed makeup cost often unaccounted"]),
 ]),
 ("03", "Auxiliary Power Reduction", "Run the right auxiliaries, at the right load, at the right time", [
  ("Aux Pumps + Fans Efficiency Retrace & Load Scheduling", "Analytics", "All boilers", 6, [
    "Re-traces live efficiency curves for BFPs, ID/FD/PA fans and CW pumps from operating data and compares each against its design curve.",
    "Detects which units run near design and which have degraded, quantifying the power penalty of running the laggards.",
    "Advises scheduling to load efficient units first, shift work away from degraded ones and prioritise their maintenance."],
   ["Rotating aux efficiency degrades silently", "Pumps and fans selected by convention, not efficiency", "BFP — the largest APC consumer — has an untracked efficiency gap", "APC creeps up year on year inside aggregate reporting"]),
  ("Intelligent Cooling-Tower Fan Scheduling", "Closed-loop APC", "All boilers", 2, [
    "Analyses CW supply temperature, ambient wet bulb, load, condenser heat rejection requirement and per-cell fan status and power.",
    "Detects when fewer cells, or lower VFD speed across more cells, still holds target CW supply temperature.",
    "Provides cell ON/OFF sequencing that equalises wear, per-cell VFD setpoints and anticipatory adjustment for ambient and load."],
   ["All cells run regardless of need", "Ambient ignored in fan scheduling", "Vacuum–power trade-off not optimized", "Meaningful power waste in mild weather"]),
  ("Mill Parameter Optimization", "Advisory", "PF + SC + USC", 2, [
    "Analyses live coal particle size from computer vision, moisture, grindability inferred from mill power patterns and per-mill LOI feedback.",
    "Predicts mill power for the current coal source and flags when classifier speed, mill DP, outlet temperature and PA ratio should adapt.",
    "Coal-adaptive tuning — the same mill run differently per source and blend, valuable where multiple suppliers and washery rejects mix."],
   ["Mill settings fixed regardless of coal quality", "Grindability and moisture variability not adapted to", "Operator-dependent classifier settings", "Sub-optimal cross-mill bias"]),
  ("Optimal ESP TR-Set Setpoint Control", "Closed-loop APC", "All boilers", 2, [
    "Analyses stack SPM, per-field TR-set power, field current and voltage, rapping schedule and effectiveness, load and dust loading.",
    "Predicts the collection efficiency needed at current dust loading, and which fields can be trimmed versus held fully energised.",
    "Closed-loop field-by-field energisation and coordinated rapping, cutting ESP electrical load while holding SPM compliance."],
   ["ESP fields run at full power regardless of dust load", "TR-set power is a significant aux load", "Over-generous compliance margins", "Manual field tuning rarely done per shift"]),
 ]),
 ("04", "Asset Reliability", "Catch degradation weeks before it becomes a trip", [
  ("Vibration-Based Condition Monitoring", "Analytics", "All boilers", 5, [
    "Covers every critical rotating asset outside the DCS-monitored turbine train: mills, BFPs, ID/FD/PA fans, CW and CE pumps, feeder and conveyor drives, crushers, stacker-reclaimer, APH and soot-blower drives, ash and limestone handling, FGD blower, compressors, lube oil and hydraulic pumps.",
    "Analyses vibration signatures (FFT spectrum, time waveform, vector), bearing temperatures, motor current signature and lube oil quality via wired or wireless sensors.",
    "Detects bearing degradation, misalignment, unbalance, looseness, gearbox wear, lubrication issues and rotor damage <b>2–8 weeks ahead of failure</b> — with equipment-tagged alerts, remaining-useful-life estimates and recommended actions."],
   ["Critical equipment fails without warning", "Maintenance reactive on non-Tier-1 equipment", "A lost mill, BFP or fan means load reduction or a trip", "Aging assets drive insurance and reliability cost"]),
  ("Intelligent Soot Blowing Scheduler", "Closed-loop APC", "All boilers", 5, [
    "Analyses live Heat-Exchange Index per section, section-specific fouling rate, blower wear history and steam pressure dynamics during blowing.",
    "Separates sections that genuinely need blowing from time-based blows with negligible heat-exchange impact.",
    "Pushes closed-loop blow commands to the DCS section by section with post-blow HEI verification — cutting blowing steam and tube erosion, and restoring the SH/RH/economizer absorption profile to reduce downstream attemperation."],
   ["Time-based blowing wastes steam", "Sections cleaned uniformly regardless of fouling", "Blowing steam is a meaningful loss", "Over-blowing erodes tubes"]),
  ("Heat Exchange Index & Section-Level Fouling (incl. APH)", "Analytics", "All boilers", 3, [
    "Analyses both-side inlet/outlet temperatures and flows for every major section — APH, economizer, primary and final superheater, reheater banks, water walls; for APH also O<sub>2</sub> in/out, hot air, cold gas to ESP and DPs.",
    "Detects section-specific fouling, scaling, tube plugging and flow short-circuits, and triangulates APH seal leakage across radial, axial, hot- and cold-end seals.",
    "Gives section-level fouling visibility and seal-specific APH advisory, driving the soot-blowing use case and catching drift that periodic efficiency tests find too late."],
   ["Fouling degrades efficiency silently", "APH seal wear progressive and unseen", "Cleaning on calendar, not condition", "Cold-end corrosion hidden until damage"]),
  ("HP & LP Heater Performance Monitoring", "Analytics", "All boilers", 3, [
    "Analyses TTD, DCA, feedwater outlet temperature, drain flows, extraction pressures and bypass valve positions across HP heaters, deaerator and LP heaters.",
    "Detects per-heater degradation from fouling, tube damage, drain malfunction, air ingress and bypass leakage.",
    "Heater-by-heater advisory with feedwater terminal temperature recovery, restoring efficiency on a cycle that drifts silently."],
   ["Heater degradation is silent", "Bypass valves open unnoticed", "Sub-optimal drain handling", "TTD/DCA rarely tracked"]),
  ("ESP Health Monitoring", "Analytics", "All boilers", 2, [
    "Analyses per-field TR-set current and voltage patterns, insulator leakage current, rapping effectiveness, hopper levels and SPM excursion correlation.",
    "Detects insulator failures before TR-set tripping, plate ash build-up, rapping failures, hopper bridging and TR-set component degradation.",
    "Replaces time-based ESP overhauls with condition-based scheduling and location-tagged alerts before issues become compliance violations."],
   ["ESP failures cause SPM spikes", "Field-level issues hidden until breakdown", "Insulator failures common but unpredictable", "Time-based maintenance"]),
  ("Generator Winding + Air Cooler Health", "Analytics", "All boilers", 2, [
    "Analyses stator and rotor winding temperatures, cooler inlet/outlet temperatures, cooling water flow, partial discharge sensors where fitted and leakage flux.",
    "Detects winding hot spots from restricted cooling, seasonal cooler effectiveness loss, and partial discharge as an insulation-degradation precursor.",
    "Provides a generator health view, insulation aging-rate tracking and cooler maintenance advisory."],
   ["Generator failures rare but catastrophic", "Winding deterioration silent", "Cooler effectiveness untracked across seasons", "PD measured only on instrumented units"]),
  ("Corrosion & Scaling Surveillance", "Analytics", "All boilers", 2, [
    "Analyses feedwater pH, conductivity and dissolved oxygen, drum water chemistry, dosing residuals, blowdown and the historic tube-failure record.",
    "Detects chemistry excursions in real time and predicts tube corrosion, scaling and turbine deposit risk from exposure history.",
    "Chemistry-to-tube-life and dosing advisory — the long-term integrity management that spot checks miss."],
   ["Chemistry excursions cause tube damage years later", "Chemistry–failure linkage is tribal knowledge", "Monitoring not continuous", "Corrections only after failure"]),
  ("Condensate Contamination & Condenser Tube Leak Detection", "Analytics", "All boilers", 2, [
    "Analyses condensate conductivity, sodium and silica trends, hardness and boiler makeup water consumption.",
    "Detects condenser tube leaks from the condensate chemistry signature — typically the fastest reliable method.",
    "Early warning, localisation to the leaking water box and tube-isolation advisory, before CW chemistry silently damages boiler tubes."],
   ["Tube leaks contaminate condensate", "Resulting boiler tube damage is slow and costly to unwind", "Manual rounds inadequate for early detection", "Water-box localisation is manual"]),
 ]),
]

TYPE_CLS = {"Analytics": "t-an", "Advisory": "t-cl", "Closed-loop APC": "t-cl"}
TYPE_LBL = {"Analytics": "Process Data Analytics", "Advisory": "Automated Process Control", "Closed-loop APC": "Automated Process Control"}

def fmt_cr(v):
    return (f"{v:g}")

def uc_card(i, uc):
    name, typ, app, val, bullets, probs = uc
    lis = "".join(f"<li><span class='k'>{k}</span><span>{b}</span></li>" for k, b in zip(["Sees", "Finds", "Acts"], bullets))
    pr = "".join(f"<span class='chip'>{p}</span>" for p in probs)
    return f"""
<div class="uc">
  <div class="uc-head">
    <div class="uc-num">{i:02d}</div>
    <div class="uc-title">
      <h4>{name}</h4>
      <div class="tags"><span class="tag {TYPE_CLS[typ]}">{TYPE_LBL[typ]}</span><span class="tag t-app">{app}</span></div>
    </div>
    <div class="uc-val"><div class="v">₹{fmt_cr(val)} cr</div><div class="u">up to, per 100 MW</div></div>
  </div>
  <ul class="uc-body">{lis}</ul>
  <div class="uc-probs"><span class="pl">Problems today</span>{pr}</div>
</div>"""

# ---------- index table ----------
idx_rows = ""
n = 0
for sn, st, sd, ucs in SECTIONS:
    idx_rows += f"<tr class='grp'><td colspan='4'>{sn} · {st}</td></tr>"
    for uc in ucs:
        n += 1
        w = uc[3] / 6 * 100
        idx_rows += (f"<tr><td class='n'>{n:02d}</td><td class='nm'>{uc[0]}</td>"
                     f"<td><span class='tag {TYPE_CLS[uc[1]]}'>{TYPE_LBL[uc[1]]}</span></td>"
                     f"<td class='bar'><div class='b'><i style='width:{w:.0f}%'></i></div><span>₹{fmt_cr(uc[3])} cr</span></td></tr>")

# ---------- sections ----------
sec_html = ""
n = 0
for sn, st, sd, ucs in SECTIONS:
    cards = ""
    for uc in ucs:
        n += 1
        cards += uc_card(n, uc)
    sec_html += f"""
<section class="ucsec">
  <div class="sec-label"><span class="sn">{sn}</span><div><h3>{st}</h3><p>{sd} · {len(ucs)} use cases</p></div></div>
  {cards}
</section>"""

CASES = [
 ("SPB", "21 MW cogeneration · 16 MW recovery boiler", [
   ("Automated RCA Agents", "AI agents on DCS and lab data that flag deviations across boiler, turbine, generator and auxiliaries and return root cause plus recommendation, built with a domain SME.", [("100+", "RCAs generated daily"), ("98.4%", "validated recommendation accuracy")]),
   ("Closed-loop Soot Blower Automation", "AI-driven blowing across 29 soot blowers on a 16 MW recovery boiler — fewer wash cycles, less tube erosion, better flue-gas heat recovery.", [("20 TPD", "aux steam saved"), ("₹1 cr", "annual savings")]),
   ("APC for Coal Feeding", "Automated process control across 7 coal feeders of the AFBC boiler to cut process variability and hold bed stability.", [("7", "feeders under APC"), ("In progress", "")]),
 ]),
 ("JSW Energy", "Five plants · Predictive maintenance", [
   ("Vibration-based Predictive Maintenance", "1,000+ vibration sensors deployed across five plants, cutting unplanned downtime, revenue loss and maintenance cost.", [("15+", "critical failures caught early"), ("₹1.3 cr", "savings over 2 yrs, finance-validated")]),
 ]),
 ("Hindustan Zinc", "Zawar · 91 MW captive plant", [
   ("APC & NHR Reduction", "Integrated with historian (DCS), EMS and lab data. Efficiency curves of all auxiliaries re-traced; run cycles scheduled to load, coal and season. NHR models handle IEX-driven load swings and steer operation toward HMBD reference ranges.", [("1 pp", "APC reduction target"), ("In progress", "")]),
 ]),
 ("Grasim", "175 MW captive · 5 boilers · 5 turbines", [
   ("APC, Reliability & NHR Reduction", "AI use cases to reduce net heat rate across a multi-unit captive plant.", [("5 + 5", "boilers + turbines"), ("In progress", "")]),
 ]),
 ("Tata Power", "Large thermal plant · Prayagraj", [
   ("Energy Management", "Integrated with energy meters to monitor and dynamically benchmark APC equipment — boiler feed pumps, ID and FD fans.", [("Live", "APC benchmarking")]),
 ]),
]

def case_html():
    out = ""
    for client, ctx, projs in CASES:
        ps = ""
        for t, d, stats in projs:
            st = "".join(
                (f"<div class='st'><b>{a}</b><span>{b}</span></div>" if b else f"<div class='st prog'><span>{a}</span></div>")
                for a, b in stats)
            ps += f"<div class='proj'><div class='pt'>{t}</div><p>{d}</p><div class='sts'>{st}</div></div>"
        out += f"<div class='case'><div class='cl'><div class='cn'>{client}</div><div class='cc'>{ctx}</div></div><div class='cr'>{ps}</div></div>"
    return out

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--ink:#0F1B2D;--ink2:#3A4A5F;--mute:#6B7A90;--line:#E3E8EF;--bg:#F6F8FB;--navy:#0B1A30;--blue:#3D63F5;--blue2:#6F8BFF;--amber:#F2A541;--green:#14946B;--violet:#7A4FE0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#fff}}
body{{font-family:Inter,sans-serif;color:var(--ink);width:820px;font-size:11.5px;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-feature-settings:"ss01","cv11"}}
.wrap{{padding:0 52px}}
h1,h2,h3,h4{{font-family:"Inter Display",Inter,sans-serif;letter-spacing:-.01em}}
sub{{font-size:.7em}}
.eyebrow{{font-size:9.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}}
section{{padding:44px 0}}
.rule{{height:1px;background:var(--line)}}
/* HERO */
.hero{{background:var(--navy);color:#fff;padding:40px 52px 44px;position:relative;overflow:hidden}}
.hero:after{{content:"";position:absolute;right:-120px;top:-120px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(111,139,255,.35),rgba(111,139,255,0) 70%)}}
.brand{{display:flex;justify-content:space-between;align-items:center;font-size:10px;letter-spacing:.16em;color:#9FB0CC;text-transform:uppercase;position:relative;z-index:1}}
.brand b{{color:#fff;font-weight:700;letter-spacing:.2em}}
.hero h1{{font-size:44px;line-height:1.05;font-weight:700;margin:56px 0 14px;max-width:600px;position:relative;z-index:1}}
.hero h1 em{{font-style:normal;color:var(--blue2)}}
.hero .lede{{font-size:14px;color:#C5D0E3;max-width:540px;line-height:1.55;position:relative;z-index:1}}
.hero-kpis{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,.12);margin-top:40px;border-radius:10px;overflow:hidden;position:relative;z-index:1}}
.hk{{background:#12243F;padding:16px 18px}}
.hk b{{display:block;font-family:"Inter Display";font-size:26px;font-weight:700;color:#fff}}
.hk span{{font-size:10.5px;color:#9FB0CC}}
.hk.acc b{{color:var(--amber)}}
/* glance */
.glance{{display:grid;grid-template-columns:repeat(5,1fr);border:1px solid var(--line);border-radius:10px;margin-top:18px}}
.glance div{{padding:14px 16px;border-right:1px solid var(--line)}}
.glance div:last-child{{border:0}}
.glance b{{font-family:"Inter Display";font-size:22px;font-weight:700;display:block}}
.glance span{{font-size:10px;color:var(--mute)}}
h2{{font-size:24px;font-weight:700;margin:6px 0 8px}}
.sub{{color:var(--ink2);font-size:12.5px;max-width:620px}}
/* team */
.team{{display:grid;grid-template-columns:1.15fr 1fr;gap:22px;margin-top:22px}}
.leaders{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.ld{{border:1px solid var(--line);border-radius:8px;padding:10px 12px}}
.ld b{{font-size:12px;display:block}}
.ld .r{{color:var(--blue);font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.06em}}
.ld .e{{color:var(--mute);font-size:10px;margin-top:2px}}
.sme{{background:var(--bg);border-radius:10px;padding:18px 20px;border-left:3px solid var(--amber)}}
.sme .tagl{{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:#B5701A;font-weight:700}}
.sme h4{{font-size:17px;margin:6px 0 2px}}
.sme .yrs{{font-size:12px;color:var(--ink2);margin-bottom:10px}}
.sme ul{{list-style:none}}
.sme li{{padding:5px 0;border-top:1px solid var(--line);font-size:11px;color:var(--ink2)}}
/* value drivers */
.drivers{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:22px}}
.drv{{border-radius:10px;padding:20px;border:1px solid var(--line)}}
.drv .big{{font-family:"Inter Display";font-size:30px;font-weight:700;color:var(--blue)}}
.drv.r .big{{color:var(--green)}}
.drv h4{{font-size:13px;margin:2px 0 6px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);font-weight:600}}
.drv p{{color:var(--ink2)}}
/* architecture */
.arch{{display:grid;grid-template-columns:1fr 30px 1fr 30px 1fr;align-items:stretch;margin-top:24px}}
.col{{border:1px solid var(--line);border-radius:10px;padding:14px;background:#fff}}
.col h5{{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-bottom:10px;font-weight:700}}
.col .it{{background:var(--bg);border-radius:6px;padding:8px 10px;margin-bottom:6px;font-size:11px;font-weight:500}}
.col .it small{{display:block;color:var(--mute);font-weight:400;font-size:9.5px}}
.col.mid{{background:var(--navy);border-color:var(--navy);color:#fff}}
.col.mid h5{{color:#9FB0CC}}
.col.mid .it{{background:#16294A;color:#fff}}
.col.mid .plat{{margin-top:10px;border:1px dashed #4C66A8;border-radius:6px;padding:8px;text-align:center;font-size:10.5px;color:#C5D0E3}}
.col.mid .plat b{{color:#fff;display:block;font-size:12px}}
.col.out .it{{border-left:3px solid var(--blue)}}
.arr{{display:flex;align-items:center;justify-content:center;color:var(--blue2);font-size:18px}}
.note{{font-size:10px;color:var(--mute);margin-top:10px;font-style:italic}}
/* engagement */
.steps{{display:grid;grid-template-columns:repeat(5,1fr);gap:0;margin-top:26px;position:relative}}
.steps:before{{content:"";position:absolute;left:18px;right:18px;top:17px;height:2px;background:linear-gradient(90deg,var(--blue),var(--green))}}
.step{{padding-right:12px;position:relative}}
.dot{{width:36px;height:36px;border-radius:50%;background:#fff;border:2px solid var(--blue);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:var(--blue);position:relative;z-index:1}}
.step:last-child .dot{{border-color:var(--green);color:var(--green)}}
.step h5{{font-size:12.5px;margin:12px 0 2px}}
.step .dur{{font-size:9.5px;font-weight:700;color:var(--blue);letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}}
.step p{{font-size:10.5px;color:var(--ink2);line-height:1.45}}
.callout{{margin-top:22px;background:var(--bg);border-radius:8px;padding:12px 16px;font-size:11.5px;color:var(--ink2)}}
.callout b{{color:var(--ink)}}
/* cases */
.case{{display:grid;grid-template-columns:170px 1fr;gap:20px;padding:18px 0;border-top:1px solid var(--line)}}
.case:first-of-type{{border-top:2px solid var(--ink)}}
.cn{{font-family:"Inter Display";font-size:18px;font-weight:700}}
.cc{{font-size:10.5px;color:var(--mute);margin-top:2px}}
.proj+.proj{{margin-top:14px;padding-top:14px;border-top:1px dashed var(--line)}}
.pt{{font-weight:700;font-size:12.5px;margin-bottom:3px}}
.proj p{{color:var(--ink2);font-size:11px}}
.sts{{display:flex;gap:10px;margin-top:8px}}
.st{{background:#EEF2FF;border-radius:6px;padding:6px 10px;display:flex;align-items:baseline;gap:6px}}
.st b{{font-family:"Inter Display";font-size:15px;color:var(--blue)}}
.st span{{font-size:10px;color:var(--ink2)}}
.st.prog{{background:#FFF5E6}}
.st.prog span{{color:#B5701A;font-weight:600;font-size:9.5px;text-transform:uppercase;letter-spacing:.08em}}
/* index */
table.idx{{width:100%;border-collapse:collapse;margin-top:20px}}
.idx td{{padding:6px 8px;border-bottom:1px solid var(--line);font-size:11px;vertical-align:middle}}
.idx tr.grp td{{background:var(--bg);font-weight:700;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink2);padding:7px 8px}}
.idx .n{{color:var(--mute);width:28px;font-variant-numeric:tabular-nums}}
.idx .nm{{font-weight:500}}
.idx .bar{{width:180px}}
.idx .bar .b{{display:inline-block;width:110px;height:6px;background:#EDF1F6;border-radius:3px;vertical-align:middle;margin-right:8px;overflow:hidden}}
.idx .bar i{{display:block;height:100%;background:var(--blue);border-radius:3px}}
.idx .bar span{{font-weight:600;font-variant-numeric:tabular-nums}}
.tag{{display:inline-block;font-size:9px;font-weight:600;padding:2px 7px;border-radius:20px;letter-spacing:.02em;white-space:nowrap}}
.t-an{{background:#EEF2FF;color:#3D52C9}}
.t-ad{{background:#FFF3E3;color:#A8620F}}
.t-cl{{background:#E4F6EF;color:#0E7553}}
.t-app{{background:#fff;border:1px solid var(--line);color:var(--ink2)}}
.legend{{display:flex;gap:16px;margin-top:12px;font-size:10.5px;color:var(--ink2);flex-wrap:wrap}}
.legend span.tag{{margin-right:5px}}
/* use case cards */
.ucsec{{padding:30px 0 6px}}
.sec-label{{display:flex;gap:14px;align-items:center;margin-bottom:14px;padding-bottom:12px;border-bottom:2px solid var(--ink)}}
.sec-label .sn{{font-family:"Inter Display";font-size:30px;font-weight:700;color:var(--blue)}}
.sec-label h3{{font-size:19px;font-weight:700}}
.sec-label p{{font-size:11px;color:var(--mute)}}
.uc{{border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:12px;break-inside:avoid}}
.uc-head{{display:flex;gap:12px;align-items:flex-start}}
.uc-num{{font-size:10px;font-weight:700;color:var(--mute);background:var(--bg);border-radius:5px;padding:4px 6px;margin-top:2px;font-variant-numeric:tabular-nums}}
.uc-title{{flex:1}}
.uc-title h4{{font-size:14px;font-weight:700;margin-bottom:5px;line-height:1.25}}
.tags{{display:flex;gap:5px}}
.uc-val{{text-align:right;min-width:120px}}
.uc-val .v{{font-family:"Inter Display";font-size:19px;font-weight:700;color:var(--green);line-height:1.1}}
.uc-val .u{{font-size:9px;color:var(--mute)}}
.uc-body{{list-style:none;margin:12px 0 0}}
.uc-body li{{display:grid;grid-template-columns:48px 1fr;gap:8px;padding:5px 0;color:var(--ink2);font-size:11px}}
.uc-body .k{{font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);padding-top:2px}}
.uc-probs{{margin-top:10px;padding-top:10px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:5px;align-items:center}}
.uc-probs .pl{{font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#B5452F;margin-right:4px}}
.chip{{font-size:10px;background:#FBF1EE;color:#7A3A2C;padding:2px 8px;border-radius:12px}}
/* cta */
.cta{{background:var(--navy);color:#fff;padding:40px 52px;margin-top:30px;display:flex;justify-content:space-between;align-items:center;gap:30px}}
.cta h2{{color:#fff;font-size:26px}}
.cta p{{color:#C5D0E3;font-size:12.5px;max-width:430px}}
.cta .btn{{background:var(--blue2);color:#fff;font-weight:700;padding:12px 22px;border-radius:30px;font-size:13px;white-space:nowrap}}
.foot{{background:var(--navy);color:#6F80A0;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;padding:0 52px 26px;display:flex;justify-content:space-between}}
</style></head><body>

<div class="hero">
  <div class="brand"><b>Faclon Labs</b><span>Power Plant Practice · Industrial AI</span></div>
  <h1>Industrial AI for boiler, turbine <em>&amp; auxiliaries</em></h1>
  <p class="lede">From DCS data to closed-loop control: lower net heat rate, lower auxiliary power and fewer forced outages — proven on captive and utility plants across India.</p>
  <div class="hero-kpis">
    <div class="hk acc"><b>3–5%</b><span>Net heat rate reduction</span></div>
    <div class="hk"><b>24</b><span>Power plant AI use cases</span></div>
    <div class="hk"><b>98.4%</b><span>Validated RCA recommendation accuracy</span></div>
  </div>
</div>

<div class="wrap">
<section>
  <div class="eyebrow">Faclon Labs at a glance</div>
  <h2>Leaders in industrial data integration, visualization and AI-based optimization</h2>
  <div class="glance">
    <div><b>5B+</b><span>data points daily</span></div>
    <div><b>200+</b><span>deployments</span></div>
    <div><b>60k+</b><span>assets connected</span></div>
    <div><b>50+</b><span>customers</span></div>
    <div><b>120+</b><span>employees</span></div>
  </div>
  <div class="team">
    <div>
      <div class="eyebrow" style="margin-bottom:10px">Leadership</div>
      <div class="leaders">
        <div class="ld"><b>Rishi Sharma</b><div class="r">CEO</div><div class="e">B.Tech, IIT Bombay</div></div>
        <div class="ld"><b>Parth Chaudhary</b><div class="r">President</div><div class="e">B.Tech, IIT Bombay</div></div>
        <div class="ld"><b>Utkarsh Srivastava</b><div class="r">CTO</div><div class="e">Ex-white-hat hacker</div></div>
        <div class="ld"><b>Vivek Singh</b><div class="r">Chief Data Scientist</div><div class="e">B.Tech, IIT Kanpur</div></div>
        <div class="ld"><b>Archit Naraniwal</b><div class="r">Chief Sales Officer</div><div class="e">B.Tech, IIT Bombay</div></div>
        <div class="ld"><b>Mukesh Kumar</b><div class="r">India Operations</div><div class="e">B.Tech, IIT Bombay</div></div>
      </div>
    </div>
    <div class="sme">
      <div class="tagl">Power plant SME</div>
      <h4>Dr. T.G. Sundara Raman</h4>
      <div class="yrs">50+ years in power plant operations, energy efficiency and thermal engineering</div>
      <ul>
        <li>Sector Expert, Bureau of Energy Efficiency (Ministry of Power)</li>
        <li>Consultant &amp; Adviser — Energy Efficiency &amp; Decarbonization</li>
        <li>B.Tech, M.Tech, Ph.D. (patent in heat transfer) and postdoctoral work, IIT Madras</li>
      </ul>
    </div>
  </div>
</section>
<div class="rule"></div>

<section>
  <div class="eyebrow">Strategic value drivers</div>
  <h2>Measurable impact on efficiency and reliability</h2>
  <div class="drivers">
    <div class="drv"><div class="big">3–5% NHR ↓</div><h4>Efficiency</h4><p>Continuous AI-driven optimization of boiler–turbine cycle efficiency, directly lowering the cost of steam and power and cutting emissions.</p></div>
    <div class="drv r"><div class="big">Higher availability</div><h4>Asset reliability</h4><p>Early anomaly detection and predictive diagnostics minimize unplanned downtime, extend equipment life and cut major overhaul costs.</p></div>
  </div>
</section>
<div class="rule"></div>

<section>
  <div class="eyebrow">Solution architecture</div>
  <h2>Power plant digital twin</h2>
  <p class="sub">One platform, on-premise or cloud, from plant data sources to operator-facing outcomes.</p>
  <div class="arch">
    <div class="col"><h5>Data sources</h5>
      <div class="it">DCS / SCADA<small>via OPC server, historian or data lake</small></div>
      <div class="it">Lab data<small>coal, water</small></div>
      <div class="it">Energy meters</div>
      <div class="it">Design data<small>manuals, HMBD</small></div>
    </div>
    <div class="arr">→</div>
    <div class="col mid"><h5>Data integration</h5>
      <div class="it">Historian</div>
      <div class="it">IT–OT integration / API</div>
      <div class="it">Forms / ERP / LIMS</div>
      <div class="it">File upload</div>
      <div class="plat"><b>Faclon AI Platform</b>On-premise / cloud</div>
    </div>
    <div class="arr">→</div>
    <div class="col out"><h5>Outcomes</h5>
      <div class="it">KPI benchmarking</div>
      <div class="it">RCA &amp; recommendations</div>
      <div class="it">Optimal control strategy</div>
      <div class="it">APC reduction</div>
      <div class="it">Operator chatbot</div>
    </div>
  </div>
  <p class="note">Integration architecture for DCS, lab and energy-meter data is finalized during technical discussions with the plant team.</p>
</section>
<div class="rule"></div>

<section>
  <div class="eyebrow">Engagement approach</div>
  <h2>From data exploration to plant-wide scale-up</h2>
  <p class="sub">Every engagement starts with the plant’s own data and the people who run it.</p>
  <div class="steps">
    <div class="step"><div class="dot">1</div><h5>Data Exploration</h5><div class="dur">1–2 weeks</div><p>Sample DCS, lab and design data reviewed offline. Tag coverage, data quality and loss profile screened against the use-case catalogue.</p></div>
    <div class="step"><div class="dot">2</div><h5>Plant Visit</h5><div class="dur">2–3 days on site</div><p>Walkdown of boiler, turbine and auxiliaries with our SME. Sessions with operations, maintenance, efficiency and C&amp;I teams.</p></div>
    <div class="step"><div class="dot">3</div><h5>Use Case Identification</h5><div class="dur">1–2 weeks</div><p>Shortlist agreed on data availability, boiler type and value at stake. Baseline, KPIs and success criteria fixed in writing.</p></div>
    <div class="step"><div class="dot">4</div><h5>Pilot</h5><div class="dur">8–12 weeks</div><p>One or two use cases end to end: integration, model build, advisory in operators’ hands, benefit measured against baseline.</p></div>
    <div class="step"><div class="dot">5</div><h5>Scale-Up</h5><div class="dur">Phased rollout</div><p>Remaining use cases and units on one platform. Advisory moves to closed loop where the pilot proves out.</p></div>
  </div>
  <div class="callout"><b>Nothing is committed to the DCS</b> before it is validated offline and accepted by operations.</div>
</section>
<div class="rule"></div>

<section>
  <div class="eyebrow">Proof</div>
  <h2>Customer cases</h2>
  <p class="sub" style="margin-bottom:18px">From 21 MW cogeneration to five-plant utility fleets.</p>
  {case_html()}
</section>
<div class="rule"></div>

<section>
  <div class="eyebrow">Use case catalogue</div>
  <h2>24 power plant AI use cases at a glance</h2>
  <p class="sub">Savings are indicative (“up to”, per 100 MW) and are re-baselined against your plant’s own data during use-case identification.</p>
  <div class="legend"><div><span class="tag t-an">Process Data Analytics</span>Monitoring, diagnostics and advisory</div><div><span class="tag t-cl">Automated Process Control</span>Setpoint optimization, advisory or closed loop</div></div>
  <table class="idx">{idx_rows}</table>
</section>

{sec_html}
</div>

<div class="cta">
  <div><div class="eyebrow" style="color:var(--blue2)">Next step</div><h2>Start with a plant visit</h2><p>Share a sample of DCS, lab and design data and we will come back with a shortlist of use cases sized against your plant’s own loss profile.</p></div>
  <div class="btn">www.faclonlabs.com</div>
</div>
<div class="foot"><span>Faclon Labs · Power Plant Practice</span><span>Industrial AI for boiler, turbine and auxiliaries</span></div>
</body></html>"""

TMP.write_text(HTML, encoding="utf-8")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 820, "height": 1000})
    pg.goto(TMP.as_uri())
    pg.wait_for_timeout(300)
    h = pg.evaluate("document.documentElement.scrollHeight")
    pg.pdf(path=str(OUT), width="820px", height=f"{h+2}px", print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    b.close()
TMP.unlink()
print("wrote", OUT.relative_to(ROOT), "height", h)
