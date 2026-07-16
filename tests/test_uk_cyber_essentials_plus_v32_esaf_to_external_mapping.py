from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from tools.crosswalks.io import parse_front_matter
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
COMPLETED_GROUPS: tuple[str, ...] = ()


class CyberEssentialsPlusEsafToExternalMappingTests(unittest.TestCase):
    def test_mapping_rights_gate_is_exact_and_precedes_snapshot(self) -> None:
        self.assertTrue(RIGHTS.is_file())
        text = RIGHTS.read_text(encoding="utf-8")
        for value in (
            ORACLE_SHA256,
            CANONICAL_PDF_SHA256,
            LEGACY_PDF_SHA256,
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
