from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-mapping-readiness-matrix.json"
DEFAULT_OUTPUT = ROOT / "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-mapping-go-no-go-review.md"
RIGHTS_REVIEW_PATH = "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md"
GATES = ("source_identity_and_drift", "authorized_source_artifact", "publication_rights", "provision_inventory", "semantic_and_normative_feasibility", "esaf_1600_and_schema_fit", "mapper_and_reviewer_readiness", "overclaiming_controls")
TOP_KEYS = {"blockers", "gates", "mapping_contract", "nonclaims", "reconsideration_sequence", "recorded_decision", "review_findings", "review_identifier", "reviewer_contract", "rights_review", "schema_version", "source_oracle"}
GATE_KEYS = {"blocker_ids", "evidence_references", "gate", "rationale", "status"}
BLOCKER_KEYS = {"blocker_id", "category", "gate", "missing_evidence", "owner", "reconsideration_trigger", "reentry_test", "remediation"}
CONTRACT_KEYS = {"direction", "excluded_direction", "directional_question", "granularity", "positive_feasibility_probe", "scope"}
SHA = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


def _exact(value, keys, label):
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} must contain exactly {sorted(keys)}")
    return value


def _strings(value, label, empty=False):
    if not isinstance(value, list) or (not empty and not value) or any(not isinstance(x, str) or not x.strip() for x in value) or len(value) != len(set(value)):
        raise ValueError(f"{label} must be a {'possibly empty' if empty else 'nonempty'} list of unique nonempty strings")
    return value


def _repo_path(value, label):
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must stay within the repository") from exc
    return path


def _evidence(value, label):
    if "://" in value or value.startswith(("sha256:", "symbolic:")):
        return
    path = value.split("#", 1)[0]
    if not path or not _repo_path(path, label).is_file():
        raise ValueError(f"{label} does not identify an existing repository file")


