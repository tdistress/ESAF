from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-25-pci-dss-mapping-readiness-matrix.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-07-25-pci-dss-mapping-go-no-go-review.md"
)

GATES = (
    "source_identity_and_drift",
    "authorized_source_artifact",
    "publication_rights",
    "provision_inventory",
    "semantic_and_normative_feasibility",
    "esaf_1600_and_schema_fit",
    "mapper_and_reviewer_readiness",
    "overclaiming_controls",
)
QUESTION = (
    "Does exact normative ESAF control requirement text directly support, "
    "partially support, or establish a prerequisite for the outcome required by "
    "one authorized, publishable PCI DSS v4.0.1 numbered requirement or "
    "sub-requirement, with each relationship's conditions, expected evidence, "
    "and known gaps recorded independently, without implying PCI DSS compliance, "
    "assessment, equivalence, certification, authorization, or endorsement?"
)
TOP_LEVEL_KEYS = {
    "blockers",
    "gates",
    "mapping_contract",
    "nonclaims",
    "reconsideration_sequence",
    "recorded_decision",
    "review_findings",
    "review_identifier",
    "reviewer_contract",
    "rights_review",
    "schema_version",
    "source_oracle",
}
GATE_KEYS = {
    "blocker_ids",
    "evidence_references",
    "gate",
    "rationale",
    "status",
}
BLOCKER_KEYS = {
    "blocker_id",
    "category",
    "gate",
    "missing_evidence",
    "owner",
    "reconsideration_trigger",
    "reentry_test",
}
MAPPING_CONTRACT_KEYS = {
    "direction",
    "directional_question",
    "excluded_direction",
    "granularity",
    "positive_feasibility_probe",
    "scope",
}
REVIEWER_CONTRACT_KEYS = {
    "approver",
    "candidate_change_requires_redispatch",
    "dual_role_requires_owner_approval",
    "mapper",
    "review_record_requirements",
    "reviewers",
    "separate_exact_candidate_reviews",
}
REVIEWER_ROLES = (
    "pci_subject_matter",
    "esaf_specification_and_mapping",
    "publication_rights",
    "security_and_overclaiming",
)
REVIEW_RECORD_REQUIREMENTS = {
    "identity",
    "role",
    "qualification_or_relevant_experience",
    "authorized_source_access_attestation",
    "attributable_attestation",
    "review_date",
    "exact_candidate_sha",
    "artifact_digests",
    "findings",
    "findings_disposition",
}
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
HEX_COMMIT = re.compile(r"^[0-9a-f]{40}$")


def _require_exact_keys(value: object, expected: set[str], context: str) -> dict:
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"{context} must contain exactly {sorted(expected)}")
    return value


