#!/usr/bin/env python3
"""Run the checks that Building 001 v0.3 declares about itself.

Dependency-free. Evaluates the identity, policy, coordinate, topology and
concept-profile checks that can be decided from the JSON alone, and reports
the rest as not machine-checkable. Exit code 1 if any decidable check fails.

    python examples/building-001/check_building_001.py [path-to-v0.3.json]
"""
import json
import sys
from pathlib import Path

DEFAULT = Path(__file__).parent / "spec" / "Building_001_USG_Sketch_Interpretation_v0.3.json"


def shoelace(points):
    area = 0.0
    for (x1, y1, *_), (x2, y2, *_) in zip(points, points[1:] + points[:1]):
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


def segments_cross(p1, p2, q1, q2):
    def orient(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return (v > 0) - (v < 0)
    o1, o2, o3, o4 = orient(p1, p2, q1), orient(p1, p2, q2), orient(q1, q2, p1), orient(q1, q2, p2)
    return o1 * o2 < 0 and o3 * o4 < 0


def simple_polygon(points):
    n = len(points)
    edges = [(points[i], points[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) in (1, n - 1):
                continue
            if segments_cross(*edges[i], *edges[j]):
                return False
    return True


def bbox(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def rect_size(poly):
    x0, x1, y0, y1 = bbox(poly)
    return x1 - x0, y1 - y0


def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    g = d["authoritative_geometry"]
    poly = g["footprint_polygon"]["points_mm"]
    model = g["footprint_polygon_model_mm"]
    rooms = {r["id"]: r for r in d["space_program"]}
    prof = d["concept_build_profile"]
    depth = g["overall_depth_mm"]["value"]
    results = []

    def check(cid, ok, what):
        results.append((cid, bool(ok), what))

    # Identity checks (validation.identity_checks)
    x0, x1, y0, y1 = bbox(poly)
    check("V001", x1 - x0 == 14000 == g["overall_width_mm"]["value"], "overall width 14000")
    check("V002", y1 - y0 == 14000 == depth, "overall depth 14000")
    check("V003", g["upper_bar_depth_mm"]["value"] == 6000, "upper bar depth 6000")
    check("V004", g["projecting_wing_width_mm"]["value"] == 6000, "projecting wing width 6000")
    check("V005", abs(shoelace(poly) / 1e6 - 132.0) <= 0.01 and g["footprint_area_m2"]["value"] == 132.0, "footprint area 132.0 m2 (shoelace)")
    check("V006", g["footprint_polygon"]["closed"] and simple_polygon(poly), "footprint closed and non-self-intersecting")

    # Policy checks (decidable ones)
    hints = d["proportional_hints"]
    check("V201", hints.get("non_binding") is True and hints.get("do_not_build") is True, "proportional hints non-binding")
    check("V202", d["external_envelope"]["wall_thickness_mm"] is None, "authoritative wall thickness is null")
    check("V205", d["coordinate_system"]["compass"] is None, "axes not named as compass directions")
    openings = d["openings"]["doors"] + d["openings"]["windows"]
    check("V206", all(o.get("width_mm") is None and "along_mm" not in o for o in openings), "no authoritative opening has width or position")

    # Coordinate checks (enhanced_validation)
    roundtrip = all(depth - (depth - p[1]) == p[1] for p in poly)
    mapped = [[p[0], depth - p[1]] for p in poly]
    check("EVV001", roundtrip and [m[:2] for m in model] == mapped, "sketch->model transform invertible and matches stored model polygon")
    mx0, mx1, my0, my1 = bbox(model)
    check("EVV002", (mx0, mx1) == (0, 14000), "model x extent 0..14000")
    check("EVV003", (my0, my1) == (0, 14000), "model y extent 0..14000")

    # Topology checks
    bed2, living = rooms["RM_BED_02"]["polygon_mm"], rooms["RM_LIVING_01"]["polygon_mm"]
    check("EVV101", bbox(bed2)[3] == bbox(living)[2] == 6000, "RM_BED_02 above RM_LIVING_01, shared y=6000")
    check("EVV102", rect_size(living) == (6000, 8000), "RM_LIVING_01 is 6000 x 8000")
    canopy = prof["roofs"]["canopy"]["sketch_footprint_mm"]
    cx0, cx1, cy0, cy1 = bbox(canopy)
    inside = cy0 >= 6000 and cx1 <= 8000  # re-entrant zone: below the bar, left of the wing
    check("EVV103", inside and d["covered_exterior_spaces"][0]["area_included_in_enclosed_132_m2"] is False, "porch exterior and outside the 132 m2")

    # Concept-profile checks
    r = prof["roofs"]
    import math
    def ridge(roof, span_mm):
        return roof["eave_height_mm"] + math.tan(math.radians(roof["pitch_degrees"])) * span_mm / 2
    primary_ridge = ridge(r["primary"], 6000)
    wing_ridge = ridge(r["projecting_wing"], 6000)
    check("EVV201", primary_ridge > wing_ridge, f"primary ridge {primary_ridge:.0f} > wing ridge {wing_ridge:.0f} mm")
    check("EVV202", r["canopy"]["front_edge_height_mm"] < r["canopy"]["wall_attachment_height_mm"], "canopy front edge lower than wall attachment")
    posts_ok = all(cx0 <= p["x_sketch_mm"] <= cx1 and cy0 <= p["y_sketch_mm"] <= cy1 for p in prof["posts"])
    check("EVV203", posts_ok, "all concept posts inside the re-entrant canopy zone")
    check("EVV204", "Do not cut" in prof["opening_policy"]["default"], "no approximate opening cut by default")

    width = max(len(c) for c, _, _ in results)
    for cid, ok, what in results:
        print(f"{'PASS' if ok else 'FAIL'}  {cid:<{width}}  {what}")
    print("not machine-checkable here: V101 (labels on sketch), V203, V204, EVV104, EVV301-303 (need a built model or the source image)")
    failed = [c for c, ok, _ in results if not ok]
    print(f"{len(results) - len(failed)}/{len(results)} decidable checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT))