def validate_matrix(matrix, *, verify_source_digest=True):
    _exact(matrix, TOP_KEYS, "matrix")
    if matrix["schema_version"] != "1.0.0":
        raise ValueError("unsupported schema_version")
    if not isinstance(matrix["review_identifier"], str) or not matrix["review_identifier"].strip():
        raise ValueError("review_identifier must be nonempty")
    source = _exact(matrix["source_oracle"], {"path", "sha256"}, "source_oracle")
    if not isinstance(source["path"], str) or not source["path"].strip() or not isinstance(source["sha256"], str) or not SHA.fullmatch(source["sha256"]):
        raise ValueError("source_oracle path or SHA-256 is invalid")
    if verify_source_digest:
        path = _repo_path(source["path"], "source_oracle.path")
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError("source oracle is absent or its digest is stale")
    source_path = _repo_path(source["path"], "source_oracle.path")
    try:
        source_oracle = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("source oracle cannot be read as JSON") from exc
    rights = _exact(matrix["rights_review"], {"commit", "path", "sha256"}, "rights_review")
    if rights["path"] != RIGHTS_REVIEW_PATH:
        raise ValueError("rights_review.path must be the canonical publication-rights review")
    if not isinstance(rights["commit"], str) or not COMMIT.fullmatch(rights["commit"]) or not isinstance(rights["sha256"], str) or not SHA.fullmatch(rights["sha256"]):
        raise ValueError("rights review commit or SHA-256 is invalid")
    contract = _exact(matrix["mapping_contract"], CONTRACT_KEYS, "mapping_contract")
    if contract["direction"] != "esaf_to_external" or contract["excluded_direction"] != "external_to_esaf" or contract["scope"] != "complete_publication":
        raise ValueError("mapping direction or scope is invalid")
    for field in ("directional_question", "granularity"):
        if not isinstance(contract[field], str) or not contract[field].strip():
            raise ValueError(f"mapping_contract.{field} must be nonempty")
    if not isinstance(contract["positive_feasibility_probe"], bool):
        raise ValueError("positive_feasibility_probe must be boolean")
    findings = _exact(matrix["review_findings"], {"open_critical", "open_important"}, "review_findings")
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 0 for n in findings.values()):
        raise ValueError("review findings must be nonnegative integers")
    gates = matrix["gates"]
    if not isinstance(gates, list) or [g.get("gate") if isinstance(g, dict) else None for g in gates] != list(GATES):
        raise ValueError("gate order is invalid")
    for raw in gates:
        gate = _exact(raw, GATE_KEYS, f"gate {raw.get('gate')}")
        if gate["status"] not in {"PASS", "BLOCKED"}:
            raise ValueError(f"invalid gate status for {gate['gate']}")
        if not isinstance(gate["rationale"], str) or not gate["rationale"].strip():
            raise ValueError(f"{gate['gate']}.rationale must be nonempty")
        for ref in _strings(gate["evidence_references"], f"{gate['gate']}.evidence_references"):
            _evidence(ref, f"{gate['gate']}.evidence_references")
        _strings(gate["blocker_ids"], f"{gate['gate']}.blocker_ids", empty=gate["status"] == "PASS")
        if (gate["status"] == "PASS") != (not gate["blocker_ids"]):
            raise ValueError(f"gate {gate['gate']} blocker coverage is inconsistent")
    blockers = matrix["blockers"]
    if not isinstance(blockers, list):
        raise ValueError("blockers must be a list")
    by_id = {}
    for raw in blockers:
        blocker = _exact(raw, BLOCKER_KEYS, "blocker")
        for key in BLOCKER_KEYS - {"remediation"}:
            if not isinstance(blocker[key], str) or not blocker[key].strip():
                raise ValueError(f"blocker.{key} must be nonempty")
        if blocker["gate"] not in GATES or blocker["remediation"] not in {"reconsiderable", "terminal"}:
            raise ValueError("blocker gate or remediation is invalid")
        if blocker["blocker_id"] in by_id:
            raise ValueError("duplicate blocker_id")
        by_id[blocker["blocker_id"]] = blocker
    referenced = []
    for gate in gates:
        for identifier in gate["blocker_ids"]:
            if identifier not in by_id or by_id[identifier]["gate"] != gate["gate"]:
                raise ValueError("unknown or incorrectly assigned blocker reference")
            referenced.append(identifier)
    if len(referenced) != len(set(referenced)) or set(referenced) != set(by_id):
        raise ValueError("orphan, duplicate, or unreferenced blocker")
    _strings(matrix["reconsideration_sequence"], "reconsideration_sequence")
    _strings(matrix["nonclaims"], "nonclaims")
    reviewer = matrix["reviewer_contract"]
    if not isinstance(reviewer, dict) or not reviewer:
        raise ValueError("reviewer_contract must be a nonempty object")
    blocked = [g for g in gates if g["status"] == "BLOCKED"]
    terminal = any(b["remediation"] == "terminal" for b in blockers)
    if blocked and any(not g["blocker_ids"] for g in blocked):
        raise ValueError("every blocked gate requires complete blocker coverage")
    if not blocked:
        derived = "GO" if not blockers and contract["positive_feasibility_probe"] and not findings["open_critical"] and not findings["open_important"] else None
    elif terminal:
        derived = "NO_GO"
    elif all(b["remediation"] == "reconsiderable" for b in blockers):
        derived = "HOLD"
    else:
        derived = None
    if derived is None:
        raise ValueError("matrix satisfies neither GO, HOLD, nor NO_GO contract")
    if matrix["recorded_decision"] != derived:
        raise ValueError(f"recorded_decision does not match derived decision {derived}")
    if matrix["recorded_decision"] == "HOLD" and terminal:
        raise ValueError("HOLD cannot contain terminal blockers")
    if matrix["recorded_decision"] == "NO_GO" and not terminal:
        raise ValueError("NO_GO requires a terminal blocker")
    if verify_source_digest:
        rights_path = _repo_path(rights["path"], "rights_review.path")
        if not rights_path.is_file():
            raise ValueError("rights review is absent")
        def git(*args):
            result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
            if result.returncode:
                raise ValueError("rights review commit/path verification failed")
            return result.stdout
        if git("cat-file", "-e", f"{rights['commit']}^{{commit}}") is None:
            raise ValueError("rights review commit is absent")
        blob = git("show", f"{rights['commit']}:{rights['path']}")
        git("merge-base", "--is-ancestor", rights["commit"], "HEAD")
        if hashlib.sha256(blob).hexdigest() != rights["sha256"] or rights_path.read_bytes() != blob:
            raise ValueError("rights review digest or live bytes drift")
        rights_text = blob.decode("utf-8")
    else:
        rights_path = _repo_path(rights["path"], "rights_review.path")
        rights_text = rights_path.read_text(encoding="utf-8")
    # A matrix is not itself evidence of source access or publication rights.
    # Prevent a hand-edited set of PASS statuses from authorizing GO while the
    # independently pinned source and rights records still say HOLD.
    if matrix["recorded_decision"] == "GO":
        artifact = source_oracle.get("source_artifact", {})
        access = source_oracle.get("access", {})
        inventory = source_oracle.get("inventory", {})
        boundary = source_oracle.get("boundary", {})
        if (artifact.get("state") != "retrieved" or not access.get("source_bytes_retrieved")
                or not isinstance(artifact.get("sha256"), str) or not SHA.fullmatch(artifact["sha256"])
                or not isinstance(artifact.get("byte_length"), int) or artifact["byte_length"] <= 0):
            raise ValueError("GO requires affirmative, digest-bound source artifact retrieval evidence")
        if not inventory.get("created") or not isinstance(inventory.get("inventory_sha256"), str) or not SHA.fullmatch(inventory["inventory_sha256"]):
            raise ValueError("GO requires a digest-bound, authorized provision inventory")
        if not (boundary.get("document_specific_notice_inspected") or boundary.get("written_aicpa_permission_for_esaf_evidenced")):
            raise ValueError("GO requires affirmative document-specific rights or written permission evidence")
        if not re.search(r"\*\*Disposition:\*\*\s*`PASS`", rights_text):
            raise ValueError("GO requires the pinned independent rights review to record PASS")
        raise ValueError("GO is disabled in schema 1.0.0 until digest-bound feasibility and exact-candidate reviewer attestations are supported")
    return None


