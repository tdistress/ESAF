import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.schemas import load_schemas, schema_errors


SHA256 = "a" * 64
SHA40 = "b" * 40
MAPPING_SET_ID = "nist--ai-rmf--1.0--esaf-1.0--1.0.0"


def change() -> dict[str, object]:
    return {"version": "1.0.0", "date": "2026-07-13", "change": "Initial version"}


def reviewer() -> dict[str, object]:
    return {
        "id": "reviewer-1",
        "qualification": "Independent subject-matter reviewer",
        "date": "2026-07-13",
        "authorized_source_access": True,
        "findings_disposition": "All findings resolved",
    }


def relationship() -> dict[str, object]:
    return {
        "esaf_control_id": "GOV-100",
        "esaf_control_version": "1.0.0",
        "relationship": "supports",
        "direction": "external_to_esaf",
        "coverage": "partial",
        "confidence": "high",
        "rationale": "The outcomes overlap.",
        "conditions": ["The declared scope applies."],
        "expected_evidence": ["Approved assessment record"],
        "known_gaps": ["Implementation remains organization-specific."],
    }


def valid_mapping_set(status: str = "draft") -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": "1.0.0",
        "mapping_set_id": MAPPING_SET_ID,
        "authority": {"id": "nist", "name": "NIST"},
        "publication": {"id": "ai-rmf", "name": "AI Risk Management Framework"},
        "source_version": {"id": "1.0", "label": "1.0"},
        "esaf_release": {
            "id": "1.0",
            "label": "ESAF 1.0",
            "source_commit_sha": SHA40,
            "control_catalog_sha256": SHA256,
            "control_manifest_path": "ESAF_CONTROL_MANIFEST.json",
        },
        "mapping_set_version": "1.0.0",
        "status": status,
        "source": {
            "official_url": "https://example.com/standard",
            "publication_date": "2023-01-26",
            "access_class": "public",
            "licensing_note": "Public source; derivative analysis only.",
        },
        "publication_rights": {
            "basis": "Documented publication review",
            "permitted_elements": ["identifiers", "paraphrases"],
            "prohibited_elements": ["titles"],
            "restrictions": "No verbatim requirements.",
            "approved": True,
            "reviewer_id": "rights-reviewer",
            "review_date": "2026-07-13",
        },
        "scope": {
            "type": "complete_publication",
            "statement": "All normative requirements.",
            "inventory_count": 1,
            "default_granularity": "requirement",
        },
        "mapper": {
            "id": "mapper-1",
            "qualification": "Qualified mapper",
            "date": "2026-07-13",
            "authorized_source_access": True,
        },
        "findings": [],
        "change_history": [change()],
    }
    if status in {"reviewed", "approved"}:
        value["reviewer"] = reviewer()
    if status == "approved":
        value["approver"] = {"id": "approver-1", "date": "2026-07-13"}
    return value


def valid_inventory() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "mapping_set_id": MAPPING_SET_ID,
        "scope_type": "complete_publication",
        "scope_statement": "All normative requirements.",
        "source_basis": "Official publication structure.",
        "expected_count": 1,
        "provision_ids": ["GV-1.1"],
    }


def valid_record(
    status: str = "draft", disposition: str = "mapped", granularity: str = "requirement"
) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": "1.0.0",
        "record_id": "gv-1-1",
        "mapping_set_id": MAPPING_SET_ID,
        "status": status,
        "external_provision_id": "GV-1.1",
        "granularity": granularity,
        "context": {"mode": "paraphrase", "summary": "Governance responsibilities are defined."},
        "source_locator": {"official_url": "https://example.com/standard#gv-1-1", "locator": "GV-1.1"},
        "disposition": disposition,
        "relationships": [relationship()] if disposition == "mapped" else [],
        "mapper": {"id": "mapper-1", "date": "2026-07-13"},
        "change_history": [change()],
    }
    if granularity != "requirement":
        value["granularity_exception"] = "No finer requirement identifier is published."
    if disposition != "mapped":
        value["negative_rationale"] = "No direct outcome relationship was identified."
    if status == "reviewed":
        value["reviewer"] = reviewer()
    return value


def valid_lifecycle() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "mapping_set_id": MAPPING_SET_ID,
        "snapshot_digest": SHA256,
        "events": [{
            "event_id": "initial-approval",
            "state": "approved",
            "date": "2026-07-13",
            "actor": "approver-1",
            "reason": "Review complete.",
            "approval_reference": "review-1",
            "previous_event_digest": "0" * 64,
            "event_digest": SHA256,
        }],
    }


def valid_manifest() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "esaf_release": "1.0.0",
        "source_commit_sha": SHA40,
        "control_catalog_sha256": SHA256,
        "controls": [{
            "id": "GOV-100",
            "version": "1.0.0",
            "status": "published",
            "path": "GOV/GOV-100.md",
            "record_sha256": SHA256,
        }],
    }


