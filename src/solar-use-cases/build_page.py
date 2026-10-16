"""Builds solar-use-cases/index.html (Solar Use Cases).

Run from anywhere:  python3 src/solar-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: Faclon Use Case Sheet, "solar" sheet. Edit the JSON and re-run; the page is regenerated in full.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Solar Use Cases",
    "sector": "Industrial AI · Utility-scale solar",
    "eyebrow": "Industry brief · Utility-scale solar PV",
    "h1": "An AI use-case catalogue for the <em>utility-scale solar plant</em>",
    "lede": "Ten deployable AI use cases across the solar plant, from soiling, strings and module health to inverters, forecasting, the substation and site security. Each one turns SCADA and field data into continuous intelligence and action, with the value at stake quantified per 100 MW of capacity per year.",
    "primary": "100 MW per year",
    "basis_note": "per 100 MW of installed capacity per year",
    "area": "plant area",
    "search": "Search use cases, KPIs, equipment, e.g. soiling, string, inverter, tracker",
    "description": "10 AI use cases for utility-scale solar plants, from soiling and string monitoring to inverters, forecasting and site security, with indicative value per 100 MW per year.",
    "examples": [
        [
            "One data fabric across every site",
            "I/O Connect brings SCADA, inverter, string monitoring, weather station and drone data into one namespace."
        ],
        [
            "Models tuned to the plant",
            "Deepsense models expected generation block by block, so soiling, string faults and tracker errors show up as measurable losses."
        ],
        [
            "Advisories for the O&M team",
            "Bruce AI turns losses into prioritised work: which blocks to clean, which strings to fix, with the energy recovered tracked."
        ]
    ],
    "cta": "Pick one plant and one loss from this catalogue. Faclon connects the existing SCADA and field data, stands up a live dashboard and returns a quantified value unlock with a portfolio-wide scale-out plan, typically within a 4–6 week assessment."
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "solar-use-cases" / "index.html")
