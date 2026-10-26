"""Migrate failure instances from protocol 0.5.1 to 0.6 (instance version 0.1 -> 0.2)."""
import json
LIFECYCLE = {
    "fail_no_need": [{"id": "P1", "use": "public parking", "beneficiary": "public", "start": "on completion"}],
    "fail_all_sites_prohibited": [{"id": "P1", "use": "cross-dock depot for the client's own distribution", "beneficiary": "own_use", "start": "2028"}],
}
for name in LIFECYCLE:
    p = f"instances/{name}.json"
    I = json.load(open(p))
    assert I["instance"]["protocol_version"] == "0.5.1"
    I["instance"]["protocol_version"] = "0.6"
    I["instance"]["version"] = "0.2"
    trig = I.pop("feasibility_triggers")
    a = I["answers"]
    new = {}
    for k, v in a.items():
        new[k] = v
        if k == "S00.site_mode":
            new["S00.lifecycle_use"] = {"value": LIFECYCLE[name], "authority": "human", "source_ref": "brief", "status": "confirmed"}
            new["S00.triggers"] = {"value": trig, "authority": "human", "source_ref": "project setup", "status": "confirmed"}
    I["answers"] = new
    I["strategic_feasibility_record"]["excluded_alternatives"] = []
    json.dump(I, open(p, "w"), indent=2, ensure_ascii=False)
    print("migrated", p)
