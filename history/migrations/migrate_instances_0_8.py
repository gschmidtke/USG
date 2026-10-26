"""Migrate instances from protocol 0.7 to 0.8: S00.drivers (all), S01.affected_systems (intensity != light).
Values are taken only from what each instance already records; nothing is imputed."""
import json

DRIVERS = {
    "fail_no_need": [{"id": "SH-1", "role": "initiator", "trigger": "merchant complaints about evening parking",
                      "decision_power": "City Commission", "interests": "as stated in council brief 2026-02",
                      "source_ref": "council brief 2026-02"}],
    "fail_all_sites_prohibited": [{"id": "SH-1", "role": "initiator and owner", "trigger": "regional volume exceeds existing depot capacity",
                                   "decision_power": "client board", "interests": "as stated in client brief 2026-04",
                                   "source_ref": "client brief 2026-04"}],
    "instance_adu_backyard": [{"id": "SH-1", "role": "initiator, owner and financier",
                               "trigger": "mother-in-law needs to live close to family in old age",
                               "decision_power": "owner", "interests": "as stated in the inquiry (Q1-Q5)",
                               "source_ref": "inquiry Q1-Q10"}],
}
AFFECTED = {
    "fail_no_need": [
        {"id": "AS-TRAFFIC", "kind": "infrastructure", "baseline": {"evidence_refs": ["E-DEM-1"], "confidence": "high"},
         "change": {"magnitude": "unresolved", "persistence": "persistent", "reversibility": "low"},
         "burden_bearers": ["Main St corridor residents"], "note": "induced evening traffic, from the trigger record"}],
    "fail_all_sites_prohibited": [
        {"id": "AS-ROADS", "kind": "infrastructure", "baseline": {"evidence_refs": [], "confidence": "low"},
         "change": {"magnitude": "unresolved", "persistence": "persistent", "reversibility": "low"},
         "burden_bearers": ["road users near the chosen site"], "note": "about 120 HGV movements per day, from the trigger record"},
        {"id": "AS-WETLAND-B", "kind": "ecology", "baseline": {"evidence_refs": ["E-B-ENV"], "confidence": "high"},
         "change": {"magnitude": "unresolved", "persistence": "unresolved", "reversibility": "unresolved"},
         "note": "SITE-B wetland; site dropped at S02"}],
    "instance_adu_backyard": [
        {"id": "AS-TREE", "kind": "ecology", "baseline": {"evidence_refs": ["E-OWN-TREE", "E-PHOTO-YARD"], "confidence": "medium"},
         "change": {"magnitude": "unresolved", "persistence": "unresolved", "reversibility": "unresolved"},
         "mitigation": "retain tree; root protection zone (open item)"},
        {"id": "AS-UTILITIES", "kind": "infrastructure", "baseline": {"evidence_refs": ["E-OWN-UTIL"], "confidence": "medium"},
         "change": {"magnitude": "unresolved", "persistence": "persistent", "reversibility": "high"},
         "note": "additional load on city sewer, water and the house electrical service"}],
}
for name in DRIVERS:
    p = f"instances/{name}.json"
    I = json.load(open(p))
    if I["instance"]["protocol_version"] == "0.8":
        print("already 0.8:", p); continue
    assert I["instance"]["protocol_version"] == "0.7"
    I["instance"]["protocol_version"] = "0.8"
    major, minor = I["instance"]["version"].split(".")
    I["instance"]["version"] = f"{major}.{int(minor) + 1}"
    new = {"S00.drivers": {"value": DRIVERS[name], "authority": "human", "source_ref": "migration 0.8: from recorded brief",
                           "status": "confirmed"}}
    for k, v in I["answers"].items():
        new[k] = v
        if k == "S01.delivery":
            new["S01.affected_systems"] = {"value": [a["id"] for a in AFFECTED[name]], "authority": "external_evidence",
                                           "source_ref": "migration 0.8: from recorded evidence", "status": "recorded"}
    I["answers"] = new
    I["affected_systems"] = AFFECTED[name]
    I.setdefault("current_phase", "concept")
    json.dump(I, open(p, "w"), indent=2, ensure_ascii=False)
    print("migrated", p, "->", I["instance"]["version"])
