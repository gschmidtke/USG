#!/usr/bin/env python3
"""Regenerate core/stages.json from the current USG protocol.

The protocol named in protocol/CURRENT is the source of truth; core/stages.json
is only a navigation summary of its pipeline. Run without arguments to rewrite
the summary, or with --check to fail (exit 1) when the committed summary has
drifted from the protocol. CI runs the --check form.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURRENT = ROOT / "protocol" / "CURRENT"
OUT = ROOT / "core" / "stages.json"


def current_protocol_path() -> str:
    return CURRENT.read_text(encoding="utf-8").strip()


def build(protocol_rel: str) -> dict:
    protocol = json.loads((ROOT / protocol_rel).read_text(encoding="utf-8"))
    phase_of = {
        stage_id: phase
        for phase, stage_ids in protocol["phase_model"]["stages"].items()
        for stage_id in stage_ids
    }
    stages = []
    for stage in protocol["pipeline"]:
        stages.append({
            "id": stage["id"],
            "name": stage["name"],
            "phase": phase_of.get(stage["id"]),
            "purpose": stage.get("purpose"),
            "output": stage.get("output"),
            "gate": stage.get("gate"),
        })
    return {
        "source": protocol_rel,
        "protocol_version": protocol["document"]["version"],
        "note": "Generated navigation summary. The versioned protocol JSON remains the source of truth.",
        "phases": protocol["phase_model"]["phases"],
        "stages": stages,
    }


def render(summary: dict) -> str:
    return json.dumps(summary, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if core/stages.json is out of date")
    args = parser.parse_args()

    expected = render(build(current_protocol_path()))
    if args.check:
        actual = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if json.loads(actual or "null") != json.loads(expected):
            print("core/stages.json is out of date; run: python tools/build_stages.py", file=sys.stderr)
            return 1
        print("core/stages.json matches", current_protocol_path())
        return 0
    OUT.write_text(expected, encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
