import json
import re
import subprocess
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import patch

from tools.release_gates import load_front_matter


ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_TAG_OBJECT = "2cd1cf847fdb13a8b3323f62387ad5dabc5bd41f"
PUBLISHED_COMMIT = "8abfe5a85db19d11295a0c3debeb2d58109b0ca7"
PUBLISHED_EVIDENCE = (
    "https://github.com/tdistress/ESAF/issues/39#issuecomment-5064098764"
)

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
    heading_matches = list(re.finditer(
        rf"^## {re.escape(version)} - (?:Unreleased|\d{{4}}-\d{{2}}-\d{{2}})$",
        changelog,
        re.MULTILINE,
    ))
    if len(heading_matches) != 1:
        raise AssertionError(
            f"CHANGELOG.md must contain exactly one current {version!r} release heading"
        )
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


_DEFERRED_ASSURANCE_SUBJECT = re.compile(
    r"\b(?:"
    r"owner risk(?: acceptance| decision| disposition| evidence| path)?"
    r"|deferred(?: acceptance| assurance| decision| disposition| evidence| path)"
    r")\b"
)
_AFFIRMATIVE_ASSURANCE_VERB = re.compile(
    r"\b(?:"
    r"establish(?:es|ed|ing)?"
    r"|provid(?:e|es|ed|ing)"
    r"|constitut(?:e|es|ed|ing)"
    r"|complet(?:e|es|ed|ing)"
    r"|qualif(?:y|ies|ied|ying)"
    r"|confer(?:s|red|ring)?"
    r"|demonstrat(?:e|es|ed|ing)"
    r"|prov(?:e|es|ed|ing)"
    r")\b"
)
_PROTECTED_ASSURANCE_CONCEPT = re.compile(
    r"\b(?:"
    r"qualified (?:human )?review"
    r"|external scheme approval"
    r"|production readiness"
    r"|approval"
    r"|assurance"
    r"|compliance"
    r"|certification"
    r"|equivalence"
    r"|endorsement"
    r")\b"
)
_EXPLICIT_NEGATION = re.compile(
    r"\b(?:cannot|neither|never|no|not|without)\b"
)
_COORDINATED_SEGMENT = re.compile(
    r"\s*(?:;|\b(?:and|or|then|but|however|yet)\b)\s*",
    re.IGNORECASE,
)
_ISSUE_55_TARGET = re.compile(r"\b(?:issue 55|this issue)\b")
_DIRECT_CLOSURE_CLAIM = re.compile(
    r"\b(?:issue 55|this issue) "
    r"(?:(?:is|was|stands|remains) closed|(?:shall|will|must|may|can) close)\b"
)
_CLOSURE_VERB = re.compile(r"\bclos(?:e|es|ed|ing)\b")

_NEGATION_CONTRACTIONS = {
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "isn't": "is not",
    "mustn't": "must not",
    "shan't": "shall not",
    "shouldn't": "should not",
    "wasn't": "was not",
    "weren't": "were not",
    "won't": "will not",
    "wouldn't": "would not",
}


def contract_sentences(text: str) -> tuple[str, ...]:
    sentences: list[str] = []
    for paragraph in re.split(r"(?:\r?\n){2,}", text):
        flattened = " ".join(
            line.strip()
            for line in paragraph.splitlines()
            if line.strip()
        )
        sentences.extend(
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", flattened)
            if sentence.strip()
        )
    return tuple(sentences)


def normalized_contract_words(text: str) -> str:
    expanded = text.casefold().replace("’", "'")
    for contraction, replacement in _NEGATION_CONTRACTIONS.items():
        expanded = expanded.replace(contraction, replacement)
    return normalized_words(expanded)


def affirmative_deferred_assurance_claims(text: str) -> tuple[str, ...]:
    claims: list[str] = []
    for sentence in contract_sentences(text):
        subject_in_prior_segment = False
        claim_found = False
        for segment in _COORDINATED_SEGMENT.split(sentence):
            normalized = normalized_contract_words(segment)
            subjects = tuple(_DEFERRED_ASSURANCE_SUBJECT.finditer(normalized))
            for verb in _AFFIRMATIVE_ASSURANCE_VERB.finditer(normalized):
                has_governing_subject = (
                    subject_in_prior_segment
                    or any(subject.start() < verb.start() for subject in subjects)
                )
                concept = _PROTECTED_ASSURANCE_CONCEPT.search(
                    normalized,
                    verb.end(),
                )
                if not has_governing_subject or concept is None:
                    continue
                if _EXPLICIT_NEGATION.search(normalized[:concept.end()]):
                    continue
                claims.append(sentence)
                claim_found = True
                break
            if claim_found:
                break
            subject_in_prior_segment = (
                subject_in_prior_segment
                or bool(subjects)
            )
    return tuple(claims)


