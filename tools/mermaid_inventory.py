#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

MERMAID_RE = re.compile(r"```mermaid\r?\n(.*?)\r?\n```", re.DOTALL)
V04_RELEASE_LEDGER = Path(
    "docs/superpowers/reviews/2026-07-21-v04-alpha-mermaid-rendering.md"
)
V05_RELEASE_LEDGER = Path(
    "docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md"
)
APPROVED_STATUS = "Approved on candidate content; pending final exact-head recheck"
V05_BASELINE_STATUS = (
    "Baseline renderer capability verified; not closure candidate approval"
)
RELEASE_LEDGERS = {
    V04_RELEASE_LEDGER: APPROVED_STATUS,
    V05_RELEASE_LEDGER: V05_BASELINE_STATUS,
}
PINNED_RENDERER = "@mermaid-js/mermaid-cli@11.16.0"
STATUS_FIELD_RE = re.compile(r"^Status:\s*(?P<value>.*?)\s*$", re.MULTILINE)
RENDERER_FIELD_RE = re.compile(
    r"^Renderer version:\s*`(?P<value>[^`]+)`\s*$", re.MULTILINE
)
PLACEHOLDER_REVIEWERS = {"", "pending", "tbd", "todo", "unknown", "n/a", "na", "reviewer"}
GENERIC_REVIEWER_RE = re.compile(
    r"^(?:(?:independent|lead|senior|technical|editorial|renderer|rendering|publication|evidence)\s+)*"
    r"reviewer(?:\s+\d+)?$"
)
LEDGER_ROW_RE = re.compile(
    r"^\| `(?P<path>[^`]+)` \| (?P<index>\d+) \| `(?P<digest>[0-9a-f]{64})` \| "
    r"(?P<diagram_type>[^|]+) \| (?P<render>[^|]+) \| (?P<readability>[^|]+) \| "
    r"(?P<reviewer>[^|]+) \|$"
)
BASELINE_LEDGER_ROW_RE = re.compile(
    r"^\| `(?P<path>[^`]+)` \| (?P<index>\d+) \| "
    r"`(?P<digest>[0-9a-f]{64})` \| "
    r"`(?P<output_digest>[^`]+)` \| "
    r"`(?P<renderer>[^`]+)` \| (?P<result>[^|]+) \| "
    r"(?P<reviewer>[^|]+) \|$"
)


@dataclass(frozen=True)
class MermaidBlock:
    path: str
    index: int
    digest: str
    diagram_type: str
    source: str


def extract_blocks(text: str) -> list[str]:
    return [match.group(1).replace("\r\n", "\n") for match in MERMAID_RE.finditer(text)]


def diagram_type(source: str) -> str:
    for line in source.splitlines():
        candidate = line.strip()
        if candidate and not candidate.startswith("%%"):
            return candidate.split(maxsplit=1)[0]
    raise ValueError("Mermaid block does not declare a diagram type")


