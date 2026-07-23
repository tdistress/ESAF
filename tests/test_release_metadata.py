import json
import re
import unittest
from pathlib import Path

from tools.release_gates import load_front_matter


ROOT = Path(__file__).resolve().parents[1]

BACKLOG_PATTERN_ALIASES = {
    "ARC-P140": ("private-model",),
    "ARC-P150": ("AI integration",),
}

EXPECTED_MAPPING_SET_IDS = (
    "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
    "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
)

PROHIBITED_CONTROLLER_CLAIMS = (
    "three qualified mapping reaffirmations",
    "Pending: qualified mapping-set and scope approvals",
    "mapping_reviews",
)


def read_repository_file(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def current_version() -> str:
    version_text = read_repository_file("VERSION.md")
    match = re.search(r"^Current Version: \*\*(?P<version>[^*]+)\*\*$", version_text, re.MULTILINE)
    if match is None:
        raise AssertionError("VERSION.md must declare Current Version in bold")
    return match.group("version")


def current_changelog_section(version: str) -> str:
    changelog = read_repository_file("CHANGELOG.md")
    heading = f"## {version} - Unreleased"
    heading_matches = list(
        re.finditer(rf"^{re.escape(heading)}$", changelog, re.MULTILINE)
    )
    if len(heading_matches) != 1:
        raise AssertionError(f"CHANGELOG.md must contain exactly one {heading!r} heading")
    section_start = heading_matches[0].end()
    next_release = re.search(r"^## .+$", changelog[section_start:], re.MULTILINE)
    section_end = section_start + next_release.start() if next_release else len(changelog)
    return changelog[section_start:section_end]


def draft_architecture_patterns() -> list[tuple[str, str]]:
    registry = read_repository_file("architectures/patterns/README.md")
    row_pattern = re.compile(
        r"^\| \[(?P<identifier>ARC-P\d{3})\]\([^)]+\) "
        r"\| (?P<title>[^|]+?) \| Draft \|$",
        re.MULTILINE,
    )
    return [
        (match.group("identifier"), match.group("title"))
        for match in row_pattern.finditer(registry)
    ]


def normalized_words(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))


def contains_normalized_phrase(text: str, phrase: str) -> bool:
    text_words = normalized_words(text).split()
    phrase_words = normalized_words(phrase).split()
    phrase_length = len(phrase_words)
    return any(
        text_words[index:index + phrase_length] == phrase_words
        for index in range(len(text_words) - phrase_length + 1)
    )


def markdown_list_items(text: str) -> list[str]:
    item_pattern = re.compile(
        r"^(?P<indent>\s*)(?:[-+*]|\d+[.)])\s+"
        r"(?:\[[ xX]\]\s*)?(?P<body>.*)$"
    )
    items: list[str] = []
    ancestors: list[tuple[int, str]] = []
    for line in text.splitlines():
        match = item_pattern.match(line)
        if match:
            indentation = len(match.group("indent").expandtabs(4))
            while ancestors and ancestors[-1][0] >= indentation:
                ancestors.pop()
            body = match.group("body")
            items.append(" ".join([item for _, item in ancestors] + [body]))
            ancestors.append((indentation, body))
    return items


def release_readiness_rows() -> list[tuple[str, str, str]]:
    release_plan = read_repository_file("project/RELEASE_PLAN.md")
    section_match = re.search(
        r"^## 0\.4-alpha readiness\s*$"
        r"(?P<section>.*?)"
        r"(?=^## |\Z)",
        release_plan,
        re.MULTILINE | re.DOTALL,
    )
    if section_match is None:
        raise AssertionError("project/RELEASE_PLAN.md must contain a 0.4-alpha readiness section")
    row_pattern = re.compile(
        r"^\| (?P<gate>[^|]+?) \| (?P<state>[^|]+?) \| (?P<evidence>[^|]+?) \|$",
        re.MULTILINE,
    )
    return [
        (match.group("gate"), match.group("state"), match.group("evidence"))
        for match in row_pattern.finditer(section_match.group("section"))
        if match.group("gate") != "Gate"
    ]


