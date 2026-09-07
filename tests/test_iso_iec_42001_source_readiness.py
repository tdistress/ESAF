import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RIGHTS_REVIEW = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-09-07-iso-iec-42001-publication-rights-review.md"
)
SOURCE_ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-07-iso-iec-42001-source-readiness-oracle.json"
)
TRACEABILITY = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-09-07-iso-iec-42001-2023-mapping-go-no-go-traceability.md"
)
ISO_LANDING = ROOT / "crosswalks" / "iso-iec-42001.md"
TOOLS_README = ROOT / "tools" / "README.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "catalog-validation.yml"
CROSSWALK_CATALOG = ROOT / "crosswalks" / "catalog.json"
CROSSWALK_README = ROOT / "crosswalks" / "README.md"
MAPPINGS_DIR = ROOT / "crosswalks" / "mappings"
REGISTRY_DIR = ROOT / "crosswalks" / "registry"

EXPECTED_TRACEABILITY_IDS = {
    "I143-D1A",
    "I143-D1B",
    "I143-D1C",
    "I143-D2",
    "I143-D3",
    "I143-D4",
    "I143-D5",
    "I143-GO1",
    "I143-HOLD1",
    "I143-A1",
    "I143-A2",
    "I143-A3",
    "I143-A4",
    "I143-B1",
    "I143-B2",
    "I143-B3",
    "I143-B4",
    "I143-B5",
    "I143-B6",
}

EXPECTED_READINESS_LINKS = {
    (
        "../docs/superpowers/specs/"
        "2026-09-07-iso-iec-42001-source-readiness-oracle.json"
    ),
    (
        "../docs/superpowers/reviews/"
        "2026-09-07-iso-iec-42001-publication-rights-review.md"
    ),
    (
        "../docs/superpowers/specs/"
        "2026-09-07-iso-iec-42001-mapping-readiness-matrix.json"
    ),
    (
        "../docs/superpowers/reviews/"
        "2026-09-07-iso-iec-42001-2023-mapping-go-no-go-review.md"
    ),
    (
        "../docs/superpowers/reviews/"
        "2026-09-07-iso-iec-42001-2023-mapping-go-no-go-traceability.md"
    ),
    "reviews/QUALIFIED_REVIEW_PROTOCOL.md",
}

EXPECTED_SOURCE_URLS = {
    "https://www.iso.org/copyright.html",
    "https://www.iso.org/standard/81230.html",
    "https://www.iso.org/obp/ui/",
}

EXPECTED_MAPPING_PARTITION = {
    "identifiers": "Prohibited",
    "titles": "Prohibited",
    "structural_inventory": "Prohibited",
    "paraphrases": "Prohibited",
    "derivative_mapping_analysis": "Prohibited",
    "official_links": "Permitted",
}

EXPECTED_BIBLIOGRAPHIC_METADATA = {
    "publisher_name",
    "publication_family_name",
    "document_reference",
    "version_label",
    "language",
    "format",
    "public_catalog_dates",
    "public_catalog_status_flags",
    "announcement_retirement_effective_dates",
    "retrieval_metadata",
    "official_urls",
}

EXPECTED_ORACLE_TOP_LEVEL_KEYS = {
    "access",
    "boundary",
    "dates",
    "discovery",
    "nonclaims",
    "publication",
    "rights_review",
    "schema_version",
    "source_artifact",
}

EXPECTED_PUBLICATION = {
    "document_reference": "ISO/IEC 42001:2023",
    "format": "PDF",
    "full_title": "Artificial intelligence — Management system",
    "language": "English",
    "publication_family": "ISO/IEC 42001",
    "publisher": (
        "International Organization for Standardization (ISO) / "
        "International Electrotechnical Commission (IEC)"
    ),
    "version": "2023",
}

RIGHTS_COMMIT = "8245a0513979a8e4d4dc28a4f22daa028710bee1"


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing section: {heading}")
    return match.group(1)