def delete_path(value: dict[str, object], path: str) -> dict[str, object]:
    result = copy.deepcopy(value)
    target: object = result
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[int(part)] if part.isdigit() else target[part]  # type: ignore[index]
    final = parts[-1]
    if final.isdigit():
        del target[int(final)]  # type: ignore[index]
    else:
        del target[final]  # type: ignore[index]
    return result


def object_paths(value: object, prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        paths.append(prefix)
        for key, child in value.items():
            paths.extend(object_paths(child, f"{prefix}.{key}" if prefix else key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            paths.extend(object_paths(child, f"{prefix}.{index}"))
    return paths


REQUIRED_PATHS = {
    "mapping-set": (
        "schema_version", "mapping_set_id", "authority", "authority.id", "authority.name",
        "publication", "publication.id", "publication.name", "source_version", "source_version.id",
        "source_version.label", "esaf_release", "esaf_release.id", "esaf_release.label",
        "esaf_release.source_commit_sha", "esaf_release.control_catalog_sha256",
        "esaf_release.control_manifest_path", "mapping_set_version", "status", "source",
        "source.official_url", "source.access_class", "source.licensing_note", "publication_rights",
        "publication_rights.basis", "publication_rights.permitted_elements",
        "publication_rights.prohibited_elements", "publication_rights.restrictions",
        "publication_rights.approved", "publication_rights.reviewer_id", "publication_rights.review_date",
        "scope", "scope.type", "scope.statement", "scope.inventory_count", "scope.default_granularity",
        "mapper", "mapper.id", "mapper.qualification", "mapper.date", "mapper.authorized_source_access",
        "findings", "change_history", "change_history.0.version", "change_history.0.date", "change_history.0.change",
    ),
    "provision-inventory": (
        "schema_version", "mapping_set_id", "scope_type", "scope_statement", "source_basis",
        "expected_count", "provision_ids",
    ),
    "mapping-record": (
        "schema_version", "record_id", "mapping_set_id", "status", "external_provision_id", "granularity",
        "context", "context.mode", "source_locator", "source_locator.official_url", "source_locator.locator",
        "disposition", "relationships", "mapper", "mapper.id", "mapper.date", "change_history",
        "change_history.0.version", "change_history.0.date", "change_history.0.change",
    ),
    "lifecycle-record": (
        "schema_version", "mapping_set_id", "snapshot_digest", "events", "events.0.event_id", "events.0.state",
        "events.0.date", "events.0.actor", "events.0.reason", "events.0.previous_event_digest", "events.0.event_digest",
    ),
    "esaf-control-manifest": (
        "schema_version", "esaf_release", "source_commit_sha", "control_catalog_sha256", "controls",
        "controls.0.id", "controls.0.version", "controls.0.status", "controls.0.path", "controls.0.record_sha256",
    ),
}


class CrosswalkSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = Path(__file__).resolve().parents[1]
        cls.validators = load_schemas(cls.repo)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def assert_valid(self, schema: str, value: object) -> None:
        self.assertEqual(schema_errors(self.validators[schema], value, "fixture"), [])

    def assert_invalid(self, schema: str, value: object, expected: str = "") -> None:
        errors = schema_errors(self.validators[schema], value, "fixture")
        self.assertTrue(errors)
        if expected:
            self.assertIn(expected, "\n".join(errors))

    def test_parse_front_matter_returns_metadata_and_body(self) -> None:
        path = self.root / "record.md"
        path.write_text("---\nrecord_id: req-1\n---\n# Record\n", encoding="utf-8", newline="\n")
        metadata, body = parse_front_matter(path)
        self.assertEqual(metadata["record_id"], "req-1")
        self.assertEqual(body, "# Record\n")

    def test_parse_front_matter_rejects_noncanonical_input(self) -> None:
        cases = {
            "bom": b"\xef\xbb\xbf---\na: b\n---\n",
            "crlf": b"---\r\na: b\r\n---\r\n",
            "missing": b"a: b\n",
            "malformed": b"---\na: b\n",
            "non_mapping": b"---\n- a\n---\n",
        }
        for name, raw in cases.items():
            with self.subTest(name=name):
                path = self.root / f"{name}.md"
                path.write_bytes(raw)
                with self.assertRaises(ValueError):
                    parse_front_matter(path)

    def test_valid_schema_variants(self) -> None:
        variants = (
            ("mapping-set", valid_mapping_set("draft")),
            ("mapping-set", valid_mapping_set("reviewed")),
            ("mapping-set", valid_mapping_set("approved")),
            ("provision-inventory", valid_inventory()),
            ("mapping-record", valid_record()),
            ("mapping-record", valid_record("reviewed", "mapped", "clause")),
            ("mapping-record", valid_record("reviewed", "no_direct_mapping")),
            ("mapping-record", valid_record("reviewed", "out_of_scope", "domain")),
            ("lifecycle-record", valid_lifecycle()),
            ("esaf-control-manifest", valid_manifest()),
        )
        for schema, value in variants:
            with self.subTest(schema=schema, status=value.get("status")):
                self.assert_valid(schema, value)

    def test_every_required_property_boundary(self) -> None:
        variants = {
            "mapping-set": valid_mapping_set(),
            "provision-inventory": valid_inventory(),
            "mapping-record": valid_record(),
            "lifecycle-record": valid_lifecycle(),
            "esaf-control-manifest": valid_manifest(),
        }
        for schema, paths in REQUIRED_PATHS.items():
            for path in paths:
                with self.subTest(schema=schema, path=path):
                    self.assert_invalid(schema, delete_path(variants[schema], path))

        conditional = (
            ("mapping-set", valid_mapping_set("reviewed"), "reviewer"),
            ("mapping-set", valid_mapping_set("reviewed"), "reviewer.id"),
            ("mapping-set", valid_mapping_set("reviewed"), "reviewer.qualification"),
            ("mapping-set", valid_mapping_set("reviewed"), "reviewer.date"),
            ("mapping-set", valid_mapping_set("reviewed"), "reviewer.authorized_source_access"),
            ("mapping-set", valid_mapping_set("reviewed"), "reviewer.findings_disposition"),
            ("mapping-set", valid_mapping_set("approved"), "approver"),
            ("mapping-set", valid_mapping_set("approved"), "approver.id"),
            ("mapping-set", valid_mapping_set("approved"), "approver.date"),
            ("mapping-record", valid_record("reviewed"), "reviewer"),
            ("mapping-record", valid_record("reviewed"), "reviewer.id"),
            ("mapping-record", valid_record("reviewed"), "reviewer.qualification"),
            ("mapping-record", valid_record("reviewed"), "reviewer.date"),
            ("mapping-record", valid_record("reviewed"), "reviewer.authorized_source_access"),
            ("mapping-record", valid_record("reviewed"), "reviewer.findings_disposition"),
            ("mapping-record", valid_record(), "context.summary"),
            ("mapping-record", valid_record(granularity="clause"), "granularity_exception"),
        )
        for schema, value, path in conditional:
            with self.subTest(schema=schema, path=path):
                self.assert_invalid(schema, delete_path(value, path))

        record = valid_record()
        for field in relationship():
            with self.subTest(schema="mapping-record", path=f"relationships.0.{field}"):
                self.assert_invalid("mapping-record", delete_path(record, f"relationships.0.{field}"))

    def test_every_enum_accepts_declared_values_and_rejects_unknown(self) -> None:
        cases = (
            ("mapping-set", "status", ("draft", "reviewed", "approved")),
            ("mapping-set", "source.access_class", ("public", "restricted", "licensed")),
            ("mapping-set", "scope.type", ("complete_publication", "declared_subset")),
            ("mapping-set", "scope.default_granularity", ("requirement", "clause", "domain")),
            ("mapping-record", "relationships.0.relationship", ("supports", "partially_supports", "complements", "prerequisite", "informs")),
            ("mapping-record", "relationships.0.direction", ("esaf_to_external", "external_to_esaf")),
            ("mapping-record", "relationships.0.coverage", ("substantial", "partial", "narrow", "contextual")),
            ("mapping-record", "relationships.0.confidence", ("high", "medium", "low")),
            ("lifecycle-record", "events.0.state", ("approved", "published", "deprecated", "retired")),
            ("esaf-control-manifest", "controls.0.status", ("proposed", "draft", "approved", "published", "deprecated", "retired")),
        )
        factories = {
            "mapping-set": valid_mapping_set,
            "mapping-record": valid_record,
            "lifecycle-record": valid_lifecycle,
            "esaf-control-manifest": valid_manifest,
        }
        for schema, path, values in cases:
            for enum_value in values:
                value = (
                    valid_mapping_set(enum_value)
                    if schema == "mapping-set" and path == "status"
                    else factories[schema]()
                )
                target: object = value
                parts = path.split(".")
                for part in parts[:-1]:
                    target = target[int(part)] if part.isdigit() else target[part]  # type: ignore[index]
                target[parts[-1]] = enum_value  # type: ignore[index]
                with self.subTest(schema=schema, path=path, value=enum_value):
                    self.assert_valid(schema, value)
            target[parts[-1]] = "not-a-declared-value"  # type: ignore[index]
            self.assert_invalid(schema, value)

    def test_mapping_schema_rejects_prohibited_relationship(self) -> None:
        record = valid_record()
        record["relationships"][0]["relationship"] = "equivalent"  # type: ignore[index]
        self.assert_invalid("mapping-record", record, "equivalent")

    def test_schemas_reject_additional_properties_at_every_object_boundary(self) -> None:
        variants = (
            ("mapping-set", valid_mapping_set("approved")),
            ("provision-inventory", valid_inventory()),
            ("mapping-record", valid_record("reviewed")),
            ("lifecycle-record", valid_lifecycle()),
            ("esaf-control-manifest", valid_manifest()),
        )
        for schema, original in variants:
            for path in object_paths(original):
                value = copy.deepcopy(original)
                target: object = value
                if path:
                    for part in path.split("."):
                        target = target[int(part)] if part.isdigit() else target[part]  # type: ignore[index]
                target["unexpected"] = True  # type: ignore[index]
                with self.subTest(schema=schema, path=path or "metadata"):
                    self.assert_invalid(schema, value, "unexpected")

    def test_state_and_disposition_conditionals(self) -> None:
        cases: list[tuple[str, dict[str, object], str]] = []
        reviewed_set = valid_mapping_set("reviewed")
        del reviewed_set["reviewer"]
        cases.append(("mapping-set", reviewed_set, "reviewer"))
        approved_set = valid_mapping_set("approved")
        del approved_set["approver"]
        cases.append(("mapping-set", approved_set, "approver"))
        reviewed_record = valid_record("reviewed")
        del reviewed_record["reviewer"]
        cases.append(("mapping-record", reviewed_record, "reviewer"))
        mapped = valid_record()
        mapped["relationships"] = []
        cases.append(("mapping-record", mapped, "relationships"))
        negative = valid_record(disposition="no_direct_mapping")
        negative["relationships"] = [relationship()]
        cases.append(("mapping-record", negative, "relationships"))
        clause = valid_record(granularity="clause")
        del clause["granularity_exception"]
        cases.append(("mapping-record", clause, "granularity_exception"))
        for schema, value, expected in cases:
            with self.subTest(schema=schema, expected=expected):
                self.assert_invalid(schema, value, expected)

    def test_context_modes_are_mutually_exclusive(self) -> None:
        identifier = valid_record()
        identifier["context"] = {"mode": "identifier_only", "omission_rationale": "Rights prohibit summaries."}
        self.assert_valid("mapping-record", identifier)
        identifier["context"]["summary"] = "Not permitted"  # type: ignore[index]
        self.assert_invalid("mapping-record", identifier, "summary")
        paraphrase = valid_record()
        paraphrase["context"]["omission_rationale"] = "Contradiction"  # type: ignore[index]
        self.assert_invalid("mapping-record", paraphrase, "omission_rationale")

    def test_finding_status_conditionals(self) -> None:
        base = {
            "finding_id": "finding-1",
            "affected_record_ids": ["gv-1-1"],
            "severity": "Minor",
            "status": "accepted",
            "description": "A minor residual issue.",
            "disposition": "Risk accepted.",
            "resolver_or_acceptor": "approver-1",
            "disposition_date": "2026-07-13",
            "acceptance_rationale": "Within tolerance.",
        }
        for missing in ("resolver_or_acceptor", "disposition_date", "acceptance_rationale"):
            value = valid_mapping_set("approved")
            finding = copy.deepcopy(base)
            del finding[missing]
            value["findings"] = [finding]
            with self.subTest(missing=missing):
                self.assert_invalid("mapping-set", value, missing)

    def test_array_and_format_constraints(self) -> None:
        inventory = valid_inventory()
        inventory["provision_ids"] = []
        self.assert_invalid("provision-inventory", inventory)
        inventory = valid_inventory()
        inventory["provision_ids"] = ["GV-1.1", "GV-1.1"]
        self.assert_invalid("provision-inventory", inventory, "unique")
        record = valid_record()
        record["relationships"][0]["conditions"] = []  # type: ignore[index]
        self.assert_invalid("mapping-record", record)
        manifest = valid_manifest()
        manifest["source_commit_sha"] = "ABC"
        self.assert_invalid("esaf-control-manifest", manifest, "does not match")

        record = valid_record()
        record["source_locator"]["official_url"] = "http://[invalid"  # type: ignore[index]
        self.assert_invalid("mapping-record", record, "not a 'uri'")

    def test_schema_documents_are_draft_2020_12_and_valid(self) -> None:
        from jsonschema import Draft202012Validator

        for path in sorted((self.repo / "crosswalks" / "schema").glob("*.schema.json")):
            with self.subTest(path=path.name):
                document = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(document["$schema"], "https://json-schema.org/draft/2020-12/schema")
                Draft202012Validator.check_schema(document)


if __name__ == "__main__":
    unittest.main()
