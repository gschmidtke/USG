#!/usr/bin/env python3
"""Check that documents and examples still match the machine-readable contracts.

Prose and examples drift from schemas unless something checks them. This runs in CI:

1. the JSON example in docs/handoff-to-arpl.md validates against schema/usg-output.schema.json;
2. every curation record validates against schema/curation-record.schema.json, and every
   path it names as its source or a resulting file exists;
3. examples/building-002 spec v0.2 validates against schema/neutral-building-spec.schema.json;
4. examples/building-001 passes its own declared checks.

Requires the jsonschema package. Exit code 1 on any failure.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
failures = []


def validator(schema_rel):
    schema = json.loads((ROOT / schema_rel).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def report(name, errors):
    if errors:
        failures.append(name)
        print(f"FAIL  {name}")
        for e in errors:
            print(f"      {e}")
    else:
        print(f"PASS  {name}")


# 1. Handoff example
doc = (ROOT / "docs/handoff-to-arpl.md").read_text(encoding="utf-8")
match = re.search(r"```json\n(.*?)```", doc, re.S)
example = json.loads(match.group(1)) if match else None
report("docs/handoff-to-arpl.md example vs usg-output schema",
       ["no ```json block found"] if example is None else
       [e.message for e in validator("schema/usg-output.schema.json").iter_errors(example)])

# 2. Curation records
records = validator("schema/curation-record.schema.json")
for path in sorted((ROOT / "curation/records").glob("*/*.json")):
    record = json.loads(path.read_text(encoding="utf-8"))
    errors = [e.message for e in records.iter_errors(record)]
    named = [record.get("source_submission", "")] + [f for f in record.get("resulting_files", []) if isinstance(f, str)]
    for f in named:
        candidate = f.split(" (")[0]
        if "/" in candidate and "." in candidate.rsplit("/", 1)[-1] and not (ROOT / candidate).exists():
            errors.append(f"named file does not exist: {candidate}")
    report(str(path.relative_to(ROOT)), errors)

# 3. Building 002 spec
spec = json.loads((ROOT / "examples/building-002/spec/Building_002_Neutral_Spec_v0.2.json").read_text(encoding="utf-8"))
report("examples/building-002 spec v0.2 vs neutral-building-spec schema",
       [e.message for e in validator("schema/neutral-building-spec.schema.json").iter_errors(spec)])

# 4. Building 001 self-checks
run = subprocess.run([sys.executable, str(ROOT / "examples/building-001/check_building_001.py")],
                     capture_output=True, text=True)
report("examples/building-001 declared checks",
       [] if run.returncode == 0 else [l for l in run.stdout.splitlines() if l.startswith("FAIL")])

print(f"{'all contracts hold' if not failures else str(len(failures)) + ' failing'}")
sys.exit(1 if failures else 0)
