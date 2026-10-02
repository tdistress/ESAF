import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "crosswalks/mappings/nist/ai-rmf/1.0/0.17-draft/0.1.0"
REGISTRY = ROOT / "crosswalks/registry/nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0.md"
SET_ID = "nist--ai-rmf--1.0--esaf-0.17-draft--0.1.0"


class NistAiRmfV10CrosswalkTests(unittest.TestCase):
    def test_snapshot_inventory_and_status(self) -> None:
        readme = (SNAPSHOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"mapping_set_id: {SET_ID}", readme)
        self.assertIn("status: draft", readme)
        inventory = (SNAPSHOT / "PROVISION_INVENTORY.md").read_text(encoding="utf-8")
        self.assertIn("expected_count: 72", inventory)
        records = sorted(SNAPSHOT.glob("airmf-*.md"))
        self.assertEqual(len(records), 72)
        self.assertTrue(REGISTRY.is_file())
        self.assertIn("events: []", REGISTRY.read_text(encoding="utf-8"))

    def test_catalog_includes_nist_set(self) -> None:
        catalog = json.loads((ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["counts"]["mapping_sets"], 5)
        self.assertEqual(catalog["counts"]["provisions"], 582)
        self.assertIn("nist", catalog["counts"]["by_authority"])


if __name__ == "__main__":
    unittest.main()
