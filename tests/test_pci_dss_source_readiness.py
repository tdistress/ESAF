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
    / "2026-07-25-pci-dss-publication-rights-review.md"
)
SOURCE_ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-25-pci-dss-source-readiness-oracle.json"
)
TRACEABILITY = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-07-25-pci-dss-mapping-go-no-go-traceability.md"
)
PCI_LANDING = ROOT / "crosswalks" / "pci-dss.md"
BACKLOG = ROOT / "project" / "BACKLOG.md"
TOOLS_README = ROOT / "tools" / "README.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "catalog-validation.yml"
CROSSWALK_CATALOG = ROOT / "crosswalks" / "catalog.json"

EXPECTED_TRACEABILITY_IDS = {
    "I58-D1A",
    "I58-D1B",
    "I58-D1C",
    "I58-D2",
    "I58-D3",
    "I58-D4",
    "I58-D5",
    "I58-GO1",
    "I58-HOLD1",
    "I58-A1",
    "I58-A2",
    "I58-A3",
    "I58-A4",
    "I58-B1",
    "I58-B2",
    "I58-B3",
    "I58-B4",
    "I58-B5",
    "I58-B6",
}

EXPECTED_READINESS_LINKS = {
    (
        "../docs/superpowers/specs/"
        "2026-07-25-pci-dss-source-readiness-oracle.json"
    ),
    (
        "../docs/superpowers/reviews/"
        "2026-07-25-pci-dss-publication-rights-review.md"
    ),
    (
        "../docs/superpowers/specs/"
        "2026-07-25-pci-dss-mapping-readiness-matrix.json"
    ),
    (
        "../docs/superpowers/reviews/"
        "2026-07-25-pci-dss-mapping-go-no-go-review.md"
    ),
    (
        "../docs/superpowers/reviews/"
        "2026-07-25-pci-dss-mapping-go-no-go-traceability.md"
    ),
    "reviews/QUALIFIED_REVIEW_PROTOCOL.md",
}

EXPECTED_SOURCE_URLS = {
    "https://www.pcisecuritystandards.org/terms_and_conditions/",
    "https://www.pcisecuritystandards.org/about_us/policies/",
    (
        "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/"
        "PCI-DSS-v4_0_1.pdf"
    ),
    "https://programs.pcissc.org/mla_registration.aspx",
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
    "document_reference": "pci_dss",
    "format": "PDF",
    "language": "English",
    "publication_family": "PCI DSS",
    "publisher": "PCI Security Standards Council",
    "version": "v4.0.1",
}

EXPECTED_DISCOVERY_CATALOG = {
    "byte_length": 1018867,
    "final_url": "https://docs-pub.pcisecuritystandards.org/doc_library.json",
    "retrieved_at_utc": "2026-07-26T00:55:54.992Z",
    "sha256": "6af4ba6221059e2580f7f312e179d579c02bb2bb908aee7cfe096ec7e3b58f0c",
    "sha256_scope": "mutable_public_discovery_metadata_not_standard",
}

EXPECTED_SELECTED_DOCUMENT = {
    "agreement": "pcidss",
    "archived": False,
    "category": "Standard",
    "last_updated": "2024-06-11T07:00:00+00:00",
    "name": "PCI DSS",
    "parent_reference": "pcidss",
    "protected": "yes",
    "reference": "pci_dss",
}

EXPECTED_SELECTED_VERSION = {
    "archived": False,
    "english_pdf_url": (
        "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/"
        "PCI-DSS-v4_0_1.pdf"
    ),
    "title": "v4.0.1",
}


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing section: {heading}")
    return match.group(1)


def top_level_list_item(text: str, marker: str) -> str:
    items: list[str] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if line.startswith("- "):
            if current is not None:
                items.append("\n".join(current))
            current = [line]
        elif line.startswith("#"):
            if current is not None:
                items.append("\n".join(current))
                current = None
        elif current is not None:
            current.append(line)
    if current is not None:
        items.append("\n".join(current))

    matches = [item for item in items if marker in item]
    if len(matches) != 1:
        raise AssertionError(
            f"expected exactly one top-level list item containing {marker!r}, found {len(matches)}"
        )
    return matches[0]


