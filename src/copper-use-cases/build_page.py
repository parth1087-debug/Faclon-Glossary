"""Builds copper-use-cases/index.html (Copper Use Cases).

Run from anywhere:  python3 src/copper-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: Faclon Use Case Sheet, "Copper" sheet. Edit the JSON and re-run; the page is regenerated in full.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Copper Use Cases",
    "sector": "Industrial AI · Copper",
    "eyebrow": "Industry brief · Copper smelting and refining",
    "h1": "An AI use-case catalogue for the <em>copper smelter and refinery</em>",
    "lede": "Forty-six deployable AI use cases mapped from concentrate receipt to cathode, precious metals and continuous cast rod: smelting, converting, anode casting, electrorefining, the acid plant, utilities and cross-cutting reliability. Each one turns plant data into continuous intelligence and action, with the value at stake quantified per million tonnes of annual copper capacity.",
    "primary": "MTPA copper",
    "basis_note": "per MTPA (million tonnes per annum) of copper; rod plant use cases are quoted per MTPA of copper rod",
    "area": "plant section",
    "search": "Search use cases, KPIs, equipment, e.g. matte, converter, cell house, acid",
    "description": "46 AI use cases across the copper smelter and refinery, from concentrate blending and smelting to electrorefining, acid plant and rod mill, with indicative value per MTPA.",
    "examples": [
        [
            "One data fabric across the smelter",
            "I/O Connect brings furnace, converter, acid plant, tankhouse, lab and camera data into one namespace, with no rip-and-replace."
        ],
        [
            "Models tuned to the process",
            "Deepsense builds soft sensors for matte grade, slag chemistry, cell condition and acid strength that fill the gaps between assays."
        ],
        [
            "Advisories into the control room",
            "Bruce AI turns predictions into equipment-level alerts and setpoint advisories, with the value tracked per tonne of copper."
        ]
    ],
    "cta": "Pick one plant section and one KPI from this catalogue. Faclon connects the existing instrumentation, stands up a live dashboard and returns a quantified value unlock with a plant-wide scale-out plan, typically within a 4–6 week assessment."
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "copper-use-cases" / "index.html")
