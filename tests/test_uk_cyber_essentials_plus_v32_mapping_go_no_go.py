from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-rights-re-attestation.md"
MATRIX = ROOT / "docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json"
REVIEW = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md"
ORACLE_SHA256 = "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc"
PRIOR_RIGHTS_COMMIT = "6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6"
REVIEW_IDENTIFIER = "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--mapping-feasibility--0.1.0"
FIELD_CLASSES = (
    "source_oracle_identity",
    "provision_identifiers_and_structural_classifications",
    "original_probe_selection_rationales",
    "derivative_mapping_analysis",
    "esaf_normative_citations",
    "assurance_and_overclaiming_analysis",
    "official_links",
    "directional_gate_and_decision_metadata",
)
DIRECTIONS = ("esaf_to_external", "external_to_esaf")
DISPOSITIONS = {"GO", "HOLD", "NO_GO"}
GATES = ("source", "rights", "semantic", "normative_basis", "schema", "overclaiming", "utility")
GATE_STATUSES = {"PASS", "BLOCKED", "FAIL"}
GROUPS = ("M", "T1", "S", "T2", "T3", "T4", "T5", "C", "A", "B")
KINDS = (
    "applicability", "prerequisite", "procedure_step", "decision_rule",
    "result_rule", "evidence_retention", "recommendation",
)
ACTORS = ("Assessor", "Applicant", "Certification Body", "Certifying Body", "Delivery Partner")
SCENARIOS = (
    "figure-1-decision-logic",
    "sampling-and-population-limits",
    "evidence-retention",
    "complete-assessment-file-coverage",
    "delivery-partner-discretionary-exception",
    "known-source-anomaly",
    "point-in-time-versus-continuous-assurance",
    "core-v3.3-versus-plus-v3.2-separation",
    "expected-no-direct-esaf-basis",
)
PROBE_CONCLUSIONS = {"POSITIVE_FEASIBILITY", "NO_POSITIVE_BASIS", "INDETERMINATE"}
CONDITION_STATUSES = {"SATISFIED", "NOT_APPLICABLE"}
EXTERNAL_TO_ESAF_CONDITIONS = (
    "actor", "scope", "population", "sample", "assessment_date", "evidence_date",
    "tool", "provenance", "exception", "delivery_partner_discretion",
    "point_in_time_status",
)
PROHIBITED_KEYS = {
    "relationship", "relationships", "coverage", "confidence", "mapping_disposition",
    "snapshot_digest", "lifecycle", "mapper", "approver",
}
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
UTC_ISO_8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
SCENARIO_EVIDENCE = {
    "figure-1-decision-logic": {
        "required": {"CEPTS3.2-T1-008"},
        "one_of": set(),
        "paths": set(),
    },
    "sampling-and-population-limits": {
        "required": set(),
        "one_of": {"CEPTS3.2-M-006", "CEPTS3.2-S-005", "CEPTS3.2-S-007", "CEPTS3.2-S-009"},
        "paths": {"assurance_limits.population_and_sample_boundary"},
    },
    "evidence-retention": {
        "required": set(),
        "one_of": {"CEPTS3.2-M-011", "CEPTS3.2-S-008"},
        "paths": {"assurance_limits.evidence_date_boundary"},
    },
    "complete-assessment-file-coverage": {
        "required": {"CEPTS3.2-B-001"},
        "one_of": {"CEPTS3.2-B-007", "CEPTS3.2-B-010", "CEPTS3.2-B-011", "CEPTS3.2-B-012"},
        "paths": set(),
    },
    "delivery-partner-discretionary-exception": {
        "required": {"CEPTS3.2-C-008", "CEPTS3.2-C-010", "CEPTS3.2-C-011"},
        "one_of": set(),
        "paths": {"assurance_limits.discretion_owner", "assurance_limits.discretionary_exception"},
    },
    "known-source-anomaly": {
        "required": set(),
        "one_of": set(),
        "paths": {"known_anomalies[0].anomaly_id", "known_anomalies[0].locator"},
    },
    "point-in-time-versus-continuous-assurance": {
        "required": set(),
        "one_of": set(),
        "paths": {
            "assurance_limits.assessment_date_boundary",
            "assurance_limits.evidence_date_boundary",
            "assurance_limits.point_in_time_boundary",
        },
    },
    "core-v3.3-versus-plus-v3.2-separation": {
        "required": set(),
        "one_of": set(),
        "paths": {"scope", "assurance_limits.scope_boundary"},
    },
    "expected-no-direct-esaf-basis": {
        "required": set(),
        "one_of": set(),
        "paths": set(),
    },
}


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def assert_exact_keys(
    test: unittest.TestCase,
    obj: dict,
    expected: set[str],
    context: str,
) -> None:
    test.assertEqual(expected, set(obj), context)


def recursive_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            key
            for child in value.values()
            for key in recursive_keys(child)
        }
    if isinstance(value, list):
        return {
            key
            for child in value
            for key in recursive_keys(child)
        }
    return set()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def direction_content_sha256(matrix: dict, direction: str) -> str:
    assessment = next(
        item for item in matrix["direction_assessments"]
        if item["direction"] == direction
    )
    value = {
        "direction_assessment": assessment,
        "probes": [
            probe for probe in matrix["probes"]
            if probe["direction"] == direction
        ],
    }
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def submission_payload_sha256(matrix: dict, direction: str) -> str:
    submission = next(
        item for item in matrix["analysis_provenance"]["submissions"]
        if item["direction"] == direction
    )
    assessment = next(
        item for item in matrix["direction_assessments"]
        if item["direction"] == direction
    )
    payload = {
        "direction": direction,
        "analyst": submission["analyst"],
        "direction_assessment": assessment,
        "probes": [p for p in matrix["probes"] if p["direction"] == direction],
        "no_output_file_attestation": True,
        "no_sibling_content_attestation": True,
    }
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def derive_coverage(matrix: dict, direction: str) -> dict[str, set[str]]:
    selected = [probe for probe in matrix["probes"] if probe["direction"] == direction]
    return {
        "groups": {value for probe in selected for value in probe["groups"]},
        "kinds": {value for probe in selected for value in probe["kinds"]},
        "actors": {value for probe in selected for value in probe["actors"]},
        "special_scenarios": {
            binding["scenario_id"]
            for probe in selected
            for binding in probe["special_scenario_bindings"]
        },
    }


def expected_disposition(
    assessment: dict,
    probes_by_id: dict[str, dict],
) -> str:
    statuses = {gate["status"] for gate in assessment["gate_results"]}
    derived_positive = [
        probe_id
        for probe_id, probe in probes_by_id.items()
        if probe["direction"] == assessment["direction"]
        and probe["conclusion"] == "POSITIVE_FEASIBILITY"
    ]
    if derived_positive != assessment["positive_probe_identifiers"]:
        raise ValueError("positive_probe_identifiers do not equal derived positive probes")
    if "FAIL" in statuses:
        return "NO_GO"
    if "BLOCKED" in statuses:
        return "HOLD"
    return "GO" if derived_positive else "NO_GO"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def resolve_oracle_path(oracle: dict, path: str) -> object:
    if path == "scope":
        return oracle["scope"]
    provision = re.fullmatch(r"provisions\[([^]]+)\]\.(external_provision_id|summary|locator)", path)
    if provision:
        item = next(
            entry for entry in oracle["provisions"]
            if entry["external_provision_id"] == provision.group(1)
        )
        return item[provision.group(2)]
    anomaly = re.fullmatch(r"known_anomalies\[0\]\.(anomaly_id|locator)", path)
    if anomaly:
        return oracle["known_anomalies"][0][anomaly.group(1)]
    assurance = re.fullmatch(r"assurance_limits\.([a-z_]+)", path)
    if assurance and assurance.group(1) in oracle["assurance_limits"]:
        return oracle["assurance_limits"][assurance.group(1)]
    raise KeyError(path)