class ReleaseMetadataTests(unittest.TestCase):
    def test_readme_badge_matches_current_version(self) -> None:
        version = current_version()
        readme = read_repository_file("README.md")
        badges = re.findall(
            r"!\[Version\]\((?P<url>[^)]+)\)",
            readme,
        )
        self.assertEqual(1, len(badges), "README must contain exactly one version badge")
        self.assertEqual(
            f"https://img.shields.io/badge/version-{version.replace('-', '--')}-orange",
            badges[0],
            "README version badge must match VERSION.md",
        )

    def test_roadmap_matches_current_version(self) -> None:
        version = current_version()
        roadmap = read_repository_file("ROADMAP.md")
        self.assertRegex(
            roadmap,
            rf"(?m)^\*\*Version:\*\* {re.escape(version)}$",
            "ROADMAP version must match VERSION.md",
        )

    def test_version_metadata_declares_working_draft_release_stage(self) -> None:
        version_text = read_repository_file("VERSION.md")
        self.assertIn("Status: **Working Draft**", version_text)
        self.assertIn(
            "Release Stage: **Initial Reference Architecture Draft Library**",
            version_text,
        )

    def test_current_changelog_section_is_unreleased(self) -> None:
        version = current_version()
        changelog = read_repository_file("CHANGELOG.md")
        heading = f"## {version} - Unreleased"
        self.assertEqual(
            1,
            len(re.findall(rf"^{re.escape(heading)}$", changelog, re.MULTILINE)),
            f"CHANGELOG.md must contain exactly one {heading!r} heading",
        )

    def test_current_changelog_names_all_three_draft_mapping_snapshots(self) -> None:
        section = current_changelog_section(current_version())
        required = (
            "Cyber Essentials v3.3",
            "Cyber Essentials Plus v3.2 `esaf_to_external`",
            "Cyber Essentials Plus v3.2 `external_to_esaf`",
        )
        for label in required:
            with self.subTest(label=label):
                self.assertIn(label, section)

    def test_evidence_candidate_remains_unreleased_and_untagged(self) -> None:
        record = load_front_matter(
            ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
        )
        self.assertEqual("evidence_candidate", record["phase"])
        self.assertIsNone(record["publication"]["date"])
        changelog = read_repository_file("CHANGELOG.md")
        self.assertEqual(1, changelog.count(f"## {current_version()} - Unreleased"))

    def test_release_plan_allows_one_uniform_mapping_decision_basis(self) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        self.assertIn(
            "exactly one uniform mapping decision basis: `qualified_approval` or "
            "`owner_risk_acceptance`",
            release_plan,
        )
        self.assertIn(
            "Owner risk acceptance defers qualified review; it does not complete or "
            "qualify that review.",
            release_plan,
        )
        self.assertIn(
            "Steering Committee governance approval remains a separate gate",
            release_plan,
        )

    def test_owner_risk_acceptance_retains_exact_mapping_review_backlog(self) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        item = next(
            value for value in markdown_list_items(backlog)
            if "Complete deferred qualified review for the 0.4-alpha mapping snapshots" in value
        )
        for mapping_set_id in EXPECTED_MAPPING_SET_IDS:
            with self.subTest(mapping_set_id=mapping_set_id):
                self.assertIn(mapping_set_id, item)

    def test_publication_controller_uses_two_basis_owner_risk_contract(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        for required in (
            "mapping_decision_schema: esaf-mapping-decisions-v1",
            "mapping_decision_basis",
            "owner_risk_acceptance",
            "qualified_approval",
            "new closure-head owner comment",
            "GitHub source immediately before construction, immediately before merge, and immediately before tag",
            "SHA-256 body comparison",
            "separate Steering Committee approval",
            "exact-head technical, editorial, and rendering verdicts with HTTPS locators",
            "tools/owner_risk_evidence.py",
            "owner, technical, editorial, rendering, governance, CI, merge-state, and post-merge evidence",
            "original five-file evidence-only closure allowlist",
        ):
            with self.subTest(required=required):
                self.assertIn(required, plan)
        for mapping_set_id in EXPECTED_MAPPING_SET_IDS:
            with self.subTest(mapping_set_id=mapping_set_id):
                self.assertIn(mapping_set_id, plan)
        for prohibited in PROHIBITED_CONTROLLER_CLAIMS:
            with self.subTest(prohibited=prohibited):
                self.assertNotIn(prohibited, plan)

    def test_repository_workflow_runs_release_and_link_validation(self) -> None:
        workflow = read_repository_file(".github/workflows/catalog-validation.yml")
        self.assertIn("python tools/release_gates.py --check", workflow)
        self.assertIn("python tools/validate_links.py --check", workflow)

    def test_current_changelog_names_all_draft_architecture_patterns(self) -> None:
        patterns = draft_architecture_patterns()
        self.assertEqual(7, len(patterns), "architecture registry must contain seven Draft rows")
        changelog_section = current_changelog_section(current_version()).casefold()
        for identifier, title in patterns:
            with self.subTest(identifier=identifier, field="identifier"):
                self.assertIn(identifier.casefold(), changelog_section)
            with self.subTest(identifier=identifier, field="title"):
                self.assertIn(title.casefold(), changelog_section)

    def test_backlog_does_not_queue_registered_architecture_patterns(self) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        queued_drafts = [
            normalized_words(item)
            for item in markdown_list_items(backlog)
            if re.search(
                r"\b(?:draft|drafting|queue|queued|queues)\b",
                normalized_words(item),
            )
        ]
        for identifier, title in draft_architecture_patterns():
            with self.subTest(identifier=identifier):
                aliases = (
                    identifier,
                    title,
                    *BACKLOG_PATTERN_ALIASES.get(identifier, ()),
                )
                queued = any(
                    any(
                        contains_normalized_phrase(draft, alias)
                        for alias in aliases
                    )
                    for draft in queued_drafts
                )
                self.assertFalse(
                    queued,
                    f"backlog still queues registered pattern {identifier} ({title})",
                )

    def test_backlog_queues_only_disposition_authorized_cyber_essentials_plus_work(self) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        matrix = json.loads(read_repository_file(
            "docs/superpowers/specs/"
            "2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json"
        ))
        expected_items: list[str] = []
        for assessment in matrix["direction_assessments"]:
            direction = assessment["direction"]
            disposition = assessment["disposition"]
            if disposition == "GO":
                expected = f"Design the Cyber Essentials Plus v3.2 {direction} mapping"
                if direction in {"esaf_to_external", "external_to_esaf"}:
                    # Separately authorized implementations completed both
                    # directional designs, so both items leave the backlog.
                    self.assertNotIn(f"- {expected}.", backlog)
                else:
                    expected_items.append(expected)
                    self.assertEqual(1, backlog.count(f"- {expected}."))
            elif disposition == "HOLD":
                expected = (
                    "Resolve the Cyber Essentials Plus v3.2 "
                    f"{direction} feasibility prerequisites"
                )
                expected_items.append(expected)
                self.assertEqual(1, backlog.count(f"- {expected}."))
            else:
                self.assertNotIn(
                    f"Design the Cyber Essentials Plus v3.2 {direction} mapping",
                    backlog,
                )

        plus_items = [
            item for item in markdown_list_items(backlog)
            if "Cyber Essentials Plus v3.2" in item
        ]
        self.assertEqual(
            [f"{item}." for item in expected_items],
            plus_items,
            "backlog must contain only direction-specific work authorized by the dispositions",
        )
        self.assertNotIn(
            "Conduct the Cyber Essentials Plus v3.2 mapping go/no-go review",
            backlog,
        )
        self.assertNotRegex(
            backlog,
            r"(?im)^- (?:Build|Create|Develop|Implement) (?:a |the )?"
            r"Cyber Essentials Plus v3\.2 mapping(?: set)?\.$",
        )

    def test_release_plan_preserves_readiness_boundaries(self) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        boundaries = (
            "reviewed candidate SHA",
            "resulting merged-main SHA",
            "every Mermaid diagram",
            "qualified contributors",
            "governance approval",
            "shall not be tagged or represented as released",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, release_plan)

    def test_taggable_release_gate_commands_include_the_evidence_baseline(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        commands = re.findall(
            r"^python tools/release_gates\.py --check .+ --phase taggable$",
            plan,
            re.MULTILINE,
        )
        self.assertEqual(2, len(commands))
        for command in commands:
            self.assertIn("--baseline-ref $evidenceMerge", command)

    def test_release_plan_requires_only_governance_documented_authority(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        self.assertNotIn("documented delegate", plan)
        self.assertIn("disposition `approved`", plan)

    def test_internal_publication_content_uses_shall_for_mandatory_language(self) -> None:
        paths = (
            "project/RELEASE_PLAN.md",
            "architectures/patterns/ARC-P140.md",
            "crosswalks/LIFECYCLE_RECORD_TEMPLATE.md",
            "controls/AGT/AGT-120.md",
            "controls/APP/APP-100.md",
            "controls/CMP/CMP-100.md",
            "controls/DAT/DAT-110.md",
            "controls/EDU/EDU-120.md",
            "controls/MON/MON-130.md",
            "controls/OPS/OPS-130.md",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertNotRegex(read_repository_file(path), r"(?i)\bmust(?:n['’]t| not)?\b")

    def test_release_readiness_gates_remain_open(self) -> None:
        expected_gates = (
            "Scope and milestone approval",
            "Normative and technical review",
            "Editorial and terminology review",
            "Cross-reference and rendering review",
            "Standards mapping review",
            "Release metadata synchronization",
            "Governance approval",
            "Post-merge validation",
        )
        rows = release_readiness_rows()
        self.assertEqual(expected_gates, tuple(gate for gate, _, _ in rows))
        for gate, state, _ in rows:
            with self.subTest(gate=gate):
                self.assertEqual("Open", state)


if __name__ == "__main__":
    unittest.main()
