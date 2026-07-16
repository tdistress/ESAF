from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from tools.crosswalks.io import parse_front_matter
from tools.crosswalks.digests import snapshot_digest
from tools.crosswalks.manifest import build_control_manifest, render_manifest
from tools.crosswalks.validation import validate
from tests.test_uk_cyber_essentials_plus_v32_inventory import (
    PERMITTED_SOURCE_IDENTITY_PROSE,
    SOURCE_FIVE_WORD_DIGESTS,
)


ROOT = Path(__file__).parents[1]
MAPPING_SET_ID = "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0"
SNAPSHOT = ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0"
REGISTRY = ROOT / "crosswalks/registry" / f"{MAPPING_SET_ID}.md"
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS = ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-esaf-to-external-mapping-rights-attestation.md"
BASELINE_SHA = "b4529c05c440db2f94ec12db4f21e3d0af57a5fb"
ORACLE_SHA256 = "8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc"
CANONICAL_PDF_SHA256 = "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8"
LEGACY_PDF_SHA256 = "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694"
FEASIBILITY_RIGHTS_COMMIT = "4207e1c1e8ff9f743274ebb4b626210cca053458"
EXPECTED_GROUP_COUNTS = {"M": 24, "T1": 16, "S": 11, "T2": 9, "T3": 37, "T4": 9, "T5": 7, "C": 13, "A": 4, "B": 14}
COMPLETED_GROUPS: tuple[str, ...] = ("M", "T1", "S", "T2")
CANONICAL_PDF_URL = "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf"
RESOURCE_PAGE = "https://www.ncsc.gov.uk/cyberessentials/resources"
MAPPER_ID = "esaf-crosswalk-editorial-team"


def record_id(external_id: str) -> str:
    return external_id.lower().replace(".", "")


def oracle_locator(locator: dict[str, object]) -> str:
    return (
        f"PDF page {locator['pdf_page']}; printed page {locator['printed_page']}; "
        f"{locator['section']}; {locator['detail']}"
    )


def record_narratives(record: dict[str, object]):
    context = record.get("context")
    if isinstance(context, dict) and isinstance(context.get("summary"), str):
        yield context["summary"]
    negative = record.get("negative_rationale")
    if isinstance(negative, str):
        yield negative
    relationships = record.get("relationships", [])
    if not isinstance(relationships, list):
        return
    for relationship in relationships:
        if not isinstance(relationship, dict):
            continue
        rationale = relationship.get("rationale")
        if isinstance(rationale, str):
            yield rationale
        for field in (
            "conditions",
            "expected_evidence",
            "known_gaps",
            "prohibited_inferences",
        ):
            values = relationship.get(field, [])
            if isinstance(values, list):
                yield from (value for value in values if isinstance(value, str))


def assert_no_copied_source_windows(
    testcase: unittest.TestCase,
    narratives: list[str],
    *,
    source_window_digests=SOURCE_FIVE_WORD_DIGESTS,
) -> None:
    for narrative in narratives:
        words = re.findall(r"[a-z0-9%]+", narrative.lower())
        for index in range(len(words) - 4):
            window = " ".join(words[index:index + 5])
            if any(window in phrase for phrase in PERMITTED_SOURCE_IDENTITY_PROSE):
                continue
            digest = hashlib.sha256(window.encode("utf-8")).digest()
            testcase.assertNotIn(
                digest,
                source_window_digests,
                f"normalized five-word source window reproduced: {window!r}",
            )


