import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "crosswalks/mappings/nist/csf/2.0/0.17-draft/0.1.0"
REGISTRY = ROOT / "crosswalks/registry/nist--csf--2.0--esaf-0.17-draft--0.1.0.md"
SET_ID = "nist--csf--2.0--esaf-0.17-draft--0.1.0"


class NistCsfV20CrosswalkTests(unittest.TestCase):
    def test_snapshot_inventory_and_status(self) -> None:
        readme = (SNAPSHOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"mapping_set_id: {SET_ID}", readme)
        self.assertIn("status: draft", readme)
        inventory = (SNAPSHOT / "PROVISION_INVENTORY.md").read_text(encoding="utf-8")
        self.assertIn("expected_count: 106", inventory)
        records = sorted(SNAPSHOT.glob("csf-*.md"))
        self.assertEqual(len(records), 106)
        self.assertTrue(REGISTRY.is_file())
        self.assertIn("events: []", REGISTRY.read_text(encoding="utf-8"))

    def test_catalog_includes_nist_csf_set(self) -> None:
        catalog = json.loads((ROOT / "crosswalks/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["counts"]["mapping_sets"], 5)
        self.assertEqual(catalog["counts"]["provisions"], 582)
        self.assertIn("nist", catalog["counts"]["by_authority"])
        self.assertEqual(catalog["counts"]["by_authority"]["nist"], 2)
        self.assertEqual(catalog["counts"]["by_publication"].get("csf"), 1)


if __name__ == "__main__":
    unittest.main()
