"""Migrate instances from protocol 0.11 to 0.12.
ADU: declare a right-handed coordinate frame and encode the site envelope as geometry.
Frame: origin = southwest lot corner, x = east, y = north, z = up, units ft, datum = existing grade at the studio.
(The 0.11 sandbox drawing used y = south from the north line; converted here: y_north = 74 - y_south.)
All other instances: version bump only (no geometric hypotheses)."""
import json
FT = 0.3048
LOT_D = 74.0
def yn(ys):
    return round(LOT_D - ys, 3)

for name in ("fail_no_need", "fail_all_sites_prohibited", "instance_adu_backyard", "stress_one_mile_city"):
    p = f"instances/{name}.json"
    I = json.load(open(p))
    if I["instance"]["protocol_version"] == "0.12":
        print("already 0.12:", p); continue
    assert I["instance"]["protocol_version"] == "0.11"
    I["instance"]["protocol_version"] = "0.12"
    major, minor = I["instance"]["version"].split(".")
    I["instance"]["version"] = f"{major}.{int(minor) + 1}"
    if name == "instance_adu_backyard":
        I["coordinate_frame"] = {"origin": "southwest lot corner", "x_axis": "east", "y_axis": "north", "z_axis": "up",
                                 "units": "ft", "elevation_datum": "existing grade at the studio = 0.0", "north": "+y (plan north)"}
        e = I["site_envelope"]
        e["note"] = "0.12 schema: values encoded as geometry in coordinate_frame."
        e["controlling_geometry_ref"] = "owner_sketch"
        e["boundary"]["geometry"] = {"type": "polygon", "coords": [[0, 0], [126, 0], [126, LOT_D], [0, LOT_D]]}
        w, n = e["setbacks"][0], e["setbacks"][1]
        w["geometry"] = {"type": "halfplane", "normal": [1, 0], "offset": round(3 / FT, 3)}
        n["geometry"] = {"type": "halfplane", "normal": [0, -1], "offset": -yn(5.0)}
        e["setbacks"] += [
            {"edge": "south", "distance": "5-10 ft (side setback, code range)", "status": "range", "min": "5 ft", "max": "10 ft",
             "source_ref": "E-ZONE-MIRROR", "geometry": {"type": "halfplane", "normal": [0, 1], "offset": 10.0},
             "note": "encoded at the worst case (10 ft), buildable_envelope.range_rule"},
            {"edge": "east (front, N Boyd St)", "distance": "30 ft", "status": "assumed", "source_ref": "E-ZONE-MIRROR (R-2 front yard)",
             "geometry": {"type": "halfplane", "normal": [-1, 0], "offset": -96.0}}]
        trunk = [25.0, yn(30.6)]
        e["protected_zones"] = [
            {"id": "PZ-TRUNK", "entity": "oak trunk", "rule": "no_structure", "status": "assumed", "source_ref": "E-OWN-TRUNK, E-SKETCH-SITE",
             "geometry": {"type": "circle", "center": trunk, "radius": 1.6}},
            {"id": "PZ-SRZ", "entity": "oak structural root zone", "rule": "no_footings", "status": "assumed",
             "source_ref": "AS 4970 rule of thumb; arborist to confirm", "geometry": {"type": "circle", "center": trunk, "radius": 10.7}},
            {"id": "PZ-TPZ", "entity": "oak tree protection zone", "rule": "no_excavation", "status": "assumed",
             "source_ref": "AS 4970 rule of thumb; arborist to confirm", "geometry": {"type": "circle", "center": trunk, "radius": 37.6},
             "note": "earth screws only; no trenching"}]
        for x in e["existing_elements"]:
            if x["id"] == "main house":
                x["status"] = "assumed"
                x["source_ref"] = "size and south distance: owner (Q49); west wall: sketch"
                x["geometry"] = {"type": "polygon", "coords": [[49, yn(66)], [95, yn(66)], [95, yn(20)], [49, yn(20)]]}
            if x["id"] == "oak":
                x["geometry"] = {"type": "point", "coords": trunk}
        e["reserved_areas"] = [{"id": "P1", "use": "parking (1 required)", "status": "exercise", "source_ref": "inquiry Q65",
                                "geometry": {"type": "polygon", "coords": [[0.4, yn(45.5)], [9.4, yn(45.5)], [9.4, yn(27.5)], [0.4, yn(27.5)]]}}]
        e["height_limit"].update(max=30)
        h = I["design_hypotheses"][0]
        x0, x1 = round(3 / FT, 3), round(3 / FT + 25.75, 3)
        h["footprint"] = [[x0, yn(20)], [x1, yn(20)], [x1, yn(5)], [x0, yn(5)]]
        h["appurtenances"] = {
            "terrace": [[x0, yn(25)], [x1, yn(25)], [x1, yn(20)], [x0, yn(20)]],
            "ramp_west": [[round(x0 - 6, 3), yn(25)], [x0, yn(25)], [x0, yn(20.5)], [round(x0 - 6, 3), yn(20.5)]],
            "ramp_east": [[x1, yn(25)], [round(x1 + 6, 3), yn(25)], [round(x1 + 6, 3), yn(20.5)], [x1, yn(20.5)]]}
        h["floor_level"] = 0.5
        h["uses_answers"] = sorted(set(h["uses_answers"]) | {"S04.access"})
    json.dump(I, open(p, "w"), indent=2, ensure_ascii=False)
    print("migrated", p, "->", I["instance"]["version"])
