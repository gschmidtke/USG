"""Sandbox site plan for instance_adu_backyard (exercise values, exploratory).
Coordinates in feet: x east from the west lot line, y south from the north lot line (north is up)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon

FT_M = 0.3048
LOT_W, LOT_D = 126.0, 74.0                    # from sketch, low confidence
REAR_SB, NORTH_SB = 3 / FT_M, 5.0             # exercise values
EXT_W, EXT_D = 25.75, 15.0                    # Variant B exterior
SX0, SY0 = REAR_SB, NORTH_SB
SX1, SY1 = SX0 + EXT_W, SY0 + EXT_D
TERR = 5.0
RAMP = 6.0
TRUNK = (25.0, 30.6)                          # from sketch
TRUNK_D = 3.0 / 3.14159 / FT_M                # 3 m circumference
SRZ, CANOPY, TPZ = 10.7, 30.0, 37.6
HOUSE = (49.0, 20.0, 46.0, 46.0)              # x, y, w, h: west wall from sketch, size and south distance per owner
PARK = (0.4, 27.5, 9.0, 18.0)

C = dict(lot="#222222", sb="#c0392b", studio="#1f4e79", terr="#8e6e3d", ramp="#b08d57", tree="#2e7d32",
         srz="#c62828", house="#7f8c8d", park="#5d6d7e", lane="#d5d8dc", dim="#444444", note="#555555")

fig, ax = plt.subplots(figsize=(16, 11), dpi=150)
ax.set_aspect("equal")
ax.set_xlim(-22, 132)
ax.set_ylim(92, -22)
ax.axis("off")

def dim(x0, y0, x1, y1, text, off=(0, 0), color=C["dim"], fs=8):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.9, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], text, ha="center", va="center", fontsize=fs,
            color=color, bbox=dict(fc="white", ec="none", pad=0.6))

# context: lane and street
ax.add_patch(Rectangle((-16, -14), 15, 102, fc=C["lane"], ec="none"))
ax.text(-8.5, 37, "REAR LANE\n(back driveway)\nslopes north", rotation=90, ha="center", va="center", fontsize=9, color="#555")
ax.add_patch(Rectangle((127, -14), 6, 102, fc=C["lane"], ec="none"))
ax.text(130, 37, "N BOYD ST", rotation=90, ha="center", va="center", fontsize=9, color="#555")

# tree zones (behind everything)
ax.add_patch(Circle(TRUNK, TPZ, fc="none", ec=C["tree"], lw=0.8, ls=(0, (2, 3)), alpha=0.7))
ax.add_patch(Circle(TRUNK, CANOPY, fc="#2e7d32", ec=C["tree"], lw=1.0, ls=":", alpha=0.08))
ax.add_patch(Circle(TRUNK, SRZ, fc="#c62828", ec=C["srz"], lw=1.2, ls="--", alpha=0.10))
ax.add_patch(Circle(TRUNK, TRUNK_D / 2, fc=C["tree"], ec="black", lw=0.8))
ax.text(TRUNK[0] + 2.2, TRUNK[1] + 1.2, "OAK TRUNK\n≈ 38\" dia\n(3 m circ.)", fontsize=7.5, color=C["tree"], va="top")
ax.text(TRUNK[0] + 3.5, TRUNK[1] + 9.3, "structural root zone  r ≈ 11 ft", fontsize=7, color=C["srz"], ha="left")
ax.text(TRUNK[0] - 10, TRUNK[1] + 27.5, "canopy  r ≈ 30 ft (shaded)", fontsize=7, color=C["tree"], ha="center")
ax.text(TRUNK[0] - 10, TRUNK[1] + 35.0, "tree protection zone  r ≈ 38 ft (dotted)", fontsize=7, color=C["tree"], ha="center")

# lot and setbacks
ax.add_patch(Rectangle((0, 0), LOT_W, LOT_D, fc="none", ec=C["lot"], lw=1.8))
ax.plot([REAR_SB, REAR_SB], [0, LOT_D], color=C["sb"], lw=1.0, ls="--")
ax.plot([0, LOT_W], [NORTH_SB, NORTH_SB], color=C["sb"], lw=1.0, ls="--")
ax.text(REAR_SB + 0.6, LOT_D - 2, "rear setback 3 m (9'-10\")\nexercise value", fontsize=7, color=C["sb"], va="bottom")
ax.text(LOT_W - 1, NORTH_SB - 0.8, "north setback 5 ft (exercise value)", fontsize=7, color=C["sb"], ha="right", va="bottom")
ax.text(1, -1.2, "LOT  ≈ 126 × 74 ft  (from owner's map sketch, ± 3 ft, no survey)", fontsize=8, color=C["lot"], va="bottom")

# house
hx, hy, hw, hh = HOUSE
ax.add_patch(Rectangle((hx, hy), hw, hh, fc="#ecf0f1", ec=C["house"], lw=1.4, hatch="//"))
ax.text(hx + hw / 2, hy + hh / 2, "MAIN HOUSE\n≈ 14 × 14 m (46 × 46 ft)\nsize per owner, position\nfrom sketch (approx.)",
        ha="center", va="center", fontsize=8, color="#2c3e50", bbox=dict(fc="white", ec="none", alpha=0.85))
dim(hx + hw / 2, hy + hh, hx + hw / 2, LOT_D, "8 ft\n(owner)", off=(5, 0))

# parking P1
px, py, pw, ph = PARK
ax.add_patch(Rectangle((px, py), pw, ph, fc="#eaecee", ec=C["park"], lw=1.2, ls="-."))
ax.text(px + pw / 2, py + ph / 2, "P1\nparking\n9 × 18 ft\npermeable\n(if setback\npermits)", ha="center", va="center", fontsize=7, color=C["park"])

# terrace and ramps
ax.add_patch(Rectangle((SX0, SY1), EXT_W, TERR, fc="#f3e5c8", ec=C["terr"], lw=1.2))
ax.text(SX0 + EXT_W / 2, SY1 + TERR / 2, "TERRACE  +6\"  (no footings in root zone)", ha="center", va="center", fontsize=7.5, color=C["terr"])
for x0, x1, lab in ((SX0 - RAMP, SX0, "RAMP\n1:12"), (SX1, SX1 + RAMP, "RAMP\n1:12")):
    ax.add_patch(Rectangle((x0, SY1 + 0.5), RAMP, TERR - 0.5, fc="#fbf3e2", ec=C["ramp"], lw=1.0, hatch=".."))
    ax.text((x0 + x1) / 2, SY1 + TERR + 1.4, lab.replace("\n", " "), ha="center", va="center", fontsize=6, color=C["ramp"])

# studio
ax.add_patch(Rectangle((SX0, SY0), EXT_W, EXT_D, fc="#dbe8f5", ec=C["studio"], lw=2.2))
band_y = SY0 + 0.5 + 5.5
ax.plot([SX0 + 0.5, SX1 - 0.5], [band_y, band_y], color=C["studio"], lw=0.8, ls=":")
ax.text(SX0 + EXT_W / 2, SY0 + 3.2, "service band: closet · W/D · bath · kitchen", ha="center", va="center", fontsize=6.5, color=C["studio"])
ax.text(SX0 + EXT_W / 2, SY0 - 1.6, "north wall: no windows", ha="center", va="center", fontsize=6.5, color=C["studio"])
ax.text(SX0 + EXT_W / 2, SY0 + 10.6, "STUDIO  (H-ADU-2, Variant B)\nliving · dining · sleeping", ha="center", va="center", fontsize=8.5, color=C["studio"], fontweight="bold")
ax.plot([SX0 + 4, SX1 - 4], [SY1, SY1], color="white", lw=2.5)
ax.text(SX0 + EXT_W / 2, SY1 - 1.0, "south sliding doors", ha="center", fontsize=6.5, color=C["studio"])
ax.text(SX0 - 0.6, SY0 + 3.2, "window ▸", fontsize=5.5, color=C["studio"], ha="right", va="center")

# dimensions
dim(0, -6, REAR_SB, -6, "9'-10\"")
dim(SX0, -6, SX1, -6, "25'-9\" ext.  (24'-9\" net)")
dim(SX1, -6, hx, -6, f"≈ {hx - SX1:.0f} ft (sketch)")
dim(-3 + 0.0, 0, -3 + 0.0, NORTH_SB, "5'", off=(-2.2, 0))
dim(SX1 + 9, SY0, SX1 + 9, SY1, "15'-0\" ext.\n(14'-0\" net)", off=(5, 0))
dim(TRUNK[0] + 0.6, SY1, TRUNK[0] + 0.6, TRUNK[1] - TRUNK_D / 2, f"≈ {TRUNK[1] - SY1:.1f} ft", off=(4.2, 0), color=C["srz"])
dim(SX1 + RAMP, SY1 + TERR + 2.5, hx, SY1 + TERR + 2.5, f"≈ {hx - SX1 - RAMP:.0f} ft", color=C["dim"])
dim(px + pw + 1.5, py, px + pw + 1.5, py + ph, "18'", off=(1.8, 0), fs=7)

# north arrow and scale
ax.add_patch(FancyArrowPatch((120, 86), (120, 79), arrowstyle="-|>", mutation_scale=18, color="black"))
ax.text(120, 77.5, "N", ha="center", va="bottom", fontsize=12, fontweight="bold")
for i, x in enumerate(range(90, 110, 5)):
    ax.add_patch(Rectangle((x, 86), 5, 1.2, fc="black" if i % 2 == 0 else "white", ec="black", lw=0.6))
for x, t in ((90, "0"), (100, "10"), (110, "20 ft")):
    ax.text(x, 88.8, t, ha="center", fontsize=7)

# title and status notes
ax.text(-21, -19, "USG · instance_adu_backyard · SANDBOX SITE PLAN", fontsize=13, fontweight="bold")
ax.text(-21, -15.8, "Exploratory: exercise values and assumptions, not for construction.  Coordinates in ft from the west and north lot lines.",
        fontsize=8.5, color=C["note"])
notes = ("Open before commitment (ordinance / professional):\n"
         "• setback figures (Ord. 26-17) · ramp and parking inside rear setback\n"
         "• north eave within 5 ft of line (FBC-R R302.1) · heat + AC requirement\n"
         "• tree permit · arborist root mapping for earth-screw positions\n"
         "• survey: lot lines, house size/position (owner 46 ft / 8 ft vs sketch 51 / 12 ft)")
ax.text(-21, 79.5, notes, fontsize=7.5, color=C["note"], va="top",
        bbox=dict(fc="#fbfcfc", ec="#bbbbbb", pad=4))

plt.savefig("/home/claude/usg/drawings/sandbox_site_plan.png", bbox_inches="tight", facecolor="white")
plt.savefig("/home/claude/usg/drawings/sandbox_site_plan.svg", bbox_inches="tight", facecolor="white")
print("written")
