import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RIGHTS_REVIEW = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-07-25-pci-dss-publication-rights-review.md"
)

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


if __name__ == "__main__":
    unittest.main()