def parse_rights_record(text: str) -> dict[str, object]:
    def field(label: str) -> str:
        match = re.search(rf"(?m)^\*\*{re.escape(label)}:\*\*\s*(?:`([^`]+)`|(.+))$", text)
        if not match:
            raise ValueError(f"missing rights record field: {label}")
        return (match.group(1) or match.group(2)).strip()

    section = text.split("## Approved field classes", 1)[1].split("## ", 1)[0]
    return {
        "reviewer": field("Reviewer"),
        "review_date": field("Review date"),
        "prior_rights_commit": field("Prior rights commit"),
        "oracle_sha256": field("Oracle SHA-256"),
        "iasme_partition_preserved": field("IASME partition preserved").lower() == "yes",
        "copied_source_prohibition_preserved": field("Copied-source prohibition preserved").lower() == "yes",
        "disposition": field("Disposition").lower(),
        "field_classes_reviewed": re.findall(r"(?m)^- `([^`]+)`$", section),
    }


def validate_rights_binding(matrix: dict, rights_text: str) -> None:
    record = parse_rights_record(rights_text)
    rights = matrix["rights_re_attestation"]
    bound_fields = (
        "reviewer", "review_date", "prior_rights_commit", "oracle_sha256",
        "iasme_partition_preserved", "copied_source_prohibition_preserved",
        "field_classes_reviewed", "disposition",
    )
    if any(rights.get(key) != record[key] for key in bound_fields):
        raise ValueError("rights record mismatch")
    analyst_roles = {
        matrix["roles"]["esaf_to_external_analyst"],
        matrix["roles"]["external_to_esaf_analyst"],
    }
    if rights["reviewer"] in analyst_roles:
        raise ValueError("rights reviewer is not independent")


def validate_nonempty_contract_strings(value: object, path: str = "matrix") -> None:
    if value is None:
        raise ValueError(f"empty required value at {path}")
    if isinstance(value, str):
        if not value.strip():
            raise ValueError(f"empty required string at {path}")
    elif isinstance(value, dict):
        for key, child in value.items():
            validate_nonempty_contract_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_nonempty_contract_strings(child, f"{path}[{index}]")


def validate_missing_outcomes(probes: list[dict]) -> None:
    for probe in probes:
        if probe["conclusion"] != "NO_POSITIVE_BASIS":
            continue
        match = re.search(r"(?i)\bmissing outcome:\s*(\S(?:.*\S)?)", probe["rationale"])
        if not match:
            raise ValueError(f"{probe['probe_id']} must name a nonempty missing outcome")


def markdown_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", text):
        anchor = re.sub(r"[^a-z0-9 -]", "", heading.lower())
        anchors.add(re.sub(r"[ -]+", "-", anchor).strip("-"))
    return anchors


def approved_official_urls(oracle: dict) -> set[str]:
    return {
        oracle["source"]["resource_page_url"],
        oracle["rights"]["licence_url"],
        *(variant["url"] for variant in oracle["source"]["variants"]),
    }


def validate_evidence_reference(reference: str, probe_ids: set[str], oracle: dict) -> None:
    if reference in probe_ids:
        return
    if reference in approved_official_urls(oracle):
        return
    path_text, separator, locator = reference.partition("#")
    if not separator or not path_text or not locator:
        raise ValueError(f"invalid evidence reference: {reference}")
    path = (ROOT / path_text).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError(f"invalid evidence reference: {reference}") from error
    if not path.is_file():
        raise ValueError(f"invalid evidence reference: {reference}")
    if path.suffix.lower() == ".md":
        if locator not in markdown_anchors(path.read_text(encoding="utf-8")):
            raise ValueError(f"invalid evidence reference: {reference}")
        return
    if path == ORACLE.resolve():
        try:
            resolve_oracle_path(oracle, locator)
        except (KeyError, StopIteration) as error:
            raise ValueError(f"invalid evidence reference: {reference}") from error
        return
    raise ValueError(f"invalid evidence reference: {reference}")


def validate_scenario_binding(probe: dict, binding: dict, oracle: dict) -> None:
    scenario = binding["scenario_id"]
    if scenario not in SCENARIO_EVIDENCE:
        raise ValueError(f"unknown scenario: {scenario}")
    ids = set(binding["provision_ids"])
    paths = set(binding["oracle_paths"])
    if not ids or not ids <= set(probe["provision_ids"]) or not paths:
        raise ValueError(f"invalid {scenario} binding")
    for path in paths:
        try:
            resolve_oracle_path(oracle, path)
        except (KeyError, StopIteration) as error:
            raise ValueError(f"invalid {scenario} oracle path: {path}") from error
        match = re.match(r"provisions\[([^]]+)\]", path)
        if match and match.group(1) not in ids:
            raise ValueError(f"unbound provision path in {scenario}: {path}")
    contract = SCENARIO_EVIDENCE[scenario]
    if not contract["required"] <= ids:
        raise ValueError(f"{scenario} is missing required provisions")
    if contract["one_of"] and not contract["one_of"] & ids:
        raise ValueError(f"{scenario} is missing an alternative provision")
    if not contract["paths"] <= paths:
        raise ValueError(f"{scenario} is missing required oracle paths")
    if scenario == "figure-1-decision-logic":
        ids_required = {"CEPTS3.2-T1-008", *(f"CEPTS3.2-T1-{number:03d}" for number in range(9, 17))}
        if not ids_required <= ids:
            raise ValueError("figure-1-decision-logic is incomplete")
    for provision_id in ids:
        if f"provisions[{provision_id}].external_provision_id" not in paths:
            raise ValueError(f"{scenario} lacks bound provision identity path")
    if scenario == "known-source-anomaly":
        if resolve_oracle_path(oracle, "known_anomalies[0].anomaly_id") != "cepts32-anomaly-001":
            raise ValueError("known-source-anomaly identity mismatch")
    if scenario == "expected-no-direct-esaf-basis":
        if probe["conclusion"] != "NO_POSITIVE_BASIS":
            raise ValueError("expected-no-direct-esaf-basis requires NO_POSITIVE_BASIS")
        for provision_id in ids:
            if not {
                f"provisions[{provision_id}].summary",
                f"provisions[{provision_id}].locator",
            } <= paths:
                raise ValueError("expected-no-direct-esaf-basis lacks summary and locator")


def validate_probe_scenario_bindings(probe: dict, oracle: dict) -> None:
    labels = probe["special_scenarios"]
    bindings = probe["special_scenario_bindings"]
    if labels != [binding["scenario_id"] for binding in bindings] or len(labels) != len(set(labels)):
        raise ValueError("scenario labels and bindings disagree")
    for binding in bindings:
        validate_scenario_binding(probe, binding, oracle)