def tracked_markdown(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--", "*.md"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return sorted(result.stdout.splitlines())


def discover(root: Path) -> list[MermaidBlock]:
    blocks: list[MermaidBlock] = []
    for relative in tracked_markdown(root):
        text = (root / relative).read_text(encoding="utf-8")
        for index, source in enumerate(extract_blocks(text), start=1):
            blocks.append(
                MermaidBlock(
                    relative.replace("\\", "/"),
                    index,
                    sha256(source.encode("utf-8")).hexdigest(),
                    diagram_type(source),
                    source,
                )
            )
    return blocks


def write_render_inputs(blocks: list[MermaidBlock], output_dir: Path) -> Path:
    output_dir = output_dir.resolve()
    root = Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
    ).resolve()
    if output_dir == root or output_dir.is_relative_to(root):
        raise ValueError("renderer output shall be outside the repository")
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if not output_dir.is_relative_to(temporary_root):
        raise ValueError("renderer output shall be beneath the system temporary directory")
    if output_dir.exists() and (not output_dir.is_dir() or any(output_dir.iterdir())):
        raise ValueError("renderer output directory shall be empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for ordinal, block in enumerate(blocks, start=1):
        name = f"{ordinal:03d}-{Path(block.path).stem}-{block.index}.mmd"
        (output_dir / name).write_text(block.source + "\n", encoding="utf-8", newline="\n")
        rows.append({**asdict(block), "source": None, "input": name})
    inventory = output_dir / "inventory.json"
    inventory.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8", newline="\n")
    return inventory


def ledger_rows(blocks: list[MermaidBlock]) -> str:
    return "\n".join(
        f"| `{block.path}` | {block.index} | `{block.digest}` | {block.diagram_type} | "
        "Pending | Pending | Pending |"
        for block in blocks
    )


def check_record(
    blocks: list[MermaidBlock],
    record: Path,
    expected_status: str = APPROVED_STATUS,
) -> list[str]:
    text = record.read_text(encoding="utf-8")
    structured_baseline = expected_status == V05_BASELINE_STATUS
    row_pattern = BASELINE_LEDGER_ROW_RE if structured_baseline else LEDGER_ROW_RE
    observed = []
    for line in text.splitlines():
        match = row_pattern.match(line)
        if match:
            observed.append(match.groupdict())
    if structured_baseline:
        expected = [
            (block.path, str(block.index), block.digest)
            for block in blocks
        ]
        actual = [
            (row["path"], row["index"], row["digest"])
            for row in observed
        ]
    else:
        expected = [
            (block.path, str(block.index), block.digest, block.diagram_type)
            for block in blocks
        ]
        actual = [
            (
                row["path"],
                row["index"],
                row["digest"],
                row["diagram_type"].strip(),
            )
            for row in observed
        ]
    failures = []
    statuses = [match.group("value") for match in STATUS_FIELD_RE.finditer(text)]
    if statuses != [expected_status]:
        failures.append(
            "ledger status does not match registered release ledger"
            if structured_baseline
            else "ledger status is not approved on candidate content"
        )
    renderers = [match.group("value") for match in RENDERER_FIELD_RE.finditer(text)]
    if renderers != [PINNED_RENDERER]:
        failures.append("renderer version is not pinned to the publication candidate")
    if actual != expected:
        failures.append("ledger rows do not exactly match the current Mermaid inventory")
    for row in observed:
        if structured_baseline:
            if (
                row["renderer"].strip() != PINNED_RENDERER
                or row["result"].strip() != "Pass"
                or not re.fullmatch(r"[0-9a-f]{64}", row["output_digest"])
            ):
                failures.append(
                    f"{row['path']} block {row['index']} structured render "
                    "evidence is incomplete"
                )
        elif (
            row["render"].strip() != "Pass"
            or row["readability"].strip() != "Pass"
        ):
            failures.append(f"{row['path']} block {row['index']} is not fully reviewed")
        reviewer = " ".join(row["reviewer"].split()).casefold()
        if reviewer in PLACEHOLDER_REVIEWERS or GENERIC_REVIEWER_RE.fullmatch(reviewer):
            failures.append(f"{row['path']} block {row['index']} reviewer identity is missing")
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory tracked Markdown Mermaid blocks.")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--write", action="store_true", help="write renderer inputs")
    parser.add_argument("--check-record", type=Path, help="validate a rendering ledger")
    parser.add_argument("--record-template", action="store_true", help="print Pending ledger rows")
    args = parser.parse_args(argv)
    if args.write and args.output_dir is None:
        parser.error("--write requires --output-dir")
    if args.output_dir is not None and not args.write:
        parser.error("--output-dir requires --write")
    if not (args.write or args.check_record or args.record_template):
        parser.error("one of --write, --check-record, or --record-template is required")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(__file__).resolve().parents[1]
    expected_status = None
    if args.check_record:
        resolved_record = args.check_record.resolve()
        registered = [
            (relative, status)
            for relative, status in RELEASE_LEDGERS.items()
            if (root / relative).resolve() == resolved_record
        ]
        if len(registered) != 1:
            print(
                "--check-record requires the exact tracked release ledger or "
                "another registered release ledger",
                file=sys.stderr,
            )
            return 2
        relative_record, expected_status = registered[0]
        if relative_record.as_posix() not in tracked_markdown(root):
            raise ValueError("the exact tracked release ledger is unavailable")
    blocks = discover(root)
    if args.record_template:
        print(ledger_rows(blocks))
    if args.write:
        output_dir = args.output_dir.resolve()
        inventory = write_render_inputs(blocks, output_dir)
        print(f"Wrote {len(blocks)} Mermaid blocks to {inventory.parent}")
    if args.check_record:
        failures = check_record(
            blocks,
            args.check_record,
            expected_status=expected_status,
        )
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print(f"Validated {len(blocks)} Mermaid ledger rows in {args.check_record.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
