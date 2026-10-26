"""USG instance runner: walks a program instance through the protocol pipeline and applies stage gates.

Usage:
  python3 run_usg.py USG_v0_6.json instances/fail_no_need.json [--out record.json] [--quiet]

What it does
  - Reads every gate definition it can from the protocol file (stage order, questions, authorities,
    required/when conditions, feasibility triggers and rules, evidence model, S02 mapping and gate, loops).
  - Recomputes every claim status from raw evidence (validator independence); recorded statuses are
    compared, never trusted. Applies the evidence precedence rule and the owner_statement cap (0.6).
  - Enforces authority per answer and the site rule; accepts library-gap answers to domain_library
    questions only when human-confirmed, and then keeps the project exploratory (0.6).
  - Stops at the first stop gate and reports stage, reason, loop and escalation.
  - Compares the outcome with the instance's `expected` block.

Exit codes: 0 = outcome as expected and instance valid; 1 = instance violations; 2 = outcome differs from expected.

Scope: S00-S02 gates are implemented in full. S03-S10 check required answers, authorities and library-gap
handling. S11 onward needs a domain library and a generator; the runner halts there with reason
'runner_limit' and never reports geometry as reached unless S13 has actually passed.
"""
import json, re, sys
from datetime import date

CONF_RANK = {"low": 0, "medium": 1, "high": 2}
LEVEL_RANK = {"light": 0, "standard": 1, "full": 2}
OPEN_STATUSES = {"pending_review", "unknown"}


