"""Builds agrochemicals-use-cases/index.html (Agrochemicals Use Cases).

Run from anywhere:  python3 src/agrochemicals-use-cases/build_page.py
Content lives in use_cases.json next to this script (format: see src/shared/use_case_map.py).
Source: written for the site (Oct 2026), adapted from Chemicals Use Cases with agrochemical formulation, packing, waste and planning use cases; there is no approved value source yet, so use cases carry no
₹ values or priority tiers. When a sized sheet arrives, add "v", "basis", "calc" and "tier" to each use
case, set "primary" below, and the value chart, totals and tier filter appear automatically.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "shared"))
from use_case_map import build  # noqa: E402

CFG = {
    "title": "Agrochemicals Use Cases",
    "sector": "Industrial AI · Crop protection chemicals",
    "eyebrow": "Industry brief · Agrochemicals, from technical to retail pack",
    "h1": 'An AI use-case catalogue for <em>agrochemical manufacturing</em>',
    "lede": "Thirty-five deployable AI use cases across crop protection manufacturing: multi-step synthesis of technical active ingredients, isolation and solvent recovery, SC, EC and granule formulation, small-pack filling, utilities, effluent and hazardous waste, safety, season-driven planning and multi-site benchmarking. Each one turns plant data into continuous intelligence and action for higher yield, consistent quality and safer, cleaner operation.",
    "primary": None,
    "basis_note": "",
    "area": "plant area",
    "search": "Search use cases, KPIs, equipment, e.g. batch, wet mill, granules, solvent, pack",
    "description": "35 AI use cases for agrochemical plants, from technical synthesis and solvent recovery to SC, EC and granule formulation, small-pack filling, ZLD, incineration and campaign planning.",
    "novalue_hero": "Value is sized for each site in a short assessment of its own batch, formulation, energy and quality data.",
    "novalue_note": "Value is sized for each plant: a 4–6 week assessment of your own data turns these use cases into a costed, prioritised plan.",
    "examples": [
        ["One data fabric across synthesis, formulation and packing", "I/O Connect brings DCS, PLC, batch systems, historians, LIMS, filling lines and cameras into one namespace, with batch and campaign context attached."],
        ["Models tuned to the chemistry and the formulation", "Deepsense builds soft sensors for conversion, purity, particle size, moisture and stability that fill the gaps between lab samples."],
        ["Advisories into the control room and the line", "Bruce AI turns predictions into batch-level and line-level alerts and advisories that operators can act on while the batch can still be saved."]
    ],
    "cta": "Pick one plant, one product and one KPI from this catalogue. Faclon connects the existing instrumentation, stands up a live dashboard and returns a quantified value unlock with a multi-site scale-out plan, typically within a 4–6 week assessment.",
}

if __name__ == "__main__":
    build(CFG, HERE / "use_cases.json", HERE.parents[1] / "agrochemicals-use-cases" / "index.html")