def contradictory_issue_closure_claims(text: str) -> tuple[str, ...]:
    claims: list[str] = []
    for sentence in contract_sentences(text):
        subject_in_prior_segment = False
        claim_found = False
        for segment in _COORDINATED_SEGMENT.split(sentence):
            normalized = normalized_contract_words(segment)
            if _DIRECT_CLOSURE_CLAIM.search(normalized):
                claims.append(sentence)
                claim_found = True
                break
            subjects = tuple(_DEFERRED_ASSURANCE_SUBJECT.finditer(normalized))
            for verb in _CLOSURE_VERB.finditer(normalized):
                has_governing_subject = (
                    subject_in_prior_segment
                    or any(subject.start() < verb.start() for subject in subjects)
                )
                target = _ISSUE_55_TARGET.search(normalized, verb.end())
                if not has_governing_subject or target is None:
                    continue
                if _EXPLICIT_NEGATION.search(normalized[:target.end()]):
                    continue
                claims.append(sentence)
                claim_found = True
                break
            if claim_found:
                break
            subject_in_prior_segment = (
                subject_in_prior_segment
                or bool(subjects)
            )
    return tuple(claims)


def uk_mapping_set_ids(text: str) -> tuple[str, ...]:
    return tuple(re.findall(
        r"`(uk-ncsc--[a-z0-9.-]+(?:--[a-z0-9.-]+)*)`",
        text,
    ))


def fenced_markdown_in_task(plan: str, task_heading: str) -> str:
    task_start = plan.index(task_heading)
    next_task = re.search(r"^## Task \d+:", plan[task_start + 1:], re.MULTILINE)
    task_end = (
        task_start + 1 + next_task.start()
        if next_task is not None
        else len(plan)
    )
    task = plan[task_start:task_end]
    fence_start = task.index("```markdown\n") + len("```markdown\n")
    fence_end = task.index("\n```", fence_start)
    return task[fence_start:fence_end]


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


def markdown_section(text: str, heading: str) -> str:
    start_match = re.search(
        rf"^{re.escape(heading)}\s*$",
        text,
        re.MULTILINE,
    )
    if start_match is None:
        raise AssertionError(f"missing Markdown section {heading!r}")
    section_start = start_match.end()
    next_heading = re.search(
        r"^#{1,6}\s+.+$",
        text[section_start:],
        re.MULTILINE,
    )
    section_end = (
        section_start + next_heading.start()
        if next_heading is not None
        else len(text)
    )
    return text[section_start:section_end]


