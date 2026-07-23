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
