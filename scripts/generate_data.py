from __future__ import annotations

import csv
import random
from pathlib import Path


DEPARTMENTS = {
    "roads": {
        "issues": ["pothole", "damaged asphalt", "broken curb", "road crack", "uneven road", "open manhole"],
        "places": ["main road", "side street", "intersection", "school entrance", "neighborhood road", "service road"],
        "effects": ["damaging cars", "blocking traffic", "unsafe for drivers", "getting worse", "causing congestion", "hard to avoid"],
    },
    "lighting": {
        "issues": ["street light is out", "lamp is flickering", "broken light pole", "dark street", "several lights are off", "street lamp is damaged"],
        "places": ["park entrance", "residential street", "main avenue", "walkway", "intersection", "neighborhood"],
        "effects": ["area is very dark", "visibility is poor", "pedestrians cannot see well", "drivers struggle at night", "has been dark for days", "needs repair"],
    },
    "waste": {
        "issues": ["garbage is overflowing", "trash was not collected", "waste container is full", "rubbish is scattered", "illegal dumping", "garbage bags are piling up"],
        "places": ["outside our building", "near the market", "beside the school", "public parking area", "neighborhood corner", "next to the mosque"],
        "effects": ["smells bad", "attracts insects", "blocks the sidewalk", "has been there for days", "is spreading", "needs collection"],
    },
    "water": {
        "issues": ["water pipe is leaking", "water supply is weak", "no water is reaching homes", "clean water is flooding the street", "water meter area is leaking", "water pressure is very low"],
        "places": ["our block", "near the building", "residential street", "outside the house", "commercial area", "neighborhood"],
        "effects": ["water is being wasted", "residents have no supply", "the street is wet", "pressure keeps dropping", "problem is continuous", "needs inspection"],
    },
    "sewage": {
        "issues": ["sewage is overflowing", "sewer drain is blocked", "wastewater is backing up", "sewer cover is leaking", "drain smells strongly", "sewage water is in the street"],
        "places": ["near our homes", "at the intersection", "behind the shops", "residential street", "near the school", "neighborhood entrance"],
        "effects": ["bad odor is spreading", "wastewater is pooling", "the drain is not working", "pedestrians cannot pass", "it is getting worse", "needs urgent cleaning"],
    },
    "parks": {
        "issues": ["playground equipment is broken", "park irrigation is damaged", "grass is dying", "park bench is broken", "play area is dirty", "tree branch is blocking the path"],
        "places": ["community park", "children's park", "public garden", "walking park", "neighborhood park", "playground"],
        "effects": ["children cannot use it safely", "needs maintenance", "looks neglected", "blocks the walkway", "has been damaged for days", "needs cleaning"],
    },
    "building": {
        "issues": ["construction debris is blocking access", "building work appears unsafe", "wall is cracked", "abandoned building is deteriorating", "construction fence is damaged", "unauthorized structure blocks the walkway"],
        "places": ["next door", "near the sidewalk", "residential block", "commercial street", "near our house", "corner property"],
        "effects": ["debris reaches the road", "people cannot pass safely", "parts may fall", "work continues late", "site needs inspection", "hazard is visible"],
    },
    "public_safety": {
        "issues": ["fire in a building", "gas leak", "smoke coming from a utility box", "fallen electrical cable", "dangerous exposed wires", "traffic signal is hanging loose"],
        "places": ["near my building", "at the intersection", "beside the school", "outside the market", "on our street", "near a public facility"],
        "effects": ["people may be in danger", "area needs immediate attention", "residents are worried", "could cause injuries", "situation is unsafe", "needs a safety response"],
    },
}

PREFIXES = [
    "Please check", "I want to report", "Residents noticed", "There is", "We have", "Can the municipality inspect",
    "A complaint about", "Please send a team for", "Our neighborhood has", "I am reporting",
]
SUFFIXES = [
    "please resolve it", "please inspect the issue", "we need assistance", "please send maintenance",
    "this needs attention", "please handle it soon", "kindly investigate", "please arrange a visit",
]


def make_text(rng: random.Random, details: dict[str, list[str]]) -> str:
    prefix = rng.choice(PREFIXES)
    issue = rng.choice(details["issues"])
    place = rng.choice(details["places"])
    effect = rng.choice(details["effects"])
    suffix = rng.choice(SUFFIXES)
    patterns = [
        f"{prefix} {issue} {place}; it is {effect}. {suffix}.",
        f"{prefix} {issue} {place}. It is {effect}, so {suffix}.",
        f"{issue.capitalize()} {place} and it is {effect}. {suffix}.",
        f"{prefix} an issue: {issue} {place}. It is {effect}. {suffix}.",
        f"At the {place}, {issue}. It is {effect}. {suffix}.",
    ]
    return rng.choice(patterns)


def main() -> None:
    rng = random.Random(113)
    output = Path(__file__).resolve().parents[1] / "data" / "complaints_synthetic.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    record_id = 1
    for department, details in DEPARTMENTS.items():
        seen = set()
        while len(seen) < 1500:
            text = make_text(rng, details)
            text = text.replace("  ", " ")
            if text in seen:
                text = f"{text[:-1]} Reference area {rng.randint(1, 9999)}."
            if text in seen:
                continue
            seen.add(text)
            rows.append({
                "record_id": record_id,
                "complaint": text,
                "department": department,
                "data_source": "SYNTHETIC TRAINING DATA",
            })
            record_id += 1
    rng.shuffle(rows)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["record_id", "complaint", "department", "data_source"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"saved_records={len(rows)}")
    print(f"dataset={output}")


if __name__ == "__main__":
    main()