def release_readiness_rows() -> list[tuple[str, str, str]]:
    release_plan = read_repository_file("project/RELEASE_PLAN.md")
    section_match = re.search(
        r"^## 0\.4-alpha publication\s*$"
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

    def test_current_changelog_section_records_published_working_draft(self) -> None:
        changelog = read_repository_file("CHANGELOG.md")
        self.assertEqual(
            1,
            len(re.findall(
                r"^## 0\.4-alpha - 2026-07-23$",
                changelog,
                re.MULTILINE,
            )),
        )
        self.assertNotIn("0.4-alpha - 2026-07-23 (conditional)", changelog)

    def test_changelog_distinguishes_published_and_unreleased_working_drafts(self) -> None:
        changelog = read_repository_file("CHANGELOG.md").casefold()
        self.assertIn(
            "0.2-alpha and 0.3-alpha remain unreleased working-draft stages",
            changelog,
        )
        self.assertIn("0.4-alpha is a tagged working draft", changelog)

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

    def test_published_record_uses_owner_risk_acceptance_and_fixed_evidence(self) -> None:
        record = load_front_matter(
            ROOT / "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
        )
        self.assertEqual("published", record["phase"])
        self.assertEqual("owner_risk_acceptance", record["mapping_decision_basis"])
        self.assertEqual(date(2026, 7, 23), record["publication"]["date"])
        self.assertEqual(PUBLISHED_TAG_OBJECT, record["publication"]["tag_object"])
        self.assertEqual(PUBLISHED_COMMIT, record["publication"]["tagged_commit"])
        self.assertEqual(PUBLISHED_EVIDENCE, record["publication"]["evidence"])
        self.assertTrue(all(value["state"] == "closed" for value in record["gates"].values()))

    def test_recorded_annotated_tag_matches_local_repository(self) -> None:
        tag_object = subprocess.run(
            ["git", "rev-parse", "v0.4-alpha"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        peeled_commit = subprocess.run(
            ["git", "rev-parse", "v0.4-alpha^{commit}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(PUBLISHED_TAG_OBJECT, tag_object)
        self.assertEqual(PUBLISHED_COMMIT, peeled_commit)

    def test_published_wording_retains_owner_risk_and_draft_limitations(self) -> None:
        readiness = read_repository_file(
            "docs/superpowers/reviews/2026-07-21-v04-alpha-publication-readiness.md"
        ).casefold()
        self.assertTrue(contains_normalized_phrase(
            readiness,
            "does not convert draft controls, architectures, or mappings into "
            "reviewed or approved artifacts",
        ))
        for required in (
            "owner risk acceptance",
            "qualified mapping review is deferred",
            "draft snapshots",
            "does not assert assurance",
            "certification",
            "compliance",
            "equivalence",
            "endorsement",
            "external-scheme approval",
            "production readiness",
        ):
            with self.subTest(required=required):
                self.assertTrue(contains_normalized_phrase(readiness, required))
        for path in ("CHANGELOG.md", "project/RELEASE_PLAN.md"):
            with self.subTest(path=path):
                self.assertNotIn("qualified mapping review completed", read_repository_file(path).casefold())

    def test_release_plan_allows_one_uniform_mapping_decision_basis(self) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        self.assertIn(
            "exactly one uniform mapping decision basis: `qualified_approval` or "
            "`owner_risk_acceptance`",
            release_plan,
        )
        self.assertTrue(contains_normalized_phrase(
            release_plan,
            "Owner risk acceptance defers qualified review; it does not complete or "
            "qualify that review.",
        ))
        self.assertIn(
            "Steering Committee governance approval remains a separate gate",
            release_plan,
        )

        assurance = markdown_section(
            release_plan,
            "## v0.5-beta deferred mapping assurance",
        )
        for required in (
            "exact v0.5-beta release candidate",
            "one authenticated owner source",
            "remain Draft",
            "Issue 55 remains open for the six qualified human role dispositions.",
        ):
            with self.subTest(required=required):
                self.assertTrue(contains_normalized_phrase(assurance, required))
        for required in (
            "mapping_decision_basis: owner_risk_acceptance",
            "decision_type: owner_risk_acceptance",
            "qualified_review_status: deferred",
        ):
            with self.subTest(required=required):
                self.assertIn(required, assurance)
        self.assertEqual(EXPECTED_MAPPING_SET_IDS, uk_mapping_set_ids(assurance))
        for prohibited in (
            "issue 55 is closed",
            "issue 55 shall close",
            "owner-risk acceptance closes issue 55",
        ):
            with self.subTest(prohibited=prohibited):
                self.assertFalse(contains_normalized_phrase(assurance, prohibited))
        self.assertEqual((), affirmative_deferred_assurance_claims(assurance))
        self.assertEqual((), contradictory_issue_closure_claims(assurance))

    def test_release_plan_contract_rejects_appended_affirmative_compliance_claim(
        self,
    ) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        assurance = markdown_section(
            release_plan,
            "## v0.5-beta deferred mapping assurance",
        )
        mutations = (
            "Owner-risk acceptance establishes compliance.",
            "Owner-risk acceptance does not complete qualified review and "
            "establishes compliance.",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assertEqual(
                    (mutation,),
                    affirmative_deferred_assurance_claims(
                        f"{assurance}\n\n{mutation}"
                    ),
                )

    def test_issue_55_contract_rejects_appended_affirmative_assurance_claim(
        self,
    ) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/"
            "2026-07-27-v05-beta-deferred-mapping-assurance.md"
        )
        issue_body = fenced_markdown_in_task(
            plan,
            "## Task 6: Synchronize GitHub Issue 55",
        )
        mutation = "Owner-risk acceptance provides qualified-review assurance."

        self.assertEqual(
            (mutation,),
            affirmative_deferred_assurance_claims(f"{issue_body}\n\n{mutation}"),
        )

    def test_issue_55_contract_rejects_appended_closed_state(
        self,
    ) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/"
            "2026-07-27-v05-beta-deferred-mapping-assurance.md"
        )
        issue_body = fenced_markdown_in_task(
            plan,
            "## Task 6: Synchronize GitHub Issue 55",
        )
        mutations = (
            "This issue is closed.",
            "Owner-risk acceptance does not complete qualified review and "
            "closes this issue.",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assertEqual(
                    (mutation,),
                    contradictory_issue_closure_claims(
                        f"{issue_body}\n\n{mutation}"
                    ),
                )

    def test_issue_59_contract_rejects_appended_closed_state(
        self,
    ) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/"
            "2026-07-27-v05-beta-deferred-mapping-assurance.md"
        )
        issue_body = fenced_markdown_in_task(
            plan,
            "## Task 7: Synchronize GitHub Issue 59",
        )
        mutation = "This issue is closed."
        mutated_plan = plan.replace(
            issue_body,
            f"{issue_body}\n\n{mutation}",
            1,
        )

        with patch(
            f"{__name__}.read_repository_file",
            return_value=mutated_plan,
        ):
            with self.assertRaises(AssertionError):
                self.test_planned_issue_59_body_preserves_complete_release_gate_set()

    def test_affirmative_claim_detector_covers_protected_verbs_and_concepts(
        self,
    ) -> None:
        claims = (
            "Owner-risk acceptance establishes compliance.",
            "Owner-risk acceptance provides qualified-review assurance.",
            "Deferred acceptance constitutes approval.",
            "Deferred assurance completes certification.",
            "Owner-risk decision qualifies equivalence.",
            "Deferred disposition confers endorsement.",
            "Owner-risk acceptance demonstrates external-scheme approval.",
            "The deferred path proves production readiness.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertEqual(
                    (claim,),
                    affirmative_deferred_assurance_claims(claim),
                )

    def test_affirmative_claim_detector_ignores_explicitly_negated_boundaries(
        self,
    ) -> None:
        boundaries = (
            "Owner-risk acceptance does not establish compliance.",
            "Owner-risk acceptance cannot provide qualified-review assurance.",
            "Deferred acceptance does not constitute approval.",
            "Deferred assurance shall not complete certification.",
            "Owner-risk decision does not qualify equivalence.",
            "Deferred disposition cannot confer endorsement.",
            "Owner-risk acceptance never demonstrates external-scheme approval.",
            "No deferred path proves production readiness.",
            "Neither deferred assurance nor later qualified review establishes "
            "compliance.",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertEqual(
                    (),
                    affirmative_deferred_assurance_claims(boundary),
                )

    def test_closure_detector_covers_issue_55_and_this_issue_variants(
        self,
    ) -> None:
        claims = (
            "This issue is closed.",
            "Issue 55 is closed.",
            "This issue shall close.",
            "Issue 55 shall close.",
            "Owner-risk acceptance closes this issue.",
            "Deferred acceptance closes issue 55.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                self.assertEqual(
                    (claim,),
                    contradictory_issue_closure_claims(claim),
                )

    def test_closure_detector_ignores_explicitly_negated_open_boundaries(
        self,
    ) -> None:
        boundaries = (
            "This issue is not closed.",
            "Issue 55 shall not close.",
            "Owner-risk acceptance cannot close this issue.",
            "Deferred acceptance does not close issue 55.",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertEqual(
                    (),
                    contradictory_issue_closure_claims(boundary),
                )

    def test_deferred_release_preserves_draft_state_and_required_nonclaims(
        self,
    ) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        assurance = markdown_section(
            release_plan,
            "## v0.5-beta deferred mapping assurance",
        )
        self.assertTrue(contains_normalized_phrase(
            assurance,
            "all three mapping sets and their records remain Draft",
        ))
        self.assertTrue(contains_normalized_phrase(
            assurance,
            "It does not establish qualified review, approval, assurance, compliance, "
            "certification, equivalence, endorsement, external-scheme approval, or "
            "production readiness.",
        ))
        lower_assurance = assurance.casefold()
        for prohibited in (
            "qualified review completed",
            "approved mappings",
        ):
            with self.subTest(prohibited=prohibited):
                self.assertNotIn(prohibited, lower_assurance)
        self.assertEqual((), affirmative_deferred_assurance_claims(assurance))

    def test_deferred_assurance_followup_keeps_issue_55_open_for_all_three_mapping_sets(
        self,
    ) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        deferred = markdown_section(
            backlog,
            "## Deferred assurance follow-up",
        )
        self.assertIn("https://github.com/tdistress/ESAF/issues/55", deferred)
        self.assertTrue(contains_normalized_phrase(
            deferred,
            "remains open until qualified review is complete for all three exact "
            "mapping sets",
        ))
        self.assertEqual(EXPECTED_MAPPING_SET_IDS, uk_mapping_set_ids(deferred))

    def test_v05_beta_has_bounded_workstreams_and_exit_criteria(self) -> None:
        milestones = read_repository_file("project/MILESTONES.md")
        for heading in (
            "### Entry state",
            "### Required workstreams",
            "### Exit criteria",
            "### Non-goals",
        ):
            self.assertIn(heading, milestones)
        for required in (
            "all three UK mapping sets",
            "minimum ESAF-1500 assessment foundation",
            "one Draft pilot",
            "PCI DSS",
            "`GO`",
            "`HOLD`",
            "Critical and Important",
        ):
            self.assertIn(required, milestones)

    def test_v05_beta_accepts_qualified_or_coordinated_deferred_mapping_assurance(
        self,
    ) -> None:
        milestones = read_repository_file("project/MILESTONES.md")
        for section in (
            markdown_section(milestones, "### Required workstreams"),
            markdown_section(milestones, "### Exit criteria"),
        ):
            for required in (
                "completed qualified-review dispositions",
                "one coordinated owner-risk disposition",
                "all three",
                "exact v0.5-beta release candidate",
            ):
                with self.subTest(required=required):
                    self.assertTrue(contains_normalized_phrase(section, required))
        self.assertTrue(contains_normalized_phrase(
            milestones,
            "DEFERRED is a milestone assurance disposition, not an ESAF-1600 "
            "mapping lifecycle state",
        ))
        self.assertTrue(contains_normalized_phrase(
            milestones,
            "all three mapping sets and their records remain Draft",
        ))

    def test_historical_v05_closure_issue_body_requires_complete_gate_set(self) -> None:
        required_gate_set = (
            "The full test suite, control, architecture, crosswalk, link, release, "
            "working-tree, and applicable Mermaid-rendering gates pass on the exact "
            "candidate."
        )
        milestones = read_repository_file("project/MILESTONES.md")
        exit_criteria = milestones[
            milestones.index("### Exit criteria"):
            milestones.index("### Non-goals")
        ]
        self.assertTrue(contains_normalized_phrase(exit_criteria, required_gate_set))

        historical_plan = read_repository_file(
            "docs/superpowers/plans/2026-07-23-v05-beta-plan-reconciliation.md"
        )
        historical_closure_body = historical_plan[
            historical_plan.index("$closureBody=@'"):
            historical_plan.index(
                "'@",
                historical_plan.index("$closureBody=@'"),
            )
        ]
        self.assertTrue(contains_normalized_phrase(
            historical_closure_body,
            required_gate_set,
        ))

        backlog = read_repository_file("project/BACKLOG.md")
        active_workstreams = markdown_section(
            backlog,
            "## Active release workstreams",
        )
        self.assertIn("https://github.com/tdistress/ESAF/issues/59", active_workstreams)
        for required in (
            "completed qualified approval or validated exact-candidate "
            "owner-risk acceptance",
            "every other release gate remains required",
        ):
            with self.subTest(required=required):
                self.assertTrue(
                    contains_normalized_phrase(active_workstreams, required)
                )

    def test_planned_issue_55_body_preserves_deferred_assurance_boundaries(
        self,
    ) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/"
            "2026-07-27-v05-beta-deferred-mapping-assurance.md"
        )
        issue_body = fenced_markdown_in_task(
            plan,
            "## Task 6: Synchronize GitHub Issue 55",
        )

        self.assertIn(
            "For `v0.5-beta`, the mapping-assurance release gate may be satisfied "
            "by either:",
            issue_body,
        )
        self.assertEqual(EXPECTED_MAPPING_SET_IDS, uk_mapping_set_ids(issue_body))
        for required in (
            "This issue remains open if v0.5-beta proceeds under the coordinated "
            "owner-risk deferred-assurance path.",
            "Owner-risk acceptance cannot substitute for qualified human review and "
            "cannot close this issue.",
            "specification and inventory review for Core",
            "security and overclaiming review for Core",
            "specification and inventory review for Plus forward",
            "security and overclaiming review for Plus forward",
            "specification and inventory review for Plus reverse",
            "security and overclaiming review for Plus reverse",
            "The second path permits Working Draft publication only. It does not "
            "complete this issue, complete qualified review, or change any mapping "
            "lifecycle state.",
            "All three mapping sets and all records remain draft.",
            "Update reviewer metadata, lifecycle events, approval state, or "
            "publication state only when every ESAF-1600 transition condition is "
            "satisfied.",
            "Neither deferred assurance nor later qualified review establishes "
            "compliance, certification, equivalence, endorsement, external-scheme "
            "approval, production readiness, or assurance beyond the expressly "
            "recorded scope.",
        ):
            with self.subTest(required=required):
                self.assertTrue(contains_normalized_phrase(issue_body, required))
        for prohibited in (
            "issue 55 is closed",
            "issue 55 shall close",
            "owner-risk acceptance closes issue 55",
        ):
            with self.subTest(prohibited=prohibited):
                self.assertFalse(contains_normalized_phrase(issue_body, prohibited))
        self.assertEqual((), affirmative_deferred_assurance_claims(issue_body))
        self.assertEqual((), contradictory_issue_closure_claims(issue_body))

    def test_planned_issue_59_body_preserves_complete_release_gate_set(
        self,
    ) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/"
            "2026-07-27-v05-beta-deferred-mapping-assurance.md"
        )
        issue_body = fenced_markdown_in_task(
            plan,
            "## Task 7: Synchronize GitHub Issue 59",
        )

        self.assertEqual(EXPECTED_MAPPING_SET_IDS, uk_mapping_set_ids(issue_body))
        for required in (
            "completed qualified-review dispositions for all six human roles tracked "
            "in #55",
            "one authenticated owner-risk decision that defers qualified review for "
            "all three exact mapping sets",
            "bind every decision to the exact v0.5-beta release candidate SHA",
            "use one uniform decision basis and one authenticated owner source",
            "all three mapping sets and their records remain draft, no reviewer "
            "metadata or lifecycle event is added, and #55 remains open",
            "Technical, editorial, terminology, mapping, profile-scope, and governance "
            "reviews are complete.",
            "The full test suite, control, architecture, crosswalk, assessment, link, "
            "release, working-tree, and applicable Mermaid-rendering gates pass on "
            "the exact candidate.",
            "The complete branch diff is reviewed, GitHub checks pass, and merge state "
            "is clean.",
            "Post-merge validation passes before an immutable tag or publication "
            "statement is created.",
            "Critical and Important findings are resolved.",
            "The deferred path does not claim qualified review, approval, "
            "certification, compliance, equivalence, endorsement, external-scheme "
            "approval, production readiness, or assurance beyond the recorded "
            "Working Draft basis.",
            "Evidence from v0.4-alpha is historical and cannot approve v0.5-beta.",
        ):
            with self.subTest(required=required):
                self.assertTrue(contains_normalized_phrase(issue_body, required))
        self.assertEqual((), affirmative_deferred_assurance_claims(issue_body))
        self.assertEqual((), contradictory_issue_closure_claims(issue_body))

    def test_v05_beta_preserves_bounded_non_goals(self) -> None:
        milestones = read_repository_file("project/MILESTONES.md")
        for non_goal in (
            "all roadmap crosswalks",
            "all nine planned profiles",
            "complete assessment workbook",
            "substantive HITRUST CSF mapping",
            "redesigning `v0.9-rc1` and `v1.0`",
        ):
            self.assertIn(non_goal, milestones)

    def test_backlog_removes_completed_work_and_preserves_remaining_dependencies(
        self,
    ) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        self.assertNotIn("Complete open 0.4-alpha publication gates", backlog)
        self.assertNotIn("Select and publish one Draft pilot", backlog)
        active_workstreams = markdown_section(
            backlog,
            "## Active release workstreams",
        )
        deferred_assurance = markdown_section(
            backlog,
            "## Deferred assurance follow-up",
        )
        self.assertIn("[issue 59]", active_workstreams.casefold())
        self.assertNotIn("[issue 59]", deferred_assurance.casefold())
        self.assertIn("[issue 55]", deferred_assurance.casefold())
        self.assertNotIn("[issue 55]", active_workstreams.casefold())
        self.assertNotIn("Define the minimum ESAF-1500 assessment foundation", backlog)
        for mapping_set_id in EXPECTED_MAPPING_SET_IDS:
            with self.subTest(mapping_set_id=mapping_set_id):
                self.assertIn(mapping_set_id, backlog)
        self.assertNotIn("Complete PCI DSS source readiness", backlog)
        self.assertIn("completed through the evidenced `HOLD`", backlog)
        self.assertIn("publication-rights boundary", backlog)
        self.assertTrue(contains_normalized_phrase(backlog, "qualified-review contract"))
        self.assertIn("without\n  creating a PCI DSS mapping artifact", backlog)
        self.assertNotIn("This supersedes the former initiative", backlog)

    def test_hitrust_is_readiness_gated_and_not_a_v05_blocker(self) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        for required in (
            "licensed-source access",
            "publication rights",
            "qualified-review availability",
            "does not block `v0.5-beta`",
        ):
            self.assertTrue(contains_normalized_phrase(backlog, required))

    def test_roadmap_keeps_deferred_mapping_assurance_nonblocking_after_beta(
        self,
    ) -> None:
        roadmap = read_repository_file("ROADMAP.md")
        sequence = markdown_section(
            roadmap,
            "## 0.5-beta delivery sequence",
        )
        for required in (
            "deferred mapping assurance remains tracked after beta",
            "does not stop later engineering work",
            "issue 55",
        ):
            with self.subTest(required=required):
                self.assertTrue(contains_normalized_phrase(sequence, required))
        self.assertFalse(contains_normalized_phrase(
            sequence,
            "first closes mapping assurance debt",
        ))

    def test_v05_issue_bodies_state_their_dependencies(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-23-v05-beta-plan-reconciliation.md"
        )
        cases = {
            "qualifiedBody": (
                "Depends on the merged planning reconciliation.",
                "does not depend on any other v0.5-beta content issue",
            ),
            "assessmentBody": (
                "Depends on the merged planning reconciliation.",
                "does not depend on any other v0.5-beta content issue",
            ),
            "pciBody": (
                "may proceed in parallel with the qualified-review and assessment "
                "workstreams",
                "No mapping records may be published before the go/no-go decision.",
            ),
            "hitrustBody": (
                "licensed-source access",
                "publication-rights confirmation",
                "exact-version identification",
                "qualified-review availability",
                "unmilestoned and non-blocking for v0.5-beta",
            ),
        }
        for variable, requirements in cases.items():
            with self.subTest(variable=variable):
                start = plan.index(f"${variable}=@'")
                body = plan[start:plan.index("'@", start)]
                self.assertIn("## Dependencies", body)
                for required in requirements:
                    self.assertTrue(contains_normalized_phrase(body, required))

    def test_v05_queue_preflights_titles_and_labels_before_first_write(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-23-v05-beta-plan-reconciliation.md"
        )
        queue = plan[plan.index("### Task 6: Create and verify"):]
        first_write = queue.index(
            "$milestone=gh api repos/tdistress/ESAF/milestones -X POST"
        )
        preflight = queue[:first_write]
        self.assertIn("$existingIssueTitles=@", preflight)
        for title in (
            "Complete qualified review of the three UK mapping snapshots",
            "Define the minimum ESAF-1500 assessment foundation",
            "Select and publish one Draft pilot ESAF industry profile",
            "Complete PCI DSS source readiness and mapping go/no-go",
            "Close the v0.5-beta publication gates",
            "Establish HITRUST CSF source and review readiness",
        ):
            with self.subTest(title=title):
                self.assertIn(f"Assert-IssueTitleAbsent '{title}'", preflight)
        self.assertIn("$requiredLabels=@", preflight)
        self.assertIn("$existingLabels=@", preflight)
        self.assertIn("$missingLabels=@", preflight)
        for label in (
            "crosswalk",
            "assessment",
            "profile",
            "governance",
            "priority:critical",
            "priority:high",
            "priority:medium",
        ):
            with self.subTest(label=label):
                self.assertIn(f"'{label}'", preflight)

    def test_published_sha_exception_plan_is_phase_scoped(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-23-v05-beta-plan-reconciliation.md"
        )
        self.assertIn(
            'if phase == "published" and path in PUBLISHED_SHA_PATHS:',
            plan,
        )

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

    def test_owner_risk_controller_rebuilds_live_evidence_at_each_required_point(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        for fetched_path in (
            "esaf-v04-$suffix.json",
            "esaf-v04-$name-prefetch-merge.json",
            "esaf-v04-owner-prefetch-tag.json",
        ):
            with self.subTest(fetched_path=fetched_path):
                self.assertIn(fetched_path, plan)
        self.assertGreaterEqual(
            plan.count('gh api "repos/tdistress/ESAF/issues/comments/$commentId"'),
            2,
        )
        self.assertGreaterEqual(plan.count("--technical-comment-json"), 2)
        self.assertGreaterEqual(plan.count("--editorial-comment-json"), 2)
        self.assertGreaterEqual(plan.count("--rendering-comment-json"), 2)
        self.assertGreaterEqual(plan.count("--governance-comment-json"), 2)
        self.assertGreaterEqual(plan.count("--pr-state-json"), 2)
        self.assertIn("--base-evidence $externalEvidence", plan)
        self.assertIn("Remove-Item -LiteralPath $externalEvidence", plan)
        self.assertIn("Remove-Item -LiteralPath $taggableEvidence", plan)
        for operation in (
            "Assert-NativeSuccess 'Rebuild closure evidence'",
            "Assert-NativeSuccess 'Validate refreshed closure evidence'",
            "Assert-NativeSuccess 'Build refreshed taggable evidence'",
            "Assert-NativeSuccess 'Validate refreshed taggable evidence'",
        ):
            with self.subTest(operation=operation):
                self.assertIn(operation, plan)

    def test_controller_resolves_basis_and_summary_inside_each_consumer_block(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        self.assertNotIn("@ownerRiskRefreshArgs", plan)
        summary_definition = "$mappingDecisionSummary ="
        tag_block = plan[
            plan.index("- [ ] **Step 4: Create and push the annotated tag atomically after validation**"):
            plan.index("- [ ] **Step 5: Resolve the remote annotated tag to the exact commit**")
        ]
        issue_block = plan[
            plan.index("- [ ] **Step 6: Record publication evidence and close issue #39**"):
            plan.index("- [ ] **Step 7: Clean branches/worktrees and verify final repository state**")
        ]
        for block, use in (
            (tag_block, "Mapping decision basis: $mappingDecisionBasis. $mappingDecisionSummary"),
            (issue_block, "- Mapping decision: $mappingDecisionBasis; $mappingDecisionSummary"),
        ):
            with self.subTest(use=use):
                self.assertIn(use, block)
                self.assertLess(block.index("$mappingDecisionBasis ="), block.index(use))
                self.assertLess(block.index(summary_definition), block.index(use))

    def test_owner_risk_refreshes_compare_exact_fetched_comment_digests(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        self.assertGreaterEqual(plan.count("[Security.Cryptography.SHA256]::HashData"), 3)
        self.assertGreaterEqual(plan.count("Assert-OwnerSourceUnchanged"), 3)
        for required in (
            "Owner source digest differs from the prior validated source",
            "Owner source comment identity differs from the prior validated source",
            "Owner source author identity differs from the prior validated source",
            "Owner source timestamps differ from the prior validated source",
            "body_sha256",
        ):
            with self.subTest(required=required):
                self.assertIn(required, plan)

    def test_controller_constructs_and_validates_both_mapping_decision_bases(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        self.assertGreaterEqual(
            plan.count("elseif ($mappingDecisionBasis -eq 'qualified_approval')"),
            3,
        )
        for required in (
            "function New-QualifiedClosureEvidence",
            "mapping_decision_schema = 'esaf-mapping-decisions-v1'",
            "qualified_review_status='completed'",
            "claims_not_made = @(",
            "mapping_decisions = $qualifiedDecisions",
            "scope=$qualifiedScope",
            "Unsupported mapping decision basis",
            "--phase closure",
            "--phase taggable",
        ):
            with self.subTest(required=required):
                self.assertIn(required, plan)

    def test_final_owner_issue_evidence_reports_digest_comparison(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        issue_block = plan[
            plan.index("- [ ] **Step 6: Record publication evidence and close issue #39**"):
            plan.index("- [ ] **Step 7: Clean branches/worktrees and verify final repository state**")
        ]
        for required in (
            "$owner.comment_url",
            "$owner.comment_id",
            "$owner.body_sha256",
            "$ownerComparison",
            "Owner source live comparison: $ownerComparison",
            "Qualified approval is completed",
        ):
            with self.subTest(required=required):
                self.assertIn(required, issue_block)

    def test_qualified_approval_acquisition_requires_three_live_structured_decisions(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        for required in (
            "function New-QualifiedInputFromSources",
            "qualified decision comment shall contain a JSON object",
            "decision_type -ne 'qualified_approval'",
            "decided_at -notmatch '^\\d{4}-\\d{2}-\\d{2}T",
            "qualified_review_status -ne 'completed'",
            "claims_not_made -join ','",
            "Qualified decision evidence URL shall equal fetched comment URL",
            "esaf-v04-qualified-$index-response.json",
            "Capture qualified decision comment IDs",
        ):
            with self.subTest(required=required):
                self.assertIn(required, plan)
        self.assertGreaterEqual(
            plan.count('gh api "repos/tdistress/ESAF/issues/comments/$qualifiedCommentId"'),
            3,
        )
        for mapping_set_id in EXPECTED_MAPPING_SET_IDS:
            with self.subTest(mapping_set_id=mapping_set_id):
                self.assertIn(mapping_set_id, plan)
        self.assertNotIn("equivalently complete basis-specific builder", plan)
        acquisition = plan[
            plan.index("For \x60qualified_approval\x60, acquire the three reviewer decisions"):
            plan.index("- [ ] **Step 4: Push and open closure PR B")
        ]
        for required in (
            "$expectedClaims",
            "[DateTimeOffset]::Parse([string]$decision.decided_at)",
            "$decision.reviewer",
            "$decision.qualification",
            "$decision.limitations.lifecycle -eq 'draft'",
            "$decision.limitations.claims_not_made -join ','",
        ):
            with self.subTest(required=required):
                self.assertIn(required, acquisition)

    def test_qualified_inputs_are_produced_from_fresh_live_sources_before_each_consumer(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        sections = (
            (
                "- [ ] **Step 5: Fetch sources and build complete closure evidence before merge**",
                "- [ ] **Step 6: Immediately refresh every live source and merge PR B**",
                "esaf-v04-qualified-closure-input.json",
                "New-QualifiedClosureEvidence $qualifiedInputsPath $closureHead",
            ),
            (
                "- [ ] **Step 6: Immediately refresh every live source and merge PR B**",
                "### Task 7:",
                "esaf-v04-qualified-prefetch-merge-input.json",
                "New-QualifiedClosureEvidence $qualifiedInputsPath $closureHead",
            ),
            (
                "- [ ] **Step 4: Create and push the annotated tag atomically after validation**",
                "- [ ] **Step 5: Resolve the remote annotated tag to the exact commit**",
                "esaf-v04-qualified-taggable-input.json",
                "New-QualifiedTaggableEvidence $qualifiedInputsPath $closureHead $closureMerge $postMergePath",
            ),
        )
        for start, end, input_name, consumer in sections:
            with self.subTest(input_name=input_name):
                block = plan[plan.index(start):plan.index(end)]
                producer = "Set-Content -LiteralPath $qualifiedInputsPath -Encoding utf8"
                self.assertIn(input_name, block)
                self.assertIn(producer, block)
                self.assertIn(consumer, block)
                self.assertLess(block.index(producer), block.index(consumer))
                self.assertIn("New-QualifiedInputFromSources", block)
                self.assertIn("ConvertFrom-Json", block)
                self.assertIn("gh api", block)
        self.assertGreaterEqual(plan.count("exactly three fixed qualified comment IDs"), 3)
        self.assertIn("$priorEvidence.mapping_decisions.source.comment_id", plan)
        self.assertIn("$baseEvidence.mapping_decisions.source.comment_id", plan)

    def test_qualified_evidence_builder_revalidates_produced_decisions(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        builder = plan[
            plan.index("function New-QualifiedClosureEvidence"):
            plan.index("function New-QualifiedTaggableEvidence")
        ]
        for required in (
            "$expectedMappingIds",
            "Qualified mapping decision decided_at shall be RFC3339",
            "Qualified mapping decisions shall contain exactly the three expected mapping-set IDs",
            "Qualified mapping decision source is incomplete",
        ):
            with self.subTest(required=required):
                self.assertIn(required, builder)

    def test_qualified_input_producer_emits_every_builder_decision_field(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        producer = plan[
            plan.index("function New-QualifiedInputFromSources"):
            plan.index("function New-QualifiedClosureEvidence")
        ]
        builder_required_fields = {
            "mapping_set_id": "$body.mapping_set_id",
            "decision_type": "decision_type='qualified_approval'",
            "sha": "$body.sha",
            "decided_at": "$body.decided_at",
            "reviewer": "$body.reviewer",
            "qualification": "$body.qualification",
            "disposition": "$body.disposition",
            "qualified_review_status": "$body.qualified_review_status",
            "url": "$body.url",
            "source": "comment_id=[long]$comment.id",
        }
        for field, value in builder_required_fields.items():
            with self.subTest(field=field):
                self.assertIn(field, producer)
                self.assertIn(value, producer)

    def test_qualified_acquisition_defines_native_guard_before_its_first_call(self) -> None:
        plan = read_repository_file(
            "docs/superpowers/plans/2026-07-21-v04-alpha-publication-gates.md"
        )
        acquisition = plan[
            plan.index("For \x60qualified_approval\x60, acquire the three reviewer decisions"):
            plan.index("- [ ] **Step 4: Push and open closure PR B")
        ]
        definition = "function Assert-NativeSuccess([string]$operation)"
        self.assertIn(definition, acquisition)
        self.assertLess(
            acquisition.index(definition),
            acquisition.index("Assert-NativeSuccess '"),
        )

    def test_repository_workflow_runs_release_and_link_validation(self) -> None:
        workflow = read_repository_file(".github/workflows/catalog-validation.yml")
        self.assertIn("python tools/release_gates.py --check", workflow)
        self.assertIn("python tools/validate_links.py --check", workflow)

    def test_workflow_path_filters_track_qualified_review_evidence_tools(self) -> None:
        """Changing any review-evidence tool must trigger repository validation."""
        workflow = read_repository_file(".github/workflows/catalog-validation.yml")
        pull_request = workflow.split("  pull_request:\n", 1)[1].split(
            "  push:\n", 1
        )[0]
        main_push = workflow.split("  push:\n", 1)[1].split(
            "  workflow_dispatch:", 1
        )[0]
        for path in (
            "tools/build_mapping_review_bundle.py",
            "tools/validate_qualified_review_evidence.py",
            "tools/seal_qualified_review_campaign.py",
            "tools/crosswalks/qualified_review_evidence.py",
        ):
            with self.subTest(event="pull_request", path=path):
                self.assertIn(path, pull_request)
            with self.subTest(event="push", path=path):
                self.assertIn(path, main_push)

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

    def test_release_plan_preserves_publication_boundaries(self) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md").casefold()
        boundaries = (
            "0.4-alpha publication",
            "publication gates are closed",
            "tag object",
            "peeled commit",
            "every mermaid diagram",
            "qualified contributors",
            "governance approval",
            "closes only `v0.4-alpha`",
            "cannot approve a later release",
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

    def test_release_publication_gates_are_closed(self) -> None:
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
        for gate, state, evidence in rows:
            with self.subTest(gate=gate):
                self.assertEqual("Closed", state)
                self.assertIn("https://", evidence)


if __name__ == "__main__":
    unittest.main()
