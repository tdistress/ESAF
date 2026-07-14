from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
RIGHTS_REVIEW = ROOT / "docs/superpowers/reviews/2026-07-14-uk-cyber-essentials-plus-v3.2-rights-review.md"
SOURCE_TITLE = "Cyber Essentials Plus Test Specification"
SOURCE_AUTHORITY = "UK National Cyber Security Centre"
PUBLICATION_IDENTIFIER = "cyber-essentials-plus-test-specification"
DISPLAY_DATE = "April 2025"
RESOURCE_PAGE = "https://www.ncsc.gov.uk/cyberessentials/resources"
RESOURCE_PAGE_DATE = "2025-04-28"
CANONICAL_URL = "https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf"
CANONICAL_BYTES = 424226
CANONICAL_SHA256 = "2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8"
LEGACY_URL = "https://www.ncsc.gov.uk/files/cyber-essentials-plus-test-specification-v3-2.pdf"
LEGACY_BYTES = 419191
LEGACY_SHA256 = "d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694"
GROUPS = ("M", "T1", "S", "T2", "T3", "T4", "T5", "C", "A", "B")
KINDS = {
    "applicability", "prerequisite", "procedure_step", "decision_rule",
    "result_rule", "evidence_retention", "recommendation",
}
RIGHTS_ELEMENTS = (
    "identifiers", "titles", "structural_inventory", "paraphrases",
    "derivative_mapping_analysis", "official_links",
)
PROHIBITED_INFERENCES = (
    "certification", "compliance", "equivalence", "endorsement",
    "predictive_sufficiency", "full_population_assurance",
    "continuous_assurance", "current_scheme_completeness",
)

ACTORS = {
    "Assessor", "Applicant", "Certification Body", "Certifying Body",
    "Delivery Partner",
}
TOP_LEVEL_KEYS = {
    "schema_version", "atomization_rule_version", "scope", "source", "rights",
    "inventory_provenance", "direction_boundary", "operational_context",
    "known_anomalies", "groups", "section_ledger", "counts",
    "assurance_limits", "provisions",
}
LOCATOR_KEYS = {"pdf_page", "printed_page", "section", "detail"}
LANDING_PAGE = ROOT / "crosswalks/uk-cyber-essentials.md"
SCOPE_STATEMENT = (
    "This complete-publication oracle inventories the public NCSC Cyber Essentials "
    "Plus Test Specification v3.2. It is not a complete inventory of the current "
    "operational Cyber Essentials Plus scheme, Delivery Partner methodology, or "
    "certification process."
)
ORIGINAL_FREE_TEXT_PATHS = (
    re.compile(r"^scope\.statement$"),
    re.compile(r"^rights\.publication_basis$"),
    re.compile(r"^rights\.restrictions\[\d+\]$"),
    re.compile(r"^rights\.iasme_partition\.(?:permitted_facts|prohibited_source_derived_elements)\[\d+\]$"),
    re.compile(r"^operational_context\[\d+\]\.relevance$"),
    re.compile(r"^known_anomalies\[\d+\]\.treatment$"),
    re.compile(r"^section_ledger\[\d+\]\.rationale$"),
    re.compile(r"^provisions\[\d+\]\.(?:actor_basis|summary)$"),
    re.compile(r"^provisions\[\d+\]\.locator\.detail$"),
    re.compile(
        r"^assurance_limits\.(?:scope_boundary|population_and_sample_boundary|"
        r"assessment_date_boundary|evidence_date_boundary|tool_and_provenance_boundary|"
        r"point_in_time_boundary)$"
    ),
)
AFFIRMATIVE_PROHIBITED_CLAIMS = {
    "certification": (
        r"\b(?:provides|confers|establishes|demonstrates|proves|guarantees) (?:a )?certification\b",
        r"\bcertifies (?:the|an|any)\b",
    ),
    "compliance": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) compliance\b",
        r"\b(?:is|are) compliant with\b",
    ),
    "equivalence": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) equivalence\b",
        r"\b(?:is|are) equivalent to\b",
    ),
    "endorsement": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) endorsement\b",
        r"\b(?:is|are) endorsed by\b",
        r"\b(?:has|carries|receives) (?:NCSC |IASME |government )?endorsement\b",
        r"\b(?:NCSC|IASME) endorses\b",
    ),
    "predictive_sufficiency": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) predictive sufficiency\b",
        r"\b(?:is|are) sufficient to predict\b",
        r"\bpredicts future (?:security|compliance|performance|outcomes?)\b",
    ),
    "full_population_assurance": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) full[- ]population assurance\b",
        r"\bassures (?:the )?(?:entire|full) population\b",
    ),
    "continuous_assurance": (
        r"\b(?:provides|establishes|demonstrates|proves|guarantees) continuous assurance\b",
    ),
    "current_scheme_completeness": (
        r"\b(?:is|provides|establishes) (?:a )?complete inventory of the current operational\b",
        r"\bfully describes the current (?:operational )?scheme\b",
    ),
}


