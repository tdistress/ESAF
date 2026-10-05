from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = ROOT
DEFAULT_MATRIX = ROOT / "docs/superpowers/specs/2026-10-02-soc2-aicpa-tsc-mapping-readiness-matrix.json"
DEFAULT_OUTPUT = ROOT / "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-mapping-go-no-go-review.md"
RIGHTS_REVIEW_PATH = "docs/superpowers/reviews/2026-10-02-soc2-aicpa-tsc-publication-rights-review.md"
GATES = ("source_identity_and_drift", "authorized_source_artifact", "publication_rights", "provision_inventory", "semantic_and_normative_feasibility", "esaf_1600_and_schema_fit", "mapper_and_reviewer_readiness", "overclaiming_controls")
TOP_KEYS = {"blockers", "gates", "mapping_contract", "nonclaims", "reconsideration_sequence", "recorded_decision", "review_findings", "review_identifier", "reviewer_contract", "rights_review", "schema_version", "source_oracle"}
GATE_KEYS = {"blocker_ids", "evidence_references", "gate", "rationale", "status"}
BLOCKER_KEYS = {"blocker_id", "category", "gate", "missing_evidence", "owner", "reconsideration_trigger", "reentry_test", "remediation"}
CONTRACT_KEYS = {"direction", "excluded_direction", "directional_question", "granularity", "positive_feasibility_probe", "scope"}
EVIDENCE_CONTRACT_KEYS = {"direction", "excluded_direction", "directional_question", "granularity", "evidence_manifest", "mapper_identity", "scope"}
MANIFEST_PATH = "docs/superpowers/specs/2026-10-05-soc2-aicpa-tsc-evidence-manifest.json"
MANIFEST_KEYS = {"schema_version", "feasibility", "evidence_inputs", "evidence_subject_sha256", "review"}
FEASIBILITY_KEYS = {"blocker_ids", "method", "rationale", "scope", "status"}
REVIEW_KEYS = {"attestations", "blocker_ids", "participants", "rationale", "status"}
ATTESTATION_KEYS = {"identity", "role", "qualification", "authorized_source_access", "independence", "conflict_disposition", "review_date", "disposition", "evidence_subject_sha256", "findings"}
PARTICIPANT_KEYS = {"identity", "role", "qualification", "qualification_evidence", "authorized_source_access", "source_access_evidence", "independent_from_mapper", "owner_approved", "owner_approval_reference", "conflict_disposition"}
INPUT_KEYS = {"category", "path", "sha256"}
REVIEWER_ROLES = {"inventory_and_specification", "security_and_overclaiming"}
PARTICIPANT_ROLES = {"mapper", "aicpa_tsc_subject_matter", "esaf_specification_and_mapping", "publication_rights", "security_and_overclaiming", "owner_authorized_approver"}
ROLE_QUALIFICATIONS = {
    "mapper": {"2017 Trust Services Criteria with Revised Points of Focus – 2022", "ESAF-1600"},
    "aicpa_tsc_subject_matter": {"Owner-approved Trust Services Criteria subject-matter reviewer"},
    "esaf_specification_and_mapping": {"Independent ESAF specification and mapping reviewer"},
    "publication_rights": {"Independent publication-rights reviewer"},
    "security_and_overclaiming": {"Independent security and overclaiming reviewer"},
    "owner_authorized_approver": {"An approver authorized by the ESAF project owner"},
}
MAPPER_EXPERIENCE = ROLE_QUALIFICATIONS["mapper"]
INPUT_CATEGORIES = {"source", "inventory", "probe"}
CONFLICT_DISPOSITIONS = {"none", "resolved", "mitigated"}
SUBJECT_PATHS = {"matrix.json", DEFAULT_MATRIX.as_posix(), MANIFEST_PATH, DEFAULT_OUTPUT.relative_to(ROOT).as_posix()}
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