TESTING_POSITIVE_GRAMMAR = (
    r"(?:assessment|test(?:ing)?)\s+(?:"
    r"(?:has|had|is|was)\s+(?:(?:[a-z]+ly|very|and)\s+)*"
    r"(?:been\s+)?(?:(?:[a-z]+ly|very|and)\s+)*(?:pass(?:ed|es)?|successful)"
    r"|(?:(?:[a-z]+ly|very|and)\s+)*(?:pass(?:ed|es)?|succeed(?:ed|s)?|successful)"
    r"|completed\s+successfully"
    r"|(?:achieved|constitutes|resulted\s+in)\s+(?:a\s+|an\s+)?"
    r"(?:(?:[a-z]+ly|[a-z]+(?:ed|al|ful|ive|ous|ary|ic))\s+)*"
    r"(?:successful\s+)?pass"
    r"|success\s+was\s+established)"
)
PROHIBITED_OUTCOME_PATTERNS = (
    re.compile(r"\bcertif(?:ication|ied|y|ies)\b", re.I),
    re.compile(r"\bcomplian(?:ce|t)\b", re.I),
    re.compile(r"\bequivalen(?:ce|t)\b", re.I),
    re.compile(r"\bendorse(?:ment|d|s)?\b", re.I),
    re.compile(
        r"\b(?:predictive(?:ly)?\s+sufficien\w*|predicts?\s+future\s+sufficien\w*)\b",
        re.I,
    ),
    re.compile(
        rf"\b(?:{TESTING_POSITIVE_GRAMMAR}|testing\s+outcome)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:current[- ](?:operational[- ])?scheme(?:\s+(?:completeness|inventory))?"
        r"|complete\s+(?:inventory\s+(?:of|for)\s+)?the\s+current\s+operational\s+scheme"
        r"|complete\s+current[- ]scheme\s+inventory)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:full[- ]population\s+assurance"
        r"|assurance\s+(?:over|for|across|of)\s+(?:the\s+)?full\s+population"
        r"|all\s+(?:untested\s+)?(?:devices|accounts|services|configurations|systems)\s+are\s+assured)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:continuous\s+assurance|continuously\s+assures?"
        r"|assured\s+continuously|assurance\s+continuously)\b",
        re.I,
    ),
)
OUTCOME_ANCHOR = re.compile(
    "(?:" + "|".join(pattern.pattern for pattern in PROHIBITED_OUTCOME_PATTERNS) + ")",
    re.I,
)
INHERENTLY_AFFIRMATIVE_OUTCOME = re.compile(
    r"^(?:certif(?:ied|y|ies)|endorse(?:d|s)?|predicts?\s+future\s+sufficien\w*"
    r"|(?:assessment|test(?:ing)?)\s+(?:(?:has|had|is|was)\s+)?"
    r"(?:[a-z]+ly\s+)*(?:pass(?:ed|es)?|succeed(?:ed|s)?|successful)"
    r"|(?:assessment|test(?:ing)?)\s+(?:resulted\s+in\s+(?:a\s+)?successful\s+pass"
    r"|constitutes\s+(?:a\s+)?pass|success\s+was\s+established)"
    r"|complete\s+(?:inventory\s+(?:of|for)\s+)?the\s+current\s+operational\s+scheme"
    r"|complete\s+current[- ]scheme\s+inventory"
    r"|all\s+(?:untested\s+)?(?:devices|accounts|services|configurations|systems)\s+are\s+assured"
    r"|continuously\s+assures?|assured\s+continuously)$",
    re.I,
)
AFFIRMATIVE_PREFIX_PREDICATE = re.compile(
    r"\b(?:achiev\w*|are|certif\w*|confer\w*|confirm\w*|constitut\w*|covers?"
    r"|declar\w*|demonstrat\w*|endorse\w*|ensur\w*|establish\w*|guarantee\w*|has|have"
    r"|impl(?:y|ies)|indicat\w*|is|offers?|provides?|prov(?:e|es)|represents?|shows?)\b"
    r"|\bverif(?:y|ies)\b",
    re.I,
)
PREFIX_PROPOSITION_BOUNDARY = re.compile(
    r"(?:[,;.!?]|\b(?:after|although|as|before|but|despite|except|if|no|nor|not|or|"
    r"unless|until|when|whereas|while|without|yet)\b)",
    re.I,
)
OUTCOME_AFFIRMATIVE_POSTPREDICATE = re.compile(
    r"^\s+(?:is|are|was|were)\s+(?:[a-z]+ly\s+)*"
    r"(?:achieved|confirmed|conferred|demonstrated|established|provided|successful)\b",
    re.I,
)
OUTCOME_BOUNDARY_POSTPREDICATE = re.compile(
    r"^\s+(?:"
    r"(?:is|are|was|were)\s+(?:not\s+assessed|neither\b|outside\s+(?:the\s+)?(?:scope|evidence\s+boundary)|"
    r"a\s+prohibited\s+inference|considered\b)"
    r"|remains?\s+(?:a\s+)?customer\s+determination"
    r"|requires?\s+separate\s+evidence)\b",
    re.I,
)
OUTCOME_POSTPREDICATE = re.compile(
    r"^\s+(?:is|are|was|were|remains?|requires?)\b",
    re.I,
)
COORDINATION_BOUNDARY = re.compile(
    r"(?:[.;!\n]+|,\s*(?:but|and|yet|however)\s+|\s+(?:but|yet|however)\s+)",
    re.I,
)
NEGATED_AUXILIARY = re.compile(
    r"\b(?:do|does|did|is|are|was|were|has|have|can|could|will|would)\s+not"
    r"(?:\s+[a-z]+ly){0,2}(?:\s+[a-z]+)?(?:\s+that)?"
    r"(?:\s+(?:the|a|an|this|such))?(?:\s+[a-z]+(?:al|ful|ive|ous|ary|ic|ed))?\s*$",
    re.I,
)
NEGATED_OPERATOR = re.compile(
    r"\b(?:neither|nor|never|cannot)"
    r"(?:\s+[a-z]+ly){0,2}(?:\s+[a-z]+)?(?:\s+that)?"
    r"(?:\s+(?:the|a|an|this|such))?(?:\s+[a-z]+(?:al|ful|ive|ous|ary|ic|ed))?\s*$",
    re.I,
)
NEGATED_NO_LIST_START = re.compile(
    r"\b(?:provides?|establishes?|shows?|offers?|confers?)\s+no\b",
    re.I,
)
NEGATED_GOVERNED_LIST_START = re.compile(
    r"\b(?:(?:do|does|did|is|are|was|were|has|have|can|could|will|would)\s+not"
    r"|never|cannot)(?:\s+[a-z]+ly){0,2}\s+[a-z]+(?:\s+that)?"
    r"(?:\s+(?:the|a|an|this|such))?(?:\s+[a-z]+(?:al|ful|ive|ous|ary|ic|ed)\b)?",
    re.I,
)
NEGATED_NEITHER_NOR = re.compile(
    r"\bneither(?:\s+[a-z]+ly){0,2}\s+[a-z]+(?:\s+(?:the|a|an|this|such))?\s+"
    + OUTCOME_ANCHOR.pattern
    + r"\s+nor(?:\s+[a-z]+ly){0,2}(?:\s+[a-z]+)?(?:\s+(?:the|a|an|this|such))?\s*$",
    re.I,
)
NEGATED_AFTER_PROPOSITION = re.compile(
    r"^\s*(?:is|are|was|were|has|have|does|do)?\s*not\s+"
    r"(?:implied|established|demonstrated|proven|proved|supported|shown|conferred|achieved)\b",
    re.I,
)


