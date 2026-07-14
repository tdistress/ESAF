import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
    if heading not in changelog:
        raise AssertionError(f"CHANGELOG.md must contain {heading!r}")
    section = changelog.split(heading, 1)[1]
    return section.split("\n## ", 1)[0]


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


class ReleaseMetadataTests(unittest.TestCase):
    def test_readme_badge_matches_current_version(self) -> None:
        version = current_version()
        readme = read_repository_file("README.md")
        badge_version = version.replace("-", "--")
        self.assertIn(
            f"/badge/version-{badge_version}-orange",
            readme,
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
        self.assertIn(f"## {version} - Unreleased", changelog)

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
            normalized_words(line)
            for line in backlog.splitlines()
            if re.match(r"^- Draft\b", line, re.IGNORECASE)
        ]
        for identifier, title in draft_architecture_patterns():
            with self.subTest(identifier=identifier):
                title_words = normalized_words(title).split()
                title_alias = " ".join(
                    title_words[:-1]
                    if title_words[-1] in {"deployment", "services"}
                    else title_words
                )
                queued = any(
                    normalized_words(identifier) in draft
                    or title_alias in draft
                    for draft in queued_drafts
                )
                self.assertFalse(
                    queued,
                    f"backlog still queues registered pattern {identifier} ({title})",
                )

    def test_backlog_preserves_cyber_essentials_plus_next_activity(self) -> None:
        backlog = read_repository_file("project/BACKLOG.md")
        self.assertIn(
            "Cyber Essentials Plus public-source acquisition and atomization design",
            backlog,
        )
        self.assertIn("separate, source-versioned", backlog)

    def test_release_plan_preserves_readiness_boundaries(self) -> None:
        release_plan = read_repository_file("project/RELEASE_PLAN.md")
        boundaries = (
            "exact candidate SHA",
            "every Mermaid diagram",
            "qualified contributors",
            "governance approval",
            "must not be tagged or represented as released",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, release_plan)


if __name__ == "__main__":
    unittest.main()
