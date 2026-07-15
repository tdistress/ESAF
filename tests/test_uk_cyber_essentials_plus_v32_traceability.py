from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACEABILITY = ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-traceability.md"
TRACKED_ARTIFACTS = {
    "Locked oracle": ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json",
    "Tracked reconciliation record": ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-inventory-reconciliation.md",
    "Rights review and R2 re-attestation": ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md",
    "Focused inventory contract test": ROOT / "tests/test_uk_cyber_essentials_plus_v32_inventory.py",
    "Focused link-validator test": ROOT / "tests/test_validate_links.py",
    "Link validator": ROOT / "tools/validate_links.py",
}


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


class SourceInventoryTraceabilityTests(unittest.TestCase):
    def test_tracked_artifact_digests_match_lf_normalized_bytes(self) -> None:
        text = TRACEABILITY.read_text(encoding="utf-8")
        for label, path in TRACKED_ARTIFACTS.items():
            match = re.search(
                rf"\| {re.escape(label)} \| SHA-256 `([0-9a-f]{{64}})` \|",
                text,
            )
            self.assertIsNotNone(match, label)
            self.assertEqual(normalized_sha256(path), match.group(1), label)
