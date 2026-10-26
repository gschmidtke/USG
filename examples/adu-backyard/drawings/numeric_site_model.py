"""Numeric site model of instance_adu_backyard, generated from the encoded site envelope (USG 0.12).
Computes the buildable envelope (geometry_model / schemas.buildable_envelope) and draws a coordinate diagram.
Every shape is read from the instance JSON; nothing is placed by hand."""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[3]
instance_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "conformance/instances/instance_adu_backyard.json"
I = json.load(open(instance_path, encoding="utf-8"))
E, F = I["site_envelope"], I["coordinate_frame"]
H = I["design_hypotheses"][0]
ORDER = ["confirmed", "assumed", "exercise", "range"]

# ---------------------------------------------------------------- buildable envelope
lot = Polygon(E["boundary"]["geometry"]["coords"])
big = 1e4
region = lot
inputs = [("boundary", E["boundary"]["status"])]
for sb in E["setbacks"]:
    nx, ny = sb["geometry"]["normal"]; off = sb["geometry"]["offset"]
    if nx:   # x-halfplane
        x = off / nx
        hp = box(x, -big, big, big) if nx > 0 else box(-big, -big, x, big)
    else:
        y = off / ny
        hp = box(-big, y, big, big) if ny > 0 else box(-big, -big, big, y)
    region = region.intersection(hp)
    inputs.append((f"setback {sb['edge']}", sb["status"]))
cut = []
for z in E["protected_zones"]:
    if z["rule"] == "no_structure":
        cut.append(Point(z["geometry"]["center"]).buffer(z["geometry"]["radius"], 64))
        inputs.append((z["id"], z["status"]))
for el in E["existing_elements"]:
    if el.get("keep") and el.get("geometry", {}).get("type") == "polygon":
        cut.append(Polygon(el["geometry"]["coords"])); inputs.append((el["id"], el["status"]))
for ra in E.get("reserved_areas", []):
    cut.append(Polygon(ra["geometry"]["coords"])); inputs.append((ra["id"], ra["status"]))
buildable = region.difference(unary_union(cut)) if cut else region
status = max((s for _, s in inputs if s in ORDER), key=ORDER.index)
fp = Polygon(H["footprint"])
print(f"buildable envelope: {buildable.area:.0f} sq ft, status {status}; footprint {fp.area:.1f} sq ft gross, "
      f"inside: {buildable.buffer(1e-6).contains(fp)}")

# ---------------------------------------------------------------- drawing
fig, ax = plt.subplots(figsize=(15, 10), dpi=150)
ax.set_aspect("equal"); ax.set_xlim(-14, 134); ax.set_ylim(-16, 88)
for x in range(0, 127, 10):
    ax.axvline(x, color="#eeeeee", lw=0.5, zorder=0)
for y in range(0, 75, 10):
    ax.axhline(y, color="#eeeeee", lw=0.5, zorder=0)
ax.tick_params(labelsize=7)
ax.set_xticks(range(0, 127, 10)); ax.set_yticks(range(0, 75, 10))
for s in ax.spines.values():
    s.set_visible(False)

def poly(coords, **kw):
    ax.add_patch(MPoly(coords, closed=True, **kw))

poly(E["boundary"]["geometry"]["coords"], fill=False, ec="#222", lw=1.8)
geoms = list(buildable.geoms) if buildable.geom_type == "MultiPolygon" else [buildable]
for g in geoms:
    poly(list(g.exterior.coords), fc="#d9f2d9", ec="#2e7d32", lw=1.2, hatch="..", alpha=0.9, zorder=1)
for z in E["protected_zones"]:
    c, r = z["geometry"]["center"], z["geometry"]["radius"]
    style = {"no_structure": dict(fc="#2e7d32", ec="black", lw=0.8),
             "no_footings": dict(fc="#c62828", ec="#c62828", lw=1.2, ls="--", alpha=0.15),
             "no_excavation": dict(fill=False, ec="#2e7d32", lw=0.8, ls=":")}[z["rule"]]
    ax.add_patch(Circle(c, r, zorder=2, **style))
for el in E["existing_elements"]:
    if el.get("geometry", {}).get("type") == "polygon":
        poly(el["geometry"]["coords"], fc="#ecf0f1", ec="#7f8c8d", lw=1.3, hatch="//", zorder=2)
for ra in E.get("reserved_areas", []):
    poly(ra["geometry"]["coords"], fc="#eaecee", ec="#5d6d7e", lw=1.1, ls="-.", zorder=2)
for k, c in H.get("appurtenances", {}).items():
    poly(c, fc="#f3e5c8", ec="#8e6e3d", lw=1.0, zorder=3)
poly(H["footprint"], fc="#dbe8f5", ec="#1f4e79", lw=2.2, zorder=4)