def _participant_evidence_reference(value, label, repository_root):
    if not isinstance(value, dict) or set(value) not in ({"path", "sha256"}, {"uri", "sha256"}):
        raise ValueError(f"{label} must be a digest-pinned repository path or HTTPS URI")
    digest = value["sha256"]
    if not isinstance(digest, str) or not SHA.fullmatch(digest):
        raise ValueError(f"{label} SHA-256 is invalid")
    if "uri" in value:
        uri = value["uri"]
        if not isinstance(uri, str):
            raise ValueError(f"{label} URI must be a nonempty HTTPS address")
        parsed = urlsplit(uri)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or
                parsed.query or not uri.strip() or any(character.isspace() for character in uri)):
            raise ValueError(f"{label} URI must be HTTPS without credentials or query parameters")
        return
    raw_path = value["path"]
    if (not isinstance(raw_path, str) or not raw_path or raw_path.startswith("/") or "\\" in raw_path or
            any(part in {"", ".", ".."} for part in raw_path.split("/"))):
        raise ValueError(f"{label} path must be repository-relative POSIX")
    normalized = posixpath.normpath(raw_path)
    if not normalized.startswith("participant-evidence/") or normalized in SUBJECT_PATHS:
        raise ValueError(f"{label} path is outside the participant-evidence allowlist")
    root = Path(repository_root).resolve()
    path = root
    for component in normalized.split("/"):
        path = path / component
        if path.is_symlink():
            raise ValueError(f"{label} path cannot contain symlinks")
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} path escapes the repository") from exc
    if not resolved.is_file() or hashlib.sha256(resolved.read_bytes()).hexdigest() != digest:
        raise ValueError(f"{label} evidence file is absent or its digest is stale")


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
    if not isinstance(source_oracle, dict):
        raise ValueError("source oracle must be a JSON object")
    rights = _exact(matrix["rights_review"], {"commit", "path", "sha256"}, "rights_review")
    if rights["path"] != RIGHTS_REVIEW_PATH:
        raise ValueError("rights_review.path must be the canonical publication-rights review")
    if not isinstance(rights["commit"], str) or not COMMIT.fullmatch(rights["commit"]) or not isinstance(rights["sha256"], str) or not SHA.fullmatch(rights["sha256"]):
        raise ValueError("rights review commit or SHA-256 is invalid")
    contract = matrix["mapping_contract"]
    if isinstance(contract, dict) and "evidence_manifest" in contract:
        contract = _exact(contract, EVIDENCE_CONTRACT_KEYS, "mapping_contract")
    else:
        contract = _exact(contract, CONTRACT_KEYS, "mapping_contract")
    if contract["direction"] != "esaf_to_external" or contract["excluded_direction"] != "external_to_esaf" or contract["scope"] != "complete_publication":
        raise ValueError("mapping direction or scope is invalid")
    for field in ("directional_question", "granularity"):
        if not isinstance(contract[field], str) or not contract[field].strip():
            raise ValueError(f"mapping_contract.{field} must be nonempty")
    if "positive_feasibility_probe" in contract and not isinstance(contract["positive_feasibility_probe"], bool):
        raise ValueError("positive_feasibility_probe must be boolean")
    if "evidence_manifest" in contract:
        ref = _exact(contract["evidence_manifest"], {"path", "sha256"}, "evidence_manifest")
        if (not isinstance(ref["path"], str) or
                (ref["path"] != MANIFEST_PATH and not (ROOT.resolve() != CODE_ROOT.resolve() and ref["path"] == "evidence/manifest.json")) or
                not isinstance(ref["sha256"], str) or not SHA.fullmatch(ref["sha256"])):
            raise ValueError("evidence manifest path or SHA-256 is invalid")
        if not isinstance(contract["mapper_identity"], str) or not contract["mapper_identity"].strip():
            raise ValueError("mapper_identity must be nonempty")
    findings = _exact(matrix["review_findings"], {"open_critical", "open_important"}, "review_findings")
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 0 for n in findings.values()):
        raise ValueError("review findings must be nonnegative integers")
    gates = matrix["gates"]
    if not isinstance(gates, list) or [g.get("gate") if isinstance(g, dict) else None for g in gates] != list(GATES):
        raise ValueError("gate order is invalid")
    for raw in gates:
        gate = _exact(raw, GATE_KEYS, f"gate {raw.get('gate')}")
        if not isinstance(gate["status"], str) or gate["status"] not in {"PASS", "BLOCKED"}:
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
        if (not isinstance(blocker["gate"], str) or blocker["gate"] not in GATES or
                not isinstance(blocker["remediation"], str) or blocker["remediation"] not in {"reconsiderable", "terminal"}):
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
        derived = "GO" if not blockers and contract.get("positive_feasibility_probe", True) and not findings["open_critical"] and not findings["open_important"] else None
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
    elif matrix["recorded_decision"] == "GO":
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
        if any(not isinstance(section, dict) for section in (artifact, access, inventory, boundary)):
            raise ValueError("GO requires structured source-oracle evidence")
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
        if "evidence_manifest" not in contract:
            raise ValueError("GO is disabled in schema 1.0.0 until digest-bound feasibility and exact-candidate reviewer attestations are supported")
    return None


