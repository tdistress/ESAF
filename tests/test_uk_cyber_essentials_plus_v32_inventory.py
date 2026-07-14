from __future__ import annotations

import base64
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
EXPECTED_COUNT = 144
EXPECTED_GROUP_COUNTS = {
    "M": 24, "T1": 16, "S": 11, "T2": 9, "T3": 37,
    "T4": 9, "T5": 7, "C": 13, "A": 4, "B": 14,
}
EXPECTED_SECTION_OCCURRENCES = (('sec-m-cover', None, 'Cover', 'M', 1, 1, None, None, 'context_only'), ('sec-m-contents', None, 'Contents', 'M', 2, 3, 1, 2, 'context_only'), ('sec-m-whats-new', None, "What's new", 'M', 4, 4, 3, 3, 'context_only'), ('sec-m-audience', None, 'Audience', 'M', 4, 4, 3, 3, 'context_only'), ('sec-m-purpose', None, 'Purpose', 'M', 4, 5, 3, 4, 'included'), ('sec-m-before-you-begin', None, 'Before you begin', 'M', 5, 5, 4, 4, 'included'), ('sec-m-general-prerequisites', None, 'General prerequisites for testing', 'M', 6, 6, 5, 5, 'included'), ('sec-m-success-criteria', None, 'Success criteria', 'M', 6, 7, 5, 6, 'context_only'), ('sec-m-test-results', 'sec-m-success-criteria', 'Test results', 'M', 6, 6, 5, 5, 'included'), ('sec-m-pass', 'sec-m-test-results', 'Pass', 'M', 6, 6, 5, 5, 'included'), ('sec-m-fail', 'sec-m-test-results', 'Fail', 'M', 6, 7, 5, 6, 'included'), ('sec-m-advisory-notes', 'sec-m-success-criteria', 'Advisory notes', 'M', 7, 7, 6, 6, 'included'), ('sec-t1-test-case', None, 'Test case 1: Remote vulnerability assessment', 'T1', 8, 10, 7, 9, 'context_only'), ('sec-t1-purpose', 'sec-t1-test-case', 'Test purpose', 'T1', 8, 8, 7, 7, 'context_only'), ('sec-t1-description', 'sec-t1-test-case', 'Test description', 'T1', 8, 9, 7, 8, 'context_only'), ('sec-t1-prerequisites', 'sec-t1-description', 'Prerequisites', 'T1', 8, 8, 7, 7, 'included'), ('sec-t1-subtest-1-1', 'sec-t1-description', 'Sub-test 1.1', 'T1', 8, 9, 7, 8, 'included'), ('sec-t1-figure-1', 'sec-t1-subtest-1-1', 'Figure 1: Sub-test flow diagram for assessing services accessible through the firewall', 'T1', 9, 9, 8, 8, 'included'), ('sec-t1-interpretation', 'sec-t1-test-case', 'Interpreting the test case results', 'T1', 10, 10, 9, 9, 'included'), ('sec-s-sample-testing', None, 'Sample testing', 'S', 10, 10, 9, 9, 'included'), ('sec-t2-test-case', None, 'Test case 2: Check patching, by authenticated vulnerability scan of devices', 'T2', 11, 12, 10, 11, 'included'), ('sec-t2-purpose', 'sec-t2-test-case', 'Test purpose', 'T2', 11, 11, 10, 10, 'context_only'), ('sec-t2-description', 'sec-t2-test-case', 'Test description', 'T2', 11, 12, 10, 11, 'context_only'), ('sec-t2-prerequisites', 'sec-t2-description', 'Prerequisites', 'T2', 11, 11, 10, 10, 'included'), ('sec-t2-subtest-2-1', 'sec-t2-description', 'Sub-test 2.1', 'T2', 11, 12, 10, 11, 'included'), ('sec-t2-interpretation', 'sec-t2-test-case', 'Interpreting the test case results', 'T2', 12, 12, 11, 11, 'included'), ('sec-t3-test-case', None, 'Test case 3: Check malware protection', 'T3', 13, 16, 12, 15, 'included'), ('sec-t3-purpose', 'sec-t3-test-case', 'Test purpose', 'T3', 13, 13, 12, 12, 'context_only'), ('sec-t3-description', 'sec-t3-test-case', 'Test description', 'T3', 13, 16, 12, 15, 'context_only'), ('sec-t3-prerequisites', 'sec-t3-description', 'Prerequisites', 'T3', 13, 13, 12, 12, 'included'), ('sec-t3-select-subtests', 'sec-t3-description', 'Selecting appropriate sub-tests', 'T3', 13, 13, 12, 12, 'included'), ('sec-t3-subtest-3-1', 'sec-t3-description', 'Sub-test 3.1 (for devices that use anti-malware software)', 'T3', 13, 13, 12, 12, 'included'), ('sec-t3-subtest-3-1-1', 'sec-t3-subtest-3-1', 'Sub-test 3.1.1 (Check effectiveness of defences against malware delivered by email)', 'T3', 14, 14, 13, 13, 'included'), ('sec-t3-subtest-3-1-2', 'sec-t3-subtest-3-1', 'Sub-test 3.1.2 (Check effectiveness of defences against malware delivered by browser)', 'T3', 14, 15, 13, 14, 'included'), ('sec-t3-subtest-3-1-3', 'sec-t3-subtest-3-1', 'Sub-test 3.1.3 (Manual Checks for devices that use anti-malware software)', 'T3', 15, 15, 14, 14, 'included'), ('sec-t3-subtest-3-2', 'sec-t3-description', 'Sub-test 3.2 (for devices that use certificate-based application allow listing)', 'T3', 16, 16, 15, 15, 'included'), ('sec-t3-interpretation', 'sec-t3-test-case', 'Interpreting the test case results', 'T3', 16, 16, 15, 15, 'included'), ('sec-t4-test-case', None, 'Test case 4: Check multi-factor authentication configuration', 'T4', 17, 18, 16, 17, 'included'), ('sec-t4-purpose', 'sec-t4-test-case', 'Test purpose', 'T4', 17, 17, 16, 16, 'context_only'), ('sec-t4-description', 'sec-t4-test-case', 'Test description', 'T4', 17, 17, 16, 16, 'included'), ('sec-t4-case-4-1', 'sec-t4-test-case', 'Test case 4.1', 'T4', 17, 17, 16, 16, 'included'), ('sec-t4-interpretation', 'sec-t4-test-case', 'Interpreting the test case results', 'T4', 18, 18, 17, 17, 'included'), ('sec-t5-test-case', None, 'Test case 5: Check account separation', 'T5', 19, 19, 18, 18, 'included'), ('sec-t5-purpose', 'sec-t5-test-case', 'Test purpose', 'T5', 19, 19, 18, 18, 'context_only'), ('sec-t5-description', 'sec-t5-test-case', 'Test description', 'T5', 19, 19, 18, 18, 'included'), ('sec-t5-case-5-1', 'sec-t5-test-case', 'Test case 5.1', 'T5', 19, 19, 18, 18, 'included'), ('sec-t5-interpretation', 'sec-t5-test-case', 'Interpreting the test case results', 'T5', 19, 19, 18, 18, 'included'), ('sec-c-conclude', None, 'Conclude the assessment', 'C', 20, 20, 19, 19, 'included'), ('sec-c-note-deferral', 'sec-c-conclude', 'Note for Delivery Partner', 'C', 20, 20, 19, 19, 'included'), ('sec-c-note-exception', 'sec-c-conclude', 'Note for Delivery Partner', 'C', 20, 20, 19, 19, 'included'), ('sec-a-appendix', None, 'Appendix A: Vulnerability scanning', 'A', 21, 21, 20, 20, 'included'), ('sec-a-note-delivery-partner', 'sec-a-appendix', 'Note for Delivery Partner', 'A', 21, 21, 20, 20, 'included'), ('sec-b-appendix', None, 'Appendix B: Types of test file', 'B', 22, 23, 21, 22, 'included'), ('sec-b-note-delivery-partner', 'sec-b-appendix', 'Note for Delivery Partner', 'B', 22, 22, 21, 21, 'included'), ('sec-m-rights-notice', None, 'Rights and attribution notice', 'M', 24, 24, None, None, 'context_only'))
EXPECTED_SECTION_IDS = tuple(item[0] for item in EXPECTED_SECTION_OCCURRENCES)
SOURCE_FIVE_WORD_DIGEST_BYTES = base64.b64decode(
    "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"
    "JDgMf5sCAckRu5favk9b6NRVwGnLWqeABSULNcinfIgkO86aZhiKcVb4vg3A+A76ooEES7Zy/OYPHBIoR0456yRE/76IVoKoCFHc"
    "Qv8XH3QVHTheasp2w0U76a+iliabJEZxrx/IXdcdVtD/+XdnH5D7tqSbs1WDjAhx7eDEuA0kRxZ9Y4izNLMlvkeqy6xcCNn9XStk"
    "FhucYmx5WsrPsiRxtjrCMHdGoYEXy5NuJq5PIfy7C6Z2/skErkXtmQhKJHWgBv0IobLr4/JSl7PdvuT9orxo6eNjBrsLy5Mgg8Qk"
    "eR7SU3ML/MhmAbHPm0EXEJRZBjK6Xq9op71OvykfmyR+8RG+rb/wYMXuGIasWcODz9j6ttV4ui8ka/Tr11FMJIt5otH7sQl6Gl6I"
    "DOTPsRn01QlY4bZQNrCEhQGylRkki+FZ62EsCS/+oTswDkD2wzo7OMnPcCvxt3YZpeoJKSSMK1Y3axT4hj49FB7TzQu7lDGPY4Zv"
    "PhI+WhWYod6OJI/GCTGxV7Z4LrrwtKVbmH5MVzu6fZOn+43uR2NRR/gkoVSfNAZ6Ebp8NVZhYefxNEB0WOpF9tpPt2xqBNwgKiSr"
    "ym1kaJwfQIUtBZ3FswMln6fbIJDNvwnB8xgQObdSJMB8+o2C5QpagWC8NG9Tm9drrwDuNWpD6jc1wajkV6okxYDoq4StrVYuSXDK"
    "hyKsv3aKJPRns7hZo9Re8JP9IyT0oVnMv5zi1BI9SYxwAfWmjbq65+prIVyeqpTQQUHaJUyHdZKIQj4PZrZclCWezeJYoh2x0xHC"
    "9ZHmV0jHrj0lVht/HA6gUvX7KvybgA9lWQ/2X3cqbzKQ6dnFP9p99iVlCNnUqfMwyOcwIiQHflhKXgXyo6bIojUp/hkxgCy2JWlr"
    "ZreTukzUrIq0ToA5z6ib/ee+3oZfO9lN2Gt6h0clla5xfQeVmGgv+JR4ccXumFuqXpngXJ+3qcCKJTa4qiWis/vscu9Z1WAlRl8q"
    "T6RHun1CSeXkXbBn/MoMh8LdJbg2WtD4Y66DtcJuIuposOmwTCpqY8pMsUs16fL7Wtsl1XxVQWjeLp9v+H3Snb3bTXPYaIXw2HGB"
    "snXYCk/75yXrOACZQAtWvL2Lr+vMc48NtHoQOhZYnJBGw+6J+WKWJe7P7uALC3yILFHxES1ioCSurOEzdCWq/0YQSb0jSJcmCNCz"
    "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"
)
SOURCE_FIVE_WORD_DIGESTS = frozenset(
    SOURCE_FIVE_WORD_DIGEST_BYTES[index:index + 32]
    for index in range(0, len(SOURCE_FIVE_WORD_DIGEST_BYTES), 32)
)
PERMITTED_SOURCE_IDENTITY_PROSE = tuple(
    " ".join(re.findall(r"[a-z0-9%]+", value.lower()))
    for value in (
        SOURCE_TITLE, f"{SOURCE_TITLE} v3.2", SOURCE_AUTHORITY,
        "Open Government Licence v3.0",
    )
)
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

    def assert_no_copied_source_passage_digests(
        self, oracle: object, *, source_window_digests=None,
    ) -> None:
        for path, value in self.original_free_text(oracle):
            words = self.normalized_prose(value).split()
            for index in range(len(words) - 4):
                window = " ".join(words[index:index + 5])
                if any(window in phrase for phrase in PERMITTED_SOURCE_IDENTITY_PROSE):
                    continue
                digest = hashlib.sha256(window.encode("utf-8")).digest()
                copied = (
                    digest.hex() in source_window_digests
                    if source_window_digests is not None
                    else digest in SOURCE_FIVE_WORD_DIGESTS
                )
                self.assertFalse(
                    copied,
                    f"normalized five-word source window reproduced at {path}",
                )

    def test_source_copy_digest_guard_rejects_copied_words_with_surrounding_text(self) -> None:
        copied_words = "assessor observes distinct authentication challenge"
        copied_digest = hashlib.sha256(copied_words.encode("utf-8")).hexdigest()
        candidate = {
            "provisions": [{
                "summary": f"During review the {copied_words} before access",
            }],
        }

        with self.assertRaisesRegex(AssertionError, r"provisions\[0\]\.summary"):
            self.assert_no_copied_source_passage_digests(
                candidate, source_window_digests={copied_digest},
            )

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
        self.assertLessEqual(len(inventory_commits), 1)
        first_inventory_commit = inventory_commits[0] if inventory_commits else "HEAD"
        candidate_parent = f"{first_inventory_commit}^" if inventory_commits else first_inventory_commit
        precedence = self.git(
            "merge-base", "--is-ancestor", rights_sha, candidate_parent,
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

        actual_occurrences = tuple(
            (
                item["section_id"], item["parent_section_id"], item["heading"],
                item["group"], item["pdf_pages"]["start"], item["pdf_pages"]["end"],
                None if item["printed_pages"] is None else item["printed_pages"]["start"],
                None if item["printed_pages"] is None else item["printed_pages"]["end"],
                item["decision"],
            )
            for item in ledger
        )
        self.assertEqual(EXPECTED_SECTION_OCCURRENCES, actual_occurrences)
        self.assertEqual(EXPECTED_SECTION_IDS, tuple(section_ids))

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
        t4_008 = next(
            item for item in provisions
            if item["external_provision_id"] == "CEPTS3.2-T4-008"
        )
        self.assertEqual(
            "Pass when access first prompts the user or administrator for an MFA form; otherwise fail.",
            t4_008["summary"],
        )
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
    def test_counts_are_derived_and_equal_reconciled_constants(self) -> None:
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
        self.assertEqual(EXPECTED_COUNT, counts["total"])
        self.assertEqual(EXPECTED_GROUP_COUNTS, by_group)

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
    def test_original_free_text_does_not_reproduce_normalized_source_passages(self) -> None:
        self.assertTrue(SOURCE_FIVE_WORD_DIGESTS)
        self.assert_no_copied_source_passage_digests(self.oracle())

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

    @unittest.skipUnless(ORACLE.is_file(), "locked oracle is intentionally absent")
    def test_landing_page_publishes_plus_source_inventory_boundary(self) -> None:
        oracle = self.oracle()
        landing = LANDING_PAGE.read_text(encoding="utf-8")
        oracle_link = (
            "../docs/superpowers/specs/"
            "2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json"
        )

        required_text = (
            oracle_link,
            oracle["source"]["resource_page_url"],
            oracle["source"]["variants"][0]["url"],
            oracle["source"]["variants"][1]["url"],
            f'{oracle["source"]["variants"][0]["byte_length"]:,} bytes',
            f'{oracle["source"]["variants"][1]["byte_length"]:,} bytes',
            f'{oracle["counts"]["total"]} provisions',
            "Cyber Essentials core v3.3",
            "Cyber Essentials Plus v3.2",
            "complete only for the pinned public v3.2 specification",
            "2026 operational context",
            "not consolidated into the public v3.2 PDF",
            "No Cyber Essentials Plus mapping snapshot exists",
            "not a complete inventory of the current operational Cyber Essentials Plus scheme",
            "does not establish certification",
        )
        for expected in required_text:
            with self.subTest(expected=expected):
                self.assertIn(expected, landing)

        self.assert_no_affirmative_prohibited_claims(landing)


if __name__ == "__main__":
    unittest.main()