class Run:
    def __init__(self, U, I):
        self.U, self.I = U, I
        self.stages = U["pipeline"]
        self.sidx = {s["id"]: i for i, s in enumerate(self.stages)}
        self.questions = {q["id"]: q for s in self.stages for q in s["questions"]}
        self.answers = I.get("answers", {})
        self.as_of = date.fromisoformat(I["instance"]["as_of"])
        self.trace, self.violations, self.notes, self.review_items = [], [], [], []
        self.stop = None
        self.ctx = {}
        self.project_status = I.get("project_status", "real")
        self.evidence = {e["id"]: e for e in I.get("evidence", [])}
        self.claims = {c["id"]: c for c in I.get("claims", [])}
        self.claim_status = {}
        self.screen_results = []
        self.library_gaps = []
        self.reaches_geometry = False

    # ------------------------------------------------------------ helpers
    def log(self, stage, msg):
        self.trace.append(f"{stage}  {msg}")

    def violate(self, where, msg):
        self.violations.append(f"{where}: {msg}")

    def halt(self, stage, reason, protocol_ref, loop=None, escalation=None, detail=""):
        self.stop = {"stage": stage, "reason": reason, "protocol_ref": protocol_ref,
                     "loop": loop, "escalation": escalation, "detail": detail}

    def make_exploratory(self, why):
        if self.project_status != "exploratory":
            self.project_status = "exploratory"
            self.notes.append(f"project_status -> exploratory: {why}")

    def interested(self, e):
        """0.9 reviewer_independence: review by a stakeholder whose interest the item decides."""
        if "reviewer_independence" not in self.U.get("professional_review_classes", {}):
            return False
        if e.get("interested"):
            return True
        drivers = self.answers.get("S00.drivers", {}).get("value", [])
        ids = {d.get("id") for d in drivers} if isinstance(drivers, list) else set()
        return e.get("reviewer") in ids

    def effective_conf(self, e):
        conf = e["confidence"]
        if e.get("kind") == "owner_statement" and CONF_RANK.get(conf, 0) > CONF_RANK["medium"]:
            conf = "medium"  # evidence_model: owner_statement never exceeds medium
        if self.interested(e) and CONF_RANK.get(conf, 0) > CONF_RANK["medium"]:
            conf = "medium"  # reviewer_independence: interested review never exceeds medium
        if e.get("valid_until") and date.fromisoformat(e["valid_until"]) < self.as_of:
            conf = "low"  # evidence_model.rules: expired evidence counts as low confidence
        return conf

    def compute_claim(self, cid):
        """evidence_model.claim_status_rule, with precedence_rule for professional confirmations (0.6)."""
        sup = [e for e in self.evidence.values() if cid in e.get("supports", [])]
        con = [e for e in self.evidence.values() if cid in e.get("contradicts", [])]
        prof = lambda e: e.get("kind") == "professional_confirmation" and not self.interested(e)
        why = {"high_supporting": [], "high_contradicting": [], "expired": [],
               "professional": [e["id"] for e in sup + con if prof(e)]}
        why["expired"] = [e["id"] for e in sup + con if e.get("valid_until")
                          and date.fromisoformat(e["valid_until"]) < self.as_of]
        if "precedence_rule" in self.U.get("evidence_model", {}) and why["professional"]:
            ps = any(prof(e) for e in sup)
            pc = any(prof(e) for e in con)
            return ("conflicting" if ps and pc else "confirmed_positive" if ps else "confirmed_negative"), why
        why["high_supporting"] = [e["id"] for e in sup if self.effective_conf(e) == "high"]
        why["high_contradicting"] = [e["id"] for e in con if self.effective_conf(e) == "high"]
        hs, hc = why["high_supporting"], why["high_contradicting"]
        st = "conflicting" if hs and hc else "confirmed_positive" if hs else "confirmed_negative" if hc else "insufficient"
        return st, why

    def eval_claims(self):
        valid_status = set(self.U["ontology"]["claim"]["status_values"])
        for eid, e in self.evidence.items():
            for k in self.U["ontology"]["evidence"]["required_fields"]:
                if k not in e:
                    self.violate(eid, f"evidence missing required field '{k}'")
            if e.get("kind") in self.U["ontology"]["evidence"].get("kind_forbidden", []):
                self.violate(eid, f"kind '{e.get('kind')}' is never evidence (speculation_rule); cite it as derived_from")
            if e.get("kind") == "owner_statement" and e.get("confidence") == "high" and \
                    "owner_statement" in self.U["ontology"]["evidence"].get("kind_reserved", {}):
                self.violate(eid, "owner_statement recorded as high confidence (capped at medium)")
            for cid in e.get("supports", []) + e.get("contradicts", []):
                if cid not in self.claims:
                    self.violate(eid, f"references undeclared claim {cid}")
        for cid, c in self.claims.items():
            st, why = self.compute_claim(cid)
            self.claim_status[cid] = st
            if c.get("status") not in valid_status:
                self.violate(cid, f"recorded status '{c.get('status')}' not in ontology.claim.status_values")
            elif c["status"] != st:
                self.violate(cid, f"recorded status '{c['status']}' but evidence gives '{st}'")
            extra = f", expired->low: {why['expired']}" if why["expired"] else ""
            extra += f", decided by professional confirmation {why['professional']}" if why["professional"] else ""
            self.notes.append(f"claim {cid}: {st} (high+ {why['high_supporting']}, high- {why['high_contradicting']}{extra})")

    def condition(self, text):
        m = re.search(r"(\w+)\s*(!=|==)\s*(\w+)", text)
        if not m or m.group(1) not in self.ctx:
            return None
        v = self.ctx[m.group(1)]
        return (v != m.group(3)) if m.group(2) == "!=" else (v == m.group(3))

    def own_use(self):
        return self.ctx.get("beneficiary") == "own_use"

    def is_required(self, q):
        if "when" in q:
            applies = self.condition(q["when"])
            if applies is None:
                self.notes.append(f"{q['id']}: 'when' condition not machine-evaluable: {q['when']}")
                return True
            if not applies:
                return False
        if q.get("rule") == "feasibility_module.intensity.own_use_rule" and self.own_use():
            return False  # own_use_rule: the stated need is the demand evidence
        r = q["required"]
        if isinstance(r, bool):
            return r
        if "standard and full" in r:  # 0.5.1 wording
            return self.ctx.get("intensity") in ("standard", "full")
        c = self.condition(r)
        if c is None:
            self.notes.append(f"{q['id']}: 'required' condition not machine-evaluable: {r}")
            return True
        return c

    def check_answers(self, stage):
        """Presence, authority, confirmation and library-gap handling for one stage. Returns missing required ids."""
        missing = []
        for q in stage["questions"]:
            a = self.answers.get(q["id"])
            req = self.is_required(q)
            if a is None:
                if req:
                    missing.append(q["id"])
                continue
            if a.get("status") == "unknown":
                blocks = a.get("blocks_stage")
                if blocks is None or self.sidx.get(blocks, 0) <= self.sidx[stage["id"]]:
                    if req:
                        missing.append(q["id"])
                else:
                    self.notes.append(f"{q['id']}: explicit unknown, blocks {blocks}")
                continue
            if "when" in q and self.condition(q["when"]) is False:
                self.violate(q["id"], f"answered although not applicable ({q['when']})")
            auth = a.get("authority")
            default_ok = ("default" in q and auth == "domain_library" and a.get("source_ref") == q["default"])
            gap_ok = (q["authority"] == "domain_library" and a.get("library_gap") and auth == "ai_generated")
            if gap_ok:
                if a.get("confirmed_by", {}).get("authority") != "human":
                    self.violate(q["id"], "library-gap value not confirmed by the human")
                scope = a.get("scope", "instance_only")
                self.library_gaps.append((q["id"], scope))
                self.make_exploratory(f"library-gap assumption at {q['id']}")
            elif auth != q["authority"] and not default_ok and auth not in q.get("also_answerable_by", []):
                self.violate(q["id"], f"answered by '{auth}', protocol authority is '{q['authority']}'")
            if "values" in q and a.get("value") not in q["values"]:
                self.violate(q["id"], f"value '{a.get('value')}' not in {q['values']}")
            if "confirmation" in q and q["id"] != "S02.site_candidates":
                if a.get("confirmed_by", {}).get("authority") != q["confirmation"]:
                    self.review_items.append(f"{q['id']}: confirmation by {q['confirmation']} open")
            if q["authority"] == "human" and a.get("status") == "default_by_silence" and \
                    "no_default_by_silence" in self.U.get("inquiry_model", {}):
                self.violate(q["id"], "human-authority value set by silence (inquiry_model.no_default_by_silence)")
            if a.get("status") == "pending_review":
                self.review_items.append(f"{q['id']}: {q['authority']} pending ({q.get('review_class', 'unclassified')})")
            if "review_class" in q and a.get("review_class") not in (None, q["review_class"]):
                self.violate(q["id"], f"review_class '{a.get('review_class')}' differs from protocol '{q['review_class']}'")
        return missing

    # ------------------------------------------------------------ stage gates
    def gate_S00(self, s):
        if "S00.lifecycle_use" in self.answers:
            phases = self.answers["S00.lifecycle_use"].get("value", [])
            bvals = set(self.U["ontology"].get("lifecycle_phase", {}).get("beneficiary_values", []))
            for p in phases:
                for k in self.U["ontology"].get("lifecycle_phase", {}).get("required_fields", []):
                    if k not in p:
                        self.violate("S00.lifecycle_use", f"phase {p.get('id')} missing '{k}'")
                if bvals and p.get("beneficiary") not in bvals:
                    self.violate("S00.lifecycle_use", f"phase {p.get('id')}: beneficiary '{p.get('beneficiary')}' invalid")
            if phases:
                self.ctx["beneficiary"] = phases[0].get("beneficiary")
        missing = self.check_answers(s)
        if missing:
            return self.halt("S00", "required_answer_missing", "pipeline.S00.gate", detail=", ".join(missing))
        self.check_never()
        self.ctx["site_mode"] = self.answers["S00.site_mode"]["value"]
        lib = self.answers["S00.library"]["value"]
        if lib.get("status") == "draft":
            self.make_exploratory(f"library {lib['id']} {lib['version']} is a draft")
        self.log("S00", f"pass  site_mode={self.ctx['site_mode']}, library={lib['id']} {lib['version']}, "
                        f"beneficiary(phase 1)={self.ctx.get('beneficiary')}")

    def check_never(self):
        """0.7: every S00.never statement is classified; vacuous/unevaluable ones need the human's decision."""
        spec = self.questions["S00.never"].get("classification")
        a = self.answers.get("S00.never")
        if not spec or not a:
            return
        for st in a.get("value", []):
            if not isinstance(st, dict):
                self.violate("S00.never", f"unclassified statement '{st}'")
                continue
            c = st.get("class")
            if c not in spec["classes"]:
                self.violate("S00.never", f"'{st.get('statement')}': invalid class '{c}'")
            elif c in ("vacuous", "unevaluable") and not st.get("kept_by_human"):
                self.violate("S00.never", f"'{st.get('statement')}' is {c} and was not returned to the human")
            elif c == "use_restriction":
                self.notes.append(f"S00.never '{st.get('statement')}': use restriction, checked against lifecycle phases")
            elif c == "design_rule" and "evaluable_stage" in spec:
                es = st.get("evaluable_stage")
                if es not in self.sidx:
                    self.violate("S00.never", f"'{st.get('statement')}': design_rule without a valid evaluable_stage")

    def check_delivery(self):
        """0.7: bootstrap-cycle check (conflict_detection.bootstrap_rule). Returns True if the run must halt."""
        if "S01.delivery" not in self.questions:
            return False
        routes = self.answers.get("S01.delivery", {}).get("value", [])
        spec = self.U["ontology"]["delivery_route"]
        reserved = set(spec["reserved_dependencies"])
        independent, dependent = [], []
        for r in routes:
            for k in spec["required_fields"]:
                if k not in r:
                    self.violate("S01.delivery", f"route {r.get('id')} missing '{k}'")
            (dependent if reserved & set(r.get("depends_on", [])) else independent).append(r.get("id"))
        if routes and not independent:
            self.halt("S01", "bootstrap_conflict", "conflict_detection.bootstrap_rule", escalation="human",
                      detail=f"every delivery route depends on the intervention or its excluded success event: {dependent}")
            return True
        if dependent:
            self.notes.append(f"S01.delivery: routes {dependent} are self-dependent; independent routes {independent} carry the run")
        return False

    def check_log(self):
        """0.7: inquiry_log granularity, one question id asked per step."""
        if "log" not in self.U.get("inquiry_model", {}):
            return
        for st in self.I.get("inquiry_log", []):
            asked = st.get("asked")
            if not isinstance(asked, str):
                self.violate("inquiry_log", f"step {st.get('step')} asks {asked!r}; exactly one question id per step")
            elif asked not in self.questions:
                self.violate("inquiry_log", f"step {st.get('step')} asks unknown question {asked}")
            for qid in st.get("routed", []):
                if qid not in self.questions:
                    self.violate("inquiry_log", f"step {st.get('step')} routes to unknown question {qid}")

    def capabilities(self):
        return {c.get("id"): c for c in self.I.get("program", {}).get("enabled_by", [])}

    def premise_ok(self, pid):
        """Simple premise check usable before the design layer (claims, assumptions, capabilities, questions)."""
        if pid in self.claims:
            return self.claim_status.get(pid) == "confirmed_positive"
        a = next((x for x in self.I.get("assumptions", []) if x.get("id") == pid), None)
        if a is not None:
            return a.get("status") == "confirmed"
        caps = self.capabilities()
        if pid in caps:
            return caps[pid].get("status") == "demonstrated"
        ans = self.answers.get(pid)
        return bool(ans) and ans.get("status") not in OPEN_STATUSES

    def check_program_and_closure(self):
        """0.10: program capabilities, means statements, by-product sinks, derived closure level."""
        self.closure_level = None
        pm = self.U.get("program_model")
        if pm:
            for c in self.capabilities().values():
                for k in pm["capability_fields"]:
                    if k not in c:
                        self.violate(c.get("id", "?"), f"capability missing '{k}'")
                if c.get("status") not in pm["capability_status_values"]:
                    self.violate(c.get("id", "?"), f"invalid capability status '{c.get('status')}'")
        smod = self.U.get("statement_model", {})
        if "concerns_values" in smod:
            for s in self.I.get("statements", []):
                con = s.get("concerns", "outcome")
                if con not in smod["concerns_values"]:
                    self.violate(s.get("id", "?"), f"invalid concerns '{con}'")
                if con == "means" and s.get("statement_type") in ("requirement", "constraint") \
                        and s.get("declared_by") != "human":
                    self.violate(s.get("id", "?"), "a means is typed preference unless the human declares it a requirement (means_separation)")
        if "byproduct_rule" in self.U["conflict_detection"]:
            for f in self.I.get("flows", []):
                if f.get("byproduct") and not f.get("sink"):
                    self.violate(f.get("id", "?"), "by-product flow without a declared sink (byproduct_rule)")
        cm = self.U.get("closure_model")
        crit = [r for r in self.answers.get("S01.delivery", {}).get("value", []) if r.get("critical")]
        if cm and crit:
            target = self.I.get("autonomy_target_days")
            def level(r):
                b = r.get("supply_basis")
                if b == "locally_reproducible":
                    return 3
                if b == "locally_produced":
                    return 2
                if b == "stocked" and r.get("stock_duration_days") is not None and \
                        (target is None or r["stock_duration_days"] >= target):
                    return 1
                return 0
            self.closure_level = cm["order"][min(level(r) for r in crit)]

    def check_jurisdiction(self):
        """0.7: absence of regulation is a claim that needs evidence (evidence_model.regulatory_absence_rule)."""
        jo = self.I.get("jurisdiction_overlay")
        if not jo or "regulatory_absence_rule" not in self.U.get("evidence_model", {}):
            return
        if jo.get("basis") == "none":
            cid = jo.get("claim")
            if not cid or self.claim_status.get(cid) != "confirmed_positive":
                self.violate("jurisdiction_overlay", "absence of regulation asserted without an evidenced claim")

    def intensity_floor(self):
        inten = self.U["feasibility_module"]["intensity"]
        trig = inten["triggers"]
        if "S00.triggers" in self.answers:
            given = self.answers["S00.triggers"]["value"]
        else:
            given = self.I.get("feasibility_triggers", {})
        floor, hits = "light", []
        for t in trig:
            if t["condition"] == "none of the above":
                continue
            f = given.get(t["condition"])
            if f is None:
                self.violate("S00.triggers", f"no value for universal trigger '{t['condition']}'")
                continue
            if f.get("authority") not in self.U["answer_authority"]["authorities"]:
                self.violate("S00.triggers", f"'{t['condition']}' has no valid authority")
            v = f.get("value")
            if v is None:
                why = f"classification {f['classification']}" if f.get("classification") else "fact unknown"
                self.notes.append(f"trigger '{t['condition']}' unknown ({why}) -> applied conservatively")
            if v is False and f.get("assumption"):
                if "library threshold" not in t["condition"]:
                    self.violate("S00.triggers", f"'{t['condition']}': only library-dependent triggers may be asserted false as an assumption")
                else:
                    self.notes.append(f"trigger '{t['condition']}' asserted false by the human as an assumption")
            if v or v is None:
                hits.append(t["condition"])
                if LEVEL_RANK[t["minimum"]] > LEVEL_RANK[floor]:
                    floor = t["minimum"]
        return floor, hits

    def gate_S01(self, s):
        rec = self.I.get("strategic_feasibility_record")
        if rec is None:
            return self.halt("S01", "no_feasibility_record", "feasibility_module.required_input")
        floor, hits = self.intensity_floor()
        level = rec.get("intensity")
        if level not in LEVEL_RANK:
            self.violate("S01.intensity", f"invalid level '{level}'")
            level = floor
        elif LEVEL_RANK[level] < LEVEL_RANK[floor]:
            self.violate("S01.intensity", f"'{level}' is below the derived floor '{floor}' (triggers: {hits})")
        self.ctx["intensity"] = level
        if self.answers.get("S01.intensity", {}).get("value") != level:
            self.violate("S01.intensity", f"answer differs from record '{level}'")
        self.log("S01", f"intensity floor={floor} from {hits or ['none of the above']}; record={level}"
                        + ("; own_use_rule applies" if self.own_use() else ""))

        missing = self.check_answers(s)
        if missing:
            return self.halt("S01", "required_answer_missing", "pipeline.S01.gate", detail=", ".join(missing))
        if self.check_delivery():
            return

        sch = self.U["schemas"]["strategic_feasibility_record"]
        for k, spec in sch.items():
            if k not in rec and "required when" not in str(spec):  # conditional fields are checked by their own rule
                self.violate("strategic_feasibility_record", f"missing field '{k}'")
        if not rec.get("need_statement"):
            self.violate("S01", "need not stated")
        alts = rec.get("alternatives", [])
        opts = set(self.U["ontology"]["intervention_alternative"]["option_values"])
        for al in alts + rec.get("excluded_alternatives", []):
            if al.get("option") not in opts:
                self.violate("S01.alternatives", f"{al.get('id', al.get('option'))}: unknown option {al.get('option')}")
        for ex in rec.get("excluded_alternatives", []):
            if not ex.get("reason") or not ex.get("excluded_by"):
                self.violate("S01.alternatives", f"excluded {ex.get('option')} without reason and authority")
        considered = {a.get("option") for a in alts} | {a.get("option") for a in rec.get("excluded_alternatives", [])}
        if not considered - {"new_build"}:
            self.violate("S01.alternatives", "no non-build alternative considered (alternatives_to_build.required_test)")
        # 0.10: option rules and generation duty
        rules = self.U["ontology"]["intervention_alternative"].get("option_rules", {})
        for al in alts:
            if al.get("option") == "staged_precursor" and "staged_precursor" in rules and not al.get("enables"):
                self.violate("S01.alternatives", f"{al.get('id')}: staged_precursor must name what it enables")
            if al.get("option") == "defer_commitment" and "defer_commitment" in rules and not al.get("revisit_trigger"):
                self.violate("S01.alternatives", f"{al.get('id')}: defer_commitment must name a revisit_trigger")
        gd = self.U["alternatives_to_build"].get("generation_duty")
        if gd:
            trig = self.answers.get("S00.triggers", {}).get("value", {})
            novelty = next((v for k, v in trig.items() if k.startswith("novelty")), {}).get("value") is True
            unresolved = [p for rt in self.answers.get("S01.delivery", {}).get("value", [])
                          for p in rt.get("premises", []) if not self.premise_ok(p)]
            if (novelty or unresolved) and not considered & set(gd["strategy_level_options"]):
                why = "novelty is true" if novelty else f"delivery premises {unresolved} are unresolved"
                self.violate("S01.alternatives", f"no strategy-level alternative considered although {why} (generation_duty)")
        if LEVEL_RANK[level] >= 1:
            fields = ["existing_supply"] + ([] if self.own_use() else ["demand_evidence"])
            for fld in fields:
                refs = rec.get(fld, [])
                if not refs:
                    self.violate("S01", f"{level} depth requires {fld}")
                ok = [r for r in refs if r in self.evidence and CONF_RANK[self.effective_conf(self.evidence[r])] >= 1]
                for r in refs:
                    if r not in self.evidence:
                        self.violate("S01", f"{fld} references unknown evidence {r}")
                    elif r not in ok:
                        self.notes.append(f"S01: {fld} item {r} is below medium confidence (does not count toward depth)")
                if refs and not ok:
                    self.violate("S01", f"{fld}: no item at medium confidence or better")
        if LEVEL_RANK[level] >= 2:
            gaps = rec.get("identified_gap", [])
            if not gaps or not all(isinstance(g.get("quantity"), (int, float)) for g in gaps):
                self.violate("S01", "full depth requires a quantified gap (numeric quantity, zero allowed)")
            if not rec.get("value_case"):
                self.violate("S01", "full depth requires a value case")
            dims = self.U["alternatives_to_build"]["comparison"]["dimensions"]
            adr = rec.get("alternatives_decision_record", {})
            for al in alts:
                row = adr.get(al["id"])
                if row is None:
                    self.violate("alternatives_decision_record", f"no row for {al['id']}")
                    continue
                miss = [d for d in dims if d not in row]
                if miss:
                    self.violate("alternatives_decision_record", f"{al['id']} omits {miss} (mark unknown, never omit)")
            if adr.get("winner") or adr.get("recommended"):
                self.violate("alternatives_decision_record", "contains an automatic winner (comparison.form forbids it)")
        if "novelty_rule" in self.U["feasibility_module"]["intensity"]:
            trig = self.answers.get("S00.triggers", {}).get("value", {})
            nov = next((v for k, v in trig.items() if k.startswith("novelty")), {})
            if nov.get("value") is True:
                prec = [r for r in rec.get("failure_precedents", [])
                        if self.evidence.get(r, {}).get("kind") == "failure_precedent"]
                if not prec:
                    self.violate("S01", "novelty is true but the record has no failure precedents (novelty_rule)")

        decision = rec.get("decision")
        if self.answers["S01.decision"].get("value") != decision:
            self.violate("S01.decision", f"answer '{self.answers['S01.decision'].get('value')}' differs from record '{decision}'")
        need_claims = [c for c in self.claims.values() if c.get("gate") == "S01"]
        neg = [c["id"] for c in need_claims if self.claim_status.get(c["id"]) == "confirmed_negative"]
        if need_claims:
            self.log("S01", "claims: " + ", ".join(f"{c['id']}={self.claim_status[c['id']]}" for c in need_claims))
        if decision == "stop":
            return self.halt("S01", "strategic_fail", "early_stop_logic.strategic_fail",
                             detail=f"human decision 'stop'; negative claims {neg}")
        if decision == "exploratory":
            self.make_exploratory("S01.decision = exploratory")
        elif decision == "proceed" and neg:
            if "decision_rules" in s:
                self.make_exploratory(f"proceed against confirmed_negative {neg} (S01.decision_rules)")
            else:
                self.notes.append(f"S01: proceed as real although {neg} are confirmed_negative (protocol silent)")
        elif decision != "proceed":
            self.violate("S01.decision", f"invalid decision '{decision}'")
        self.log("S01", f"pass  decision={decision}, project_status={self.project_status}")

    def gate_S02(self, s):
        missing = self.check_answers(s)
        if missing:
            return self.halt("S02", "required_answer_missing", "pipeline.S02.gate", detail=", ".join(missing))
        cats = s["categories"]
        prec = s.get("overall_precedence", ["prohibited", "unresolved", "conditional", "permitted"])
        mode = self.ctx["site_mode"]
        confirmed = []
        for c in self.I.get("site_candidates", []):
            for k in self.U["ontology"]["site_candidate"]["required_fields"]:
                if k not in c:
                    self.violate(c.get("id", "?"), f"site_candidate missing '{k}'")
            if mode == "given":
                if c.get("proposed_by", "human") != "human":
                    self.violate(c["id"], "site_mode=given but the site was not supplied by the human")
                confirmed.append(c)
                continue
            cb = c.get("confirmed_by", {})
            if c.get("proposed_by") == "ai_generated" and not c.get("within_search_criteria"):
                self.violate(c["id"], "AI-proposed site not declared within S02.search_criteria (answer_authority.site_rule)")
            if cb.get("authority") == "human" and cb.get("decision") == "confirmed":
                confirmed.append(c)
            else:
                self.log("S02", f"{c['id']}: not human-confirmed ({cb.get('decision', 'pending')}); excluded from screen")
        if mode == "given" and len(confirmed) != 1:
            self.violate("S02", f"site_mode=given requires exactly one site, found {len(confirmed)}")

        records = {r["site_ref"]: r for r in self.I.get("screen_records", [])}
        for r in records:
            if r not in {c["id"] for c in confirmed}:
                self.violate("S02", f"screen record for {r}, which is not a confirmed candidate")
        survivors = []
        for c in confirmed:
            rec = records.get(c["id"])
            if rec is None:
                self.violate("S02", f"no constraint_screen_record for confirmed candidate {c['id']}")
                continue
            per_cat = {}
            for cat in cats:
                entry = rec.get("categories", {}).get(cat)
                if entry is None:
                    self.violate(c["id"], f"category '{cat}' missing (must have evidence or be marked insufficient)")
                    per_cat[cat] = "unresolved"
                    continue
                for cid in entry.get("claims", []):
                    if cid not in self.claims:
                        self.violate(c["id"], f"{cat}: undeclared claim {cid}")
                sts = [self.claim_status.get(cid, "insufficient") for cid in entry.get("claims", [])]
                if not sts or any(x in ("conflicting", "insufficient") for x in sts) and "confirmed_negative" not in sts:
                    computed = "unresolved"
                elif "confirmed_negative" in sts:
                    computed = "prohibited"
                else:
                    computed = "conditional" if entry.get("conditions") else "permitted"
                per_cat[cat] = computed
                if entry.get("status") != computed:
                    self.violate(c["id"], f"{cat}: recorded '{entry.get('status')}' but claims give '{computed}'")
                if "conflicting" in sts:
                    self.notes.append(f"S02 {c['id']}/{cat}: conflicting evidence shown side by side, not averaged")
            overall = next(p for p in prec if p in per_cat.values()) if per_cat else "unresolved"
            scenario = rec.get("human_requested_scenario")
            if overall == "prohibited" and scenario and scenario.get("authority") == "human":
                if "scenario_rule" in s:
                    overall = "under_scenario"
                self.review_items.append(f"{c['id']}: {scenario['kind']} scenario (blocking)")
            if rec.get("overall_status") != overall:
                self.violate(c["id"], f"overall_status '{rec.get('overall_status')}' but categories give '{overall}'")
            if not any(p.get("review_class") == "blocking" for p in rec.get("professional_review_items", [])):
                self.violate(c["id"], "S02.status is a blocking professional-review item; none recorded")
            if overall == "prohibited":
                fate = "dropped (gate.any_prohibited)"
            elif overall in ("unresolved", "under_scenario"):
                if self.project_status == "exploratory":
                    fate = f"continues, exploratory ({overall})"
                    survivors.append((c["id"], overall))
                else:
                    fate = f"blocked from geometry ({overall})"
                    survivors.append((c["id"], "blocked"))
            else:
                fate = "continues"
                survivors.append((c["id"], overall))
            self.screen_results.append({"site_ref": c["id"], "categories": per_cat, "overall_status": overall, "fate": fate})
            self.log("S02", f"{c['id']}: " + ", ".join(f"{k}={v}" for k, v in per_cat.items()) + f" -> {overall}; {fate}")

        if not survivors:
            loop = next(l for l in self.U["controlled_feedback_loops"]["loops"] if l["from"] == "S02" and l["to"] == "S00")
            return self.halt("S02", "no_candidate_survives", "pipeline.S02.gate.no_candidate_survives / "
                             "early_stop_logic.screen_prohibited_all_sites", loop=loop["id"],
                             escalation=loop.get("escalation"),
                             detail=f"{len(confirmed)} confirmed candidates screened, all dropped")
        self.ctx["survivors"] = survivors
        self.log("S02", f"pass  survivors: {survivors}")

    def gate_generic(self, s):
        missing = self.check_answers(s)
        if missing:
            return self.halt(s["id"], "required_answer_missing", f"pipeline.{s['id']}.gate", detail=", ".join(missing))
        self.log(s["id"], "pass  required answers present (gate content not evaluated by runner)")

    def check_library_candidates(self):
        spec = self.U["ontology"].get("library_candidate")
        cands = self.I.get("library_candidates", [])
        if cands and not spec:
            self.violate("library_candidates", "protocol has no library_candidate class")
            return
        for c in cands:
            for k in spec["required_fields"]:
                if k not in c:
                    self.violate(c.get("id", "?"), f"library_candidate missing '{k}'")
            if "domain" not in c.get("scope", {}):
                self.violate(c.get("id", "?"), "library_candidate scope has no domain")
            if c.get("source_instance") != self.I["instance"]["id"]:
                self.violate(c.get("id", "?"), "library_candidate source_instance is not this instance")
            if c.get("basis") not in spec.get("basis_values", []):
                self.violate(c.get("id", "?"), f"invalid basis '{c.get('basis')}'")
            if c.get("status") != "proposed":
                self.violate(c.get("id", "?"), "an instance may only propose candidates; acceptance is library curation")

    # ------------------------------------------------------------ run
    def run(self):
        inst = self.I["instance"]
        if inst.get("protocol_version") != self.U["document"]["version"]:
            self.violate("instance", f"pinned to protocol {inst.get('protocol_version')}, file is {self.U['document']['version']}")
        for k in self.answers:
            if k not in self.questions:
                self.violate(k, "answer for unknown question id")
        self.eval_claims()
        self.check_library_candidates()
        self.check_log()
        self.check_jurisdiction()
        self.check_program_and_closure()
        handlers = {"S00": self.gate_S00, "S01": self.gate_S01, "S02": self.gate_S02}
        for s in self.stages:
            if self.stop:
                break
            if s["id"] == "S14":
                sv = self.ctx.get("survivors", [])
                if sv and all(st == "blocked" for _, st in sv):
                    self.halt("S14", "all_sites_blocked_from_geometry", "pipeline.S02.gate.any_unresolved")
                    break
            if self.sidx[s["id"]] >= self.sidx["S11"]:
                self.halt(s["id"], "runner_limit", "run_usg.py scope",
                          detail="semantic model assembly needs a domain library and generator")
                break
            handlers.get(s["id"], self.gate_generic)(s)
        self.reaches_geometry = self.stop is None or self.sidx[self.stop["stage"]] > self.sidx["S14"]
        self.design_layer()
        return self

    # ------------------------------------------------------------ 0.8 design layer (views over the same state)
    def design_layer(self):
        self.awareness, self.strain, self.commit_results = [], {}, []
        pm = self.U.get("phase_model")
        if not pm:
            return
        O = self.U["ontology"]
        phases = pm["phases"]
        cur = self.I.get("current_phase", "concept")
        if cur not in phases:
            self.violate("current_phase", f"unknown phase '{cur}'")
            cur = "concept"
        self.current_phase = cur
        hyps = {h.get("id"): h for h in self.I.get("design_hypotheses", [])}
        odvs = {o.get("id"): o for o in self.I.get("open_design_variables", [])}
        asys = {a.get("id"): a for a in self.I.get("affected_systems", [])}
        assm = {a.get("id"): a for a in self.I.get("assumptions", [])}
        strain = {k: [] for k in self.U["schemas"]["strain_report"] if k != "note"}

        def need(rec, cls, where):
            for k in O[cls]["required_fields"]:
                if k not in rec:
                    self.violate(where, f"{cls} missing '{k}'")

        # --- record validation
        for h in hyps.values():
            need(h, "design_hypothesis", h.get("id", "?"))
            if h.get("status") not in O["design_hypothesis"]["status_values"]:
                self.violate(h.get("id", "?"), f"invalid status '{h.get('status')}'")
            if h.get("phase") not in phases:
                self.violate(h.get("id", "?"), f"invalid phase '{h.get('phase')}'")
        for o in odvs.values():
            need(o, "open_design_variable", o.get("id", "?"))
            if o.get("decide_by") not in phases:
                self.violate(o.get("id", "?"), f"decide_by '{o.get('decide_by')}' is not a phase")
            if o.get("owner") != "human":
                self.violate(o.get("id", "?"), "an open design variable is owned by the human")
        kinds = set(O["affected_system"]["kind_values"])
        for a in asys.values():
            need(a, "affected_system", a.get("id", "?"))
            if a.get("kind") not in kinds:
                self.violate(a.get("id", "?"), f"invalid kind '{a.get('kind')}'")
            nobase = not a.get("baseline", {}).get("evidence_refs")
            if nobase and a.get("change", {}).get("magnitude") not in (None, "unresolved"):
                self.violate(a.get("id", "?"), "impact claim without baseline (no baseline, no impact claim)")
            for ch in a.get("change_by_scenario", []):
                if nobase and ch.get("magnitude") not in (None, "unresolved"):
                    self.violate(a.get("id", "?"), f"impact claim without baseline in scenario {ch.get('scenario')}")
        for v in self.I.get("value_ledger", []):
            need(v, "value_perspective", v.get("id", "?"))
            for k in ("score", "net", "total", "rank"):
                if k in v:
                    self.violate(v.get("id", "?"), f"value perspective carries an aggregate '{k}' (value_rule)")
        smod = self.U["statement_model"]
        for s in self.I.get("statements", []):
            if s.get("statement_type") not in smod["statement_types"]:
                self.violate(s.get("id", "?"), f"invalid statement_type '{s.get('statement_type')}'")
            if s.get("basis") not in smod["basis_values"]:
                self.violate(s.get("id", "?"), f"invalid basis '{s.get('basis')}'")
            if s.get("statement_type") == "constraint" and s.get("relaxable_by"):
                self.violate(s.get("id", "?"), f"typed constraint but relaxable by {s['relaxable_by']} (statement_model.rule)")
        for p in self.I.get("pressures", []):
            strain["pressure_vs_constraint"].append({"statement": p.get("statement"), "stakeholder": p.get("stakeholder")})
        for d in self.answers.get("S00.drivers", {}).get("value", []) if isinstance(self.answers.get("S00.drivers", {}).get("value"), list) else []:
            if d.get("interests_source") == "ai_generated":
                self.violate("S00.drivers", f"{d.get('id')}: interests imputed by the AI (driver_rule: asked, never imputed)")

        # --- premise resolution
        held = {cid for rec in self.I.get("screen_records", [])
                if rec.get("human_requested_scenario", {}).get("authority") == "human"
                for cat in rec.get("categories", {}).values() for cid in cat.get("claims", [])}

        def resolve(pid):
            if pid in self.claims:
                st = self.claim_status.get(pid)
                if st == "confirmed_negative" and pid in held:
                    return "unresolved"  # held under a human-requested scenario (commitment_rule.negative)
                return {"confirmed_positive": "ok", "confirmed_negative": "negative",
                        "conflicting": "conflicting"}.get(st, "unresolved")
            if pid in asys:
                b = asys[pid].get("baseline", {})
                return "ok" if b.get("evidence_refs") and CONF_RANK.get(b.get("confidence"), 0) >= 1 else "unresolved"
            if pid in assm:
                return "ok" if assm[pid].get("status") == "confirmed" else "unresolved"
            if pid in odvs:
                return "ok"  # protected, not missing
            if pid in self.capabilities():
                return "ok" if self.capabilities()[pid].get("status") == "demonstrated" else \
                    ("negative" if self.capabilities()[pid].get("status") == "failed" else "unresolved")
            if pid in self.questions:
                a = self.answers.get(pid)
                return "ok" if a and a.get("status") not in OPEN_STATUSES else "unresolved"
            self.violate("design_hypotheses", f"premise '{pid}' is not a declared claim, question, assumption, affected system or ODV")
            return "unresolved"

        SEV = {"negative": 3, "conflicting": 3, "unresolved": 2}
        items = {}
        for h in hyps.values():
            if h.get("status") == "retired":
                continue
            for pid in h.get("presupposes", []):
                r = resolve(pid)
                if r == "ok":
                    continue
                it = items.setdefault(pid, {"item": pid, "state": r, "dependents": []})
                it["dependents"].append(h["id"])
                if r == "negative":
                    strain["hypothesis_on_negative_claim"].append({"hypothesis": h["id"], "premise": pid})
            for oid, val in h.get("fixes", {}).items():
                o = odvs.get(oid)
                if o and h.get("status") == "committed" and o.get("status") == "open" and \
                        phases.index(o["decide_by"]) > phases.index(cur):
                    strain["odv_collapsed"].append({"odv": oid, "hypothesis": h["id"]})
                    self.violate(h["id"], f"commits {oid} = {val!r} before its decide_by phase '{o['decide_by']}'")
        # 0.9: delivery route premises (show-stoppers) and late-evaluable never rules (deferred risk)
        delivery_premises = []
        if "premises" in O.get("delivery_route", {}).get("optional_fields", []):
            for rt in self.answers.get("S01.delivery", {}).get("value", []):
                if set(rt.get("depends_on", [])) & set(O["delivery_route"]["reserved_dependencies"]):
                    continue
                for pid in rt.get("premises", []):
                    r = resolve(pid)
                    if r != "ok":
                        delivery_premises.append(pid)
                        it = items.setdefault(pid, {"item": pid, "state": r, "dependents": []})
                        it["dependents"].append(f"route {rt.get('id')}")
        show = set(delivery_premises) | {c for c, v in self.claims.items() if v.get("gate") in ("S01", "S02")}
        for it in items.values():
            it["score"] = len(it["dependents"]) * SEV[it["state"]]
            it["show_stopper"] = it["item"] in show and "show-stopper" in self.U["awareness_model"]["ranking"].lower()
        cur_last = max(self.sidx[s] for p in phases[:phases.index(cur) + 1] for s in self.U["phase_model"]["stages"][p])
        nv = self.answers.get("S00.never", {}).get("value", [])
        for stt in nv if isinstance(nv, list) else []:
            if isinstance(stt, dict) and stt.get("class") == "design_rule" and stt.get("evaluable_stage") in self.sidx \
                    and self.sidx[stt["evaluable_stage"]] > cur_last:
                key = f"S00.never: {stt.get('statement')}"
                items[key] = {"item": key, "state": f"deferred_risk (evaluable at {stt['evaluable_stage']})",
                              "dependents": [], "score": 2, "show_stopper": False}
        # 0.11: sandbox and consistency rules for geometric hypotheses
        em = self.U.get("execution_model", {})
        if "sandbox_rule" in em:
            se = self.U["schemas"]["site_envelope"]
            statuses = set(se["status_values"])
            levels = set(O["design_hypothesis"]["level_values"])
            geo = [h for h in hyps.values() if h.get("status") != "retired" and h.get("level") == "geometric"]
            for h in hyps.values():
                if "level" in h and h["level"] not in levels:
                    self.violate(h.get("id", "?"), f"invalid level '{h['level']}'")
            env = self.I.get("site_envelope")
            undefined = []
            if env is not None:
                for f in se["fields"]:
                    val = env.get(f)
                    recs = val if isinstance(val, list) else [val]
                    if val is None or val == []:
                        undefined.append(f)
                        continue
                    for rec in recs:
                        st = rec.get("status") if isinstance(rec, dict) else None
                        if st not in statuses:
                            self.violate("site_envelope", f"{f}: status '{st}' not in {sorted(statuses)}")
                        elif st == "undefined":
                            undefined.append(f)
                        elif st == "range" and not ({"min", "max"} <= set(rec)):
                            self.violate("site_envelope", f"{f}: a range needs min and max")
            for h in geo:
                if env is None:
                    self.violate(h["id"], "geometric hypothesis without a site envelope (sandbox_rule)")
                elif undefined:
                    self.violate(h["id"], f"geometric hypothesis outside a defined sandbox: undefined {sorted(set(undefined))} (sandbox_rule)")
                if h.get("rests_on") == "favourable":
                    self.notes.append(f"{h['id']}: rests on the favourable end of a range (sandbox_rule)")
                ua = h.get("uses_answers", [])
                if not ua:
                    self.violate(h["id"], "geometric hypothesis cites no recorded answers (consistency_rule)")
                for qid in ua:
                    if qid not in self.questions:
                        self.violate(h["id"], f"uses_answers names unknown question {qid}")
                    elif qid not in self.answers or self.answers[qid].get("status") in OPEN_STATUSES:
                        self.violate(h["id"], f"uses {qid}, which has no recorded answer (consistency_rule)")
                for d in h.get("deviations", []):
                    if d.get("resolved_by") != "human":
                        self.violate(h["id"], f"deviates from {d.get('question')} (recorded: {d.get('recorded')!r}, proposed: "
                                              f"{d.get('proposed')!r}) without the human's resolution (consistency_rule)")
            if geo and undefined:
                for f in sorted(set(undefined)):
                    key = f"site_envelope.{f}"
                    items[key] = {"item": key, "state": "undefined (blocks layouts)", "dependents": [h["id"] for h in geo],
                                  "score": 3 * len(geo), "show_stopper": True}

        # 0.12: encoded geometry, frame, buildable checks, exports
        self.export_results = {}
        gmod = self.U.get("geometry_model", {})
        if "encoding_rule" in gmod:
            import usg_geometry as G
            geo = [h for h in hyps.values() if h.get("status") != "retired" and h.get("level") == "geometric"]
            env = self.I.get("site_envelope") or {}
            if geo:
                frame = self.I.get("coordinate_frame")
                if frame is None:
                    self.violate("coordinate_frame", "geometric hypotheses exist but no coordinate frame is declared (frame_rule)")
                else:
                    rh = G.right_handed(frame)
                    if rh is None:
                        self.violate("coordinate_frame", "invalid axis names")
                    elif not rh:
                        self.violate("coordinate_frame", "frame is left-handed (frame_rule requires right-handed)")
                if env.get("controlling_geometry_ref") not in gmod["authority"]["hierarchy"]:
                    self.violate("site_envelope", f"controlling_geometry_ref '{env.get('controlling_geometry_ref')}' not in the authority hierarchy")
                spatial = [("boundary", [env.get("boundary")] if env.get("boundary") else [])] + \
                          [(f, env.get(f, [])) for f in ("setbacks", "protected_zones")] + \
                          [("existing_elements", [e for e in env.get("existing_elements", []) if e.get("keep")])]
                for f, recs in spatial:
                    for rec in recs:
                        if isinstance(rec, dict) and not rec.get("geometry"):
                            self.violate("site_envelope", f"{f} {rec.get('id', rec.get('edge', ''))} is not encoded as geometry (encoding_rule)".replace("  ", " "))
                for h in geo:
                    fp = h.get("footprint")
                    if not fp:
                        self.notes.append(f"{h['id']}: no encoded footprint; export checks not run")
                        continue
                    unresolved = sum(1 for d in h.get("deviations", []) if d.get("resolved_by") != "human")
                    res = G.export_checks(fp, env, unresolved, h.get("height"))
                    self.export_results[h["id"]] = res
                    for r in res:
                        if r["result"] == "fail":
                            self.notes.append(f"{h['id']}: export check failed: {r['check']} ({r['detail']})")
            em_ = self.U.get("export_model", {})
            mf_fields = self.U["schemas"].get("export_manifest", {})
            for ex in self.I.get("exports", []):
                m = ex.get("manifest", {})
                where = f"export {ex.get('file')}"
                for f in mf_fields:
                    if f not in m:
                        self.violate(where, f"manifest missing '{f}'")
                subj = m.get("subject", {})
                if subj.get("type") not in em_.get("subjects", []):
                    self.violate(where, f"invalid subject type '{subj.get('type')}'")
                if subj.get("type") == "design_hypothesis":
                    if m.get("class") != "concept":
                        self.violate(where, "a hypothesis export must be concept geometry")
                    if m.get("topology_validated") is not False:
                        self.violate(where, "a hypothesis export must record topology_validated = false")
                if m.get("class") == "construction" and (subj.get("type") != "geometric_candidate" or self.project_status != "real"):
                    self.violate(where, "construction geometry requires an accepted candidate and project_status real")
                if m.get("project_status") != self.project_status:
                    self.violate(where, f"manifest says project_status '{m.get('project_status')}', run says '{self.project_status}'")
                actual = {r["check"]: r["result"] for r in self.export_results.get(subj.get("id"), [])}
                if not actual:
                    self.violate(where, f"no export checks could be run for {subj.get('id')}")
                for chk, resu in actual.items():
                    if resu == "fail":
                        self.violate(where, f"exported although check failed: {chk} (export_checks)")
                for c in m.get("checks", []):
                    if c.get("result") == "pass" and actual.get(c.get("check")) not in (None, "pass"):
                        self.violate(where, f"manifest claims pass for '{c.get('check')}', recomputed {actual.get(c.get('check'))}")

        # unanswered required questions of the current or an earlier phase
        saved = list(self.notes)
        upto = [st for p in phases[:phases.index(cur) + 1] for st in self.U["phase_model"]["stages"][p]]
        for s in self.stages:
            if s["id"] not in upto:
                continue
            for q in s["questions"]:
                if q["id"] not in self.answers and q["id"] not in items and self.is_required(q):
                    items[q["id"]] = {"item": q["id"], "state": "unanswered", "dependents": [], "score": 1, "show_stopper": False}
        self.notes = saved
        self.awareness = sorted(items.values(), key=lambda x: (not x.get("show_stopper"), -x["score"], x["item"]))

        # 0.9 strain: interested review, environmental absorption, imposed burden
        if "interested_review" in strain:
            strain["interested_review"] = [e["id"] for e in self.evidence.values()
                                           if e.get("kind") == "professional_confirmation" and self.interested(e)]
        if "environmental_absorption" in strain:
            scen = {s.get("id"): s for s in self.I.get("scenarios", [])}
            outside = set(asys) | {c.get("id") for c in self.I.get("context", []) if c.get("outside_boundary")}
            for f in self.I.get("flows", []):
                fails = [s for s in f.get("scenarios", []) if scen.get(s, {}).get("kind") == "failure"]
                if fails and f.get("sink") in outside and f.get("containment") != "engineered" \
                        and f.get("absorption_accepted_by") != "human":
                    strain["environmental_absorption"].append({"flow": f["id"], "sink": f["sink"], "scenario": fails[0]})
            for s in scen.values():
                if s.get("kind") not in O["scenario"]["kind_values"]:
                    self.violate(s.get("id", "?"), f"invalid scenario kind '{s.get('kind')}'")
        if "imposed_burden" in strain:
            strain["imposed_burden"] = [v["id"] for v in self.I.get("value_ledger", []) if v.get("consent") == "imposed"]

        for v in self.I.get("value_ledger", []):
            if v.get("burden") not in (None, "", "none") and not v.get("compensation"):
                strain["burden_without_compensation"].append(v["id"])
        for a in asys.values():
            if a.get("burden_bearers") and not a.get("compensation"):
                strain["burden_without_compensation"].append(a["id"])
        for a in assm.values():
            up = a.get("until_phase")
            if up in phases and phases.index(up) < phases.index(cur) and a.get("status") != "confirmed":
                strain["assumption_past_phase"].append(a["id"])
        self.strain = {k: v for k, v in strain.items() if v}

        # --- commitments
        cps = pm["commitment_points"]
        for c in self.I.get("commitments", []):
            pt = c.get("point")
            if pt not in cps:
                self.violate("commitments", f"unknown commitment point '{pt}'")
                continue
            transition = "->" in pt
            blocked, reasons = False, []
            for hid in c.get("hypotheses", []):
                h = hyps.get(hid)
                if h is None:
                    self.violate("commitments", f"unknown hypothesis {hid}")
                    continue
                for pid in h.get("presupposes", []):
                    r = resolve(pid)
                    if r == "negative":
                        blocked = True; reasons.append(f"{hid}: {pid} negative")
                    elif r in ("unresolved", "conflicting"):
                        if transition and self.project_status == "exploratory":
                            reasons.append(f"{hid}: {pid} {r}, passed under exploratory status")
                        else:
                            blocked = True; reasons.append(f"{hid}: {pid} {r}")
                    # 0.9 assumption aging: an assumption whose until_phase has ended blocks, even exploratory
                    if transition and pid in assm and "assumption_aging" in pm["commitment_rule"]:
                        up = assm[pid].get("until_phase")
                        frm = pt.split("->")[0]
                        if up in phases and phases.index(up) <= phases.index(frm) and assm[pid].get("status") != "confirmed":
                            blocked = True; reasons.append(f"{hid}: {pid} past its until_phase '{up}' (assumption_aging)")
                for oid in h.get("fixes", {}):
                    o = odvs.get(oid)
                    if o and o.get("status") == "open":
                        frm = pt.split("->")[0] if transition else phases[-2]
                        if phases.index(o["decide_by"]) > phases.index(frm):
                            self.violate(hid, f"commits {oid} at '{pt}' before its decide_by phase '{o['decide_by']}'")
            if not transition:  # 0.9: unverified delivery premises block acceptance, export and irreversible acts
                for pid in sorted(set(delivery_premises)):
                    blocked = True; reasons.append(f"delivery premise {pid} unresolved")
            self.commit_results.append({"point": pt, "blocked": blocked, "reasons": reasons})

    def report(self, quiet=False):
        exp = self.I.get("expected", {})
        st = self.stop or {}
        out = [f"USG run  protocol {self.U['document']['version']}  instance {self.I['instance']['id']}  as_of {self.as_of}"]
        if not quiet:
            out.append("TRACE"); out += ["  " + t for t in self.trace]
            out.append("NOTES"); out += ["  " + n for n in self.notes] or ["  none"]
            out.append("OPEN REVIEW ITEMS"); out += ["  " + n for n in self.review_items] or ["  none"]
            if self.library_gaps:
                out.append("LIBRARY GAPS"); out += [f"  {q}: {sc}" for q, sc in self.library_gaps]
            if getattr(self, "awareness", None):
                out.append(f"AWARENESS (phase {self.current_phase}; ! = show-stopper; first line surfaces next, one per design turn)")
                out += [f"  {'!' if a.get('show_stopper') else ' '}{a['score']:>2}  {a['item']}: {a['state']}" + (f"  <- {a['dependents']}" if a["dependents"] else "")
                        for a in self.awareness[:8]]
                if len(self.awareness) > 8:
                    out.append(f"  ... {len(self.awareness) - 8} more queued")
            if getattr(self, "strain", None):
                out.append("STRAIN (derived, never a score)")
                out += [f"  {k}: {v}" for k, v in self.strain.items()]
            if getattr(self, "commit_results", None):
                out.append("COMMITMENTS")
                out += [f"  {c['point']}: {'BLOCKED' if c['blocked'] else 'allowed'}  {c['reasons']}" for c in self.commit_results]
        out.append("VIOLATIONS"); out += ["  " + v for v in self.violations] or ["  none"]
        out.append("OUTCOME")
        out.append(f"  stopped at {st.get('stage')}: {st.get('reason')}  [{st.get('protocol_ref')}]")
        if st.get("detail"):
            out.append(f"  detail: {st['detail']}")
        out.append(f"  loop: {st.get('loop')}  escalation: {st.get('escalation')}")
        out.append(f"  project_status: {self.project_status}  reaches_geometry: {self.reaches_geometry}  "
                   f"library_candidates: {len(self.I.get('library_candidates', []))}"
                   + (f"  closure_level: {self.closure_level}" if getattr(self, "closure_level", None) else ""))
        actual = {"stop_stage": st.get("stage"), "stop_reason": st.get("reason"), "loop": st.get("loop"),
                  "escalation": st.get("escalation"), "reaches_geometry": self.reaches_geometry,
                  "project_status": self.project_status,
                  "library_candidates": len(self.I.get("library_candidates", [])),
                  "commit_blocked": any(c["blocked"] for c in getattr(self, "commit_results", [])),
                  "awareness_top": self.awareness[0]["item"] if getattr(self, "awareness", None) else None,
                  "strain_categories": sorted(getattr(self, "strain", {})),
                  "closure_level": getattr(self, "closure_level", None)}
        mism = [f"{k}: expected {v!r}, got {actual.get(k, '<unknown key>')!r}" for k, v in exp.items()
                if k != "violations" and actual.get(k, "<unknown key>") != v]
        # expected violations: an instance may document known defects; each must occur, and nothing else
        expv = exp.get("violations", [])
        unexpected = [v for v in self.violations if not any(e in v for e in expv)]
        missing = [e for e in expv if not any(e in v for v in self.violations)]
        mism += [f"expected violation not raised: {e}" for e in missing]
        out.append("EXPECTED"); out += ["  MISMATCH " + m for m in mism] or ["  match"]
        if expv and not unexpected and not missing:
            out.append(f"  ({len(self.violations)} documented violations, all expected)")
        print("\n".join(out))
        self.mismatches = mism
        self.unexpected_violations = unexpected
        return 1 if unexpected else (2 if mism else 0)

    def record(self):
        return {"instance": self.I["instance"]["id"], "protocol_version": self.U["document"]["version"],
                "stop": self.stop, "project_status": self.project_status,
                "reaches_geometry": self.reaches_geometry, "claim_status": self.claim_status,
                "screen": self.screen_results, "library_gaps": self.library_gaps,
                "review_items": self.review_items, "violations": self.violations, "notes": self.notes,
                "awareness": getattr(self, "awareness", []), "strain": getattr(self, "strain", {}),
                "commitments": getattr(self, "commit_results", []), "trace": self.trace}


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    U, I = json.load(open(a[0])), json.load(open(a[1]))
    r = Run(U, I).run()
    code = r.report(quiet="--quiet" in a)
    if "--out" in a:
        json.dump(r.record(), open(a[a.index("--out") + 1], "w"), indent=2)
    sys.exit(code)
