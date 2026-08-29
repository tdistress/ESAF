import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "tools" / "render_nist_ai_rmf_mapping_go_no_go.py"
MATRIX = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-29-nist-ai-rmf-mapping-readiness-matrix.json"
)
REVIEW = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-08-29-nist-ai-rmf-1.0-mapping-go-no-go-review.md"
)
RIGHTS = (
    ROOT
    / "docs"
    / "superpowers"
    / "reviews"
    / "2026-08-29-nist-ai-rmf-publication-rights-review.md"
)
ORACLE = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-29-nist-ai-rmf-source-readiness-oracle.json"
)


class RenderNistAiRmfMappingGoNoGoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))

    def test_check_passes_on_committed_artifacts(self) -> None:
        result = subprocess.run(
            [sys.executable, str(RENDERER), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rendered_review_is_hold(self) -> None:
        text = REVIEW.read_text(encoding="utf-8")
        self.assertIn("**Decision:** `HOLD`", text)
        self.assertIn("`NIST-AI-RMF-READINESS-B001`", text)
        self.assertIn("`mapper_and_reviewer_readiness`", text)
        self.assertIn("`BLOCKED`", text)

    def test_source_oracle_digest_is_current(self) -> None:
        self.assertEqual(
            self.matrix["source_oracle"]["sha256"],
            hashlib.sha256(ORACLE.read_bytes()).hexdigest(),
        )

    def test_rights_review_commit_is_ancestral_and_digest_matches(self) -> None:
        rights = self.matrix["rights_review"]
        self.assertEqual(
            rights["sha256"],
            hashlib.sha256(RIGHTS.read_bytes()).hexdigest(),
        )
        commit = rights["commit"]
        exists = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(exists.returncode, 0, exists.stderr)
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(ancestor.returncode, 0, ancestor.stderr)

    def test_check_rejects_stale_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stale = Path(tmp) / "review.md"
            stale.write_text("stale\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--check",
                    "--output",
                    str(stale),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("stale", result.stderr)


if __name__ == "__main__":
    unittest.main()
