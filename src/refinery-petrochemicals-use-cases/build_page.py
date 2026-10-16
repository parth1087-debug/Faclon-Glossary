"""Builds refinery-petrochemicals-use-cases/index.html (Refinery & Petrochemicals Use Cases).

Run from anywhere:  python3 src/refinery-petrochemicals-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: Faclon Use Case Sheet, "Refinery" sheet. Edit the JSON and re-run; the page is regenerated in full.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Refinery & Petrochemicals Use Cases",
    "sector": "Industrial AI · Refining and petrochemicals",
    "eyebrow": "Industry brief · Refinery and petrochemical complex",
    "h1": "An AI use-case catalogue for the <em>refinery and petrochemical complex</em>",
    "lede": "Fifty-six deployable AI use cases mapped from crude receipt to finished fuels and polymers: distillation, hydrotreating, reforming, FCC, hydrocracking, coking, hydrogen and sulphur recovery, the steam cracker, polymer units, blending, utilities and cross-cutting reliability. Each one turns plant data into continuous intelligence and action, with the value at stake quantified per million tonnes of annual crude throughput.",
    "primary": "MMTPA crude",
    "basis_note": "per MMTPA (million metric tonnes per annum) of crude; steam cracker and polymer use cases are quoted per MMTPA of ethylene and of polymer",
    "area": "process area",
    "search": "Search use cases, KPIs, equipment, e.g. FCC, catalyst, heater, GRM",
    "flow_word": "Process flow order",
    "description": "56 AI use cases across the refinery and petrochemical complex, from crude selection and distillation to FCC, hydrocracker, steam cracker and polymers, with indicative value per MMTPA.",
    "examples": [
        [
            "One data fabric across the complex",
            "I/O Connect brings DCS, APC, LIMS, historian and analyser data into one namespace across process units and off-sites."
        ],
        [
            "Models tuned to the process",
            "Deepsense builds soft sensors and unit models for yields, catalyst activity, fouling and product quality between lab samples."
        ],
        [
            "Advisories into the control room",
            "Bruce AI turns predictions into unit-level alerts and setpoint advisories, with the margin impact tracked per barrel."
        ]
    ],
    "cta": "Pick one process area and one KPI from this catalogue. Faclon connects the existing instrumentation, stands up a live dashboard and returns a quantified value unlock with a complex-wide scale-out plan, typically within a 4–6 week assessment."
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "refinery-petrochemicals-use-cases" / "index.html")
