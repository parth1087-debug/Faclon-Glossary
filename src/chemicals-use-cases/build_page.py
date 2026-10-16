"""Builds chemicals-use-cases/index.html (Chemicals Use Cases).

Run from anywhere:  python3 src/chemicals-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: written for the site (Oct 2026); there is no approved value source yet, so use cases carry no
₹ values or priority tiers. When a sized sheet arrives, add "v", "basis", "calc" and "tier" to each use
case, set "primary" below, and the value chart, totals and tier filter appear automatically.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Chemicals Use Cases",
    "sector": "Industrial AI · Chemicals",
    "eyebrow": "Industry brief · Bulk, specialty and fine chemicals",
    "h1": 'An AI use-case catalogue for the <em>chemical plant</em>',
    "lede": "Twenty-eight deployable AI use cases across a batch or continuous chemical plant: raw material receipt, reactors, distillation, crystallisation and drying, packing, utilities, effluent and emissions, safety and cross-cutting reliability. Each one turns plant data into continuous intelligence and action for safer, higher-yield and lower-energy operation.",
    "primary": None,
    "basis_note": "",
    "area": "plant area",
    "search": "Search use cases, KPIs, equipment, e.g. batch, reactor, solvent, dryer",
    "description": "28 AI use cases for chemical plants, from golden batch and reactor yield to distillation energy, solvent recovery, utilities, effluent, safety and traceability.",
    "novalue_hero": "Value is sized for each site in a short assessment of its own batch, energy and quality data.",
    "novalue_note": "Value is sized for each plant: a 4–6 week assessment of your own data turns these use cases into a costed, prioritised plan.",
    "examples": [
        ["One data fabric across the plant", "I/O Connect brings DCS, PLC, batch systems, historians, LIMS and camera data into one namespace, with batch context attached."],
        ["Models tuned to the chemistry", "Deepsense builds soft sensors for conversion, purity, moisture and end-point that fill the gaps between lab samples."],
        ["Advisories into the control room", "Bruce AI turns predictions into batch-level alerts and setpoint advisories that operators can act on while the batch can still be saved."]
    ],
    "cta": "Pick one plant area and one KPI from this catalogue. Faclon connects the existing instrumentation, stands up a live dashboard and returns a quantified value unlock with a plant-wide scale-out plan, typically within a 4–6 week assessment.",
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "chemicals-use-cases" / "index.html")
