import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CC_BY_4_SHA256 = (
    "9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411"
)
APACHE_2_SHA256 = (
    "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
)

APACHE_PATHS = (
    ".github/",
    "tools/",
    "tests/",
    "requirements-dev.txt",
    "assessment/schema/",
    "controls/schema/",
    "crosswalks/schema/",
)


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def normalized_sha256(relative_path: str) -> str:
    data = (ROOT / relative_path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


class LicenseMetadataTests(unittest.TestCase):
    def test_official_license_texts_are_complete_and_unmodified(self) -> None:
        self.assertEqual(CC_BY_4_SHA256, normalized_sha256("LICENSE"))
        self.assertEqual(
            APACHE_2_SHA256,
            normalized_sha256("LICENSES/Apache-2.0.txt"),
        )

    def test_scope_routes_implementation_assets_to_apache(self) -> None:
        scope = read_text("LICENSE_SCOPE.md")
        for path in APACHE_PATHS:
            with self.subTest(path=path):
                self.assertIn(f"`{path}`", scope)
        self.assertIn("Apache-2.0", scope)
        self.assertIn("CC-BY-4.0", scope)
        self.assertIn("A more specific path rule overrides a broader rule.", scope)
        self.assertIn(
            "Original ESAF material in every other path is licensed under "
            "CC BY 4.0.",
            scope,
        )
        self.assertIn("does not relicense third-party material", scope)

    def test_notice_has_exact_holder_and_nonendorsement_boundary(self) -> None:
        notice = read_text("NOTICE")
        self.assertIn("Copyright 2026 ESAF Project Maintainers", notice)
        self.assertIn("Enterprise Secure AI Framework (ESAF)", notice)
        self.assertIn("licensed under CC BY 4.0", notice)
        self.assertIn("does not imply endorsement", notice)
        self.assertNotIn("Hearst", notice)

    def test_third_party_notice_preserves_ncsc_terms(self) -> None:
        notice = read_text("THIRD_PARTY_NOTICES.md")
        self.assertIn("National Cyber Security Centre", notice)
        self.assertIn("Open Government Licence v3.0", notice)
        self.assertIn(
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            notice,
        )
        self.assertIn("do not relicense", notice)
        self.assertIn("mapping-level rights statements", notice)

    def test_trademark_policy_does_not_create_certification_or_registration(self) -> None:
        policy = read_text("TRADEMARKS.md")
        self.assertIn("truthful references", policy)
        self.assertIn("modified works", policy)
        self.assertIn("official ESAF publication", policy)
        self.assertIn("does not create a certification program", policy)
        self.assertIn("does not claim that any ESAF mark is registered", policy)
        for prohibited_claim in ("sponsored by", "endorsed by", "certified by"):
            with self.subTest(prohibited_claim=prohibited_claim):
                self.assertIn(prohibited_claim, policy)


if __name__ == "__main__":
    unittest.main()
