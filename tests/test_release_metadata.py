import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BACKLOG_PATTERN_ALIASES = {
    "ARC-P140": ("private-model",),
    "ARC-P150": ("AI integration",),
}


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
            "reviewed candidate SHA",
            "resulting merged-main SHA",
            "every Mermaid diagram",
            "qualified contributors",
            "governance approval",
            "must not be tagged or represented as released",
        )
        for boundary in boundaries:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, release_plan)

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
