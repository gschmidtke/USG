"""Migrate instances from protocol 0.9 to 0.10.
Full-depth instances: S01.need_behind recorded as not asked (unknown, blocks S19). One Mile City: the exercise
never considered a strategy-level alternative although delivery premise A-R1 is unresolved; this is recorded as
a documented expected violation (the Mars memo's Discovery A, reproduced on One Mile City)."""
import json
for name in ("fail_no_need", "fail_all_sites_prohibited", "instance_adu_backyard", "stress_one_mile_city"):
    p = f"instances/{name}.json"
    I = json.load(open(p))
    if I["instance"]["protocol_version"] == "0.10":
        print("already 0.10:", p); continue
    assert I["instance"]["protocol_version"] == "0.9"
    I["instance"]["protocol_version"] = "0.10"
    major, minor = I["instance"]["version"].split(".")
    I["instance"]["version"] = f"{major}.{int(minor) + 1}"
    if I["strategic_feasibility_record"].get("intensity") == "full":
        new = {}
        for k, v in I["answers"].items():
            new[k] = v
            if k == "S01.need":
                new["S01.need_behind"] = {"value": None, "authority": "human", "status": "unknown", "blocks_stage": "S19",
                                          "source_ref": "not asked: question added in protocol 0.10"}
        I["answers"] = new
    if name == "stress_one_mile_city":
        I["expected"]["violations"].append("no strategy-level alternative considered")
    json.dump(I, open(p, "w"), indent=2, ensure_ascii=False)
    print("migrated", p, "->", I["instance"]["version"])
