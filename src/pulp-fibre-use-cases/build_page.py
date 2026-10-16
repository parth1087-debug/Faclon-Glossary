"""Builds pulp-fibre-use-cases/index.html (Pulp & Fibre Use Cases).

Run from anywhere:  python3 src/pulp-fibre-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: Faclon Use Case Sheet, "Pulp and Fibre" sheet. Edit the JSON and re-run; the page is regenerated in full.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Pulp & Fibre Use Cases",
    "sector": "Industrial AI · Dissolving pulp and VSF",
    "eyebrow": "Industry brief · Dissolving pulp and viscose staple fibre",
    "h1": "An AI use-case catalogue for <em>dissolving pulp and viscose fibre</em>",
    "lede": "Forty-seven deployable AI use cases mapped from wood yard to finished viscose staple fibre: dissolving pulp, steeping and xanthation, viscose preparation, spinning, washing and drying, chemical recovery, utilities and cross-cutting reliability. Each one turns plant data into continuous intelligence and action, with the value at stake quantified per million tonnes of annual capacity.",
    "primary": "MTPA fibre",
    "basis_note": "per MTPA (million tonnes per annum) of fibre; wood yard, pulp and pulp drying use cases are quoted per MTPA of pulp",
    "area": "process area",
    "search": "Search use cases, KPIs, equipment, e.g. viscose, spinneret, CS2, DP",
    "flow_word": "Process flow order",
    "description": "47 AI use cases across dissolving pulp and viscose staple fibre production, from wood yard to spinning, chemical recovery and utilities, with indicative value per MTPA.",
    "examples": [
        [
            "One data fabric from pulp to fibre",
            "I/O Connect brings DCS, PLC, lab, spin-bath and camera data into one namespace across the pulp mill and fibre plant."
        ],
        [
            "Models tuned to the process",
            "Deepsense builds soft sensors for DP, alpha cellulose, viscose ripeness, filterability and spin-bath chemistry between lab samples."
        ],
        [
            "Advisories into the control room",
            "Bruce AI turns predictions into line-level alerts and setpoint advisories, with the value tracked per tonne of fibre."
        ]
    ],
    "cta": "Pick one process area and one KPI from this catalogue. Faclon connects the existing instrumentation, stands up a live dashboard and returns a quantified value unlock with a plant-wide scale-out plan, typically within a 4–6 week assessment."
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "pulp-fibre-use-cases" / "index.html")
