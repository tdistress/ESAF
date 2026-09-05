from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

CORE = {
    "1300": ROOT / "governance" / "ESAF-1300.md",
    "1400": ROOT / "implementation" / "ESAF-1400.md",
    "1700": ROOT / "data-model" / "ESAF-1700.md",
}

PACK_FILES = {
    "1300": [
        "examples/esaf-1300/README.md",
        "examples/esaf-1300/charter-worksheet.md",
        "examples/esaf-1300/decision-rights-matrix.example.md",
        "examples/esaf-1300/exception-workflow.example.md",
    ],
    "1400": [
        "examples/esaf-1400/README.md",
        "examples/esaf-1400/adoption-vignette.example.md",
        "examples/esaf-1400/capability-control-mapping.example.md",
    ],
    "1700": [
        "examples/esaf-1700/README.md",
        "examples/esaf-1700/entity-instances.example.md",
    ],
}


class BreadthDeepenContracts(unittest.TestCase):
    def test_core_docs_are_version_0_2_0_working_draft(self) -> None:
        for key, path in CORE.items():
            text = path.read_text(encoding="utf-8")
            self.assertRegex(
                text,
                r"(?m)^(?:\|\s*Version\s*\|\s*0\.2\.0\s*\||\*\*Version:\*\*\s*0\.2\.0)",
                msg=f"{key} missing Version 0.2.0",
            )
            self.assertIn("Working Draft", text)

    def test_example_pack_files_exist(self) -> None:
        for paths in PACK_FILES.values():
            for relative in paths:
                self.assertTrue(
                    (ROOT / relative).is_file(),
                    msg=f"missing {relative}",
                )

    def test_core_docs_link_to_their_example_packs(self) -> None:
        expected = {
            "1300": "examples/esaf-1300/",
            "1400": "examples/esaf-1400/",
            "1700": "examples/esaf-1700/",
        }
        for key, needle in expected.items():
            text = CORE[key].read_text(encoding="utf-8")
            self.assertIn(
                needle,
                text.replace("\\", "/"),
                msg=f"{key} shall link to {needle}",
            )

    def test_esaf_1300_has_inline_example_anchors(self) -> None:
        text = CORE["1300"].read_text(encoding="utf-8")
        for needle in (
            "examples/esaf-1300/charter-worksheet.md",
            "examples/esaf-1300/decision-rights-matrix.example.md",
            "examples/esaf-1300/exception-workflow.example.md",
            "**Version:** 0.2.0",
        ):
            self.assertIn(needle, text.replace("\\", "/"))

    def test_esaf_1300_does_not_overstate_raci_or_quorum_requirements(self) -> None:
        text = CORE["1300"].read_text(encoding="utf-8")
        self.assertIn(
            "Internal audit or independent assurance is Informed at every gate.",
            text,
        )
        self.assertNotIn(
            "internal audit or independent assurance\nshall be Consulted",
            text,
        )
        self.assertNotIn(
            "quorum, and meeting cadence, as\nrequired by GOV-100",
            text,
        )

    def test_esaf_1400_has_inline_example_anchors(self) -> None:
        text = CORE["1400"].read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^\|\s*Version\s*\|\s*0\.2\.0\s*\|")
        for needle in (
            "examples/esaf-1400/adoption-vignette.example.md",
            "examples/esaf-1400/capability-control-mapping.example.md",
        ):
            self.assertIn(needle, text.replace("\\", "/"))

    def test_esaf_1400_vignette_uses_esaf_1500_record_identifiers(self) -> None:
        text = (
            ROOT / "examples/esaf-1400/adoption-vignette.example.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`EVD-140-001`", text)
        self.assertIn("`ASR-140-01`", text)
        for reserved_or_legacy in ("`EV-140-", "`ASM-140-", "`FND-140-"):
            self.assertNotIn(reserved_or_legacy, text)

    def test_esaf_1700_has_inline_example_anchors(self) -> None:
        text = CORE["1700"].read_text(encoding="utf-8")
        self.assertIn("**Version:** 0.2.0", text)
        self.assertIn(
            "examples/esaf-1700/entity-instances.example.md",
            text.replace("\\", "/"),
        )
        self.assertRegex(text, r"CAP-[A-Z0-9-]+")
        self.assertIn("EVD-", text)

    def test_esaf_1700_tables_and_example_cover_parent_attributes(self) -> None:
        core = CORE["1700"].read_text(encoding="utf-8")
        example = (
            ROOT / "examples/esaf-1700/entity-instances.example.md"
        ).read_text(encoding="utf-8")
        for attribute in (
            "required_evidence",
            "approval_authority",
            "monitoring",
            "review_frequency",
            "independent_assurance",
            "human_oversight",
            "acceptance_authority",
        ):
            marker = f"`{attribute}`"
            self.assertIn(marker, core, msg=f"core table missing {marker}")
            self.assertIn(marker, example, msg=f"example missing {marker}")

    def test_esaf_1400_remains_informative_without_local_shall(self) -> None:
        text = CORE["1400"].read_text(encoding="utf-8")
        self.assertIn("informative", text.lower())
        # Strip fenced code and quoted parent-publication restatements that
        # appear only inside explicit pointer sentences is unnecessary if the
        # document keeps the established rule: no bare "shall" outside the
        # informative-status / nonclaims section's "contains no shall".
        self.assertRegex(
            text,
            r"contains no `shall` requirements of its own",
        )
        body_after_status = text.split("## 2. Purpose", 1)[-1]
        self.assertIsNone(
            re.search(r"(?i)(?<!no )`shall`|(?<!no )(?<!contains no )shall ", body_after_status),
            msg="ESAF-1400 body after Purpose shall not introduce local shall",
        )

    def test_examples_readme_indexes_three_packs(self) -> None:
        text = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        for pack in ("esaf-1300", "esaf-1400", "esaf-1700"):
            self.assertIn(pack, text)
        self.assertRegex(text, r"(?i)non-normative|informative|not.*conformance")


if __name__ == "__main__":
    unittest.main()
