"""Builds aluminium-use-cases/index.html (Aluminium Use Cases).

Run from anywhere:  python3 src/aluminium-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: Faclon Use Case Sheet, "Aluminium" sheet. Edit the JSON and re-run; the page is regenerated in full.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Aluminium Use Cases",
    "sector": "Industrial AI · Aluminium",
    "eyebrow": "Industry brief · Integrated aluminium",
    "h1": "An AI use-case catalogue for the <em>integrated aluminium plant</em>",
    "lede": "Sixty-two deployable AI use cases mapped from bauxite mine to finished coil and extrusion: alumina refining, anode making, potlines, casthouse, rolling and extrusion, utilities and cross-cutting reliability. Each one turns plant data into continuous intelligence and action, with the value at stake quantified per million tonnes of annual aluminium capacity.",
    "primary": "MTPA aluminium",
    "basis_note": "per MTPA (million tonnes per annum) of aluminium; downstream rolling, extrusion and finishing use cases are quoted per MTPA of their own product",
    "area": "plant section",
    "search": "Search use cases, KPIs, equipment, e.g. potline, silica, anode, coil",
    "description": "62 AI use cases across the integrated aluminium plant, from bauxite mining and Bayer refining to potlines, casthouse, rolling and extrusion, with indicative value per MTPA.",
    "examples": [
        [
            "One data fabric from mine to mill",
            "I/O Connect brings potline controllers, DCS, PLC, lab, LIMS and camera streams into one namespace, with no rip-and-replace."
        ],
        [
            "Models tuned to the process",
            "Deepsense builds soft sensors for bath chemistry, superheat, alumina quality and anode condition that fill the gaps between lab samples."
        ],
        [
            "Advisories into the control room",
            "Bruce AI turns predictions into pot-level and furnace-level alerts and setpoint advisories, with the value tracked per tonne."
        ]
    ],
    "cta": "Pick one plant section and one KPI from this catalogue. Faclon connects the existing instrumentation, stands up a live dashboard and returns a quantified value unlock with a plant-wide scale-out plan, typically within a 4–6 week assessment."
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "aluminium-use-cases" / "index.html")