def derive_decision(matrix, *, verify_source_digest=True):
    validate_matrix(matrix, verify_source_digest=verify_source_digest)
    return matrix["recorded_decision"]


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render(matrix):
    decision = derive_decision(matrix)
    lines = ["# SOC 2 AICPA TSC mapping readiness decision", "", f"**Decision:** `{decision}`", "", f"**Review identifier:** `{matrix['review_identifier']}`", "", "The decision is mechanically derived from the closed readiness matrix.", "", "## Directional question", "", f"> {matrix['mapping_contract']['directional_question']}", "", "## Gate results", "", "| Gate | Status | Rationale | Evidence |", "|---|---|---|---|"]
    for gate in matrix["gates"]:
        lines.append(f"| `{gate['gate']}` | `{gate['status']}` | {_cell(gate['rationale'])} | {_cell('; '.join(gate['evidence_references']))} |")
    lines.extend(["", "## Blockers", "", "| Blocker | Category | Gate | Owner | Missing evidence | Remediation | Trigger | Re-entry test |", "|---|---|---|---|---|---|---|---|"])
    for b in matrix["blockers"]:
        lines.append("| " + " | ".join(_cell(b[k]) for k in ("blocker_id", "category", "gate", "owner", "missing_evidence", "remediation", "reconsideration_trigger", "reentry_test")) + " |")
    lines.extend(["", "## Reconsideration sequence", ""])
    lines.extend(f"{i}. {item}" for i, item in enumerate(matrix["reconsideration_sequence"], 1))
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in matrix["nonclaims"])
    lines.extend(["", f"**Final decision:** `{decision}`", ""])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render the SOC 2 AICPA TSC mapping readiness decision.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    try:
        matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
        rendered = render(matrix)
        if args.write:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        elif args.check:
            if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
                print(f"error: rendered review is absent or stale: {args.output}", file=sys.stderr)
                return 1
        else:
            sys.stdout.write(rendered)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
