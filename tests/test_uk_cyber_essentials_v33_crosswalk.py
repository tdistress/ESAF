from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.crosswalks.io import parse_front_matter


ROOT = Path(__file__).parents[1]
SOURCE_URL = "https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf"
SOURCE_SHA256 = "e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923"
BASELINE_SHA = "5de9ff356ddad1e193444cd7308eff16ed83e811"
MAPPING_SET_ID = "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0"
SNAPSHOT = ROOT / "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0"
REGISTRY = ROOT / "crosswalks/registry" / f"{MAPPING_SET_ID}.md"
PROVISION_ORACLE = ROOT / "docs/superpowers/specs/2026-07-13-uk-cyber-essentials-v3.3-provision-oracle.json"


class UkCyberEssentialsV33CrosswalkTests(unittest.TestCase):
    def test_landing_page_freezes_source_rights_and_draft_boundary(self) -> None:
        text = (ROOT / "crosswalks/uk-cyber-essentials.md").read_text(encoding="utf-8")
        for expected in (
            "**Status:** Draft mapping in development",
            "Requirements for IT Infrastructure v3.3",
            SOURCE_URL,
            SOURCE_SHA256,
            "Open Government Licence v3.0",
            "116",
            "Cyber Essentials Plus",
            "does not establish certification",
        ):
            self.assertIn(expected, text)
        self.assertNotRegex(text, r"(?im)^\*\*Status:\*\*\s*(?:Reviewed|Approved|Published)\s*$")

    def test_decisions_lock_core_plus_separation_and_draft_posture(self) -> None:
        text = (ROOT / "project/DECISION_LOG.md").read_text(encoding="utf-8")
        for decision in (
            "Cyber Essentials core and Cyber Essentials Plus use separate mapping sets.",
            "Cyber Essentials v3.3 uses 116 ESAF-assigned atomic provision locators.",
            "The initial Cyber Essentials v3.3 mapping remains draft pending qualified human review.",
        ):
            self.assertIn(decision, text)
