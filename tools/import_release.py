from __future__ import annotations

import json
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "USG_v0_12.zip"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    ensure_parent(dst)
    shutil.copy2(src, dst)


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if not ZIP.exists():
        raise SystemExit("USG_v0_12.zip not found at repository root")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        with zipfile.ZipFile(ZIP) as zf:
            zf.extractall(tmp)

        src = tmp / "USG_v0_12"
        if not src.exists():
            candidates = [p for p in tmp.iterdir() if p.is_dir()]
            if len(candidates) != 1:
                raise SystemExit("Could not identify unpacked USG release directory")
            src = candidates[0]

        # 1. Immutable protocol versions.
        versions = [
            "USG_v0_5_1.json",
            "USG_v0_6.json",
            "USG_v0_7.json",
            "USG_v0_8.json",
            "USG_v0_9.json",
            "USG_v0_10.json",
            "USG_v0_11.json",
            "USG_v0_12.json",
        ]
        for name in versions:
            copy_file(src / name, ROOT / "protocol" / "versions" / name)

        # 2. Runtime/checking tools.
        for name in ["check_usg.py", "run_usg.py", "usg_geometry.py"]:
            copy_file(src / name, ROOT / "tools" / name)

        # 3. Pinned conformance instances.
        for path in sorted((src / "instances").glob("*.json")):
            copy_file(path, ROOT / "conformance" / "instances" / path.name)

        # 4. Mutation suite. Preserve tests; adapt only repository paths/import.
        test_text = (src / "test_runner.py").read_text(encoding="utf-8")
        test_text = test_text.replace(
            "import copy, json, sys\nfrom run_usg import Run",
            "import copy, json, sys\nfrom pathlib import Path\n"
            "ROOT = Path(__file__).resolve().parents[1]\n"
            "sys.path.insert(0, str(ROOT / 'tools'))\n"
            "from run_usg import Run",
        )
        old = (
            'U = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "USG_v0_6.json"))\n'
            'A = json.load(open("instances/fail_no_need.json"))\n'
            'B = json.load(open("instances/fail_all_sites_prohibited.json"))\n'
            'C = json.load(open("instances/instance_adu_backyard.json"))\n'
            'M = json.load(open("instances/stress_one_mile_city.json"))'
        )
        new = (
            'protocol_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "protocol/versions/USG_v0_12.json"\n'
            'U = json.load(open(protocol_path, encoding="utf-8"))\n'
            'FIX = ROOT / "conformance/instances"\n'
            'A = json.load(open(FIX / "fail_no_need.json", encoding="utf-8"))\n'
            'B = json.load(open(FIX / "fail_all_sites_prohibited.json", encoding="utf-8"))\n'
            'C = json.load(open(FIX / "instance_adu_backyard.json", encoding="utf-8"))\n'
            'M = json.load(open(FIX / "stress_one_mile_city.json", encoding="utf-8"))'
        )
        if old not in test_text:
            raise SystemExit("test_runner path block no longer matches release")
        test_text = test_text.replace(old, new)
        write_text(ROOT / "tests" / "test_runner.py", test_text)

        # 5. Patch history and instance migrations.
        for path in sorted((src / "patches").glob("*.py")):
            if path.name.startswith("patch_"):
                dst = ROOT / "history" / "patches" / path.name
            elif path.name.startswith("migrate_instances_"):
                dst = ROOT / "history" / "migrations" / path.name
            else:
                continue
            copy_file(path, dst)

        # 6. Worked ADU drawing example.
        for path in sorted((src / "drawings").iterdir()):
            copy_file(path, ROOT / "examples" / "adu-backyard" / "drawings" / path.name)

        numeric = ROOT / "examples" / "adu-backyard" / "drawings" / "numeric_site_model.py"
        txt = numeric.read_text(encoding="utf-8")
        txt = txt.replace("import json, sys", "import json, sys\nfrom pathlib import Path")
        txt = txt.replace(
            'I = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "instances/instance_adu_backyard.json"))',
            'ROOT = Path(__file__).resolve().parents[3]\n'
            'instance_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "conformance/instances/instance_adu_backyard.json"\n'
            'I = json.load(open(instance_path, encoding="utf-8"))',
        )
        numeric.write_text(txt, encoding="utf-8")

        # 7. Archive exact distribution and original release README.
        copy_file(src / "README.md", ROOT / "archive" / "releases" / "v0.12" / "README.md")
        archive_zip = ROOT / "archive" / "releases" / "USG_v0_12.zip"
        ensure_parent(archive_zip)
        shutil.copy2(ZIP, archive_zip)

        # 8. Move explanatory root artifacts into docs.
        article = ROOT / "USG_Article_Need_First_Geometry_Last.docx"
        if article.exists():
            copy_file(article, ROOT / "docs" / "articles" / article.name)
            article.unlink()

        figure = ROOT / "Inductive vs Deductive Thinking Infographic.png"
        if figure.exists():
            copy_file(figure, ROOT / "docs" / "figures" / figure.name)
            figure.unlink()

        # 9. Actual 21-stage summary derived from canonical 0.12 protocol.
        U = json.loads((src / "USG_v0_12.json").read_text(encoding="utf-8"))
        phase_for = {
            stage_id: phase
            for phase, stage_ids in U["phase_model"]["stages"].items()
            for stage_id in stage_ids
        }
        stage_summary = {
            "source": "protocol/versions/USG_v0_12.json",
            "protocol_version": U["document"]["version"],
            "note": "Generated navigation summary. The versioned protocol JSON remains the source of truth.",
            "phases": U["phase_model"]["phases"],
            "stages": [
                {
                    "id": s["id"],
                    "name": s["name"],
                    "phase": phase_for.get(s["id"]),
                    "purpose": s["purpose"],
                    "output": s.get("output"),
                    "gate": s.get("gate"),
                }
                for s in U["pipeline"]
            ],
        }
        write_text(ROOT / "core" / "stages.json", json.dumps(stage_summary, indent=2, ensure_ascii=False) + "\n")

        # 10. Structure documentation.
        write_text(
            ROOT / "protocol" / "README.md",
            """# Protocol\n\n"
            "The canonical USG protocol is versioned and immutable under `versions/`.\n\n"
            "- Current source of truth: `versions/USG_v0_12.json`\n"
            "- Previous versions are retained for non-regression and rebuild.\n"
            "- Never rewrite an old protocol version in place. A change becomes a new version produced by a patch.\n\n"
            "The current protocol contains the 21-stage pipeline, ontology, evidence model, phase model, geometry authority, schemas, feedback loops, export rules and governance.\n""",
        )
        write_text(
            ROOT / "conformance" / "README.md",
            """# Conformance\n\n"
            "Pinned program instances used to test whether an implementation behaves as USG v0.12 specifies.\n\n"
            "- `fail_no_need.json` — strategic stop at S01\n"
            "- `fail_all_sites_prohibited.json` — all site candidates prohibited\n"
            "- `instance_adu_backyard.json` — exploratory ADU/site-envelope case\n"
            "- `stress_one_mile_city.json` — design-ahead-of-premise stress case\n\n"
            "Run `python tests/test_runner.py protocol/versions/USG_v0_12.json`.\n""",
        )
        write_text(
            ROOT / "tools" / "README.md",
            """# Tools\n\n"
            "- `check_usg.py` — protocol self-consistency, governance and non-regression checker.\n"
            "- `run_usg.py` — executes pinned instances through implemented stage gates.\n"
            "- `usg_geometry.py` — dependency-free geometry checks used by the runner.\n\n"
            "These tools implement/check the protocol; they are not protocol authority.\n""",
        )
        write_text(
            ROOT / "tests" / "README.md",
            """# Tests\n\n"
            "`test_runner.py` contains the v0.12 mutation/conformance suite. Test definitions are preserved from the release; only repository path handling is adapted.\n""",
        )
        write_text(
            ROOT / "history" / "README.md",
            """# History\n\n"
            "USG governance is **patch, never rewrite**.\n\n"
            "- `patches/` contains protocol patches 0.6 through 0.12.\n"
            "- `migrations/` contains corresponding instance migrations.\n\n"
            "The exact compact release bundle remains under `archive/releases/` for verbatim historical reproduction.\n""",
        )
        write_text(
            ROOT / "archive" / "README.md",
            """# Archive\n\nImmutable historical release artifacts. The structured repository is the working view; archived ZIPs preserve the exact distributed bundle.\n""",
        )
        write_text(
            ROOT / "docs" / "articles" / "README.md",
            """# Articles\n\nDiscussion and explanatory material. These documents explain USG but do not override the versioned machine-readable protocol.\n""",
        )
        write_text(
            ROOT / "docs" / "figures" / "README.md",
            """# Figures\n\nVisual explanations and diagrams associated with USG and the wider strata architecture.\n""",
        )
        write_text(
            ROOT / "schema" / "README.md",
            """# Schemas\n\nThis folder is for external integration and handoff schemas. USG v0.12's canonical internal schemas remain embedded in `protocol/versions/USG_v0_12.json` until they can be extracted without breaking non-regression.\n\n`usg-output.schema.json` is an integration draft, not a replacement for the protocol's internal schemas.\n""",
        )
        write_text(
            ROOT / "docs" / "repository-structure.md",
            """# Repository structure\n\n"
            "```text\n"
            "USG/\n"
            "├── README.md\n"
            "├── AGENTS.md\n"
            "├── core/                  # navigation summaries derived from protocol\n"
            "├── protocol/versions/     # immutable protocol versions\n"
            "├── schema/                # external/handoff schemas\n"
            "├── conformance/instances/ # pinned regression/stress cases\n"
            "├── tests/                 # mutation/conformance tests\n"
            "├── tools/                 # runner, checker, geometry validator\n"
            "├── history/               # patches and migrations\n"
            "├── examples/              # generated drawings / worked examples\n"
            "├── docs/                  # architecture and explanatory material\n"
            "└── archive/               # exact historical release bundles\n"
            "```\n\n"
            "## Authority\n\n"
            "`protocol/versions/USG_v0_12.json` is the current machine-readable source of truth. Navigation summaries, docs and external schemas must not silently override it.\n""",
        )

        # 11. Today’s sketch lesson is useful, but is a proposal until a protocol patch adopts it.
        write_text(
            ROOT / "docs" / "proposals" / "architectural-sketch-reconstruction.md",
            """# Proposed architectural sketch reconstruction rule\n\n"
            "**Status: proposal — not yet canonical USG v0.12 protocol.**\n\n"
            "Architectural sketches communicate through explicit dimensions, topology, proportion and perspective. A reconstruction system should not treat every undimensioned feature as unusable.\n\n"
            "## Proposed rule\n\n"
            "**Dimensions override proportion. Proportion fills the gaps. User clarification resolves contradictions.**\n\n"
            "Suggested evidence states:\n\n"
            "- `exact` — explicitly dimensioned or stated; build exactly.\n"
            "- `derived` — calculated from exact information without adding unsupported intent.\n"
            "- `approximate` — intent is clear but value/geometry is inferred proportionally; reconstruct and label approximate.\n"
            "- `observed` — presence/relationship is visible but usable geometry is not reliable.\n"
            "- `ambiguous` — multiple materially different readings remain; ask the user.\n"
            "- `unknown` — no useful information exists; leave unresolved.\n\n"
            "Do not confuse uncertainty of measurement with uncertainty of design intent. Ask the user when explicit evidence conflicts or ambiguity materially changes the design, not for every missing dimension.\n""",
        )

        # 12. Remove root release ZIP after safe archive copy.
        ZIP.unlink()

    print("USG v0.12 organized successfully")


if __name__ == "__main__":
    main()