def markdown_table_dispositions(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\| `([^`]+)` \| (Permitted|Prohibited) \|", line)
        if match:
            rows[match.group(1)] = match.group(2)
    return rows


class IsoIec42001PublicationRightsReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.review = RIGHTS_REVIEW.read_text(encoding="utf-8")

    def test_records_reviewer_date_sources_and_hold_disposition(self) -> None:
        self.assertRegex(
            self.review,
            r"\*\*Reviewer:\*\* Codex ISO/IEC 42001 Publication Rights Reviewer R1",
        )
        self.assertRegex(self.review, r"\*\*Review date:\*\* 2026-09-07")
        self.assertRegex(self.review, r"\*\*Disposition:\*\* `HOLD`")

        sources = section(self.review, "Reviewed public rights sources")
        self.assertEqual(
            set(re.findall(r"https://[^)>`\s]+", sources)),
            EXPECTED_SOURCE_URLS,
        )

    def test_records_independence_access_and_publication_basis_attestations(self) -> None:
        self.assertIn(
            "**Reviewer independence:** The reviewer shall not serve as a mapper",
            self.review,
        )
        self.assertIn(
            "**Authorized public-rights-source access:** Attested",
            self.review,
        )
        self.assertIn(
            "**Publication basis reviewed:** Attested",
            self.review,
        )

    def test_mapping_field_classes_are_exhaustive_disjoint_and_fail_closed(self) -> None:
        partition = markdown_table_dispositions(
            section(self.review, "ESAF-1600 mapping field-class partition")
        )
        self.assertEqual(partition, EXPECTED_MAPPING_PARTITION)
        self.assertEqual(
            {name for name, disposition in partition.items() if disposition == "Permitted"},
            {"official_links"},
        )
        self.assertEqual(
            {name for name, disposition in partition.items() if disposition == "Prohibited"},
            set(EXPECTED_MAPPING_PARTITION) - {"official_links"},
        )

    def test_minimal_bibliographic_metadata_is_separate_from_mapping_fields(self) -> None:
        bibliographic_section = section(
            self.review, "Separate bibliographic source-identity allowance"
        )
        metadata = set(
            re.findall(
                r"^\| `([^`]+)` \| Permitted \|",
                bibliographic_section,
                re.MULTILINE,
            )
        )
        self.assertEqual(metadata, EXPECTED_BIBLIOGRAPHIC_METADATA)
        self.assertIn(
            "This allowance is separate from the six ESAF-1600 mapping field classes",
            bibliographic_section,
        )
        self.assertIn(
            "does not permit ISO/IEC 42001:2023 clause or control identifiers, titles, "
            "structural inventory, paraphrases, or derivative mapping analysis",
            bibliographic_section,
        )

    def test_requires_case_specific_written_permission(self) -> None:
        trigger = section(self.review, "Reconsideration trigger")
        self.assertIn("case-specific written permission", trigger)
        self.assertIn("equivalent licensing", trigger)
        self.assertIn(
            "covers the exact proposed artifact, field classes, publication channels, "
            "and redistribution terms",
            trigger,
        )
        self.assertIn("Until then, the disposition remains `HOLD`", trigger)

    def test_preserves_non_legal_advice_and_statutory_exception_boundaries(self) -> None:
        boundaries = section(self.review, "Decision boundaries")
        self.assertIn("This review is not legal advice", boundaries)
        self.assertIn(
            "does not decide whether any statutory exception is available",
            boundaries,
        )
        self.assertIn(
            "fail-closed absence-of-permission publication-control decision",
            boundaries,
        )


