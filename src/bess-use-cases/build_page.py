"""Builds bess-use-cases/index.html (Battery Energy Storage Use Cases).

Run from anywhere:  python3 src/bess-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: Faclon Use Case Sheet, "bess" sheet. Edit the JSON and re-run; the page is regenerated in full.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Battery Energy Storage Use Cases",
    "sector": "Industrial AI · Battery energy storage",
    "eyebrow": "Industry brief · Battery energy storage systems",
    "h1": "An AI use-case catalogue for <em>battery energy storage</em>",
    "lede": "Seven deployable AI use cases across the BESS asset, from cell safety and state of health to dispatch revenue, thermal management and site safety. Each one turns BMS, PCS and EMS data into continuous intelligence and action, with the value at stake quantified per 100 MWh of capacity per year.",
    "primary": "100 MWh per year",
    "basis_note": "per 100 MWh of installed capacity per year",
    "area": "system area",
    "search": "Search use cases, KPIs, equipment, e.g. thermal runaway, SoH, dispatch, HVAC",
    "description": "7 AI use cases for battery energy storage systems, from cell anomaly early warning and state of health to revenue-optimal dispatch, with indicative value per 100 MWh per year.",
    "examples": [
        [
            "One data fabric across every rack",
            "I/O Connect brings cell-level BMS, PCS, EMS, HVAC and fire-system data into one namespace."
        ],
        [
            "Models tuned to the battery",
            "Deepsense estimates state of health and spots outlier cells independently of the BMS, ahead of alarm thresholds."
        ],
        [
            "Advisories for operations and trading",
            "Bruce AI turns predictions into isolation advisories, maintenance work and dispatch recommendations, with the value tracked."
        ]
    ],
    "cta": "Pick one site and one KPI from this catalogue. Faclon connects the existing BMS, PCS and EMS data, stands up a live dashboard and returns a quantified value unlock with a fleet-wide scale-out plan, typically within a 4–6 week assessment."
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "bess-use-cases" / "index.html")