def negative_no_list_governs(clause: str, match: re.Match[str]) -> bool:
    starts = list(NEGATED_NO_LIST_START.finditer(clause[:match.start()]))
    if not starts:
        return False
    intervening = clause[starts[-1].end():match.start()]
    remainder = OUTCOME_ANCHOR.sub("", intervening)
    return bool(re.fullmatch(r"(?:\s|,|\band\b|\bor\b|\bnor\b)*", remainder, re.I))


def negative_governed_list_governs(clause: str, match: re.Match[str]) -> bool:
    starts = list(NEGATED_GOVERNED_LIST_START.finditer(clause[:match.start()]))
    if not starts:
        return False
    intervening = clause[starts[-1].end():match.start()]
    remainder = OUTCOME_ANCHOR.sub("", intervening)
    return bool(re.fullmatch(r"(?:\s|,|\band\b|\bor\b|\bnor\b)*", remainder, re.I))


def prohibited_outcome_is_affirmed(clause: str, match: re.Match[str]) -> bool:
    suffix = clause[match.end():]
    if OUTCOME_BOUNDARY_POSTPREDICATE.search(suffix):
        return False
    if OUTCOME_AFFIRMATIVE_POSTPREDICATE.search(suffix):
        return True
    if OUTCOME_POSTPREDICATE.search(suffix):
        return False
    if re.fullmatch(TESTING_POSITIVE_GRAMMAR, match.group(0), re.I):
        return True
    if INHERENTLY_AFFIRMATIVE_OUTCOME.fullmatch(match.group(0)):
        return True
    prefix = clause[:match.start()]
    predicates = list(AFFIRMATIVE_PREFIX_PREDICATE.finditer(prefix))
    if not predicates:
        return False
    return not PREFIX_PROPOSITION_BOUNDARY.search(prefix[predicates[-1].end():])


def prohibited_proposition_is_negated(clause: str, match: re.Match[str]) -> bool:
    proposition = match.group(0)
    if re.search(r"\b(?:not|no|without|never|neither)\b", proposition, re.I):
        return True
    prefix = clause[:match.start()]
    if re.search(r"\bno\s*$", prefix, re.I):
        return True
    if NEGATED_AUXILIARY.search(prefix) or NEGATED_OPERATOR.search(prefix):
        return True
    if negative_no_list_governs(clause, match):
        return True
    if negative_governed_list_governs(clause, match):
        return True
    if NEGATED_NEITHER_NOR.search(prefix):
        return True
    if re.search(
        r"\bwithout(?:\s+(?:directly|independently|validly|defensibly|conclusively|actually|materially)){0,2}\s*$",
        prefix,
        re.I,
    ):
        return True
    return bool(NEGATED_AFTER_PROPOSITION.search(clause[match.end():]))


def prohibited_claim_violations(text: str) -> list[str]:
    violations: list[str] = []
    for clause in COORDINATION_BOUNDARY.split(text):
        for pattern in PROHIBITED_OUTCOME_PATTERNS:
            for match in pattern.finditer(clause):
                if (
                    prohibited_outcome_is_affirmed(clause, match)
                    and not prohibited_proposition_is_negated(clause, match)
                ):
                    violations.append(match.group(0))
    return violations


class MappingGoNoGoTests(unittest.TestCase):
    def test_oracle_digest_is_locked(self) -> None:
        self.assertEqual(normalized_sha256(ORACLE), ORACLE_SHA256)

    def test_rights_re_attestation_exists_before_analysis(self) -> None:
        self.assertTrue(RIGHTS.is_file())

    def test_rights_re_attestation_contract_is_exact(self) -> None:
        text = RIGHTS.read_text(encoding="utf-8")
        self.assertIn(f"`{ORACLE_SHA256}`", text)
        self.assertIn(f"`{PRIOR_RIGHTS_COMMIT}`", text)
        self.assertIn("**Disposition:** Approved", text)
        for field_class in FIELD_CLASSES:
            self.assertIn(f"`{field_class}`", text)
        self.assertIn("**IASME partition preserved:** yes", text)
        self.assertIn("**Copied-source prohibition preserved:** yes", text)

    def test_matrix_and_rendered_review_exist(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in (MATRIX, REVIEW) if not path.is_file()]
        self.assertEqual([], missing)


class MappingValidatorRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        cls.rights_text = RIGHTS.read_text(encoding="utf-8")

    def test_rights_binding_comes_from_committed_record(self) -> None:
        record = parse_rights_record(self.rights_text)
        matrix = {
            "rights_re_attestation": {
                "reviewer": record["reviewer"],
                "review_date": record["review_date"],
                "prior_rights_commit": record["prior_rights_commit"],
                "oracle_sha256": record["oracle_sha256"],
                "field_classes_reviewed": list(FIELD_CLASSES),
                "iasme_partition_preserved": True,
                "copied_source_prohibition_preserved": True,
                "disposition": "approved",
            },
            "roles": {
                "esaf_to_external_analyst": "Analyst A",
                "external_to_esaf_analyst": "Analyst B",
                "reconciler": "Reconciler",
            },
        }
        validate_rights_binding(matrix, self.rights_text)
        for key, forged in (("reviewer", "Forged reviewer"), ("review_date", "2099-01-01")):
            with self.subTest(key=key):
                mutated = json.loads(json.dumps(matrix))
                mutated["rights_re_attestation"][key] = forged
                with self.assertRaisesRegex(ValueError, "rights record mismatch"):
                    validate_rights_binding(mutated, self.rights_text)
        matrix["roles"]["esaf_to_external_analyst"] = record["reviewer"]
        with self.assertRaisesRegex(ValueError, "rights reviewer is not independent"):
            validate_rights_binding(matrix, self.rights_text)

    def test_empty_contract_strings_and_generic_missing_outcomes_are_rejected(self) -> None:
        value = {"roles": {"reconciler": "Reconciler"}, "items": ["evidence"]}
        validate_nonempty_contract_strings(value)
        value["roles"]["reconciler"] = "  "
        with self.assertRaisesRegex(ValueError, "empty required string"):
            validate_nonempty_contract_strings(value)
        value["roles"]["reconciler"] = None
        with self.assertRaisesRegex(ValueError, "empty required value"):
            validate_nonempty_contract_strings(value)
        probe = {
            "probe_id": "probe-1",
            "conclusion": "NO_POSITIVE_BASIS",
            "rationale": "The material does not establish the needed result.",
        }
        with self.assertRaisesRegex(ValueError, "missing outcome"):
            validate_missing_outcomes([probe])
        probe["rationale"] = "Missing outcome: a retained-evidence duty for the Applicant."
        validate_missing_outcomes([probe])

    def test_evidence_references_are_closed_and_locators_resolve(self) -> None:
        approved_url = self.oracle["source"]["resource_page_url"]
        validate_evidence_reference("probe-1", {"probe-1"}, self.oracle)
        validate_evidence_reference(approved_url, set(), self.oracle)
        validate_evidence_reference(
            f"{RIGHTS.relative_to(ROOT).as_posix()}#approved-field-classes",
            set(), self.oracle,
        )
        validate_evidence_reference(
            f"{ORACLE.relative_to(ROOT).as_posix()}#assurance_limits.scope_boundary",
            set(), self.oracle,
        )
        for invalid in (
            "https://example.invalid/evidence",
            f"{RIGHTS.relative_to(ROOT).as_posix()}#invented-heading",
            RIGHTS.relative_to(ROOT).as_posix(),
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "invalid evidence reference"):
                    validate_evidence_reference(invalid, set(), self.oracle)

    def test_every_claimed_scenario_binding_is_validated(self) -> None:
        probe = {
            "probe_id": "probe-1",
            "conclusion": "POSITIVE_FEASIBILITY",
            "provision_ids": ["CEPTS3.2-M-006", "CEPTS3.2-M-011"],
            "special_scenarios": [
                "sampling-and-population-limits", "evidence-retention",
            ],
            "special_scenario_bindings": [
                {
                    "scenario_id": "sampling-and-population-limits",
                    "provision_ids": ["CEPTS3.2-M-006"],
                    "oracle_paths": [
                        "provisions[CEPTS3.2-M-006].external_provision_id",
                        "assurance_limits.population_and_sample_boundary",
                    ],
                },
                {
                    "scenario_id": "evidence-retention",
                    "provision_ids": ["CEPTS3.2-M-011"],
                    "oracle_paths": [
                        "provisions[CEPTS3.2-M-011].external_provision_id",
                    ],
                },
            ],
        }
        with self.assertRaisesRegex(ValueError, "evidence-retention"):
            validate_probe_scenario_bindings(probe, self.oracle)
        probe["special_scenario_bindings"][1]["oracle_paths"].append(
            "assurance_limits.evidence_date_boundary"
        )
        validate_probe_scenario_bindings(probe, self.oracle)

    def test_affirmative_prohibited_inferences_are_detected_without_boundary_false_positives(self) -> None:
        claims = (
            "This analysis establishes certification.",
            "The result proves compliance.",
            "The frameworks are equivalent.",
            "NCSC endorses this review.",
            "The sample is predictively sufficient for future state.",
            "The evidence proves the assessment passed.",
            "This inventory covers the current operational scheme.",
            "The sample provides full-population assurance.",
            "The result provides continuous assurance.",
            "This certifies the Applicant and the Applicant is compliant.",
            "The sources have equivalent requirements.",
            "This constitutes NCSC endorsement.",
            "The sample predicts future sufficiency.",
            "Testing succeeded for this control.",
            "This is a complete current-scheme inventory.",
            "All untested devices are assured by the sample.",
            "The controls remain assured continuously.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertTrue(prohibited_claim_violations(claim))
        boundaries = (
            "This analysis does not establish certification or compliance.",
            "The frameworks are not equivalent and NCSC does not endorse this review.",
            "The result provides no predictive sufficiency, testing outcome, current-scheme completeness, full-population assurance, or continuous assurance.",
            "No mapping snapshot exists. A GO authorizes design only.",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertEqual(prohibited_claim_violations(boundary), [])

    def test_prohibited_inference_negation_is_scoped_to_its_proposition(self) -> None:
        for claim in (
            "This does not establish certification, but it guarantees compliance.",
            "No evidence was omitted, and this analysis establishes certification.",
        ):
            with self.subTest(claim=claim):
                self.assertTrue(prohibited_claim_violations(claim))
        for boundary in (
            "The review establishes that certification is not implied.",
            "The analysis proves equivalence is not established.",
            "The analysis neither establishes certification nor proves compliance.",
            "The analysis never establishes certification.",
            "The analysis cannot establish certification.",
        ):
            with self.subTest(boundary=boundary):
                self.assertEqual(prohibited_claim_violations(boundary), [])
        for mixed in (
            "The analysis neither establishes certification nor proves compliance, but it guarantees endorsement.",
            "The analysis never omits evidence, but it establishes certification.",
            "The analysis cannot inspect the source, and it establishes certification.",
            "The analysis neither establishes certification nor proves compliance; it establishes equivalence.",
            "The analysis never omits evidence while it establishes certification.",
            "The analysis cannot inspect evidence while it establishes certification.",
            "The analysis neither omits evidence nor hides limits whereas it establishes certification.",
            "The analysis never reviews evidence before it establishes certification.",
            "The analysis cannot inspect logs although it proves compliance.",
            "The analysis neither omits facts nor obscures sources even as it proves equivalence.",
            "The analysis does not prove a gap while it establishes certification.",
            "The analysis never demonstrates an omission before it guarantees compliance.",
            "The analysis cannot establish source identity although it proves compliance.",
            "The review does not establish a source fact whereas it directly confers certification.",
        ):
            with self.subTest(mixed=mixed):
                self.assertTrue(prohibited_claim_violations(mixed))
        for tightly_governed in (
            "The analysis never directly establishes certification.",
            "The analysis cannot defensibly establish certification.",
        ):
            with self.subTest(tightly_governed=tightly_governed):
                self.assertEqual(prohibited_claim_violations(tightly_governed), [])

    def test_outcome_anchors_detect_reviewer_examples_with_open_modifiers(self) -> None:
        examples = (
            "This analysis guarantees successful certification.",
            "This analysis demonstrates full compliance.",
            "This analysis proves organizational compliance.",
            "The frameworks are functionally equivalent.",
            "This constitutes official NCSC endorsement.",
            "The evidence proves that the assessment successfully passed.",
            "This provides assurance over the full population.",
            "This provides assurance continuously.",
        )
        for example in examples:
            with self.subTest(example=example):
                self.assertTrue(prohibited_claim_violations(example))

    def test_neutral_outcome_references_are_accepted(self) -> None:
        boundaries = (
            "No certification is conferred.",
            "No compliance is established.",
            "There is no equivalence between the frameworks.",
            "Certification and compliance are not established.",
            "Certification, compliance, and equivalence are not established.",
            "Certification is neither demonstrated nor implied.",
            "Certification is outside the scope of this analysis.",
            "Compliance remains a customer determination.",
            "Equivalence was not assessed.",
            "Endorsement is a prohibited inference.",
            "The risk of certification overclaiming is documented.",
            "The risk of highly consequential certification overclaiming is documented.",
            "Full-population assurance is outside the evidence boundary.",
            "Continuous assurance requires separate evidence.",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertEqual(prohibited_claim_violations(boundary), [])

    def test_positive_testing_outcomes_are_detected(self) -> None:
        claims = (
            "The assessment has demonstrably passed.",
            "The assessment was successfully passed.",
            "The test was successful.",
            "Testing was successful.",
            "The assessment resulted in a successful pass.",
            "The assessment constitutes a pass.",
            "Test success was established.",
            "This analysis establishes unexpectedly bespoke certification.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertTrue(prohibited_claim_violations(claim))

    def test_outcome_first_affirmative_predicates_are_detected(self) -> None:
        claims = (
            "Certification is established.",
            "Compliance is demonstrated.",
            "The frameworks’ equivalence is confirmed.",
            "NCSC endorsement is conferred.",
            "Predictive sufficiency is established.",
            "The testing outcome is successful.",
            "Current-scheme completeness is confirmed.",
            "Full-population assurance is provided.",
            "Continuous assurance is achieved.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertTrue(prohibited_claim_violations(claim))

    def test_direct_prefix_predicates_are_local_and_open_to_modifiers(self) -> None:
        claims = (
            "The analysis declares certification.",
            "The analysis verifies functional equivalence.",
            "This establishes a highly context-specific externally audited certification.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertTrue(prohibited_claim_violations(claim))

    def test_anchor_owned_boundary_predicates_override_reporting_verbs(self) -> None:
        boundaries = (
            "The review shows certification is outside the scope of this analysis.",
            "The analysis confirms compliance remains a customer determination.",
            "The review establishes that equivalence was not assessed.",
            "The report indicates endorsement is a prohibited inference.",
            "The evidence indicates full-population assurance requires separate evidence.",
            "The review confirms continuous assurance requires separate evidence.",
            "The review establishes source identity before certification is considered.",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertEqual(prohibited_claim_violations(boundary), [])

    def test_testing_clause_positive_relationships_are_detected(self) -> None:
        claims = (
            "The test has been successfully passed.",
            "The assessment has conclusively been passed.",
            "The assessment has very clearly passed.",
            "The assessment has independently and successfully passed.",
            "The testing completed successfully.",
            "The assessment achieved a successful pass.",
            "The assessment constitutes an unqualified pass.",
            "The assessment resulted in a demonstrably successful pass.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertTrue(prohibited_claim_violations(claim))


@unittest.skipUnless(MATRIX.is_file() and REVIEW.is_file(), "Task 4 artifacts are absent")
class MatrixClosedContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        cls.review = REVIEW.read_text(encoding="utf-8")
        cls.provisions = {
            item["external_provision_id"]: item for item in cls.oracle["provisions"]
        }
        cls.probes = {item["probe_id"]: item for item in cls.matrix["probes"]}

    def assert_nonempty_string(self, value: object, context: str) -> None:
        self.assertIsInstance(value, str, context)
        self.assertTrue(value.strip(), context)

    def assert_evidence_reference(self, reference: str) -> None:
        validate_evidence_reference(reference, set(self.probes), self.oracle)

    def test_top_level_source_rights_roles_and_coverage_are_closed(self) -> None:
        validate_nonempty_contract_strings(self.matrix)
        assert_exact_keys(self, self.matrix, {
            "schema_version", "review_identifier", "source_oracle",
            "rights_re_attestation", "roles", "coverage_contract",
            "analysis_provenance", "direction_assessments", "probes",
        }, "matrix")
        self.assertEqual(self.matrix["schema_version"], "1.0.0")
        self.assertEqual(self.matrix["review_identifier"], REVIEW_IDENTIFIER)
        source = self.matrix["source_oracle"]
        assert_exact_keys(self, source, {
            "path", "sha256", "source_version", "expected_provision_count",
            "atomization_rule_version", "scope_statement",
        }, "source_oracle")
        self.assertEqual(source["path"], ORACLE.relative_to(ROOT).as_posix())
        self.assertEqual(source["sha256"], ORACLE_SHA256)
        self.assertEqual(source["source_version"], "3.2")
        self.assertEqual(source["expected_provision_count"], 144)
        self.assertEqual(source["atomization_rule_version"], "1.0.0")
        self.assertEqual(source["scope_statement"], self.oracle["scope"]["statement"])
        for key in ("path", "sha256", "source_version", "atomization_rule_version", "scope_statement"):
            self.assert_nonempty_string(source[key], f"source_oracle.{key}")
        rights = self.matrix["rights_re_attestation"]
        assert_exact_keys(self, rights, {
            "record_path", "record_commit", "reviewer", "review_date",
            "prior_rights_commit", "oracle_sha256", "publication_basis_covered",
            "iasme_partition_preserved", "copied_source_prohibition_preserved",
            "field_classes_reviewed", "disposition",
        }, "rights_re_attestation")
        self.assertEqual(rights["record_path"], RIGHTS.relative_to(ROOT).as_posix())
        self.assertEqual(rights["prior_rights_commit"], PRIOR_RIGHTS_COMMIT)
        self.assertEqual(rights["oracle_sha256"], ORACLE_SHA256)
        self.assertEqual(rights["field_classes_reviewed"], list(FIELD_CLASSES))
        for key in ("publication_basis_covered", "iasme_partition_preserved", "copied_source_prohibition_preserved"):
            self.assertIs(rights[key], True)
        self.assertEqual(rights["disposition"], "approved")
        for key in (
            "record_path", "record_commit", "reviewer", "review_date",
            "prior_rights_commit", "oracle_sha256", "disposition",
        ):
            self.assert_nonempty_string(rights[key], f"rights_re_attestation.{key}")
        for value in rights["field_classes_reviewed"]:
            self.assert_nonempty_string(value, "rights field class")
        assert_exact_keys(self, self.matrix["roles"], {
            "esaf_to_external_analyst", "external_to_esaf_analyst", "reconciler",
        }, "roles")
        roles = self.matrix["roles"]
        self.assertEqual(len(set(roles.values())), 3)
        for key, value in roles.items():
            self.assert_nonempty_string(value, f"roles.{key}")
        validate_rights_binding(self.matrix, RIGHTS.read_text(encoding="utf-8"))
        coverage = self.matrix["coverage_contract"]
        assert_exact_keys(self, coverage, {"groups", "kinds", "actors", "special_scenarios"}, "coverage_contract")
        self.assertEqual(coverage, {
            "groups": list(GROUPS), "kinds": list(KINDS), "actors": list(ACTORS),
            "special_scenarios": list(SCENARIOS),
        })

    def test_rights_commit_is_rights_only_and_precedes_analysis(self) -> None:
        commit = self.matrix["rights_re_attestation"]["record_commit"]
        self.assertRegex(commit, r"^[0-9a-f]{40}$")
        self.assertEqual(git("diff-tree", "--no-commit-id", "--name-only", "-r", commit), RIGHTS.relative_to(ROOT).as_posix())
        self.assertEqual(subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ROOT
        ).returncode, 0)
        first_probe_commit = git("log", "--diff-filter=A", "--format=%H", "--reverse", "--", MATRIX.relative_to(ROOT).as_posix())
        if first_probe_commit:
            self.assertEqual(subprocess.run(
                ["git", "merge-base", "--is-ancestor", commit, first_probe_commit.splitlines()[0]], cwd=ROOT
            ).returncode, 0)

    def test_provenance_is_closed_immutable_and_digest_bound(self) -> None:
        provenance = self.matrix["analysis_provenance"]
        assert_exact_keys(self, provenance, {
            "broker_protocol", "prompt_digests", "common_input_sha256",
            "submissions", "direction_content_digests", "reconciliation",
        }, "analysis_provenance")
        broker = provenance["broker_protocol"]
        assert_exact_keys(self, broker, {
            "dispatch_mode", "fork_turns", "concurrent", "analyst_output_channel",
            "no_output_files", "controller_withholding_attestation",
            "sibling_mailbox_inaccessible_attestation", "fail_closed_fallback",
        }, "broker_protocol")
        self.assertEqual(broker, {
            "dispatch_mode": "codex_sibling_agents", "fork_turns": "none",
            "concurrent": True, "analyst_output_channel": "controller_mailbox_final_response",
            "no_output_files": True, "controller_withholding_attestation": True,
            "sibling_mailbox_inaccessible_attestation": True,
            "fail_closed_fallback": "separate_principals_or_containers_else_stop",
        })
        prompts = provenance["prompt_digests"]
        self.assertEqual([item["direction"] for item in prompts], list(DIRECTIONS))
        for item in prompts:
            assert_exact_keys(self, item, {"direction", "sha256"}, "prompt_digest")
            self.assert_nonempty_string(item["direction"], "prompt direction")
            self.assert_nonempty_string(item["sha256"], "prompt digest")
            self.assertRegex(item["sha256"], HEX_SHA256)
        self.assertEqual(len({item["sha256"] for item in prompts}), 2)
        self.assertRegex(provenance["common_input_sha256"], HEX_SHA256)
        submissions = provenance["submissions"]
        self.assertEqual([item["direction"] for item in submissions], list(DIRECTIONS))
        self.assertEqual([item["analyst"] for item in submissions], [
            self.matrix["roles"]["esaf_to_external_analyst"],
            self.matrix["roles"]["external_to_esaf_analyst"],
        ])
        for item in submissions:
            assert_exact_keys(self, item, {
                "direction", "analyst", "received_at_utc", "payload_sha256",
                "digest_reference", "no_output_file_attestation",
                "no_sibling_content_attestation",
            }, "submission")
            self.assertRegex(item["received_at_utc"], UTC_ISO_8601)
            self.assertRegex(item["payload_sha256"], HEX_SHA256)
            for key in ("direction", "analyst", "received_at_utc", "payload_sha256", "digest_reference"):
                self.assert_nonempty_string(item[key], f"submission.{key}")
            self.assertEqual(item["payload_sha256"], submission_payload_sha256(self.matrix, item["direction"]))
            self.assertIs(item["no_output_file_attestation"], True)
            self.assertIs(item["no_sibling_content_attestation"], True)
        self.assertEqual(len({item["payload_sha256"] for item in submissions}), 2)
        self.assertEqual(len({item["digest_reference"] for item in submissions}), 2)
        digests = provenance["direction_content_digests"]
        self.assertEqual([item["direction"] for item in digests], list(DIRECTIONS))
        for item in digests:
            assert_exact_keys(self, item, {"direction", "sha256"}, "direction_content_digest")
            self.assert_nonempty_string(item["direction"], "digest direction")
            self.assert_nonempty_string(item["sha256"], "direction digest")
            self.assertEqual(item["sha256"], direction_content_sha256(self.matrix, item["direction"]))
        reconciliation = provenance["reconciliation"]
        assert_exact_keys(self, reconciliation, {
            "reconciler", "submission_digest_references", "direction_validations",
            "post_seal_changes_prohibited", "packaging_disposition",
        }, "reconciliation")
        self.assertEqual(reconciliation["reconciler"], self.matrix["roles"]["reconciler"])
        self.assert_nonempty_string(reconciliation["reconciler"], "reconciliation.reconciler")
        self.assertEqual(reconciliation["submission_digest_references"], [item["digest_reference"] for item in submissions])
        for reference in reconciliation["submission_digest_references"]:
            self.assert_nonempty_string(reference, "submission digest reference")
        self.assertIs(reconciliation["post_seal_changes_prohibited"], True)
        self.assertEqual(reconciliation["packaging_disposition"], "accepted")
        validations = reconciliation["direction_validations"]
        self.assertEqual([item["direction"] for item in validations], list(DIRECTIONS))
        for item in validations:
            assert_exact_keys(self, item, {"direction", "status", "evidence_references"}, "direction_validation")
            self.assertEqual(item["status"], "ACCEPTED")
            self.assert_nonempty_string(item["direction"], "validation direction")
            self.assert_nonempty_string(item["status"], "validation status")
            self.assertTrue(item["evidence_references"])
            for reference in item["evidence_references"]:
                self.assert_evidence_reference(reference)
        keys = recursive_keys(self.matrix)
        self.assertFalse({
            key for key in keys
            if "correction" in key.lower() or "supersession" in key.lower()
            or key == "supersedes_digest_reference"
        })

    def test_assessments_gates_and_dispositions_are_mechanical(self) -> None:
        assessments = self.matrix["direction_assessments"]
        self.assertEqual([item["direction"] for item in assessments], list(DIRECTIONS))
        for assessment in assessments:
            assert_exact_keys(self, assessment, {
                "direction", "analyst", "question", "gate_results",
                "positive_probe_identifiers", "disposition", "decision_rationale",
                "prerequisites", "reconsideration_triggers",
            }, "direction_assessment")
            role = self.matrix["roles"][f"{assessment['direction']}_analyst"]
            self.assertEqual(assessment["analyst"], role)
            for key in ("direction", "analyst", "question", "disposition", "decision_rationale"):
                self.assert_nonempty_string(assessment[key], f"assessment.{key}")
            for probe_id in assessment["positive_probe_identifiers"]:
                self.assert_nonempty_string(probe_id, "positive probe identifier")
            self.assertEqual([gate["gate"] for gate in assessment["gate_results"]], list(GATES))
            self.assertEqual(assessment["disposition"], expected_disposition(assessment, self.probes))
            self.assertIn(assessment["disposition"], DISPOSITIONS)
            for gate in assessment["gate_results"]:
                assert_exact_keys(self, gate, {"gate", "status", "rationale", "evidence_references"}, "gate")
                self.assertIn(gate["status"], GATE_STATUSES)
                self.assert_nonempty_string(gate["rationale"], "gate rationale")
                self.assertTrue(gate["evidence_references"])
                for reference in gate["evidence_references"]:
                    self.assert_evidence_reference(reference)
            for prerequisite in assessment["prerequisites"]:
                assert_exact_keys(self, prerequisite, {"prerequisite", "required_evidence", "reentry_test"}, "prerequisite")
                for value in prerequisite.values():
                    self.assert_nonempty_string(value, "prerequisite value")
            for trigger in assessment["reconsideration_triggers"]:
                assert_exact_keys(self, trigger, {"change", "required_evidence"}, "reconsideration trigger")
                for value in trigger.values():
                    self.assert_nonempty_string(value, "trigger value")
            if assessment["disposition"] == "GO":
                self.assertEqual(assessment["prerequisites"], [])
                self.assertEqual(assessment["reconsideration_triggers"], [])
            elif assessment["disposition"] == "HOLD":
                self.assertIn("BLOCKED", {g["status"] for g in assessment["gate_results"]})
                self.assertTrue(assessment["prerequisites"])
                self.assertEqual(assessment["reconsideration_triggers"], [])
            else:
                self.assertEqual(assessment["prerequisites"], [])
                self.assertTrue(assessment["reconsideration_triggers"])

    def test_probe_contract_oracle_derivation_and_conditions_are_exact(self) -> None:
        self.assertEqual(len(self.probes), len(self.matrix["probes"]))
        validate_missing_outcomes(self.matrix["probes"])
        for probe in self.matrix["probes"]:
            assert_exact_keys(self, probe, {
                "probe_id", "direction", "provision_ids", "selection_basis", "groups",
                "kinds", "actors", "special_scenarios", "special_scenario_bindings",
                "condition_checklist", "esaf_normative_bases", "semantic_fit_analysis",
                "assurance_and_overclaiming_risks", "source_rights_and_operational_limits",
                "conclusion", "rationale",
            }, "probe")
            self.assertIn(probe["direction"], DIRECTIONS)
            self.assertIn(probe["conclusion"], PROBE_CONCLUSIONS)
            self.assertTrue(probe["provision_ids"])
            for key in (
                "probe_id", "direction", "selection_basis", "semantic_fit_analysis",
                "assurance_and_overclaiming_risks",
                "source_rights_and_operational_limits", "conclusion", "rationale",
            ):
                self.assert_nonempty_string(probe[key], f"probe.{key}")
            for key in ("provision_ids", "groups", "kinds", "actors", "special_scenarios"):
                for value in probe[key]:
                    self.assert_nonempty_string(value, f"probe.{key}")
            selected = [self.provisions[item] for item in probe["provision_ids"]]
            self.assertEqual(probe["groups"], list(dict.fromkeys(item["group"] for item in selected)))
            self.assertEqual(probe["kinds"], list(dict.fromkeys(item["kind"] for item in selected)))
            self.assertEqual(probe["actors"], list(dict.fromkeys(actor for item in selected for actor in item["actors"])))
            expected_conditions = (
                probe["direction"] == "external_to_esaf"
                and probe["conclusion"] == "POSITIVE_FEASIBILITY"
            )
            if expected_conditions:
                self.assertEqual([entry["condition"] for entry in probe["condition_checklist"]], list(EXTERNAL_TO_ESAF_CONDITIONS))
                for entry in probe["condition_checklist"]:
                    assert_exact_keys(self, entry, {"condition", "status", "evidence_references"}, "condition")
                    self.assertIn(entry["status"], CONDITION_STATUSES)
                    self.assertTrue(entry["evidence_references"])
                    for reference in entry["evidence_references"]:
                        self.assert_evidence_reference(reference)
            else:
                self.assertEqual(probe["condition_checklist"], [])
            if probe["conclusion"] == "POSITIVE_FEASIBILITY":
                self.assertTrue(probe["esaf_normative_bases"])
            if probe["conclusion"] == "INDETERMINATE":
                assessment = next(item for item in self.matrix["direction_assessments"] if item["direction"] == probe["direction"])
                self.assertTrue(assessment["prerequisites"])
                self.assertTrue(any(item["prerequisite"] in probe["rationale"] for item in assessment["prerequisites"]))
            for basis in probe["esaf_normative_bases"]:
                assert_exact_keys(self, basis, {"control_id", "requirement_locator", "relevance_analysis"}, "normative basis")
                control = ROOT / "controls" / basis["control_id"].split("-", 1)[0] / f"{basis['control_id']}.md"
                self.assertTrue(control.is_file(), basis["control_id"])
                self.assertEqual(basis["requirement_locator"], f"{control.relative_to(ROOT).as_posix()}#requirement")
                requirement = control.read_text(encoding="utf-8").split("## Requirement", 1)[1].split("## ", 1)[0]
                self.assertRegex(requirement, r"\bshall\b")
                self.assert_nonempty_string(basis["relevance_analysis"], "relevance analysis")

    def test_direction_local_coverage_and_scenario_bindings_are_complete(self) -> None:
        for direction in DIRECTIONS:
            coverage = derive_coverage(self.matrix, direction)
            self.assertEqual(coverage, {
                "groups": set(GROUPS), "kinds": set(KINDS), "actors": set(ACTORS),
                "special_scenarios": set(SCENARIOS),
            })
            selected = [probe for probe in self.matrix["probes"] if probe["direction"] == direction]
            for probe in selected:
                validate_probe_scenario_bindings(probe, self.oracle)
                for binding in probe["special_scenario_bindings"]:
                    assert_exact_keys(self, binding, {"scenario_id", "provision_ids", "oracle_paths"}, "scenario binding")
            for scenario, contract in SCENARIO_EVIDENCE.items():
                probe, binding = next(
                    (probe, binding)
                    for probe in selected
                    for binding in probe["special_scenario_bindings"]
                    if binding["scenario_id"] == scenario
                )
                ids = set(binding["provision_ids"])
                self.assertTrue(contract["required"] <= ids, scenario)
                if contract["one_of"]:
                    self.assertTrue(contract["one_of"] & ids, scenario)
                self.assertTrue(contract["paths"] <= set(binding["oracle_paths"]), scenario)
                if scenario == "figure-1-decision-logic":
                    self.assertTrue({f"CEPTS3.2-T1-{number:03d}" for number in range(9, 17)} <= ids)
                elif scenario == "known-source-anomaly":
                    self.assertEqual(resolve_oracle_path(self.oracle, "known_anomalies[0].anomaly_id"), "cepts32-anomaly-001")
                elif scenario == "expected-no-direct-esaf-basis":
                    self.assertEqual(probe["conclusion"], "NO_POSITIVE_BASIS")
                    for provision_id in ids:
                        self.assertIn(f"provisions[{provision_id}].summary", binding["oracle_paths"])
                        self.assertIn(f"provisions[{provision_id}].locator", binding["oracle_paths"])
                elif scenario in {"point-in-time-versus-continuous-assurance", "core-v3.3-versus-plus-v3.2-separation", "known-source-anomaly"}:
                    self.assertTrue(ids)

    def test_prohibited_fields_claims_literals_and_mapping_tree_changes_are_absent(self) -> None:
        self.assertEqual(PROHIBITED_KEYS & recursive_keys(self.matrix), set())
        combined = MATRIX.read_text(encoding="utf-8") + "\n" + self.review
        self.assertNotIn(self.oracle["known_anomalies"][0]["source_literal"], combined)
        self.assertEqual(prohibited_claim_violations(combined), [])
        base = git("merge-base", "HEAD", "origin/main")
        changed = git("diff", "--name-only", base, "--", "crosswalks/mappings", "crosswalks/registry")
        self.assertEqual(changed, "")

    def test_rendered_review_is_derived_from_matrix(self) -> None:
        self.assertIn("No mapping snapshot exists", self.review)
        self.assertIn("design only", self.review)
        for assessment in self.matrix["direction_assessments"]:
            direction = assessment["direction"]
            section = self.review.split(f"## {direction}", 1)[1].split("## ", 1)[0]
            self.assertIn(f"**Disposition:** {assessment['disposition']}", section)
            for gate in assessment["gate_results"]:
                self.assertIn(f"| `{gate['gate']}` | `{gate['status']}` |", section)
            selected = [probe for probe in self.matrix["probes"] if probe["direction"] == direction]
            conclusions = {value: sum(p["conclusion"] == value for p in selected) for value in PROBE_CONCLUSIONS}
            self.assertIn(
                f"Probes: {len(selected)}; positive: {conclusions['POSITIVE_FEASIBILITY']}; "
                f"no positive basis: {conclusions['NO_POSITIVE_BASIS']}; "
                f"indeterminate: {conclusions['INDETERMINATE']}.", section,
            )
            coverage = derive_coverage(self.matrix, direction)
            for label, key in (("Groups", "groups"), ("Kinds", "kinds"), ("Actors", "actors"), ("Special scenarios", "special_scenarios")):
                self.assertIn(f"| {label} | {len(coverage[key])} |", section)
