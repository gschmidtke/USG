"""Minimal 2D geometry for USG export checks (no external dependencies).

Polygons are lists of [x, y] in the instance coordinate frame, assumed convex where noted.
Used by run_usg.py so the validator stays independent of any CAD library.
"""
import math

AXES = {"east": (1, 0, 0), "west": (-1, 0, 0), "north": (0, 1, 0), "south": (0, -1, 0), "up": (0, 0, 1), "down": (0, 0, -1)}


def right_handed(frame):
    try:
        x, y, z = AXES[frame["x_axis"]], AXES[frame["y_axis"]], AXES[frame["z_axis"]]
    except KeyError:
        return None
    cross = (x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0])
    return cross == z


def point_in_polygon(p, poly, eps=1e-9):
    """True if p is inside or on the boundary of poly."""
    x, y = p
    n = len(poly)
    for i in range(n):  # on an edge counts as inside
        a, b = poly[i], poly[(i + 1) % n]
        if seg_point_dist(a, b, p) <= eps:
            return True
    inside = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xin:
                inside = not inside
    return inside


def seg_point_dist(a, b, p):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def polygon_circle_distance(poly, center, radius):
    """Distance from the polygon to the circle's edge; negative or zero means they intersect."""
    if point_in_polygon(center, poly):
        return -radius
    d = min(seg_point_dist(poly[i], poly[(i + 1) % len(poly)], center) for i in range(len(poly)))
    return d - radius


def _project(poly, axis):
    dots = [p[0] * axis[0] + p[1] * axis[1] for p in poly]
    return min(dots), max(dots)


def convex_overlap(p1, p2, eps=1e-9):
    """Separating-axis test for two convex polygons; touching edges do not count as overlap."""
    for poly in (p1, p2):
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            axis = (y1 - y2, x2 - x1)
            a0, a1 = _project(p1, axis)
            b0, b1 = _project(p2, axis)
            if a1 <= b0 + eps or b1 <= a0 + eps:
                return False
    return True


def polygon_distance(p1, p2):
    if convex_overlap(p1, p2):
        return 0.0
    d = math.inf
    for P, Q in ((p1, p2), (p2, p1)):
        for v in P:
            for i in range(len(Q)):
                d = min(d, seg_point_dist(Q[i], Q[(i + 1) % len(Q)], v))
    return d


def satisfies_halfplane(poly, hp, eps=1e-9):
    nx, ny = hp["normal"]
    return all(nx * x + ny * y >= hp["offset"] - eps for x, y in poly)


def export_checks(footprint, envelope, deviations_unresolved, height=None):
    """Run the universal export checks of validation.export_checks for one footprint.
    Returns a list of {check, result, detail} in protocol order."""
    out = []
    # 1 inside the buildable envelope
    problems = []
    bg = (envelope.get("boundary") or {}).get("geometry") or {}
    b = bg.get("coords") if bg.get("type") == "polygon" else None
    if b and not all(point_in_polygon(v, b) for v in footprint):
        problems.append("outside boundary")
    for sb in envelope.get("setbacks", []):
        g = sb.get("geometry")
        if g and g.get("type") == "halfplane" and not satisfies_halfplane(footprint, g):
            problems.append(f"setback {sb.get('edge')}")
    for ra in envelope.get("reserved_areas", []):
        g = ra.get("geometry")
        if g and convex_overlap(footprint, g["coords"]):
            problems.append(f"reserved area {ra.get('id')}")
    out.append({"check": "footprint inside the buildable envelope", "result": "fail" if problems else "pass",
                "detail": ", ".join(problems)})
    # 2 no_structure zones
    hits, near = [], []
    for z in envelope.get("protected_zones", []):
        g = z.get("geometry")
        if not g or g.get("type") != "circle":
            continue
        d = polygon_circle_distance(footprint, g["center"], g["radius"])
        if z.get("rule") == "no_structure" and d <= 0:
            hits.append(z.get("id"))
        elif z.get("rule") == "no_footings" and d <= 0.5:
            near.append(f"{z.get('id')} ({'inside' if d <= 0 else f'{d:.1f} ft away'}): footing positions must avoid it")
    out.append({"check": "no intersection with protected zones of rule no_structure", "result": "fail" if hits else "pass",
                "detail": ", ".join(hits + near)})
    # 3 fixed existing elements
    over = [e.get("id") for e in envelope.get("existing_elements", [])
            if e.get("keep") and e.get("geometry", {}).get("type") == "polygon" and convex_overlap(footprint, e["geometry"]["coords"])]
    out.append({"check": "no overlap with fixed existing elements", "result": "fail" if over else "pass", "detail": ", ".join(over)})
    # 4 separations
    sep_fail, sep_detail = [], []
    for s in envelope.get("separations", []):
        target = next((e for e in envelope.get("existing_elements", []) if e.get("id") == s.get("from")), None)
        if target and target.get("geometry", {}).get("type") == "polygon":
            d = polygon_distance(footprint, target["geometry"]["coords"])
            sep_detail.append(f"{s.get('from')}: {d:.1f}")
            if isinstance(s.get("min"), (int, float)) and d < s["min"]:
                sep_fail.append(s.get("from"))
    out.append({"check": "required separations met", "result": "fail" if sep_fail else "pass", "detail": "; ".join(sep_detail)})
    # 5 access: needs a circulation graph (S12/S13); not evaluable from a footprint alone
    out.append({"check": "access connected from an access point to every entry", "result": "not_evaluable",
                "detail": "requires a validated circulation topology"})
    # 6 height
    hl = (envelope.get("height_limit") or {}).get("max")
    if height is None or hl is None:
        out.append({"check": "height within the height limit", "result": "not_evaluable", "detail": "height or limit not encoded"})
    else:
        out.append({"check": "height within the height limit", "result": "pass" if height <= hl else "fail",
                    "detail": f"{height} vs {hl}"})
    # 7 deviations
    out.append({"check": "no unresolved deviation from a recorded answer", "result": "fail" if deviations_unresolved else "pass",
                "detail": f"{deviations_unresolved} unresolved" if deviations_unresolved else ""})
    return out