class CyberEssentialsPlusV32InventoryTests(unittest.TestCase):
    def oracle(self) -> dict:
        return json.loads(ORACLE.read_text(encoding="utf-8"))

    def assert_exact_keys(self, value: object, expected: set[str]) -> dict:
        self.assertIsInstance(value, dict)
        assert isinstance(value, dict)
        self.assertEqual(expected, set(value))
        return value

    def assert_nonempty_string(self, value: object) -> str:
        self.assertIsInstance(value, str)
        assert isinstance(value, str)
        self.assertEqual(value, value.strip())
        self.assertTrue(value)
        return value

    def assert_nonnegative_integer(self, value: object) -> int:
        self.assertIs(type(value), int)
        assert isinstance(value, int)
        self.assertGreaterEqual(value, 0)
        return value

    def assert_positive_integer(self, value: object) -> int:
        number = self.assert_nonnegative_integer(value)
        self.assertGreater(number, 0)
        return number

    def assert_date(self, value: object) -> str:
        text = self.assert_nonempty_string(value)
        self.assertRegex(text, r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$")
        try:
            date.fromisoformat(text)
        except ValueError:
            self.fail(f"invalid calendar date: {text}")
        return text

    def assert_uri(self, value: object) -> str:
        text = self.assert_nonempty_string(value)
        self.assertRegex(text, r"^https://[^\s]+$")
        return text

    def assert_sha256(self, value: object) -> str:
        text = self.assert_nonempty_string(value)
        self.assertRegex(text, r"^[0-9a-f]{64}$")
        return text

    def assert_unique_strings(self, value: object, *, nonempty: bool = False) -> list[str]:
        self.assertIsInstance(value, list)
        assert isinstance(value, list)
        if nonempty:
            self.assertTrue(value)
        for item in value:
            self.assert_nonempty_string(item)
        self.assertEqual(len(value), len(set(value)))
        return value

    def assert_locator(self, value: object) -> dict:
        locator = self.assert_exact_keys(value, LOCATOR_KEYS)
        self.assert_positive_integer(locator["pdf_page"])
        if locator["printed_page"] is not None:
            self.assert_positive_integer(locator["printed_page"])
        self.assert_nonempty_string(locator["section"])
        self.assert_nonempty_string(locator["detail"])
        return locator

    def assert_page_range(self, value: object) -> dict:
        page_range = self.assert_exact_keys(value, {"start", "end"})
        start = self.assert_positive_integer(page_range["start"])
        end = self.assert_positive_integer(page_range["end"])
        self.assertLessEqual(start, end)
        return page_range

    def walk(self, value: object, path: str = "") -> list[tuple[str, object]]:
        found = [(path, value)]
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                found.extend(self.walk(child, child_path))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                found.extend(self.walk(child, f"{path}[{index}]"))
        return found

    def original_free_text(self, oracle: object) -> list[tuple[str, str]]:
        return [
            (path, value)
            for path, value in self.walk(oracle)
            if isinstance(value, str)
            and any(pattern.fullmatch(path) for pattern in ORIGINAL_FREE_TEXT_PATHS)
        ]

    def normalized_prose(self, value: str) -> str:
        return " ".join(re.findall(r"[a-z0-9%]+", value.lower()))

    def assert_no_copied_source_passages(
        self, oracle: object, source_passages: list[str], *, minimum_words: int = 5,
    ) -> None:
        normalized_passages = [
            self.normalized_prose(passage) for passage in source_passages
        ]
        for path, value in self.original_free_text(oracle):
            normalized_value = self.normalized_prose(value)
            if len(normalized_value.split()) < minimum_words:
                continue
            for passage in normalized_passages:
                if normalized_value in passage or passage in normalized_value:
                    self.fail(f"copied source passage found at {path}: {value!r}")

    def assert_no_affirmative_prohibited_claims(self, text: str) -> None:
        for category, claims in AFFIRMATIVE_PROHIBITED_CLAIMS.items():
            for claim in claims:
                self.assertIsNone(
                    re.search(claim, text, flags=re.IGNORECASE),
                    f"affirmative {category} claim matched {claim!r}",
                )

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False,
        )

    def test_locked_oracle_exists(self) -> None:
        self.assertTrue(ORACLE.is_file())

    def test_copied_source_text_detector_covers_all_original_free_text(self) -> None:
        source_passages = [
            "The assessor must preserve every relevant evidence record for the assessment.",
            "A complete scheme description includes all current operational methods and rules.",
        ]
        copied_summary = {
            "provisions": [{
                "summary": "The assessor must preserve every relevant evidence record for the assessment",
            }],
        }
        copied_scope = {
            "scope": {
                "statement": "A complete scheme description includes all current operational methods and rules",
            },
        }
        for candidate, path in (
            (copied_summary, "provisions[0].summary"),
            (copied_scope, "scope.statement"),
        ):
            with self.assertRaisesRegex(AssertionError, re.escape(path)):
                self.assert_no_copied_source_passages(candidate, source_passages)

    def test_prohibited_claim_detector_covers_all_eight_categories(self) -> None:
        affirmative_examples = {
            "certification": "The oracle provides certification for the Applicant.",
            "compliance": "The Applicant is compliant with ESAF.",
            "equivalence": "The assessment establishes equivalence with ESAF.",
            "endorsement": "The publication is endorsed by NCSC.",
            "predictive_sufficiency": "The result is sufficient to predict future security.",
            "full_population_assurance": "The sample provides full population assurance.",
            "continuous_assurance": "The certificate guarantees continuous assurance.",
            "current_scheme_completeness": (
                "The oracle is a complete inventory of the current operational scheme."
            ),
        }
        self.assertEqual(set(PROHIBITED_INFERENCES), set(affirmative_examples))
        for category, example in affirmative_examples.items():
            with self.assertRaisesRegex(AssertionError, category):
                self.assert_no_affirmative_prohibited_claims(example)
        self.assert_no_affirmative_prohibited_claims(
            "The oracle does not provide certification, demonstrate compliance, "
            "or establish continuous assurance."
        )

    def test_date_parser_rejects_impossible_calendar_dates(self) -> None:
        self.assertEqual("2026-07-14", self.assert_date("2026-07-14"))
        with self.assertRaisesRegex(AssertionError, "invalid calendar date"):
            self.assert_date("2026-02-31")

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_source_identity_is_exact(self) -> None:
        oracle = self.oracle()
        source = oracle["source"]
        self.assertEqual(SOURCE_TITLE, source["title"])
        self.assertEqual(SOURCE_AUTHORITY, source["authority"])
        self.assertEqual(PUBLICATION_IDENTIFIER, source["publication_identifier"])
        self.assertEqual("3.2", source["version"])
        self.assertEqual(DISPLAY_DATE, source["display_date"])
        self.assertEqual(RESOURCE_PAGE, source["resource_page_url"])
        self.assertEqual(RESOURCE_PAGE_DATE, source["resource_page_date"])
        self.assertEqual(24, source["pdf_page_count"])
        self.assertEqual(
            [("canonical", CANONICAL_URL, CANONICAL_BYTES, CANONICAL_SHA256),
             ("legacy", LEGACY_URL, LEGACY_BYTES, LEGACY_SHA256)],
            [(v["role"], v["url"], v["byte_length"], v["sha256"])
             for v in source["variants"]],
        )

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_closed_contract_versions_scope_source_and_groups(self) -> None:
        oracle = self.assert_exact_keys(self.oracle(), TOP_LEVEL_KEYS)
        self.assertEqual("1.0.0", oracle["schema_version"])
        self.assertEqual("1.0.0", oracle["atomization_rule_version"])

        scope = self.assert_exact_keys(oracle["scope"], {"type", "statement"})
        self.assertEqual("complete_publication", scope["type"])
        self.assertEqual(SCOPE_STATEMENT, scope["statement"])

        source = self.assert_exact_keys(
            oracle["source"],
            {"title", "authority", "publication_identifier", "version",
             "display_date", "resource_page_url", "resource_page_date",
             "access_date", "media_type", "pdf_page_count", "variants"},
        )
        for key in ("title", "authority", "publication_identifier", "version",
                    "display_date", "media_type"):
            self.assert_nonempty_string(source[key])
        self.assert_uri(source["resource_page_url"])
        self.assert_date(source["resource_page_date"])
        self.assertEqual("2026-07-14", self.assert_date(source["access_date"]))
        self.assertEqual("application/pdf", source["media_type"])
        self.assert_positive_integer(source["pdf_page_count"])
        self.assertIsInstance(source["variants"], list)
        self.assertEqual(2, len(source["variants"]))
        for variant in source["variants"]:
            item = self.assert_exact_keys(
                variant, {"role", "url", "byte_length", "sha256"},
            )
            self.assertIn(item["role"], {"canonical", "legacy"})
            self.assert_uri(item["url"])
            self.assert_positive_integer(item["byte_length"])
            self.assert_sha256(item["sha256"])
        self.assertEqual(list(GROUPS), oracle["groups"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_rights_contract_is_exact_and_separates_iasme(self) -> None:
        rights = self.assert_exact_keys(
            self.oracle()["rights"],
            {"copyright", "licence_name", "licence_url", "attribution",
             "publication_basis", "permitted_elements", "prohibited_elements",
             "copied_requirement_or_passage_text_prohibited",
             "allowed_verbatim_locations", "restrictions", "iasme_partition",
             "review"},
        )
        self.assertEqual("Crown copyright", rights["copyright"])
        self.assertEqual("Open Government Licence v3.0", rights["licence_name"])
        self.assertEqual(
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            self.assert_uri(rights["licence_url"]),
        )
        self.assertEqual(SOURCE_AUTHORITY, rights["attribution"])
        publication_basis = self.assert_nonempty_string(rights["publication_basis"])
        self.assertIn("Open Government Licence v3.0", publication_basis)
        permitted = self.assert_unique_strings(rights["permitted_elements"])
        prohibited = self.assert_unique_strings(rights["prohibited_elements"])
        self.assertEqual(list(RIGHTS_ELEMENTS), permitted)
        self.assertEqual([], prohibited)
        self.assertFalse(set(permitted) & set(prohibited))
        self.assertEqual(set(RIGHTS_ELEMENTS), set(permitted) | set(prohibited))
        self.assertIs(rights["copied_requirement_or_passage_text_prohibited"], True)
        self.assertEqual(
            ["known_anomalies[0].source_literal"],
            rights["allowed_verbatim_locations"],
        )
        restrictions = " ".join(
            self.assert_unique_strings(rights["restrictions"], nonempty=True)
        ).lower()
        for restricted in ("logo", "mark", "imag", "third-party", "endorsement"):
            self.assertIn(restricted, restrictions)

        iasme = self.assert_exact_keys(
            rights["iasme_partition"],
            {"owner", "licence", "permitted_facts",
             "prohibited_source_derived_elements"},
        )
        self.assertIn("IASME", self.assert_nonempty_string(iasme["owner"]))
        self.assertIsNone(iasme["licence"])
        self.assert_unique_strings(iasme["permitted_facts"], nonempty=True)
        self.assert_unique_strings(
            iasme["prohibited_source_derived_elements"], nonempty=True,
        )

        review = self.assert_exact_keys(
            rights["review"],
            {"reviewer", "review_date", "independent_of_inventory_authors",
             "canonical_sha256", "legacy_sha256", "publication_basis_verified",
             "disposition"},
        )
        self.assert_nonempty_string(review["reviewer"])
        self.assert_date(review["review_date"])
        self.assertIs(review["independent_of_inventory_authors"], True)
        self.assertEqual(CANONICAL_SHA256, self.assert_sha256(review["canonical_sha256"]))
        self.assertEqual(LEGACY_SHA256, self.assert_sha256(review["legacy_sha256"]))
        self.assertIs(review["publication_basis_verified"], True)
        self.assertEqual("approved", review["disposition"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_inventory_provenance_and_rights_commit_precedence(self) -> None:
        oracle = self.oracle()
        provenance = self.assert_exact_keys(
            oracle["inventory_provenance"],
            {"authors", "reconciler", "rights_record_commit",
             "inventories_started_after_rights_commit"},
        )
        authors = self.assert_unique_strings(provenance["authors"], nonempty=True)
        self.assertEqual(2, len(authors))
        self.assert_nonempty_string(provenance["reconciler"])
        rights_sha = self.assert_nonempty_string(provenance["rights_record_commit"])
        self.assertRegex(rights_sha, r"^[0-9a-f]{40}$")
        self.assertIs(provenance["inventories_started_after_rights_commit"], True)
        reviewer = oracle["rights"]["review"]["reviewer"]
        self.assertNotIn(reviewer, authors)

        commit_check = self.git("cat-file", "-e", f"{rights_sha}^{{commit}}")
        self.assertEqual(0, commit_check.returncode, commit_check.stderr)
        relative_rights_review = RIGHTS_REVIEW.relative_to(ROOT).as_posix()
        rights_history = self.git(
            "log", "--diff-filter=A", "--format=%H", "--", relative_rights_review,
        )
        self.assertEqual(0, rights_history.returncode, rights_history.stderr)
        self.assertEqual([rights_sha], rights_history.stdout.splitlines())
        rights_introduction = self.git(
            "diff-tree", "--root", "--no-commit-id", "--name-status", "-r",
            rights_sha,
        )
        self.assertEqual(0, rights_introduction.returncode, rights_introduction.stderr)
        self.assertEqual(
            f"A\t{relative_rights_review}", rights_introduction.stdout.strip(),
        )
        relative_oracle = ORACLE.relative_to(ROOT).as_posix()
        history = self.git(
            "log", "--diff-filter=A", "--format=%H", "--", relative_oracle,
        )
        self.assertEqual(0, history.returncode, history.stderr)
        inventory_commits = history.stdout.splitlines()
        self.assertEqual(1, len(inventory_commits))
        first_inventory_commit = inventory_commits[0]
        precedence = self.git(
            "merge-base", "--is-ancestor", rights_sha, f"{first_inventory_commit}^",
        )
        self.assertEqual(
            0, precedence.returncode,
            "rights approval must precede the first source-derived inventory commit",
        )

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_direction_context_and_anomaly_objects_are_closed(self) -> None:
        oracle = self.oracle()
        direction = self.assert_exact_keys(
            oracle["direction_boundary"],
            {"oracle_establishes_mapping_direction", "future_directions",
             "assessed_independently"},
        )
        self.assertIs(direction["oracle_establishes_mapping_direction"], False)
        self.assertEqual(
            ["esaf_to_external", "external_to_esaf"],
            direction["future_directions"],
        )
        self.assertIs(direction["assessed_independently"], True)

        self.assertIsInstance(oracle["operational_context"], list)
        for context_value in oracle["operational_context"]:
            context = self.assert_exact_keys(
                context_value,
                {"owner", "title", "url", "publication_date", "access_date",
                 "relevance", "rights_partition"},
            )
            for key in ("owner", "title", "relevance"):
                self.assert_nonempty_string(context[key])
            self.assert_uri(context["url"])
            self.assert_date(context["publication_date"])
            self.assert_date(context["access_date"])
            self.assertEqual(
                "bibliographic_facts_and_original_context_only",
                context["rights_partition"],
            )

        self.assertIsInstance(oracle["known_anomalies"], list)
        self.assertEqual(1, len(oracle["known_anomalies"]))
        anomaly = self.assert_exact_keys(
            oracle["known_anomalies"][0],
            {"anomaly_id", "source_literal", "locator", "treatment"},
        )
        self.assert_nonempty_string(anomaly["anomaly_id"])
        self.assertEqual("tests 2 to 7", anomaly["source_literal"])
        self.assert_locator(anomaly["locator"])
        treatment = self.assert_nonempty_string(anomaly["treatment"]).lower()
        self.assertIn("without", treatment)
        self.assertRegex(treatment, r"correct|expand|interpret")

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_section_ledger_is_closed_and_link_counts_are_derived(self) -> None:
        oracle = self.oracle()
        ledger = oracle["section_ledger"]
        self.assertIsInstance(ledger, list)
        self.assertTrue(ledger)
        section_ids: list[str] = []
        ledger_by_id: dict[str, dict] = {}
        for occurrence_value in ledger:
            occurrence = self.assert_exact_keys(
                occurrence_value,
                {"section_id", "parent_section_id", "heading", "group",
                 "pdf_pages", "printed_pages", "decision", "rationale",
                 "atom_count"},
            )
            section_id = self.assert_nonempty_string(occurrence["section_id"])
            self.assertRegex(section_id, r"^sec-[a-z0-9]+(?:-[a-z0-9]+)*$")
            section_ids.append(section_id)
            ledger_by_id[section_id] = occurrence
            if occurrence["parent_section_id"] is not None:
                self.assert_nonempty_string(occurrence["parent_section_id"])
            self.assert_nonempty_string(occurrence["heading"])
            self.assertIn(occurrence["group"], GROUPS)
            self.assert_page_range(occurrence["pdf_pages"])
            if occurrence["printed_pages"] is not None:
                self.assert_page_range(occurrence["printed_pages"])
            self.assertIn(occurrence["decision"], {"included", "context_only"})
            self.assert_nonempty_string(occurrence["rationale"])
            self.assert_nonnegative_integer(occurrence["atom_count"])
        self.assertEqual(len(section_ids), len(set(section_ids)))
        for occurrence in ledger:
            parent = occurrence["parent_section_id"]
            if parent is not None:
                self.assertIn(parent, ledger_by_id)
                self.assertTrue(occurrence["section_id"].startswith(f"{parent}-"))

        links = Counter(item["section_id"] for item in oracle["provisions"])
        for section_id, occurrence in ledger_by_id.items():
            self.assertEqual(links[section_id], occurrence["atom_count"])
            if occurrence["decision"] == "context_only":
                self.assertEqual(0, links[section_id])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_provisions_are_closed_controlled_linked_and_ordered(self) -> None:
        oracle = self.oracle()
        provisions = oracle["provisions"]
        self.assertIsInstance(provisions, list)
        self.assertTrue(provisions)
        ledger = {item["section_id"]: item for item in oracle["section_ledger"]}
        record_ids: list[str] = []
        external_ids: list[str] = []
        order_keys: list[tuple[int, int]] = []
        for provision_value in provisions:
            provision = self.assert_exact_keys(
                provision_value,
                {"record_id", "external_provision_id", "section_id", "group",
                 "kind", "actors", "actor_basis", "source_assigned_label",
                 "summary", "locator"},
            )
            group = provision["group"]
            self.assertIn(group, GROUPS)
            record_id = self.assert_nonempty_string(provision["record_id"])
            external_id = self.assert_nonempty_string(
                provision["external_provision_id"],
            )
            self.assertRegex(record_id, rf"^cepts32-{group.lower()}-\d{{3}}$")
            self.assertRegex(external_id, rf"^CEPTS3\.2-{group}-\d{{3}}$")
            self.assertEqual(record_id.rsplit("-", 1)[1], external_id.rsplit("-", 1)[1])
            record_ids.append(record_id)
            external_ids.append(external_id)
            order_keys.append((GROUPS.index(group), int(record_id.rsplit("-", 1)[1])))
            section_id = self.assert_nonempty_string(provision["section_id"])
            self.assertIn(section_id, ledger)
            self.assertEqual("included", ledger[section_id]["decision"])
            self.assertEqual(group, ledger[section_id]["group"])
            self.assertIn(provision["kind"], KINDS)
            actors = self.assert_unique_strings(provision["actors"], nonempty=True)
            self.assertLessEqual(set(actors), ACTORS)
            actor_basis = self.assert_nonempty_string(provision["actor_basis"])
            locator = self.assert_locator(provision["locator"])
            if len(actors) > 1:
                for actor in actors:
                    self.assertIn(actor, actor_basis)
                self.assertTrue(locator["detail"])
            if provision["source_assigned_label"] is not None:
                self.assert_nonempty_string(provision["source_assigned_label"])
                self.assertNotIn(provision["source_assigned_label"], locator.values())
            self.assert_nonempty_string(provision["summary"])
        self.assertEqual(len(record_ids), len(set(record_ids)))
        self.assertEqual(len(external_ids), len(set(external_ids)))
        self.assertEqual(sorted(order_keys), order_keys)
        for group in GROUPS:
            group_numbers = [
                number for group_index, number in order_keys
                if group_index == GROUPS.index(group)
            ]
            self.assertEqual(list(range(1, len(group_numbers) + 1)), group_numbers)

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_counts_are_derived_without_freezing_reconciliation_literals(self) -> None:
        oracle = self.oracle()
        counts = self.assert_exact_keys(oracle["counts"], {"total", "by_group"})
        by_group = self.assert_exact_keys(counts["by_group"], set(GROUPS))
        for value in by_group.values():
            self.assert_nonnegative_integer(value)
        self.assert_nonnegative_integer(counts["total"])
        derived = Counter(item["group"] for item in oracle["provisions"])
        self.assertEqual(
            {group: derived[group] for group in GROUPS},
            by_group,
        )
        self.assertEqual(len(oracle["provisions"]), counts["total"])
        self.assertEqual(counts["total"], sum(by_group.values()))
        self.assertEqual(
            counts["total"],
            sum(item["atom_count"] for item in oracle["section_ledger"]),
        )

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_assurance_limits_and_discretionary_exception_are_exact(self) -> None:
        limits = self.assert_exact_keys(
            self.oracle()["assurance_limits"],
            {"scope_boundary", "population_and_sample_boundary",
             "assessment_date_boundary", "evidence_date_boundary",
             "tool_and_provenance_boundary", "point_in_time_boundary",
             "discretion_owner", "discretionary_exception",
             "prohibited_inferences"},
        )
        for key in (
            "scope_boundary", "population_and_sample_boundary",
            "assessment_date_boundary", "evidence_date_boundary",
            "tool_and_provenance_boundary", "point_in_time_boundary",
        ):
            self.assert_nonempty_string(limits[key])
        self.assertEqual("Delivery Partner", limits["discretion_owner"])
        exception = self.assert_exact_keys(
            limits["discretionary_exception"],
            {"owner", "predicates", "all_predicates_required", "locator",
             "automatic_pass", "is_95_percent_score"},
        )
        self.assertEqual("Delivery Partner", exception["owner"])
        self.assertIs(exception["all_predicates_required"], True)
        self.assertIs(exception["automatic_pass"], False)
        self.assertIs(exception["is_95_percent_score"], False)
        self.assert_locator(exception["locator"])
        predicates = exception["predicates"]
        self.assertIsInstance(predicates, list)
        self.assertEqual(2, len(predicates))
        for predicate in predicates:
            self.assert_exact_keys(predicate, {"predicate_id", "meaning"})
        self.assertEqual(
            [
                ("marginal-deviation-under-five-percent",
                 "a marginal deviation in less than 5% of performed tests"),
                ("no-wider-process-failure-evidence",
                 "no evidence of wider failure of Applicant cybersecurity processes"),
            ],
            [(item["predicate_id"], item["meaning"]) for item in predicates],
        )
        self.assertEqual(list(PROHIBITED_INFERENCES), limits["prohibited_inferences"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_visual_decisions_and_anomaly_literal_are_complete(self) -> None:
        oracle = self.oracle()
        figure_labels = {
            item["source_assigned_label"]
            for item in oracle["provisions"]
            if isinstance(item["source_assigned_label"], str)
            and "Figure 1" in item["source_assigned_label"]
        }
        self.assertEqual(
            {f"Figure 1 decision {number}" for number in range(1, 8)},
            figure_labels,
        )
        literal_occurrences = [
            path for path, value in self.walk(oracle) if value == "tests 2 to 7"
        ]
        self.assertEqual(["known_anomalies[0].source_literal"], literal_occurrences)
        self.assertEqual(
            ["known_anomalies[0].source_literal"],
            oracle["rights"]["allowed_verbatim_locations"],
        )
        for provision in oracle["provisions"]:
            self.assertNotEqual("tests 2 to 7", provision["summary"])

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_original_free_text_excludes_source_copy_markers(self) -> None:
        free_text = self.original_free_text(self.oracle())
        self.assertTrue(free_text)
        for path, value in free_text:
            self.assertNotRegex(value, r"[\r\n•]", path)
            self.assertNotRegex(value, r"[\"“”]", path)
            self.assertNotRegex(value, r"\b(?:shall|must|should)\b", path)

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_oracle_has_no_mapping_fields_or_prohibited_claim_phrases(self) -> None:
        oracle = self.oracle()
        prohibited_fields = {
            "mapping_disposition", "disposition_rationale", "relationships",
            "relationship", "esaf_control_id", "compliance_statistics",
            "mapping_statistics",
        }
        object_keys = {
            key
            for _, value in self.walk(oracle)
            if isinstance(value, dict)
            for key in value
        }
        self.assertFalse(prohibited_fields & object_keys)

        serialized = json.dumps(oracle, ensure_ascii=False)
        landing = LANDING_PAGE.read_text(encoding="utf-8")
        for text in (serialized, landing):
            self.assert_no_affirmative_prohibited_claims(text)


if __name__ == "__main__":
    unittest.main()