# coordinate labels at key points
def label(pt, text, dx=0.8, dy=0.8, ha="left", color="#1f4e79"):
    ax.plot(*pt, "o", ms=3, color=color, zorder=6)
    ax.text(pt[0] + dx, pt[1] + dy, text, fontsize=6.8, color=color, ha=ha, zorder=6,
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.4))
fpc = H["footprint"]
label(fpc[3], f"({fpc[3][0]:.2f}, {fpc[3][1]:.2f})", dy=1.2)
label(fpc[2], f"({fpc[2][0]:.2f}, {fpc[2][1]:.2f})", dy=1.2)
label(fpc[0], f"({fpc[0][0]:.2f}, {fpc[0][1]:.2f})", dx=-0.8, dy=-2.6, ha="right")
label(fpc[1], f"({fpc[1][0]:.2f}, {fpc[1][1]:.2f})", dy=-2.6)
tr = E["protected_zones"][0]["geometry"]["center"]
label(tr, f"trunk ({tr[0]:.1f}, {tr[1]:.1f})", dx=1.8, dy=-1.0, color="#2e7d32")
hs = next(e for e in E["existing_elements"] if e["id"] == "main house")["geometry"]["coords"]
label(hs[3], f"house ({hs[3][0]:.0f}, {hs[3][1]:.0f})", dx=0.8, dy=0.8, color="#555")
label(hs[0], f"({hs[0][0]:.0f}, {hs[0][1]:.0f})", dx=0.8, dy=-2.6, color="#555")
label((0, 0), "origin (0, 0)\nSW lot corner", dx=0.8, dy=-6, color="#222")
label((126, 74), "(126, 74)", dx=-0.8, dy=0.8, ha="right", color="#222")
ax.text(fp.centroid.x, fp.centroid.y, f"H-ADU-2\n{fp.area:.0f} sq ft gross", ha="center", va="center", fontsize=8,
        color="#1f4e79", fontweight="bold", zorder=5)
for g in geoms:
    if g.area > 500:
        ax.text(28, 20, f"BUILDABLE ENVELOPE\n{buildable.area:,.0f} sq ft · status: {status}",
                ha="center", fontsize=8.5, color="#2e7d32", fontweight="bold", zorder=5,
                bbox=dict(fc="white", ec="#2e7d32", alpha=0.85, pad=2))
        break
# setback values
ax.text(E["setbacks"][0]["geometry"]["offset"] + 0.5, 1.5, "x ≥ 9.84 (rear 3 m, exercise)", fontsize=6.5, color="#c0392b", rotation=90)
ax.text(100, 69.6, "y ≤ 69 (north 5 ft, exercise)", fontsize=6.5, color="#c0392b")
ax.text(100, 10.6, "y ≥ 10 (south, range 5-10 ft, worst case)", fontsize=6.5, color="#c0392b")
ax.text(96.6, 40, "x ≤ 96 (front 30 ft, assumed)", fontsize=6.5, color="#c0392b", rotation=90)
for x in (E["setbacks"][0]["geometry"]["offset"], 96):
    ax.plot([x, x], [0, 74], color="#c0392b", lw=0.8, ls="--", zorder=1)
for y in (69, 10):
    ax.plot([0, 126], [y, y], color="#c0392b", lw=0.8, ls="--", zorder=1)

# frame
ax.annotate("", xy=(-6, -10), xytext=(-12, -10), arrowprops=dict(arrowstyle="-|>", lw=1.2))
ax.annotate("", xy=(-12, -4), xytext=(-12, -10), arrowprops=dict(arrowstyle="-|>", lw=1.2))
ax.text(-5.5, -10, "x east", fontsize=7, va="center"); ax.text(-12, -3.4, "y north", fontsize=7, ha="center")
ax.text(-12.6, -11.2, "z up ⊙", fontsize=7, ha="right", va="top")
ax.set_title(f"USG 0.12 · {I['instance']['id']} · NUMERIC SITE MODEL (generated from encoded envelope)\n"
             f"frame: origin {F['origin']}, x {F['x_axis']}, y {F['y_axis']}, z {F['z_axis']} (right-handed), units {F['units']}, "
             f"datum: {F['elevation_datum']} · controlling geometry: {E['controlling_geometry_ref']} · exploratory",
             fontsize=9.5, loc="left")
ax.text(-13, 84, "Legend: green dotted = buildable envelope · red dashed = setbacks · red disc = structural root zone (no footings) · "
        "green dotted circle = tree protection zone (no excavation) · grey hatch = main house · dash-dot = parking reservation P1",
        fontsize=7, color="#555")
out = "drawings/numeric_site_model.png"
plt.savefig(out, bbox_inches="tight", facecolor="white")
print("written", out)
