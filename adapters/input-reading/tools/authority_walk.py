"""Walk Input Reading authority_resolution over every valid field combination (first_match_wins).

Usage: python adapters/input-reading/tools/authority_walk.py adapters/input-reading/spec.json
Reports unreachable rules and combinations that fall to the invalid default (LOG-0014).
Proposal tooling: not in CI until the owner accepts Input Reading."""
import json, itertools, re, sys
J = json.load(open(sys.argv[1]))
F = J["evidence_record_model"]["fields"]
rules = J["evidence_record_model"]["authority_resolution"]["rules"]
dims = ["world_relation", "design_authority_relation", "provenance", "source_kind", "source_origin"]
dom = {d: F[d]["values"] for d in dims}

def clause(c, r):
    c = c.strip()
    m = re.fullmatch(r"(\w+)\s+in\s+\[(.*)\]", c)
    if m: return r[m[1]] in [x.strip() for x in m[2].split(",")]
    m = re.fullmatch(r"(\w+)=(\w+)", c)
    if m: return r[m[1]] == m[2]
    raise ValueError(c)
def match(rule, r): return all(clause(c, r) for c in rule["when"].split(" AND "))

hits = [0] * len(rules); gaps = []
for combo in itertools.product(*(dom[d] for d in dims)):
    r = dict(zip(dims, combo))
    # structural validity: design_authority_relation must be not_applicable unless proposed_design
    if (r["world_relation"] != "proposed_design") != (r["design_authority_relation"] == "not_applicable"):
        continue
    for i, rule in enumerate(rules):
        if match(rule, r): hits[i] += 1; break
    else:
        gaps.append(r)
for i, h in enumerate(hits):
    if h == 0: print(f"UNREACHABLE rule {i+1}: {rules[i]['when']}")
print(f"{len(gaps)} valid combinations match no rule")
from collections import Counter
key = Counter((g["world_relation"], g["design_authority_relation"], g["provenance"], g["source_kind"]) for g in gaps)
for k, n in sorted(key.items()):
    origins = sorted({g["source_origin"] for g in gaps if (g["world_relation"], g["design_authority_relation"], g["provenance"], g["source_kind"]) == k})
    print(" ", k, "origins:", "ALL" if len(origins) == len(dom["source_origin"]) else origins)
