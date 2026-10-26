"""Migrate instances from protocol 0.10 to 0.11.
ADU: the site envelope recorded on 2026-10-12 is brought into the 0.11 schema (every value gets a status);
H-ADU-2 is a geometric hypothesis citing the answers it uses (the owner already reconciled the laundry position).
One Mile City: its hypotheses are concept-level."""
import json
for name in ("fail_no_need", "fail_all_sites_prohibited", "instance_adu_backyard", "stress_one_mile_city"):
    p = f"instances/{name}.json"
    I = json.load(open(p))
    if I["instance"]["protocol_version"] == "0.11":
        print("already 0.11:", p); continue
    assert I["instance"]["protocol_version"] == "0.10"
    I["instance"]["protocol_version"] = "0.11"
    major, minor = I["instance"]["version"].split(".")
    I["instance"]["version"] = f"{major}.{int(minor) + 1}"
    if name == "instance_adu_backyard":
        e = I["site_envelope"]
        e["note"] = "0.11 schema. Coordinates in ft from the west and north lot lines."
        e["boundary"] = {"value": "about 126 x 74 ft", "status": "assumed", "source_ref": "E-SKETCH-SITE (owner sketch, no survey)"}
        for s in e["setbacks"]:
            s["status"] = "exercise"; s["source_ref"] = s.pop("ref")
        e["setbacks"][1]["min"], e["setbacks"][1]["max"] = "5 ft", "10 ft"
        e["separations"][0].update(source_ref="inquiry Q54")
        e["protected_zones"][0]["source_ref"] = "E-OWN-TRUNK; rules of thumb (AS 4970)"
        for x in e["existing_elements"]:
            x.update(status="confirmed", source_ref="owner (Q12-Q13, Q49-Q50)")
        e["orientation_datum"] = {"value": e["orientation_datum"], "status": "confirmed", "source_ref": "inquiry Q32"}
        e["access_points"] = {"value": e["access_points"], "status": "confirmed", "source_ref": "inquiry Q33, Q62-Q65"}
        e["height_limit"] = {"value": "30 ft (R-2)", "status": "assumed", "source_ref": "E-ZONE-MIRROR (low confidence)"}
        h = I["design_hypotheses"][0]
        h["uses_answers"] = ["S00.never", "S04.orientation", "S04.access", "S04.existing", "S04.intervention_zone",
                             "S06.functions", "S06.zones", "S07.size"]
        h["deviations"] = []
        h["rests_on"] = "favourable"
        h["rests_on_note"] = "north setback 5 ft is the low end of the 5-10 ft code range"
    if name == "stress_one_mile_city":
        for h in I["design_hypotheses"]:
            h["level"] = "concept"
    json.dump(I, open(p, "w"), indent=2, ensure_ascii=False)
    print("migrated", p, "->", I["instance"]["version"])
