from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.mermaid_inventory import check_record, discover, extract_blocks, ledger_rows, write_render_inputs

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md"
SCRIPT = ROOT / "tools/mermaid_inventory.py"


class MermaidInventoryTests(unittest.TestCase):
    def test_extract_blocks_accepts_lf_and_crlf_fences(self) -> None:
        text = "```mermaid\r\ngraph TD\r\nA-->B\r\n```\r\n\n```mermaid\nsequenceDiagram\nA->>B: ok\n```\n"
        self.assertEqual(extract_blocks(text), ["graph TD\nA-->B", "sequenceDiagram\nA->>B: ok"])

    def test_repository_inventory_is_complete_and_deterministic(self) -> None:
        first = discover(ROOT)
        second = discover(ROOT)
        self.assertEqual(first, second)
        self.assertEqual(23, len(first))
        self.assertEqual([(item.path, item.index) for item in first], sorted((item.path, item.index) for item in first))
        for item in first:
            self.assertEqual(item.digest, sha256(item.source.encode("utf-8")).hexdigest())

    def test_render_inputs_are_outside_repository_and_exact(self) -> None:
        blocks = discover(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve()
            inventory = write_render_inputs(blocks, output)
            self.assertFalse(output.is_relative_to(ROOT.resolve()))
            self.assertTrue(inventory.is_file())
            self.assertEqual(len(blocks), len(list(output.glob("*.mmd"))))

    def test_render_inputs_reject_repository_destination(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            write_render_inputs(discover(ROOT)[:1], ROOT / "renderer-output")

    def test_render_inputs_reject_external_non_temp_and_sibling_prefix_destinations(self) -> None:
        blocks = discover(ROOT)[:1]
        temporary_root = Path(tempfile.gettempdir()).resolve()
        destinations = [
            ROOT.parent / "renderer-output",
            temporary_root.parent / f"{temporary_root.name}-sibling",
        ]
        for destination in destinations:
            with self.subTest(destination=destination):
                with self.assertRaisesRegex(ValueError, "system temporary"):
                    write_render_inputs(blocks, destination)

    def test_render_inputs_reject_preexisting_nonempty_temp_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "renderer-inputs"
            output.mkdir()
            (output / "existing.txt").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "shall be empty"):
                write_render_inputs(discover(ROOT)[:1], output)

    def test_render_inputs_have_exact_normalized_contents_and_manifest(self) -> None:
        blocks = discover(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "renderer-inputs"
            inventory = write_render_inputs(blocks, output)
            expected_rows = []
            for ordinal, block in enumerate(blocks, start=1):
                name = f"{ordinal:03d}-{Path(block.path).stem}-{block.index}.mmd"
                self.assertEqual((output / name).read_bytes(), (block.source + "\n").encode("utf-8"))
                expected_rows.append(
                    {"path": block.path, "index": block.index, "digest": block.digest, "source": None, "input": name}
                )
            self.assertEqual(json.loads(inventory.read_text(encoding="utf-8")), expected_rows)
            self.assertEqual(list(output.glob("*.mmd")), [output / row["input"] for row in expected_rows])

    def test_check_record_accepts_exact_passing_rows(self) -> None:
        blocks = discover(ROOT)[:2]
        text = ledger_rows(blocks).replace("| Pending | Pending | Pending |", "| Pass | Pass | Reviewer |")
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            record.write_text(text + "\n", encoding="utf-8")
            self.assertEqual(check_record(blocks, record), [])

    def test_check_record_rejects_mismatched_and_duplicate_rows(self) -> None:
        blocks = discover(ROOT)[:2]
        rows = ledger_rows(blocks).replace("| Pending | Pending | Pending |", "| Pass | Pass | Reviewer |").splitlines()
        mismatched = rows.copy()
        mismatched[0] = mismatched[0].replace(blocks[0].digest, "0" * 64)
        duplicated = rows + [rows[0]]
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            record.write_text("\n".join(mismatched) + "\n", encoding="utf-8")
            self.assertIn("ledger rows do not exactly match the current Mermaid inventory", check_record(blocks, record))
            record.write_text("\n".join(duplicated) + "\n", encoding="utf-8")
            self.assertIn("ledger rows do not exactly match the current Mermaid inventory", check_record(blocks, record))

    def test_check_record_requires_both_render_and_readability_pass(self) -> None:
        block = discover(ROOT)[:1]
        rows = ledger_rows(block)
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            for disposition in ("| Pass | Pending | Reviewer |", "| Pending | Pass | Reviewer |"):
                record.write_text(rows.replace("| Pending | Pending | Pending |", disposition) + "\n", encoding="utf-8")
                self.assertIn("not fully reviewed", "\n".join(check_record(block, record)))

    def test_cli_check_record_reports_pending_canonical_ledger(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check-record", str(LEDGER)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertNotIn("ledger rows do not exactly match", result.stderr)
        self.assertEqual(result.stderr.count("is not fully reviewed"), 23)

    def test_cli_check_record_rejects_fabricated_external_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            record.write_text("| `x.md` | 1 | `" + "0" * 64 + "` | Pass | Pass | Reviewer |\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--check-record", str(record)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exact tracked release ledger", result.stderr)
