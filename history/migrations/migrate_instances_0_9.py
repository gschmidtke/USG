"""Migrate instances from protocol 0.8 to 0.9.
All: the new universal novelty trigger is recorded as not asked (null; applies conservatively, minimum standard).
ADU: design_rule never-statements get their evaluable stage. One Mile City: delivery route R1 rests on A-R1;
a failure scenario and flow are added for the 0.9 test (labelled; not from the author's exercise)."""
import json
NOVELTY = "novelty in environment, scale, technology, materials, system combination, autonomy or operating regime"
EVAL = {"no stairs": "S14", "not adjacent": "S12", "net interior area": "S14"}
for name in ("fail_no_need", "fail_all_sites_prohibited", "instance_adu_backyard", "stress_one_mile_city"):
    p = f"instances/{name}.json"
    I = json.load(open(p))
    if I["instance"]["protocol_version"] == "0.9":
        print("already 0.9:", p); continue
    assert I["instance"]["protocol_version"] == "0.8"
    I["instance"]["protocol_version"] = "0.9"
    major, minor = I["instance"]["version"].split(".")
    I["instance"]["version"] = f"{major}.{int(minor) + 1}"
    I["answers"]["S00.triggers"]["value"][NOVELTY] = {"value": None, "authority": "human",
                                                      "source_ref": "not asked: trigger added in protocol 0.9"}
    for st in I["answers"].get("S00.never", {}).get("value", []):
        if st.get("class") == "design_rule":
            st["evaluable_stage"] = next(v for k, v in EVAL.items() if k in st["statement"])
    if name == "stress_one_mile_city":
        r1 = next(r for r in I["answers"]["S01.delivery"]["value"] if r["id"] == "R1")
        r1["premises"] = ["A-R1"]
        I["scenarios"] = [{"id": "SC-FAIL-1", "kind": "failure", "description": "rupture of a mineral transfer line below the ice",
                           "initiating_event": "pipe rupture", "consequence_scope": "ocean below the ice",
                           "note": "added for the 0.9 test; not from the author's exercise"}]
        I["flows"] = [{"id": "F-SPILL", "medium": "goods", "source": "mineral logistics (H4)", "sink": "AS-OCEAN",
                       "scenarios": ["SC-FAIL-1"], "note": "added for the 0.9 test"}]
        I["expected"]["strain_categories"] = sorted(I["expected"]["strain_categories"] + ["environmental_absorption"])
    json.dump(I, open(p, "w"), indent=2, ensure_ascii=False)
    print("migrated", p, "->", I["instance"]["version"])