def markdown_table_dispositions(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\| `([^`]+)` \| (Permitted|Prohibited) \|", line)
        if match:
            rows[match.group(1)] = match.group(2)
    return rows


class PciDssPublicationRightsReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.review = RIGHTS_REVIEW.read_text(encoding="utf-8")

    def test_records_reviewer_date_sources_and_hold_disposition(self) -> None:
        self.assertRegex(
            self.review,
            r"\*\*Reviewer:\*\* Codex PCI DSS Publication Rights Reviewer R1",
        )
        self.assertRegex(self.review, r"\*\*Review date:\*\* 2026-07-25")
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
        metadata = set(re.findall(r"^\| `([^`]+)` \| Permitted \|", bibliographic_section, re.MULTILINE))
        self.assertEqual(metadata, EXPECTED_BIBLIOGRAPHIC_METADATA)
        self.assertIn(
            "This allowance is separate from the six ESAF-1600 mapping field classes",
            bibliographic_section,
        )
        self.assertIn(
            "does not permit PCI DSS provision identifiers, provision titles, "
            "structural inventory, paraphrases, or derivative mapping analysis",
            bibliographic_section,
        )

    def test_requires_case_specific_written_materials_license(self) -> None:
        trigger = section(self.review, "Reconsideration trigger")
        self.assertIn("case-specific written Materials License Agreement", trigger)
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


class PciDssSourceReadinessOracleTests(unittest.TestCase):
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
                "commit": "5bc0d82ea6dd7af3391497fc4b75be18ceb505a6",
                "path": (
                    "docs/superpowers/reviews/"
                    "2026-07-25-pci-dss-publication-rights-review.md"
                ),
            },
        )

    def test_pins_retrieved_catalog_and_selected_values(self) -> None:
        discovery = self.oracle["discovery"]
        self.assertEqual(
            set(discovery),
            {
                "catalog",
                "document_library_url",
                "selected_document",
                "selected_version",
            },
        )
        self.assertEqual(discovery["catalog"], EXPECTED_DISCOVERY_CATALOG)
        self.assertEqual(
            discovery["document_library_url"],
            "https://www.pcisecuritystandards.org/document_library/",
        )
        self.assertEqual(discovery["selected_document"], EXPECTED_SELECTED_DOCUMENT)
        self.assertEqual(discovery["selected_version"], EXPECTED_SELECTED_VERSION)

    def test_separates_artifact_publication_from_other_public_dates(self) -> None:
        self.assertEqual(
            self.oracle["dates"],
            {
                "announcement": {
                    "date": "2024-06-11",
                    "precision": "day",
                    "url": (
                        "https://blog.pcisecuritystandards.org/"
                        "just-published-pci-dss-v4-0-1"
                    ),
                },
                "artifact_publication": {
                    "date": "2024-06",
                    "precision": "month",
                },
                "catalog_last_updated": "2024-06-11T07:00:00+00:00",
                "current_retirement": {
                    "date": None,
                    "status": "not_announced",
                },
                "future_dated_requirements_effective": {
                    "date": "2025-03-31",
                    "precision": "day",
                },
                "predecessor_retirement": {
                    "date": "2024-12-31",
                    "precision": "day",
                    "version": "v4.0",
                },
            },
        )

    def test_records_protected_access_without_accepting_license(self) -> None:
        self.assertEqual(
            self.oracle["access"],
            {
                "browser_behavior": "license_interstitial_requires_acceptance",
                "direct_http_behavior": "access_response_not_pdf_bytes",
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
                    "artifact": "PCI DSS v4.0.1 English PDF",
                    "availability": "unavailable",
                    "url": EXPECTED_SELECTED_VERSION["english_pdf_url"],
                },
                "supporting": [
                    {
                        "role": "document_library",
                        "url": "https://www.pcisecuritystandards.org/document_library/",
                    },
                    {
                        "role": "mutable_discovery_catalog",
                        "url": "https://docs-pub.pcisecuritystandards.org/doc_library.json",
                    },
                    {
                        "role": "publication_announcement",
                        "url": (
                            "https://blog.pcisecuritystandards.org/"
                            "just-published-pci-dss-v4-0-1"
                        ),
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


class PciDssReadinessPublicationTests(unittest.TestCase):
    def test_traceability_covers_every_issue_58_obligation(self) -> None:
        text = TRACEABILITY.read_text(encoding="utf-8")
        rows = re.findall(
            r"^\| `(I58-[^`]+)` \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
            text,
            flags=re.MULTILINE,
        )
        row_ids = [row[0] for row in rows]
        self.assertEqual(set(row_ids), EXPECTED_TRACEABILITY_IDS)
        self.assertEqual(len(row_ids), len(set(row_ids)))

        evidence = {row_id: row for row_id, _kind, _commitment, row in rows}
        self.assertIn("source-readiness-oracle.json", evidence["I58-D1A"])
        self.assertIn("source artifact SHA-256 is `null`", evidence["I58-D1B"])
        self.assertIn("`PCI-READINESS-B001`", evidence["I58-D1B"])
        self.assertIn("provision count and inventory digest are `null`", evidence["I58-D1C"])
        self.assertIn("`PCI-READINESS-B003`", evidence["I58-D1C"])
        self.assertIn("publication-rights-review.md", evidence["I58-D2"])
        self.assertIn("mapping-readiness-matrix.json", evidence["I58-D3"])
        self.assertIn("mapping-readiness-matrix.json", evidence["I58-D4"])
        self.assertIn("mapping-go-no-go-review.md", evidence["I58-D5"])
        self.assertIn("ESAF-1600", evidence["I58-GO1"])
        self.assertIn("does not close issue 58", evidence["I58-GO1"])
        self.assertIn("zero substantive PCI DSS mapping artifacts", evidence["I58-HOLD1"])

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
        self.assertIn("PCI DSS mapping artifacts: `0`", text)
        self.assertFalse(
            any(
                "pci" in mapping_set["metadata"]["publication"]["id"].lower()
                for mapping_set in catalog["mapping_sets"]
            )
        )

    def test_pci_landing_page_publishes_hold_and_evidence_links(self) -> None:
        text = PCI_LANDING.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^\*\*Status:\*\* Readiness HOLD$")
        self.assertEqual(
            set(re.findall(r"\]\(([^)]+)\)", text)) & EXPECTED_READINESS_LINKS,
            EXPECTED_READINESS_LINKS,
        )
        self.assertIn("PCI DSS mapping artifacts: `0`", text)
        self.assertIn("source artifact checksum is unavailable", text)
        self.assertIn("provision inventory is unavailable", text)
        self.assertIn("ESAF Project Maintainer", text)

    def test_backlog_marks_issues_58_and_59_completed_while_55_is_deferred(
        self,
    ) -> None:
        text = BACKLOG.read_text(encoding="utf-8")
        deferred = section(text, "Deferred assurance follow-up")
        completed = section(text, "Completed workstreams")
        issue_59_url = "https://github.com/tdistress/ESAF/issues/59"
        issue_55_url = "https://github.com/tdistress/ESAF/issues/55"
        issue_59 = top_level_list_item(completed, issue_59_url)
        self.assertRegex(
            issue_59,
            r"publication gates, is closed",
        )
        self.assertRegex(issue_59, r"Working Draft was published\s+on 2026-08-01")
        self.assertIn("255f8806917aaf8c6a2441152b4638fc9fd2bfda", issue_59)
        self.assertNotIn("https://github.com/tdistress/ESAF/issues/59", deferred)
        issue_55 = top_level_list_item(deferred, issue_55_url)
        self.assertIn(issue_55_url, issue_55)
        self.assertRegex(
            issue_55,
            r"remains open until\s+qualified review is complete",
        )
        self.assertRegex(
            issue_55,
            r"owner-risk disposition defers this work and does not complete\s+qualified review or change a mapping lifecycle state",
        )
        self.assertIn("https://github.com/tdistress/ESAF/issues/58", completed)
        self.assertRegex(
            completed,
            r"completed through the evidenced `HOLD`\s+path",
        )

    def test_top_level_list_item_excludes_decoy_conditions_and_rejects_duplicate_markers(
        self,
    ) -> None:
        issue_url = "https://github.com/tdistress/ESAF/issues/55"
        decoy_condition = (
            "owner-risk disposition defers this work and does not complete "
            "qualified review or change a mapping lifecycle state"
        )
        item = top_level_list_item(
            "\n".join(
                (
                    f"- [Issue 55]({issue_url}) remains open",
                    "  until qualified review is complete.",
                    f"- Decoy item keeps the {decoy_condition}.",
                )
            ),
            issue_url,
        )
        self.assertIn("remains open", item)
        self.assertNotIn(decoy_condition, item)
        with self.assertRaisesRegex(AssertionError, "exactly one"):
            top_level_list_item("- another item", "marker")
        with self.assertRaisesRegex(AssertionError, "exactly one"):
            top_level_list_item("- marker\n- marker", "marker")

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
            self.assertIn("project/**", paths)
            self.assertIn("tests/**", paths)
            self.assertIn("tools/render_pci_dss_mapping_go_no_go.py", paths)

        steps = workflow["jobs"]["validate"]["steps"]
        runs = [step.get("run") for step in steps]
        self.assertEqual(
            runs.count(
                "python -m unittest discover -s tests -v --durations 50"
            ),
            1,
        )
        renderer = "python tools/render_pci_dss_mapping_go_no_go.py --check"
        self.assertEqual(runs.count(renderer), 1)
        self.assertLess(
            runs.index("python tools/validate_crosswalks.py --check"),
            runs.index(renderer),
        )

    def test_tools_readme_documents_readiness_check(self) -> None:
        text = TOOLS_README.read_text(encoding="utf-8")
        self.assertIn(
            "python tools/render_pci_dss_mapping_go_no_go.py --check",
            text,
        )


if __name__ == "__main__":
    unittest.main()
