"""Patch USG 0.11 -> 0.12. Loads the previous version and changes only what the changelog lists.

Usage: python3 patch_0_12.py USG_v0_11.json USG_v0_12.json
Theme: geometry becomes reproducible and exportable. Sources: Zara's geometry-guardrail comments (two rounds,
assessed 2026-10-12) and the ADU inquiry. 0.11 made constraints machine-readable; 0.12 makes them computable.
"""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
U = json.load(open(src))
assert U["document"]["version"] == "0.11", "patch applies to 0.11 only"


def stage(sid):
    return next(s for s in U["pipeline"] if s["id"] == sid)


def question(qid):
    return next(q for q in stage(qid.split(".")[0])["questions"] if q["id"] == qid)


CHANGELOG = [
    "Added schemas.coordinate_frame (origin, x/y/z axes, units, elevation datum, north) and geometry_model.frame_rule: every instance that holds geometry declares one frame, and the frame must be right-handed (a left-handed frame inverts exported normals and mirrors the model).",
    "Added geometry_model.authority: the geometric authority hierarchy (survey > approved site plan > professional drawing > owner statement > owner sketch) and site_envelope.controlling_geometry_ref. A source is replaced only by explicit revision, which reopens dependent work via FB9. AI-generated drawings are never geometric authority.",
    "site_envelope value records gained 'geometry' (point, polygon, circle, halfplane) in the declared frame, and 'rule' for protected zones (no_structure, no_footings, no_excavation). Added geometry_model.encoding_rule: a constraint shown in a drawing or document is evidence until encoded as a value record with geometry; only encoded constraints bind.",
    "Added schemas.buildable_envelope: derived = boundary minus setbacks, protected zones with rule no_structure, fixed existing elements and reserved areas. Its status is the weakest status among its inputs (confirmed > assumed > exercise > range). Range values enter at their worst case unless a hypothesis declares rests_on = favourable.",
    "Added invariant and geometry_model.immutability_rule: a candidate adapts to the site envelope; no generator alters the envelope or any authority geometry to accommodate a candidate. Envelope changes come only from the human or a new authority source, by revision.",
    "Added validation.export_checks: run automatically before any geometry export (STL, OBJ, IFC, ...): footprint inside the buildable envelope, no intersection with no_structure zones, no overlap with fixed existing elements, separations met, access connected, height within limit, no unresolved deviation from a recorded answer. A failed check forbids the export.",
    "Added export_model: every export is classified by subject (design_hypothesis or geometric_candidate) and class (concept or construction). A hypothesis export is always concept geometry and is never presented as a candidate. Construction geometry requires an accepted candidate (S19), project_status real and no open blocking review. Every export carries a sidecar manifest (schemas.export_manifest) and its status is printed in the file header where the format allows.",
    "Stress test deterministic_export; open questions.",
]

# ------------------------------------------------------------------ document, changelog, history
prev_log = U.pop("changelog_from_0_10")
U["history"] = {"0.11": {"changelog": prev_log, "removed": U["changelog_removed"]}, **U["history"]}
U["document"]["version"] = "0.12"
U["document"]["supersedes"] = "0.11"
new = {}
for k, v in U.items():
    new[k] = v
    if k == "document":
        new["changelog_from_0_11"] = CHANGELOG
U = new
U["changelog_removed"] = []
gm = U["geometry_model"]

# ------------------------------------------------------------------ 1 coordinate frame
U["schemas"]["coordinate_frame"] = {
    "origin": "named physical point (e.g. southwest lot corner)",
    "x_axis": "east | west | north | south",
    "y_axis": "east | west | north | south",
    "z_axis": "up | down",
    "units": "ft | m | mm",
    "elevation_datum": "named reference level (e.g. existing grade at the studio = 0)",
    "north": "direction of true or plan north in the frame"
}
gm["frame_rule"] = ("Every instance that holds geometry declares exactly one coordinate_frame. The frame must be "
                    "right-handed (x cross y = z). Units are converted only at export, never inside the model.")

# ------------------------------------------------------------------ 2 authority
gm["authority"] = {
    "hierarchy": ["survey", "approved_site_plan", "professional_drawing", "owner_statement", "owner_sketch"],
    "rule": ("The controlling geometry reference (site_envelope.controlling_geometry_ref) names the highest available "
             "source. A higher source replaces a lower one only by explicit revision, recorded with its date; the "
             "revision reopens dependent work via FB9. AI-generated drawings are never geometric authority."),
}
se = U["schemas"]["site_envelope"]
se["controlling_geometry_ref"] = "source id from geometry_model.authority.hierarchy"
se["value_record"] = "{value | min, max, unit, status, source_ref, geometry, rule}"

