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
APPROVED_STATUS = "Approved on candidate content; pending final exact-head recheck"
PINNED_RENDERER = "@mermaid-js/mermaid-cli@11.16.0"


def passing_record(blocks, reviewer: str = "Independent reviewer") -> str:
    rows = ledger_rows(blocks).replace(
        "| Pending | Pending | Pending |",
        f"| Pass | Pass | {reviewer} |",
    )
    return (
        "# Rendering ledger\n\n"
        f"Status: {APPROVED_STATUS}\n\n"
        f"Renderer version: `{PINNED_RENDERER}`\n\n"
        "| Path | Block | SHA-256 | Diagram type | Render | Readability | Reviewer |\n"
        "|---|---:|---|---|---|---|---|\n"
        f"{rows}\n"
    )


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
            self.assertEqual(item.diagram_type, item.source.splitlines()[0].split()[0])

    def test_arc_p110_recovery_paths_do_not_use_opposing_labeled_edges(self) -> None:
        blocks = extract_blocks((ROOT / "architectures/patterns/ARC-P110.md").read_text(encoding="utf-8"))
        degraded_mode = blocks[4]
        self.assertNotIn("Recovery --> SafeStop:", degraded_mode)
        self.assertIn("Recovery --> RecoveryValidation:", degraded_mode)
        self.assertIn("RecoveryValidation --> SafeStop:", degraded_mode)

    def test_arc_p150_subplane_edges_terminate_at_named_nodes(self) -> None:
        blocks = extract_blocks((ROOT / "architectures/patterns/ARC-P150.md").read_text(encoding="utf-8"))
        component_view = blocks[2]
        self.assertNotIn('subgraph OPS["Operations, administration, and evidence plane"]', component_view)
        self.assertIn('OPS["Operations, administration, and evidence plane"]', component_view)
        self.assertIn('OPS --- AD', component_view)
        self.assertIn('OPS --- EV', component_view)
        self.assertIn('AD -. "configuration, continuity, containment" .-> G', component_view)
        self.assertIn('O -. "minimized event" .-> EV', component_view)

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
                    {
                        "path": block.path,
                        "index": block.index,
                        "digest": block.digest,
                        "diagram_type": block.diagram_type,
                        "source": None,
                        "input": name,
                    }
                )
            self.assertEqual(json.loads(inventory.read_text(encoding="utf-8")), expected_rows)
            self.assertEqual(sorted(output.glob("*.mmd"), key=lambda path: path.name), [output / row["input"] for row in expected_rows])

    def test_check_record_accepts_exact_passing_rows(self) -> None:
        blocks = discover(ROOT)[:2]
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            record.write_text(passing_record(blocks), encoding="utf-8")
            self.assertEqual(check_record(blocks, record), [])

    def test_check_record_rejects_mismatched_and_duplicate_rows(self) -> None:
        blocks = discover(ROOT)[:2]
        rows = passing_record(blocks).splitlines()
        mismatched = rows.copy()
        first_row = next(index for index, line in enumerate(rows) if blocks[0].digest in line)
        mismatched[first_row] = mismatched[first_row].replace(blocks[0].digest, "0" * 64)
        duplicated = rows + [rows[first_row]]
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            record.write_text("\n".join(mismatched) + "\n", encoding="utf-8")
            self.assertIn("ledger rows do not exactly match the current Mermaid inventory", check_record(blocks, record))
            record.write_text("\n".join(duplicated) + "\n", encoding="utf-8")
            self.assertIn("ledger rows do not exactly match the current Mermaid inventory", check_record(blocks, record))

    def test_check_record_requires_both_render_and_readability_pass(self) -> None:
        block = discover(ROOT)[:1]
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            for disposition in ("| Pass | Pending | Reviewer |", "| Pending | Pass | Reviewer |"):
                record.write_text(
                    passing_record(block).replace("| Pass | Pass | Independent reviewer |", disposition),
                    encoding="utf-8",
                )
                self.assertIn("not fully reviewed", "\n".join(check_record(block, record)))

    def test_check_record_requires_approved_metadata_and_reviewer(self) -> None:
        blocks = discover(ROOT)[:1]
        mutations = (
            (APPROVED_STATUS, "Pending exact-head rendering review", "ledger status is not approved"),
            (PINNED_RENDERER, "@mermaid-js/mermaid-cli@11.15.0", "renderer version is not pinned"),
            ("Independent reviewer", "Pending", "reviewer identity is missing"),
        )
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            for before, after, diagnostic in mutations:
                with self.subTest(after=after):
                    record.write_text(passing_record(blocks).replace(before, after), encoding="utf-8")
                    self.assertIn(diagnostic, "\n".join(check_record(blocks, record)))

    def test_check_record_rejects_conflicting_metadata_and_placeholder_reviewers(self) -> None:
        blocks = discover(ROOT)[:1]
        mutations = (
            (
                f"Status: {APPROVED_STATUS}",
                f"Status: Pending exact-head rendering review\nStatus: {APPROVED_STATUS}",
                "ledger status is not approved",
            ),
            (
                f"Renderer version: `{PINNED_RENDERER}`",
                "Renderer version: `@mermaid-js/mermaid-cli@11.15.0`\n"
                f"Renderer version: `{PINNED_RENDERER}`",
                "renderer version is not pinned",
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            for before, after, diagnostic in mutations:
                with self.subTest(diagnostic=diagnostic):
                    record.write_text(passing_record(blocks).replace(before, after), encoding="utf-8")
                    self.assertIn(diagnostic, "\n".join(check_record(blocks, record)))
            for placeholder in ("Pending", "TBD", "TODO", "unknown", "n/a", "Reviewer"):
                with self.subTest(placeholder=placeholder):
                    record.write_text(passing_record(blocks, placeholder), encoding="utf-8")
                    self.assertIn("reviewer identity is missing", "\n".join(check_record(blocks, record)))

    def test_check_record_rejects_mismatched_diagram_type(self) -> None:
        blocks = discover(ROOT)[:1]
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            record.write_text(
                passing_record(blocks).replace(f"| {blocks[0].diagram_type} |", "| unknownDiagram |"),
                encoding="utf-8",
            )
            self.assertIn("ledger rows do not exactly match", "\n".join(check_record(blocks, record)))

    def test_cli_check_record_accepts_approved_canonical_ledger(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check-record", str(LEDGER)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated 23 Mermaid ledger rows", result.stdout)

    def test_cli_check_record_rejects_fabricated_external_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "ledger.md"
            record.write_text(
                "| `x.md` | 1 | `" + "0" * 64 + "` | flowchart | Pass | Pass | Reviewer |\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--check-record", str(record)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exact tracked release ledger", result.stderr)