class IsoIec42001SourceReadinessOracleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = SOURCE_ORACLE.read_bytes()
        cls.oracle = json.loads(cls.raw)

    def test_is_canonical_one_line_utf8_lf_json(self) -> None:
        expected = (
            json.dumps(
                self.oracle,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )
        self.assertEqual(self.raw, expected)
        self.assertEqual(self.raw.count(b"\n"), 1)

    def test_has_closed_identity_and_rights_review_contract(self) -> None:
        self.assertEqual(set(self.oracle), EXPECTED_ORACLE_TOP_LEVEL_KEYS)
        self.assertEqual(self.oracle["schema_version"], "1.0.0")
        self.assertEqual(self.oracle["publication"], EXPECTED_PUBLICATION)
        self.assertEqual(
            self.oracle["rights_review"],
            {
                "commit": RIGHTS_COMMIT,
                "path": (
                    "docs/superpowers/reviews/"
                    "2026-09-07-iso-iec-42001-publication-rights-review.md"
                ),
            },
        )

    def test_pins_official_discovery_without_source_bytes(self) -> None:
        discovery = self.oracle["discovery"]
        self.assertEqual(
            set(discovery),
            {
                "official_product_page_url",
                "retrieval_attempt",
                "selected_document",
                "selected_version",
            },
        )
        self.assertEqual(
            discovery["official_product_page_url"],
            "https://www.iso.org/standard/81230.html",
        )
        self.assertEqual(
            discovery["selected_document"],
            {
                "full_title": "Artificial intelligence — Management system",
                "name": "ISO/IEC 42001",
                "protected": "yes",
                "reference": "ISO/IEC 42001:2023",
            },
        )
        self.assertEqual(
            discovery["selected_version"],
            {
                "edition": "1st edition",
                "format": "PDF",
                "language": "English",
                "title": "2023",
            },
        )
        retrieval = discovery["retrieval_attempt"]
        self.assertIs(retrieval["retained_source_bytes"], False)
        self.assertIsNone(retrieval["sha256"])
        self.assertEqual(retrieval["http_status"], 403)

    def test_separates_artifact_publication_year(self) -> None:
        self.assertEqual(
            self.oracle["dates"],
            {
                "artifact_publication": {"date": "2023", "precision": "year"},
                "edition": {"label": "1st edition", "year": "2023"},
            },
        )

    def test_records_protected_access_without_accepting_license(self) -> None:
        self.assertEqual(
            self.oracle["access"],
            {
                "browser_behavior": "commercial_purchase_required_for_normative_pdf",
                "direct_http_behavior": "public_product_page_access_challenge_not_source_bytes",
                "license_accepted": False,
                "protected": True,
            },
        )

    def test_keeps_source_artifact_and_inventory_fields_unavailable(self) -> None:
        self.assertEqual(
            self.oracle["source_artifact"],
            {
                "byte_length": None,
                "inventory_digest": None,
                "page_count": None,
                "provision_count": None,
                "sha256": None,
                "state": "unavailable",
            },
        )

    def test_distinguishes_normative_artifact_from_supporting_interfaces(self) -> None:
        self.assertEqual(
            self.oracle["boundary"],
            {
                "normative": {
                    "artifact": "ISO/IEC 42001:2023 English PDF",
                    "availability": "unavailable",
                    "url": "https://www.iso.org/standard/81230.html",
                },
                "supporting": [
                    {
                        "role": "official_product_page",
                        "url": "https://www.iso.org/standard/81230.html",
                    },
                    {
                        "role": "copyright_policy",
                        "url": "https://www.iso.org/copyright.html",
                    },
                    {
                        "role": "online_browsing_platform_landing",
                        "url": "https://www.iso.org/obp/ui/",
                    },
                ],
            },
        )

    def test_records_inventory_mapping_compliance_and_checksum_nonclaims(self) -> None:
        self.assertEqual(
            self.oracle["nonclaims"],
            {
                "catalog_digest_is_source_artifact_digest": False,
                "compliance_asserted": False,
                "mapping_exists": False,
                "provision_inventory_exists": False,
                "source_artifact_checksum_available": False,
            },
        )


class IsoIec42001ReadinessPublicationTests(unittest.TestCase):
    def test_traceability_covers_every_issue_143_obligation(self) -> None:
        text = TRACEABILITY.read_text(encoding="utf-8")
        rows = re.findall(
            r"^\| `(I143-[^`]+)` \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
            text,
            flags=re.MULTILINE,
        )
        row_ids = [row[0] for row in rows]
        self.assertEqual(set(row_ids), EXPECTED_TRACEABILITY_IDS)
        self.assertEqual(len(row_ids), len(set(row_ids)))

        evidence = {row_id: row for row_id, _kind, _commitment, row in rows}
        self.assertIn("source-readiness-oracle.json", evidence["I143-D1A"])
        self.assertIn("source artifact SHA-256 is `null`", evidence["I143-D1B"])
        self.assertIn("`ISO-IEC-42001-READINESS-B001`", evidence["I143-D1B"])
        self.assertIn("provision count and inventory digest are `null`", evidence["I143-D1C"])
        self.assertIn("`ISO-IEC-42001-READINESS-B003`", evidence["I143-D1C"])
        self.assertIn("publication-rights-review.md", evidence["I143-D2"])
        self.assertIn("mapping-readiness-matrix.json", evidence["I143-D3"])
        self.assertIn("mapping-readiness-matrix.json", evidence["I143-D4"])
        self.assertIn("mapping-go-no-go-review.md", evidence["I143-D5"])
        self.assertIn("ESAF-1600", evidence["I143-GO1"])
        self.assertIn("does not close issue 143", evidence["I143-GO1"])
        self.assertIn(
            "zero substantive ISO/IEC 42001 mapping artifacts",
            evidence["I143-HOLD1"],
        )

    def test_traceability_records_catalog_invariance_and_zero_mapping_artifacts(self) -> None:
        text = TRACEABILITY.read_text(encoding="utf-8")
        catalog = json.loads(CROSSWALK_CATALOG.read_text(encoding="utf-8"))
        counts = catalog["counts"]
        self.assertEqual(
            {
                "mapping_sets": counts["mapping_sets"],
                "provisions": counts["provisions"],
                "relationships": counts["relationships"],
                "negative_dispositions": counts["negative_dispositions"],
            },
            {
                "mapping_sets": 3,
                "provisions": 404,
                "relationships": 81,
                "negative_dispositions": 325,
            },
        )
        self.assertIn("| Mapping sets | 3 | 3 |", text)
        self.assertIn("| Provisions | 404 | 404 |", text)
        self.assertIn("| Relationships | 81 | 81 |", text)
        self.assertIn("| Negative dispositions | 325 | 325 |", text)
        self.assertIn("ISO/IEC 42001 mapping artifacts: `0`", text)
        for mapping_set in catalog["mapping_sets"]:
            publication_id = mapping_set["metadata"]["publication"]["id"].lower()
            blob = json.dumps(mapping_set).lower()
            self.assertNotIn("42001", publication_id)
            self.assertFalse("iso" in publication_id and "42001" in blob)
        inventory_hits = list(ROOT.glob("**/*iso*42001*inventory*.json"))
        inventory_hits += list(ROOT.glob("**/*42001*inventory*.json"))
        self.assertEqual(inventory_hits, [])
        mapping_hits = [
            path
            for path in list(MAPPINGS_DIR.rglob("*")) + list(REGISTRY_DIR.rglob("*"))
            if path.is_file()
            and ("iso" in path.name.lower() or "42001" in path.name.lower())
        ]
        self.assertEqual(mapping_hits, [])

    def test_iso_landing_page_publishes_hold_and_evidence_links(self) -> None:
        text = ISO_LANDING.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^\*\*Status:\*\* Readiness HOLD$")
        self.assertEqual(
            set(re.findall(r"\]\(([^)]+)\)", text)) & EXPECTED_READINESS_LINKS,
            EXPECTED_READINESS_LINKS,
        )
        self.assertIn("ISO/IEC 42001 mapping artifacts: `0`", text)
        self.assertIn("source artifact checksum is unavailable", text)
        self.assertIn("provision inventory is unavailable", text)
        self.assertIn("ESAF Project Maintainer", text)

    def test_crosswalk_readme_lists_iso_hold_package(self) -> None:
        text = CROSSWALK_README.read_text(encoding="utf-8")
        self.assertIn("[ISO/IEC 42001](iso-iec-42001.md)", text)
        self.assertIn("readiness `HOLD`", text)

    def test_ci_covers_readiness_inputs_and_checks_renderer(self) -> None:
        workflow = yaml.load(
            CI_WORKFLOW.read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        for event in ("pull_request", "push"):
            paths = workflow["on"][event]["paths"]
            self.assertIn("docs/superpowers/specs/**", paths)
            self.assertIn("docs/superpowers/reviews/**", paths)
            self.assertIn("crosswalks/**", paths)
            self.assertIn("tests/**", paths)
            self.assertIn("tools/render_iso_iec_42001_mapping_go_no_go.py", paths)

        self.assertIn("validation_gates", workflow["jobs"])
        steps = workflow["jobs"]["validation_gates"]["steps"]
        runs = [step.get("run") for step in steps]
        renderer = "python tools/render_iso_iec_42001_mapping_go_no_go.py --check"
        self.assertEqual(runs.count(renderer), 1)
        self.assertLess(
            runs.index("python tools/validate_crosswalks.py --check"),
            runs.index(renderer),
        )

    def test_tools_readme_documents_readiness_check(self) -> None:
        text = TOOLS_README.read_text(encoding="utf-8")
        self.assertIn(
            "python tools/render_iso_iec_42001_mapping_go_no_go.py --check",
            text,
        )


if __name__ == "__main__":
    unittest.main()