def assert_completed_batches_match(
    testcase: unittest.TestCase,
    snapshot: Path,
    oracle_provisions: list[dict[str, object]],
    manifest: dict[str, object],
    completed_groups: tuple[str, ...],
) -> None:
    controls = {item["id"]: item for item in manifest["controls"]}
    expected = [
        provision
        for provision in oracle_provisions
        if provision["group"] in completed_groups
    ]
    expected_names = {
        f"{record_id(provision['external_provision_id'])}.md"
        for provision in expected
    }
    actual_names = {
        path.name
        for path in snapshot.glob("*.md")
        if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
    }
    testcase.assertFalse(actual_names - expected_names)

    for oracle in expected:
        if f"{record_id(oracle['external_provision_id'])}.md" not in actual_names:
            continue
        path = snapshot / f"{record_id(oracle['external_provision_id'])}.md"
        record, _ = parse_front_matter(path)
        testcase.assertEqual(
            record["record_id"], record_id(oracle["external_provision_id"])
        )
        testcase.assertEqual(
            record["external_provision_id"], oracle["external_provision_id"]
        )
        testcase.assertEqual(
            record["external_metadata"],
            {field: oracle[field] for field in ("group", "kind", "actors")},
        )
        testcase.assertEqual(record["context"]["summary"], oracle["summary"])
        testcase.assertEqual(
            record["source_locator"]["locator"], oracle_locator(oracle["locator"])
        )
        testcase.assertEqual(
            record["mapper"],
            {
                "id": MAPPER_ID,
                "date": "2026-07-16",
                "authorized_source_access": True,
            },
        )
        testcase.assertEqual(record["status"], "draft")
        testcase.assertNotEqual(record["disposition"], "out_of_scope")
        narratives = list(record_narratives(record))
        testcase.assertTrue(narratives)
        testcase.assertTrue(all(value.strip() for value in narratives))
        assert_no_copied_source_windows(testcase, narratives)
        if record["disposition"] == "no_direct_mapping":
            testcase.assertIn("Missing outcome:", record["negative_rationale"])
        for relationship in record["relationships"]:
            testcase.assertEqual(relationship["direction"], "esaf_to_external")
            control = controls[relationship["esaf_control_id"]]
            testcase.assertEqual(
                relationship["esaf_control_version"], control["version"]
            )
            testcase.assertEqual(relationship["esaf_control_path"], control["path"])
            testcase.assertEqual(
                relationship["esaf_control_sha256"], control["record_sha256"]
            )
            testcase.assertEqual(
                relationship["esaf_requirement_locator"],
                f"controls/{control['path']}#requirement",
            )
            testcase.assertIn("rationale", relationship)
            testcase.assertIsInstance(relationship["rationale"], str)
            testcase.assertTrue(relationship["rationale"].strip())
            for field in (
                "conditions",
                "expected_evidence",
                "known_gaps",
                "prohibited_inferences",
            ):
                testcase.assertIn(field, relationship)
                testcase.assertIsInstance(relationship[field], list)
                testcase.assertTrue(relationship[field])
                testcase.assertTrue(
                    all(
                        isinstance(value, str) and value.strip()
                        for value in relationship[field]
                    )
                )
    testcase.assertEqual(actual_names, expected_names)


class CyberEssentialsPlusEsafToExternalMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.oracle = json.loads(ORACLE.read_text(encoding="utf-8"))
        cls.oracle_provisions = cls.oracle["provisions"]

    def assert_rights_bindings(self, text: str) -> None:
        lines = text.splitlines()
        for value in (
            f"oracle: {ORACLE.relative_to(ROOT).as_posix()}",
            f"oracle_sha256: {ORACLE_SHA256}",
            f"canonical_pdf_sha256: {CANONICAL_PDF_SHA256}",
            f"legacy_pdf_sha256: {LEGACY_PDF_SHA256}",
        ):
            self.assertIn(value, lines)
        for value in (
            f"feasibility_rights_commit: {FEASIBILITY_RIGHTS_COMMIT}",
            "attribution: National Cyber Security Centre; Crown copyright",
            "Open Government Licence v3.0",
            "ogl_v3_url: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            "copied requirement or passage text: prohibited",
            "IASME source-derived structure: prohibited",
            "marks and imagery: excluded",
            "source_version_boundary: public NCSC v3.2 only; current operational scheme not inferred",
            "direction: esaf_to_external",
            "reviewer_authorized_source_access: true",
            "field_classes: identifiers | titles where used | structural inventory | original paraphrases | derivative mapping analysis | ESAF normative citations | assurance analysis | official links",
            "disposition: approved",
        ):
            self.assertIn(value, text)
        self.assertNotIn("conditional approval", text.lower())
        reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", text)
        self.assertIsNotNone(reviewer)
        self.assertNotEqual(reviewer.group(1), "esaf-crosswalk-editorial-team")

    def test_rights_bindings_reject_rebinding_or_relabeling(self) -> None:
        text = RIGHTS.read_text(encoding="utf-8")
        mutations = {
            "changed oracle path": text.replace(
                f"oracle: {ORACLE.relative_to(ROOT).as_posix()}",
                "oracle: docs/superpowers/specs/substitute.json",
            ),
            "relabeled oracle digest": text.replace(
                "oracle_sha256:",
                "unrelated_sha256:",
            ),
        }
        for label, mutated in mutations.items():
            with self.subTest(label):
                self.assertNotEqual(mutated, text)
                with self.assertRaises(AssertionError):
                    self.assert_rights_bindings(mutated)

    def test_mapping_rights_gate_is_exact_and_precedes_snapshot(self) -> None:
        self.assertTrue(RIGHTS.is_file())
        text = RIGHTS.read_text(encoding="utf-8")
        self.assert_rights_bindings(text)

        rights_commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%H", "--", str(RIGHTS.relative_to(ROOT))],
            cwd=ROOT,
            text=True,
        ).strip()
        if not rights_commit:
            self.assertFalse(SNAPSHOT.exists(), "snapshot creation is blocked until rights are committed")
            return
        self.assertRegex(rights_commit, r"^[0-9a-f]{40}$")
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", FEASIBILITY_RIGHTS_COMMIT, rights_commit],
            cwd=ROOT,
            check=True,
        )
        rights_files = set(subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", rights_commit],
            cwd=ROOT,
            text=True,
        ).splitlines())
        self.assertEqual(rights_files, {
            str(RIGHTS.relative_to(ROOT)).replace("\\", "/"),
            "tests/test_uk_cyber_essentials_plus_v32_esaf_to_external_mapping.py",
        })
        first_snapshot_commit = subprocess.check_output(
            ["git", "log", "--diff-filter=A", "--format=%H", "--", str((SNAPSHOT / "README.md").relative_to(ROOT))],
            cwd=ROOT,
            text=True,
        ).splitlines()
        if first_snapshot_commit:
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", rights_commit, first_snapshot_commit[-1]],
                cwd=ROOT,
                check=True,
            )
        else:
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
            self.assertEqual(head, rights_commit, "rights commit must be HEAD before snapshot creation")

    def test_authoritative_snapshot_matches_pinned_oracle_and_rights(self) -> None:
        self.assertTrue((SNAPSHOT / "README.md").is_file())
        self.assertTrue((SNAPSHOT / "PROVISION_INVENTORY.md").is_file())
        self.assertTrue((SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").is_file())
        self.assertTrue(REGISTRY.is_file())

        mapping, readme = parse_front_matter(SNAPSHOT / "README.md")
        inventory, _ = parse_front_matter(SNAPSHOT / "PROVISION_INVENTORY.md")
        lifecycle, lifecycle_body = parse_front_matter(REGISTRY)
        rights_text = RIGHTS.read_text(encoding="utf-8")
        rights_reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", rights_text).group(1)

        self.assertEqual(mapping["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(mapping["authority"], {"id": "uk-ncsc", "name": "UK National Cyber Security Centre"})
        self.assertEqual(mapping["publication"]["id"], "cyber-essentials-plus-test-specification")
        self.assertEqual(mapping["source_version"], {"id": "3.2", "label": "3.2"})
        self.assertEqual(mapping["mapping_set_version"], "0.1.0")
        self.assertEqual(mapping["status"], "draft")
        self.assertEqual(mapping["source"]["official_url"], CANONICAL_PDF_URL)
        self.assertEqual(mapping["source"]["publication_date"], "2025-04-28")
        self.assertEqual(mapping["source"]["access_class"], "public")
        self.assertEqual(mapping["publication_rights"]["reviewer_id"], rights_reviewer)
        self.assertNotEqual(rights_reviewer, MAPPER_ID)
        self.assertEqual(mapping["mapper"]["id"], MAPPER_ID)
        self.assertEqual(mapping["mapper"]["date"], "2026-07-16")
        self.assertIs(mapping["mapper"]["authorized_source_access"], True)
        self.assertEqual(mapping["scope"]["type"], "complete_publication")
        self.assertEqual(mapping["scope"]["inventory_count"], 144)
        self.assertEqual(mapping["esaf_release"]["id"], "0.4-alpha")
        self.assertEqual(mapping["esaf_release"]["source_commit_sha"], BASELINE_SHA)

        for exact in (
            f"Oracle SHA-256: `{ORACLE_SHA256}`",
            f"Canonical PDF SHA-256: `{CANONICAL_PDF_SHA256}`",
            RESOURCE_PAGE,
            "public NCSC v3.2 technical draft",
            "not the current operational scheme",
            "assessment, certification, compliance, equivalence, or endorsement",
            "Copied requirement or passage text is prohibited",
            "IASME-authored structure remains outside this snapshot",
            "marks and imagery are excluded",
        ):
            self.assertIn(exact, readme)

        oracle_ids = [item["external_provision_id"] for item in self.oracle_provisions]
        self.assertEqual(self.oracle["counts"], {"total": 144, "by_group": EXPECTED_GROUP_COUNTS})
        self.assertEqual(Counter(item["group"] for item in self.oracle_provisions), Counter(EXPECTED_GROUP_COUNTS))
        self.assertEqual(inventory["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(inventory["scope_type"], "complete_publication")
        self.assertEqual(inventory["expected_count"], 144)
        self.assertEqual(inventory["provision_ids"], oracle_ids)

        self.assertEqual(lifecycle["mapping_set_id"], MAPPING_SET_ID)
        self.assertEqual(lifecycle["events"], [])
        self.assertEqual(lifecycle["snapshot_digest"], snapshot_digest(ROOT, SNAPSHOT))
        self.assertIn("state: draft", lifecycle_body)
        record_files = sorted(
            path for path in SNAPSHOT.glob("*.md")
            if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
        )
        self.assertEqual(len(record_files), sum(EXPECTED_GROUP_COUNTS[group] for group in COMPLETED_GROUPS))
        self.assertEqual(validate(ROOT).errors, [])

    def test_manifest_is_deterministic_at_exact_esaf_baseline(self) -> None:
        expected = build_control_manifest(ROOT, BASELINE_SHA, "0.4-alpha", None)
        self.assertEqual(len(expected["controls"]), 91)
        self.assertEqual(
            (SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8"),
            render_manifest(expected),
        )

    def test_draft_catalog_entry_and_counts_are_generated(self) -> None:
        catalog = json.loads((ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8"))
        entry = next(item for item in catalog["mapping_sets"] if item["metadata"]["mapping_set_id"] == MAPPING_SET_ID)
        self.assertEqual(entry["metadata"]["status"], "draft")
        self.assertEqual(entry["inventory"]["expected_count"], 144)
        self.assertEqual(len(entry["provisions"]), 60)
        self.assertEqual(entry["lifecycle"]["events"], [])
        self.assertEqual(catalog["counts"]["mapping_sets"], 2)
        self.assertEqual(catalog["counts"]["provisions"], 176)
        self.assertEqual(catalog["counts"]["relationships"], 46)
        self.assertEqual(catalog["counts"]["negative_dispositions"], 131)
        catalog_md = (ROOT / "crosswalks/CATALOG.md").read_text(encoding="utf-8")
        self.assertIn(MAPPING_SET_ID, catalog_md)

    def test_source_copy_guard_rejects_a_surrounded_five_word_window(self) -> None:
        copied = "assessor observes distinct authentication challenge"
        supplied = {hashlib.sha256(copied.encode("utf-8")).digest()}
        with self.assertRaises(AssertionError):
            assert_no_copied_source_windows(
                self,
                [f"Before review, {copied}, during the bounded check."],
                source_window_digests=supplied,
            )

    def test_completed_batch_helper_is_oracle_ordered_and_fails_closed(self) -> None:
        manifest = {
            "controls": [
                {
                    "id": "IAM-100",
                    "version": "0.1.0",
                    "path": "IAM/IAM-100.md",
                    "record_sha256": "a" * 64,
                }
            ]
        }
        provisions = [
            {
                "external_provision_id": external_id,
                "summary": f"Original summary for {external_id}.",
                "group": "T5",
                "kind": "result_rule",
                "actors": ["Assessor"],
                "locator": {
                    "pdf_page": 19,
                    "printed_page": 18,
                    "section": "Test case 5",
                    "detail": f"synthetic {external_id}",
                },
            }
            for external_id in ("CEPTS3.2-T5-002", "CEPTS3.2-T5-001")
        ]

        def record_for(provision: dict[str, object]) -> dict[str, object]:
            return {
                "record_id": record_id(provision["external_provision_id"]),
                "external_provision_id": provision["external_provision_id"],
                "external_metadata": {
                    field: provision[field] for field in ("group", "kind", "actors")
                },
                "context": {"mode": "paraphrase", "summary": provision["summary"]},
                "source_locator": {
                    "official_url": CANONICAL_PDF_URL,
                    "locator": oracle_locator(provision["locator"]),
                },
                "mapper": {
                    "id": MAPPER_ID,
                    "date": "2026-07-16",
                    "authorized_source_access": True,
                },
                "status": "draft",
                "disposition": "mapped",
                "relationships": [
                    {
                        "esaf_control_id": "IAM-100",
                        "esaf_control_version": "0.1.0",
                        "direction": "esaf_to_external",
                        "esaf_control_path": "IAM/IAM-100.md",
                        "esaf_control_sha256": "a" * 64,
                        "esaf_requirement_locator": "controls/IAM/IAM-100.md#requirement",
                        "rationale": "Original bounded mapping rationale.",
                        "conditions": ["The stated scope applies."],
                        "expected_evidence": ["A dated assessment record."],
                        "known_gaps": ["No certification conclusion is implied."],
                        "prohibited_inferences": ["Certification"],
                    }
                ],
            }

        def write_record(snapshot: Path, record: dict[str, object]) -> None:
            path = snapshot / f"{record['record_id']}.md"
            path.write_text(
                f"---\n{json.dumps(record, indent=2)}\n---\n# Synthetic record\n",
                encoding="utf-8",
                newline="\n",
            )

        with tempfile.TemporaryDirectory() as temporary:
            snapshot = Path(temporary)
            records = [record_for(provision) for provision in provisions]
            for record in records:
                write_record(snapshot, record)

            assert_completed_batches_match(
                self, snapshot, provisions, manifest, ("T5",)
            )

            mutations = [
                (
                    "context summary",
                    lambda record: record["context"].__setitem__(
                        "summary", "Changed summary."
                    ),
                ),
                (
                    "control version",
                    lambda record: record["relationships"][0].__setitem__(
                        "esaf_control_version", "9.9.9"
                    ),
                ),
            ]
            for field in (
                "rationale",
                "conditions",
                "expected_evidence",
                "known_gaps",
                "prohibited_inferences",
            ):
                mutations.append(
                    (
                        f"missing {field}",
                        lambda record, field=field: record["relationships"][0].pop(
                            field
                        ),
                    )
                )
            for label, mutation in mutations:
                with self.subTest(label=label):
                    changed = record_for(provisions[0])
                    mutation(changed)
                    write_record(snapshot, changed)
                    with self.assertRaises(AssertionError):
                        assert_completed_batches_match(
                            self, snapshot, provisions, manifest, ("T5",)
                        )
                    write_record(snapshot, records[0])

    def test_completed_batches_match_oracle_and_manifest(self) -> None:
        manifest = json.loads((SNAPSHOT / "ESAF_CONTROL_MANIFEST.json").read_text(encoding="utf-8"))
        assert_completed_batches_match(
            self,
            SNAPSHOT,
            self.oracle_provisions,
            manifest,
            COMPLETED_GROUPS,
        )

    def test_m_batch_positive_set_and_counts_are_exact(self) -> None:
        records = [
            parse_front_matter(SNAPSHOT / f"cepts32-m-{number:03d}.md")[0]
            for number in range(1, 25)
        ]
        positive_ids = {
            record["external_provision_id"]
            for record in records
            if record["disposition"] == "mapped"
        }
        self.assertEqual(positive_ids, {"CEPTS3.2-M-010", "CEPTS3.2-M-011"})
        self.assertEqual(sum(len(record["relationships"]) for record in records), 2)
        self.assertEqual(
            sum(record["disposition"] == "no_direct_mapping" for record in records),
            22,
        )

    def test_t1_batch_positive_set_and_counts_are_exact(self) -> None:
        records = [
            parse_front_matter(SNAPSHOT / f"cepts32-t1-{number:03d}.md")[0]
            for number in range(1, 17)
        ]
        self.assertEqual(
            {
                record["external_provision_id"]
                for record in records
                if record["disposition"] == "mapped"
            },
            {"CEPTS3.2-T1-011", "CEPTS3.2-T1-013"},
        )
        self.assertEqual(sum(len(record["relationships"]) for record in records), 2)
        self.assertEqual(
            sum(record["disposition"] == "no_direct_mapping" for record in records),
            14,
        )

    def test_t1_013_positive_basis_is_credential_rotation(self) -> None:
        record = parse_front_matter(SNAPSHOT / "cepts32-t1-013.md")[0]
        relationship = record["relationships"][0]
        rationale = relationship["rationale"].lower()
        self.assertIn("iam-140", rationale)
        self.assertIn("rotate", rationale)
        self.assertIn("default-password credential", rationale)

        evidence = [value.lower() for value in relationship["expected_evidence"]]
        self.assertTrue(
            any(
                "default-password credential" in value
                and ("rotated" in value or "changed" in value)
                for value in evidence
            )
        )

    def test_t1_review_identities_are_distinct_when_reports_exist(self) -> None:
        reports = (
            ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t1-specification-review.md",
            ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t1-overclaiming-review.md",
        )
        present = [path.is_file() for path in reports]
        self.assertIn(present, ([False, False], [True, True]))
        if not all(present):
            return

        rights_text = RIGHTS.read_text(encoding="utf-8")
        rights_reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", rights_text)
        self.assertIsNotNone(rights_reviewer)
        reviewer_ids = [MAPPER_ID, rights_reviewer.group(1)]
        for report in reports:
            text = report.read_text(encoding="utf-8")
            reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", text)
            self.assertIsNotNone(reviewer)
            self.assertIn("reviewer_authorized_source_access: true", text)
            reviewer_ids.append(reviewer.group(1))
        self.assertEqual(len(reviewer_ids), len(set(reviewer_ids)))

    def test_s_batch_positive_set_and_counts_are_exact(self) -> None:
        records = [
            parse_front_matter(SNAPSHOT / f"cepts32-s-{number:03d}.md")[0]
            for number in range(1, 12)
        ]
        self.assertEqual(
            {
                record["external_provision_id"]
                for record in records
                if record["disposition"] == "mapped"
            },
            {"CEPTS3.2-S-008"},
        )
        self.assertEqual(sum(len(record["relationships"]) for record in records), 1)
        self.assertEqual(
            sum(record["disposition"] == "no_direct_mapping" for record in records),
            10,
        )

    def test_s_review_identities_are_distinct_when_reports_exist(self) -> None:
        reports = (
            ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-s-specification-review.md",
            ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-s-overclaiming-review.md",
        )
        present = [path.is_file() for path in reports]
        self.assertIn(present, ([False, False], [True, True]))
        if not all(present):
            return

        rights_text = RIGHTS.read_text(encoding="utf-8")
        rights_reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", rights_text)
        self.assertIsNotNone(rights_reviewer)
        reviewer_ids = [MAPPER_ID, rights_reviewer.group(1)]
        for report in reports:
            text = report.read_text(encoding="utf-8")
            reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", text)
            self.assertIsNotNone(reviewer)
            self.assertIn("reviewer_authorized_source_access: true", text)
            reviewer_ids.append(reviewer.group(1))
        self.assertEqual(len(reviewer_ids), len(set(reviewer_ids)))

    def test_t2_batch_universe_and_counts_are_exact(self) -> None:
        records = [
            parse_front_matter(SNAPSHOT / f"cepts32-t2-{number:03d}.md")[0]
            for number in range(1, 10)
        ]
        expected_ids = {
            f"CEPTS3.2-T2-{number:03d}"
            for number in range(1, 10)
        }
        oracle_ids = {
            provision["external_provision_id"]
            for provision in self.oracle_provisions
            if provision["group"] == "T2"
        }
        self.assertEqual(oracle_ids, expected_ids)
        self.assertEqual(
            {record["external_provision_id"] for record in records},
            expected_ids,
        )
        self.assertEqual(
            {
                record["external_provision_id"]
                for record in records
                if record["disposition"] == "mapped"
            },
            set(),
        )
        self.assertEqual(sum(len(record["relationships"]) for record in records), 0)
        self.assertEqual(
            sum(record["disposition"] == "no_direct_mapping" for record in records),
            9,
        )

    def test_t2_known_anomaly_is_recorded_without_expansion(self) -> None:
        self.assertEqual(len(self.oracle["known_anomalies"]), 1)
        anomaly = self.oracle["known_anomalies"][0]
        self.assertEqual(anomaly["anomaly_id"], "cepts32-anomaly-001")
        self.assertEqual(
            oracle_locator(anomaly["locator"]),
            "PDF page 6; printed page 5; General prerequisites for testing; "
            "introductory applicability line",
        )
        self.assertEqual(
            anomaly["treatment"],
            "Recorded without correction or expansion; the publication itself "
            "presents only Test cases 1 through 5.",
        )
        self.assertNotIn(
            anomaly["anomaly_id"],
            {provision["external_provision_id"] for provision in self.oracle_provisions},
        )
        self.assertFalse(
            any(
                provision["locator"] == anomaly["locator"]
                for provision in self.oracle_provisions
            )
        )
        t2_text = "\n".join(
            (SNAPSHOT / f"cepts32-t2-{number:03d}.md").read_text(encoding="utf-8")
            for number in range(1, 10)
        )
        self.assertNotIn(anomaly["source_literal"], t2_text)

    def test_t2_review_identities_are_distinct_when_reports_exist(self) -> None:
        reports = (
            ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t2-specification-review.md",
            ROOT / "docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-t2-overclaiming-review.md",
        )
        present = [path.is_file() for path in reports]
        self.assertIn(present, ([False, False], [True, True]))
        if not all(present):
            return

        rights_text = RIGHTS.read_text(encoding="utf-8")
        rights_reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", rights_text)
        self.assertIsNotNone(rights_reviewer)
        reviewer_ids = [MAPPER_ID, rights_reviewer.group(1)]
        for report in reports:
            text = report.read_text(encoding="utf-8")
            reviewer = re.search(r"(?m)^reviewer_id: (\S+)$", text)
            self.assertIsNotNone(reviewer)
            self.assertIn("reviewer_authorized_source_access: true", text)
            reviewer_ids.append(reviewer.group(1))
        self.assertEqual(len(reviewer_ids), len(set(reviewer_ids)))