def _subject_digest(feasibility, inputs, participants):
    pairs = [{"path": posixpath.normpath(item["path"]), "sha256": item["sha256"]} for item in inputs]
    pairs.sort(key=lambda item: item["path"])
    roster = sorted(participants, key=lambda participant: participant["role"])
    payload = json.dumps({"feasibility": feasibility, "inputs": pairs, "participants": roster}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _normalized_input_path(value, root, category):
    if not isinstance(value, str) or not value or "\\" in value or value.startswith("/"):
        raise ValueError("evidence input path must be repository-relative POSIX")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("evidence input path contains unsafe components")
    normalized = posixpath.normpath(value)
    if normalized in SUBJECT_PATHS or normalized.endswith(("mapping-readiness-matrix.json", "evidence-manifest.json", "mapping-go-no-go-review.md")):
        raise ValueError("forbidden evidence input dependency path")
    allowed = {"source": ("source/",), "inventory": ("inventory/",), "probe": ("probe/",)}
    if not isinstance(category, str) or category not in INPUT_CATEGORIES or not normalized.startswith(allowed[category]):
        raise ValueError("evidence input path is outside its category allowlist")
    category_root = root / category
    if category_root.is_symlink():
        raise ValueError("evidence input category root cannot be a symlink")
    try:
        resolved = (root / normalized).resolve()
        repository_root = root.resolve()
        resolved_category_root = category_root.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError("evidence input path contains an invalid symlink") from exc
    try:
        resolved.relative_to(repository_root)
    except ValueError as exc:
        raise ValueError("evidence input path escapes repository root") from exc
    try:
        resolved.relative_to(resolved_category_root)
    except ValueError as exc:
        raise ValueError("evidence input target escapes its category allowlist") from exc
    if not resolved.is_file():
        raise ValueError("evidence input path is absent or not a file")
    return normalized, resolved


def validate_manifest(manifest, matrix, *, repository_root=ROOT, mapper_identity=None):
    _exact(manifest, MANIFEST_KEYS, "manifest")
    _exact(matrix, TOP_KEYS, "matrix")
    if (not isinstance(matrix["gates"], list) or
            [gate.get("gate") if isinstance(gate, dict) else None for gate in matrix["gates"]] != list(GATES)):
        raise ValueError("matrix gate collection has an invalid shape or order")
    if not isinstance(matrix["mapping_contract"], dict):
        raise ValueError("matrix.mapping_contract must be an object")
    contract = _exact(matrix["mapping_contract"], EVIDENCE_CONTRACT_KEYS, "mapping_contract")
    if not isinstance(contract["mapper_identity"], str) or not contract["mapper_identity"].strip():
        raise ValueError("mapper_identity must be nonempty")
    if manifest["schema_version"] != "1.0.0":
        raise ValueError("unsupported manifest schema_version")
    feasibility = _exact(manifest["feasibility"], FEASIBILITY_KEYS, "feasibility")
    review = _exact(manifest["review"], REVIEW_KEYS, "review")
    if (not isinstance(feasibility["status"], str) or feasibility["status"] not in {"not_evidenced", "positive"} or
            not isinstance(review["status"], str) or review["status"] not in {"not_completed", "complete"}):
        raise ValueError("unsupported feasibility or review status")
    if (feasibility["status"], review["status"]) not in {("not_evidenced", "not_completed"), ("positive", "complete")}:
        raise ValueError("feasibility and review states must be paired consistently")
    for label, obj in (("feasibility", feasibility), ("review", review)):
        for field in (("method", "rationale", "scope") if label == "feasibility" else ("rationale",)):
            if not isinstance(obj[field], str) or not obj[field].strip():
                raise ValueError(f"{label}.{field} must be nonempty")
    inputs = manifest["evidence_inputs"]
    if not isinstance(inputs, list):
        raise ValueError("evidence_inputs must be a list")
    normalized_inputs = []
    seen = set()
    for item in inputs:
        item = _exact(item, INPUT_KEYS, "evidence input")
        if not isinstance(item["sha256"], str) or not SHA.fullmatch(item["sha256"]):
            raise ValueError("evidence input SHA-256 digest is invalid")
        raw_path = item["path"]
        if isinstance(raw_path, str) and posixpath.normpath(raw_path) in seen:
            raise ValueError("duplicate normalized evidence input path")
        normalized, path = _normalized_input_path(item["path"], Path(repository_root), item["category"])
        if normalized in seen:
            raise ValueError("duplicate normalized evidence input path")
        seen.add(normalized)
        if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            raise ValueError("evidence input digest is stale")
        normalized_inputs.append({"category": item["category"], "path": normalized, "sha256": item["sha256"]})
    if feasibility["status"] == "not_evidenced":
        _strings(feasibility["blocker_ids"], "feasibility.blocker_ids")
        if inputs:
            raise ValueError("not_evidenced feasibility requires empty inputs and nonempty blockers")
    else:
        _strings(feasibility["blocker_ids"], "feasibility.blocker_ids", empty=True)
        if not inputs:
            raise ValueError("positive feasibility requires evidence inputs")
    if review["status"] == "not_completed":
        _strings(review["blocker_ids"], "review.blocker_ids")
        if (not isinstance(review["attestations"], list) or review["attestations"] or
                not isinstance(review["participants"], list) or review["participants"]):
            raise ValueError("not_completed review requires empty attestations and participant roster with nonempty blockers")
    else:
        _strings(review["blocker_ids"], "review.blocker_ids", empty=True)
        if (not isinstance(review["attestations"], list) or len(review["attestations"]) != 2 or
                not isinstance(review["participants"], list) or len(review["participants"]) != len(PARTICIPANT_ROLES)):
            raise ValueError("complete review requires two reviewer attestations and the complete B005 participant roster")
    digest = _subject_digest(feasibility, inputs, review["participants"])
    if not isinstance(manifest["evidence_subject_sha256"], str) or manifest["evidence_subject_sha256"] != digest:
        raise ValueError("evidence subject digest is stale")
    if review["status"] == "complete":
        participants, participant_ids = {}, set()
        for raw in review["participants"]:
            participant = _exact(raw, PARTICIPANT_KEYS, "review participant")
            role = participant["role"]
            if not isinstance(role, str) or role not in PARTICIPANT_ROLES or role in participants:
                raise ValueError("B005 participant roles must be distinct and complete")
            for field in ("identity",):
                if not isinstance(participant[field], str) or not participant[field].strip():
                    raise ValueError(f"participant {field} must be nonempty")
            qualifications = set(_strings(participant["qualification"], "participant qualification"))
            if qualifications != ROLE_QUALIFICATIONS[role]:
                raise ValueError(f"participant qualification does not match the B005 {role} role")
            for field in ("qualification_evidence", "source_access_evidence"):
                references = participant[field]
                if not isinstance(references, list) or not references:
                    raise ValueError(f"participant {field} must be a nonempty list of evidence references")
                canonical_references = [json.dumps(reference, sort_keys=True) for reference in references]
                if len(canonical_references) != len(set(canonical_references)):
                    raise ValueError(f"participant {field} evidence references must be unique")
                for reference in references:
                    _participant_evidence_reference(reference, f"participant {field}", repository_root)
            identity = participant["identity"].strip().casefold()
            if identity in participant_ids:
                raise ValueError("B005 participants must be distinct people")
            participant_ids.add(identity)
            if participant["authorized_source_access"] is not True:
                raise ValueError("every B005 participant requires authorized source access")
            if participant["independent_from_mapper"] is not (role != "mapper"):
                raise ValueError("B005 reviewer and approver roles must be independent from the mapper")
            if participant["owner_approved"] is not (role in {"aicpa_tsc_subject_matter", "owner_authorized_approver"}):
                raise ValueError("AICPA subject-matter reviewer and owner-authorized approver require owner approval")
            if role in {"aicpa_tsc_subject_matter", "owner_authorized_approver"}:
                reference = participant["owner_approval_reference"]
                if reference is None:
                    raise ValueError("owner-approved B005 roles require an owner approval evidence reference")
                _participant_evidence_reference(reference, "participant owner_approval_reference", repository_root)
            elif participant["owner_approval_reference"] is not None:
                raise ValueError("owner_approval_reference is only allowed for owner-approved B005 roles")
            if not isinstance(participant["conflict_disposition"], str) or participant["conflict_disposition"] not in CONFLICT_DISPOSITIONS:
                raise ValueError("participant conflict disposition must be an allowed resolved state")
            participants[role] = participant
        if set(participants) != PARTICIPANT_ROLES:
            raise ValueError("complete review requires all six B005 participant roles")
        if participants["mapper"]["identity"].strip().casefold() != contract["mapper_identity"].strip().casefold():
            raise ValueError("matrix mapper_identity must match the named B005 mapper participant")
        expected_attestation_people = {
            "inventory_and_specification": "esaf_specification_and_mapping",
            "security_and_overclaiming": "security_and_overclaiming",
        }
        roles, identities = set(), set()
        for raw in review["attestations"]:
            att = _exact(raw, ATTESTATION_KEYS, "attestation")
            if not isinstance(att["role"], str) or att["role"] not in REVIEWER_ROLES or att["role"] in roles:
                raise ValueError("reviewer roles must be distinct and complete")
            roles.add(att["role"])
            for field in ("identity", "qualification"):
                if not isinstance(att[field], str) or not att[field].strip():
                    raise ValueError(f"attestation {field} must be nonempty")
            identity = att["identity"].strip().casefold()
            if identity in identities or (mapper_identity and identity == mapper_identity.strip().casefold()):
                raise ValueError("reviewer identity must be distinct and independent from mapper")
            roster_role = expected_attestation_people.get(att["role"])
            if roster_role is None or participants[roster_role]["identity"].strip().casefold() != identity:
                raise ValueError("exact-subject review identity must match its B005 participant roster role")
            identities.add(identity)
            if att["authorized_source_access"] is not True or att["independence"] is not True:
                raise ValueError("reviewer access and independence must be affirmative")
            if not isinstance(att["conflict_disposition"], str) or att["conflict_disposition"] not in CONFLICT_DISPOSITIONS:
                raise ValueError("reviewer conflict disposition must be an allowed resolved state")
            try:
                date.fromisoformat(att["review_date"])
            except (TypeError, ValueError) as exc:
                raise ValueError("review_date must be a valid ISO date") from exc
            if (not isinstance(att["disposition"], str) or att["disposition"] not in {"PASS", "PASS_WITH_NOTES"} or
                    att["evidence_subject_sha256"] != digest):
                raise ValueError("reviewer disposition or subject digest is invalid")
            findings = _exact(att["findings"], {"open_critical", "open_important"}, "attestation findings")
            if any(type(v) is not int or v < 0 for v in findings.values()) or findings["open_critical"] or findings["open_important"]:
                raise ValueError("open Critical or Important reviewer findings prevent completion")
        if roles != REVIEWER_ROLES:
            raise ValueError("required reviewer roles are incomplete")
    if "evidence_manifest" not in matrix["mapping_contract"]:
        raise ValueError("matrix must pin an evidence manifest")
    ref = matrix["mapping_contract"]["evidence_manifest"]
    ref = _exact(ref, {"path", "sha256"}, "evidence_manifest")
    if not isinstance(ref["path"], str) or not isinstance(ref["sha256"], str) or not SHA.fullmatch(ref["sha256"]):
        raise ValueError("evidence manifest path or SHA-256 is invalid")
    manifest_path = (Path(repository_root) / ref["path"]).resolve()
    try:
        manifest_path.relative_to(Path(repository_root).resolve())
    except ValueError as exc:
        raise ValueError("manifest path escapes repository") from exc
    if not manifest_path.is_file() or hashlib.sha256(manifest_path.read_bytes()).hexdigest() != ref["sha256"]:
        raise ValueError("matrix-pinned manifest digest is stale")
    try:
        pinned_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("matrix-pinned manifest cannot be read as JSON") from exc
    if pinned_manifest != manifest:
        raise ValueError("manifest object differs from matrix-pinned manifest bytes")
    # State and blocker IDs are derived from evidence, never matrix labels.
    gates = {g["gate"]: g for g in matrix["gates"]}
    if feasibility["status"] == "not_evidenced":
        if gates["semantic_and_normative_feasibility"]["status"] != "BLOCKED" or set(feasibility["blocker_ids"]) != set(gates["semantic_and_normative_feasibility"]["blocker_ids"]):
            raise ValueError("feasibility blockers must exactly cover the blocked matrix gate")
    elif gates["semantic_and_normative_feasibility"]["status"] != "PASS":
        raise ValueError("positive feasibility requires its matrix gate to pass")
    if review["status"] == "not_completed":
        if gates["mapper_and_reviewer_readiness"]["status"] != "BLOCKED" or set(review["blocker_ids"]) != set(gates["mapper_and_reviewer_readiness"]["blocker_ids"]):
            raise ValueError("review blockers must exactly cover the blocked matrix gate")
    elif gates["mapper_and_reviewer_readiness"]["status"] != "PASS":
        raise ValueError("complete reviews require the matrix reviewer gate to pass")
    return feasibility["status"]


def derive_decision(matrix, *, manifest=None, repository_root=ROOT, verify_source_digest=True):
    contract = matrix.get("mapping_contract") if isinstance(matrix, dict) else None
    if not isinstance(contract, dict) or "evidence_manifest" not in contract:
        raise ValueError("matrix must pin an evidence manifest before deriving a decision")
    if manifest is None and isinstance(contract, dict) and "evidence_manifest" in contract:
        ref = _exact(contract["evidence_manifest"], {"path", "sha256"}, "evidence_manifest")
        if not isinstance(ref["path"], str) or not isinstance(ref["sha256"], str) or not SHA.fullmatch(ref["sha256"]):
            raise ValueError("evidence manifest path or SHA-256 is invalid")
        if ref["path"] != MANIFEST_PATH and not (ROOT.resolve() != CODE_ROOT.resolve() and ref["path"] == "evidence/manifest.json"):
            raise ValueError("evidence manifest path is not canonical")
        manifest_path = Path(repository_root) / ref["path"]
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError("matrix-pinned manifest cannot be read as JSON") from exc
    if manifest is not None:
        validate_manifest(manifest, matrix, repository_root=repository_root, mapper_identity=matrix["mapping_contract"].get("mapper_identity"))
    validate_matrix(matrix, verify_source_digest=verify_source_digest)
    return matrix["recorded_decision"]


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render(matrix):
    decision = derive_decision(matrix, repository_root=ROOT)
    ref = matrix["mapping_contract"]["evidence_manifest"]
    manifest_path = ROOT / ref["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lines = ["# SOC 2 AICPA TSC mapping readiness decision", "", f"**Decision:** `{decision}`", "", f"**Review identifier:** `{matrix['review_identifier']}`", "", "The decision is mechanically derived from the closed readiness matrix.", "", "## Evidence manifest", "", f"- Manifest: `{ref['path']}`", f"- Pinned SHA-256: `{ref['sha256']}`", f"- Feasibility: `{manifest['feasibility']['status']}`", f"- Review: `{manifest['review']['status']}`", f"- Evidence subject SHA-256: `{manifest['evidence_subject_sha256']}`", "", "## Directional question", "", f"> {matrix['mapping_contract']['directional_question']}", "", "## Gate results", "", "| Gate | Status | Rationale | Evidence |", "|---|---|---|---|"]
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