# ------------------------------------------------------------------ 3 encoding
se["geometry_types"] = {
    "point": "[x, y]",
    "polygon": "[[x, y], ...] (closed implicitly)",
    "circle": "{center: [x, y], radius}",
    "halfplane": "{normal: [nx, ny], offset}: allowed where normal . p >= offset"
}
se["protected_zone_rules"] = ["no_structure", "no_footings", "no_excavation"]
gm["encoding_rule"] = ("A constraint shown in a drawing, photo or document is evidence until it is encoded as a "
                       "site_envelope value record with geometry in the declared frame. Only encoded constraints bind "
                       "generators and validators.")

# ------------------------------------------------------------------ 4 buildable envelope
U["schemas"]["buildable_envelope"] = {
    "authority": "derived",
    "derivation": "boundary minus setbacks minus protected zones (rule no_structure) minus fixed existing elements minus reserved areas",
    "status_rule": "weakest input status: confirmed > assumed > exercise > range",
    "range_rule": "range values enter at their worst case unless a hypothesis declares rests_on = favourable",
    "output": "polygon(s) in the coordinate_frame, with the list of inputs used and their statuses"
}

# ------------------------------------------------------------------ 5 immutability
gm["immutability_rule"] = ("A candidate adapts to the site envelope. No generator alters the envelope, the buildable "
                           "envelope or any authority geometry to accommodate a candidate; envelope changes come only "
                           "from the human or a new authority source, by revision.")
U["invariants"].append("A candidate adapts to the site envelope; the generator never alters the envelope to fit a candidate.")
U["invariants"].append("A drawn constraint is evidence until encoded; only encoded constraints bind.")

# ------------------------------------------------------------------ 6 export checks and export model
U["validation"]["export_checks"] = [
    "footprint inside the buildable envelope",
    "no intersection with protected zones of rule no_structure",
    "no overlap with fixed existing elements",
    "required separations met",
    "access connected from an access point to every entry",
    "height within the height limit",
    "no unresolved deviation from a recorded answer"
]
U["export_model"] = {
    "subjects": ["design_hypothesis", "geometric_candidate"],
    "classes": ["concept", "construction"],
    "rules": [
        "export_checks run automatically before any geometry export; a failed check forbids the export",
        "a design_hypothesis export is always concept geometry and is never presented as a candidate",
        "construction geometry requires an accepted geometric_candidate (S19), project_status real and no open blocking review",
        "every export carries a sidecar manifest; where the format allows, the class and status are written into the file header"
    ]
}
U["schemas"]["export_manifest"] = {
    "protocol_version": "string",
    "instance": "instance id and version",
    "subject": "{type: design_hypothesis | geometric_candidate, id}",
    "class": "concept | construction",
    "project_status": "real | exploratory",
    "coordinate_frame": "coordinate_frame",
    "controlling_geometry_ref": "source id",
    "envelope_inputs": "list<{field, status, source_ref}>",
    "assumptions": "list<assumption id>",
    "unresolved": "list<item>",
    "checks": "list<{check, result: pass | fail | not_evaluable, detail}>",
    "reviews_required": "list<{item, review_class}>",
    "topology_validated": "boolean (false for any hypothesis export)",
    "statement": "e.g. 'Exploratory concept geometry. Not for construction.'"
}
question("S20.format")["q"] = "Which formats and level of detail are required, and in which export class (concept or construction)?"

# ------------------------------------------------------------------ tests, questions
U["domain_stress_tests"]["deterministic_export"] = ("From an encoded envelope and a selected hypothesis or candidate, "
                                                    "does USG compute the buildable envelope, run the export checks and "
                                                    "produce the same geometry and manifest every time?")
U["open_questions_for_review"] += [
    "Should export_checks be extended per library (door widths, clearances) or stay universal with library additions?",
    "Should a concept export of a hypothesis be allowed before S07, or only after capacity is confirmed?"
]

json.dump(U, open(dst, "w"), indent=2, ensure_ascii=False)
print(f"wrote {dst}: version {U['document']['version']}, {len(CHANGELOG)} changelog entries")