def _require_nonempty_string(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a nonempty string")
    return value


def _require_string_list(
    value: object,
    context: str,
    *,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ValueError(f"{context} must be a nonempty list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{context} must contain nonempty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{context} must not contain duplicates")
    return value


def _resolve_repository_path(path_text: str, context: str) -> Path:
    path = (ROOT / path_text).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError(f"{context} must stay within the repository") from error
    return path


def _require_git_object(*arguments: str, context: str) -> None:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"{context}: {detail or 'git verification failed'}")


def _validate_evidence_reference(reference: str, context: str) -> None:
    if "://" in reference or reference.startswith(("sha256:", "symbolic:")):
        return
    path_text = reference.split("#", 1)[0]
    if not path_text:
        raise ValueError(f"{context} has an empty repository path")
    path = _resolve_repository_path(path_text, context)
    if not path.is_file():
        raise ValueError(f"{context} does not exist: {path_text}")


def _validate_reviewer_contract(value: object) -> None:
    contract = _require_exact_keys(value, REVIEWER_CONTRACT_KEYS, "reviewer_contract")
    mapper = _require_exact_keys(
        contract["mapper"],
        {
            "authorized_source_access_required",
            "experience_required",
            "named_person_required",
            "self_review_prohibited",
        },
        "reviewer_contract.mapper",
    )
    if mapper != {
        "authorized_source_access_required": True,
        "experience_required": ["PCI DSS v4.0.1", "ESAF-1600"],
        "named_person_required": True,
        "self_review_prohibited": True,
    }:
        raise ValueError("reviewer_contract.mapper does not meet the GO contract")

    reviewers = contract["reviewers"]
    if not isinstance(reviewers, list) or [
        reviewer.get("role") if isinstance(reviewer, dict) else None
        for reviewer in reviewers
    ] != list(REVIEWER_ROLES):
        raise ValueError("reviewer roles or order are invalid")
    for reviewer in reviewers:
        entry = _require_exact_keys(
            reviewer,
            {
                "authorized_source_access_required",
                "independent_from_mapper",
                "qualification",
                "role",
            },
            "reviewer_contract.reviewer",
        )
        if entry["independent_from_mapper"] is not True:
            raise ValueError(f"{entry['role']} must be independent from the mapper")
        if entry["authorized_source_access_required"] is not True:
            raise ValueError(f"{entry['role']} must attest authorized source access")
        _require_nonempty_string(entry["qualification"], f"{entry['role']}.qualification")
    if (
        reviewers[0]["qualification"]
        != "current QSA or owner-approved equivalent PCI reviewer"
    ):
        raise ValueError("PCI reviewer qualification is incomplete")

    requirements = _require_string_list(
        contract["review_record_requirements"],
        "reviewer_contract.review_record_requirements",
    )
    if set(requirements) != REVIEW_RECORD_REQUIREMENTS:
        raise ValueError("review record requirements are incomplete")
    if contract["separate_exact_candidate_reviews"] != [
        "inventory_and_specification",
        "security_and_overclaiming",
    ]:
        raise ValueError("separate exact-candidate reviews are incomplete")
    if contract["candidate_change_requires_redispatch"] is not True:
        raise ValueError("candidate changes must require review redispatch")
    if contract["dual_role_requires_owner_approval"] is not True:
        raise ValueError("dual reviewer roles must require owner approval")
    _require_nonempty_string(contract["approver"], "reviewer_contract.approver")


def _derived_decision_unchecked(matrix: dict[str, object]) -> str:
    statuses = [gate["status"] for gate in matrix["gates"]]
    blockers = matrix["blockers"]
    findings = matrix["review_findings"]
    positive = matrix["mapping_contract"]["positive_feasibility_probe"]
    if any(status == "BLOCKED" for status in statuses):
        return "HOLD"
    if (
        all(status == "PASS" for status in statuses)
        and not blockers
        and positive is True
        and findings["open_critical"] == 0
        and findings["open_important"] == 0
    ):
        return "GO"
    raise ValueError("matrix satisfies neither the GO nor HOLD derivation contract")


def validate_matrix(
    matrix: dict[str, object],
    *,
    verify_source_digest: bool = True,
) -> None:
    _require_exact_keys(matrix, TOP_LEVEL_KEYS, "matrix")
    if matrix["schema_version"] != "1.0.0":
        raise ValueError("unsupported schema_version")
    _require_nonempty_string(matrix["review_identifier"], "review_identifier")

    source = _require_exact_keys(matrix["source_oracle"], {"path", "sha256"}, "source_oracle")
    source_path_text = _require_nonempty_string(source["path"], "source_oracle.path")
    source_digest = _require_nonempty_string(source["sha256"], "source_oracle.sha256")
    if not HEX_SHA256.fullmatch(source_digest):
        raise ValueError("source_oracle.sha256 must be lowercase SHA-256")
    if verify_source_digest:
        source_path = _resolve_repository_path(source_path_text, "source_oracle.path")
        if not source_path.is_file():
            raise ValueError(f"source oracle does not exist: {source_path_text}")
        if hashlib.sha256(source_path.read_bytes()).hexdigest() != source_digest:
            raise ValueError("source oracle digest is stale")

    rights = _require_exact_keys(matrix["rights_review"], {"commit", "path"}, "rights_review")
    rights_path_text = _require_nonempty_string(rights["path"], "rights_review.path")
    rights_path = _resolve_repository_path(rights_path_text, "rights_review.path")
    if not rights_path.is_file():
        raise ValueError(f"rights review does not exist: {rights_path_text}")
    rights_commit = _require_nonempty_string(rights["commit"], "rights_review.commit")
    if not HEX_COMMIT.fullmatch(rights_commit):
        raise ValueError("rights_review.commit must be a full commit SHA")
    _require_git_object(
        "cat-file",
        "-e",
        f"{rights_commit}^{{commit}}",
        context="rights review commit does not exist",
    )
    _require_git_object(
        "cat-file",
        "-e",
        f"{rights_commit}:{rights_path_text}",
        context="rights review path is absent from the bound commit",
    )
    _require_git_object(
        "merge-base",
        "--is-ancestor",
        rights_commit,
        "HEAD",
        context="rights review commit is not an ancestor of HEAD",
    )

    contract = _require_exact_keys(
        matrix["mapping_contract"],
        MAPPING_CONTRACT_KEYS,
        "mapping_contract",
    )
    if contract["direction"] != "esaf_to_external":
        raise ValueError("mapping direction must be esaf_to_external")
    if contract["excluded_direction"] != "external_to_esaf":
        raise ValueError("excluded direction must be external_to_esaf")
    if contract["scope"] != "complete_publication":
        raise ValueError("mapping scope must be complete_publication")
    if (
        contract["granularity"]
        != "finest_authorized_publishable_numbered_requirement_or_sub_requirement_identifier"
    ):
        raise ValueError("mapping granularity is invalid")
    if contract["directional_question"] != QUESTION:
        raise ValueError("directional question is not exact")
    if not isinstance(contract["positive_feasibility_probe"], bool):
        raise ValueError("positive_feasibility_probe must be boolean")

    findings = _require_exact_keys(
        matrix["review_findings"],
        {"open_critical", "open_important"},
        "review_findings",
    )
    for name, count in findings.items():
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError(f"review_findings.{name} must be a nonnegative integer")

    gates = matrix["gates"]
    if not isinstance(gates, list) or [
        gate.get("gate") if isinstance(gate, dict) else None for gate in gates
    ] != list(GATES):
        raise ValueError("gate order is invalid")
    for gate in gates:
        entry = _require_exact_keys(gate, GATE_KEYS, f"gate {gate.get('gate')}")
        if entry["status"] not in {"PASS", "BLOCKED"}:
            raise ValueError(f"invalid gate status for {entry['gate']}")
        _require_nonempty_string(entry["rationale"], f"{entry['gate']}.rationale")
        evidence_references = _require_string_list(
            entry["evidence_references"],
            f"{entry['gate']}.evidence_references",
        )
        for reference in evidence_references:
            _validate_evidence_reference(
                reference,
                f"{entry['gate']}.evidence_references",
            )
        _require_string_list(
            entry["blocker_ids"],
            f"{entry['gate']}.blocker_ids",
            allow_empty=entry["status"] == "PASS",
        )
        if entry["status"] == "PASS" and entry["blocker_ids"]:
            raise ValueError(f"PASS gate {entry['gate']} cannot have blockers")
        if entry["status"] == "BLOCKED" and not entry["blocker_ids"]:
            raise ValueError(f"BLOCKED gate {entry['gate']} requires blockers")

    blockers = matrix["blockers"]
    if not isinstance(blockers, list):
        raise ValueError("blockers must be a list")
    blocker_by_id: dict[str, dict] = {}
    for blocker in blockers:
        entry = _require_exact_keys(blocker, BLOCKER_KEYS, "blocker")
        for key, value in entry.items():
            _require_nonempty_string(value, f"blocker.{key}")
        blocker_id = entry["blocker_id"]
        if blocker_id in blocker_by_id:
            raise ValueError(f"duplicate blocker_id: {blocker_id}")
        if entry["gate"] not in GATES:
            raise ValueError(f"unknown blocker gate: {entry['gate']}")
        blocker_by_id[blocker_id] = entry

    referenced_blockers: list[str] = []
    for gate in gates:
        for blocker_id in gate["blocker_ids"]:
            if blocker_id not in blocker_by_id:
                raise ValueError(f"unknown blocker reference: {blocker_id}")
            if blocker_by_id[blocker_id]["gate"] != gate["gate"]:
                raise ValueError(f"blocker {blocker_id} is assigned to the wrong gate")
            referenced_blockers.append(blocker_id)
    if len(referenced_blockers) != len(set(referenced_blockers)):
        raise ValueError("a blocker is referenced by more than one gate")
    if set(referenced_blockers) != set(blocker_by_id):
        raise ValueError("orphan or unreferenced blocker")

    _validate_reviewer_contract(matrix["reviewer_contract"])
    _require_string_list(matrix["reconsideration_sequence"], "reconsideration_sequence")
    _require_string_list(matrix["nonclaims"], "nonclaims")

    recorded = matrix["recorded_decision"]
    if recorded not in {"GO", "HOLD"}:
        raise ValueError("recorded_decision must be GO or HOLD")
    derived = _derived_decision_unchecked(matrix)
    if recorded != derived:
        raise ValueError(
            f"recorded_decision {recorded} does not match derived decision {derived}"
        )


def derive_decision(matrix: dict[str, object]) -> str:
    validate_matrix(matrix)
    return _derived_decision_unchecked(matrix)


def _table_text(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render(matrix: dict[str, object]) -> str:
    decision = derive_decision(matrix)
    contract = matrix["mapping_contract"]
    source = matrix["source_oracle"]
    rights = matrix["rights_review"]
    findings = matrix["review_findings"]
    reviewer_contract = matrix["reviewer_contract"]

    lines = [
        "# PCI DSS mapping readiness decision",
        "",
        f"**Decision:** `{decision}`",
        "",
        f"**Review identifier:** `{matrix['review_identifier']}`",
        "",
        (
            f"**Open findings:** Critical `{findings['open_critical']}`; "
            f"Important `{findings['open_important']}`"
        ),
        "",
        "The decision is derived from the closed readiness matrix. It is not an "
        "authorization to create a PCI DSS mapping.",
        "",
        "## Exact directional question",
        "",
        f"> {contract['directional_question']}",
        "",
        f"Direction: `{contract['direction']}`.",
        "",
        f"`{contract['excluded_direction']}` is excluded and requires a separate approved design.",
        "",
        f"Scope: `{contract['scope']}`.",
        "",
        f"Granularity: `{contract['granularity']}`.",
        "",
        "## Source boundary",
        "",
        f"- Source-readiness oracle: `{source['path']}`",
        f"- Source-readiness oracle SHA-256: `{source['sha256']}`",
        f"- Publication-rights review: `{rights['path']}`",
        f"- Publication-rights review commit: `{rights['commit']}`",
        (
            "- Positive feasibility probe available: "
            f"`{str(contract['positive_feasibility_probe']).lower()}`"
        ),
        "",
        "The protected PCI DSS source artifact, its digest, and its provision inventory "
        "remain unavailable. Public discovery metadata is not a substitute for source bytes.",
        "",
        "## Gate results",
        "",
        "| Gate | Status | Rationale | Evidence |",
        "|---|---|---|---|",
    ]
    for gate in matrix["gates"]:
        lines.append(
            f"| `{gate['gate']}` | `{gate['status']}` | "
            f"{_table_text(gate['rationale'])} | "
            f"{_table_text('; '.join(gate['evidence_references']))} |"
        )

    lines.extend(
        [
            "",
            "## Blockers",
            "",
            "| Blocker | Gate | Owner | Missing evidence | Reconsideration trigger | Re-entry test |",
            "|---|---|---|---|---|---|",
        ]
    )
    for blocker in matrix["blockers"]:
        lines.append(
            f"| `{blocker['blocker_id']}` | `{blocker['gate']}` | "
            f"{_table_text(blocker['owner'])} | "
            f"{_table_text(blocker['missing_evidence'])} | "
            f"{_table_text(blocker['reconsideration_trigger'])} | "
            f"{_table_text(blocker['reentry_test'])} |"
        )

    lines.extend(
        [
            "",
            "## Future mapper and reviewer requirements",
            "",
            "A future GO requires a named mapper with authorized source access and "
            "experience in PCI DSS v4.0.1 and ESAF-1600. The mapper may not review "
            "their own work.",
            "",
            "| Role | Independence | Qualification | Authorized source access |",
            "|---|---|---|---|",
        ]
    )
    for reviewer in reviewer_contract["reviewers"]:
        lines.append(
            f"| `{reviewer['role']}` | Independent from mapper | "
            f"{_table_text(reviewer['qualification'])} | Required |"
        )
    lines.extend(
        [
            "",
            "Each review record requires: "
            + ", ".join(
                f"`{requirement}`"
                for requirement in reviewer_contract["review_record_requirements"]
            )
            + ".",
            "",
            "The inventory/specification and security/overclaiming reviews shall be "
            "separate reviews of the same exact candidate SHA and artifact digests. "
            "Any candidate change requires redispatch of both reviews.",
            "",
            f"Approver: {reviewer_contract['approver']}.",
            "",
            "## Reconsideration sequence",
            "",
        ]
    )
    for index, item in enumerate(matrix["reconsideration_sequence"], start=1):
        lines.append(f"{index}. {item}")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in matrix["nonclaims"])
    lines.extend(
        [
            "",
            "## Final decision",
            "",
            f"`{decision}`. The blocked gates and their complete blocker records "
            "control re-entry. No mapping artifact may be created while this decision "
            "remains HOLD.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_matrix(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("matrix root must be an object")
    return value


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the mechanically derived PCI DSS readiness decision."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write the rendered review")
    mode.add_argument("--check", action="store_true", help="check the rendered review")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    try:
        matrix = _load_matrix(args.matrix)
        rendered = render(matrix)
        if args.write:
            _write_text(args.output, rendered)
            return 0
        if args.check:
            if not args.output.is_file():
                print(f"error: rendered review does not exist: {args.output}", file=sys.stderr)
                return 1
            if args.output.read_text(encoding="utf-8") != rendered:
                print(f"error: rendered review is stale: {args.output}", file=sys.stderr)
                return 1
            return 0
        sys.stdout.write(rendered)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
