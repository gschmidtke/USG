"""Migrate instances from protocol 0.6 to 0.7: add S01.delivery, classify S00.never statements."""
import json
DELIVERY = {
    "fail_no_need": [{"id": "R1", "means": "road delivery from regional suppliers", "depends_on": []}],
    "fail_all_sites_prohibited": [{"id": "R1", "means": "road delivery via the primary road network", "depends_on": []}],
    "instance_adu_backyard": [{"id": "R1", "means": "contractor delivery via the rear lane and back driveway", "depends_on": [],
                               "construction_method": "site-built or prefabricated, decided at S12"}],
}
NEVER_CLASS = {"heavy vehicles": "use_restriction", "no stairs": "design_rule", "not adjacent": "design_rule", "net interior area": "design_rule"}
for name, routes in DELIVERY.items():
    p = f"instances/{name}.json"
    I = json.load(open(p))
    if I["instance"]["protocol_version"] == "0.7":
        print("already 0.7:", p); continue
    assert I["instance"]["protocol_version"] == "0.6"
    I["instance"]["protocol_version"] = "0.7"
    major, minor = I["instance"]["version"].split(".")
    I["instance"]["version"] = f"{major}.{int(minor) + 1}"
    new = {}
    for k, v in I["answers"].items():
        new[k] = v
        if k == "S01.need":
            new["S01.delivery"] = {"value": routes, "authority": "human", "source_ref": "migration 0.7: delivery stated in brief",
                                   "status": "confirmed"}
    I["answers"] = new
    nv = I["answers"].get("S00.never")
    if nv:
        if isinstance(nv["value"], str):
            nv["value"] = [nv["value"]]
        nv["value"] = [{"statement": s, "class": next(c for key, c in NEVER_CLASS.items() if key in s), "kept_by_human": True}
                       for s in nv["value"]]
    json.dump(I, open(p, "w"), indent=2, ensure_ascii=False)
    print("migrated", p, "->", I["instance"]["version"])
