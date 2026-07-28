#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Callable

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
PINNED_RENDERER_VERSION = "11.16.0"
PINNED_NODE_VERSION = "22.23.1"
RENDER_CONFIG = Path("tools/mermaid-render-config.json")
RENDER_CONTRACT_SCHEMA = "esaf-mermaid-render-contract-v1"
RENDER_PROFILE = "esaf-mermaid-review-v1"
RENDER_CONTRACT_DOMAIN = b"ESAF-MERMAID-RENDER-CONTRACT-V1\0"
RENDER_OPTIONS = {
    "artifact_format": "png",
    "background": "white",
    "scale": 3,
}
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
    r"`(?P<contract_digest>[^`]+)` \| "
    r"`(?P<renderer>[^`]+)` \| `(?P<profile>[^`]+)` \| "
    r"(?P<visual_review>[^|]+) \| "
    r"(?P<reviewer>[^|]+) \|$"
)
V05_TABLE_HEADER = (
    "| Path | Block | Source SHA-256 | Render Contract SHA-256 | Renderer | "
    "Profile | Visual Review | Reviewer |"
)
V05_TABLE_SEPARATOR = "|---|---:|---|---|---|---|---|---|"
CONTRACT_SCHEMA_FIELD_RE = re.compile(
    r"^Render contract schema:\s*`(?P<value>[^`]+)`\s*$",
    re.MULTILINE,
)
RENDER_CONFIG_FIELD_RE = re.compile(
    r"^Render configuration:\s*`(?P<value>[^`]+)`\s*$",
    re.MULTILINE,
)
RENDER_CONFIG_DIGEST_FIELD_RE = re.compile(
    r"^Canonical render configuration SHA-256:\s*`(?P<value>[^`]+)`\s*$",
    re.MULTILINE,
)
NODE_FIELD_RE = re.compile(
    r"^Operational Node version:\s*`(?P<value>[^`]+)`\s*$",
    re.MULTILINE,
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


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _render_profile(root: Path) -> tuple[dict[str, object], str]:
    config_path = root / RENDER_CONFIG
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes.decode("utf-8"))
    if not isinstance(config, dict):
        raise ValueError("Mermaid render configuration shall be a JSON object")
    canonical_config = _canonical_json_bytes(config)
    config_digest = sha256(canonical_config).hexdigest()
    return (
        {
            "profile": RENDER_PROFILE,
            "renderer": PINNED_RENDERER,
            "node": PINNED_NODE_VERSION,
            "options": RENDER_OPTIONS,
            "mermaid_config": config,
        },
        config_digest,
    )


def render_contract_sha256(
    block: MermaidBlock,
    root: Path,
) -> str:
    profile, _ = _render_profile(root)
    payload = {
        "schema": RENDER_CONTRACT_SCHEMA,
        "path": block.path,
        "block": block.index,
        "diagram_type": block.diagram_type,
        "source": block.source,
        "source_sha256": block.digest,
        "render_profile": profile,
    }
    return sha256(
        RENDER_CONTRACT_DOMAIN + _canonical_json_bytes(payload)
    ).hexdigest()


def render_mermaid_blocks(
    blocks: list[MermaidBlock],
    root: Path,
) -> None:
    executable = shutil.which("mmdc")
    if executable is None:
        raise ValueError(
            f"{PINNED_RENDERER} is required on PATH for operational validation"
        )
    version = subprocess.run(
        [executable, "--version"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    if version != PINNED_RENDERER_VERSION:
        raise ValueError(
            "Mermaid renderer version shall equal "
            f"{PINNED_RENDERER_VERSION}; observed {version!r}"
        )
    with tempfile.TemporaryDirectory(prefix="esaf-mermaid-check-") as directory:
        output_root = Path(directory)
        inventory = write_render_inputs(blocks, output_root)
        rows = json.loads(inventory.read_text(encoding="utf-8"))
        for row in rows:
            input_path = output_root / row["input"]
            output_path = input_path.with_suffix(".png")
            result = subprocess.run(
                [
                    executable,
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--configFile",
                    str(root / RENDER_CONFIG),
                    "--backgroundColor",
                    RENDER_OPTIONS["background"],
                    "--scale",
                    str(RENDER_OPTIONS["scale"]),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if result.returncode != 0:
                raise ValueError(
                    f"{row['path']} block {row['index']} render failed: "
                    f"{result.stderr.strip() or result.stdout.strip()}"
                )
            if not output_path.is_file() or output_path.stat().st_size == 0:
                raise ValueError(
                    f"{row['path']} block {row['index']} render output is missing"
                )


def check_record(
    blocks: list[MermaidBlock],
    record: Path,
    expected_status: str = APPROVED_STATUS,
    *,
    renderer: Callable[[list[MermaidBlock], Path], None] = render_mermaid_blocks,
    repository_root: Path | None = None,
) -> list[str]:
    text = record.read_text(encoding="utf-8")
    root = (
        repository_root.resolve()
        if repository_root is not None
        else Path(__file__).resolve().parents[1]
    )
    structured_baseline = expected_status == V05_BASELINE_STATUS
    row_pattern = BASELINE_LEDGER_ROW_RE if structured_baseline else LEDGER_ROW_RE
    observed = []
    unparsed_rows = []
    for line in text.splitlines():
        match = row_pattern.match(line)
        if match:
            observed.append(match.groupdict())
        elif (
            structured_baseline
            and line.startswith("|")
            and line not in {V05_TABLE_HEADER, V05_TABLE_SEPARATOR}
        ):
            unparsed_rows.append(line)
    if structured_baseline:
        expected = [
            (
                block.path,
                str(block.index),
                block.digest,
                render_contract_sha256(block, root),
            )
            for block in blocks
        ]
        actual = [
            (
                row["path"],
                row["index"],
                row["digest"],
                row["contract_digest"],
            )
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
    if unparsed_rows:
        failures.append("ledger contains an unparsed table row")
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
    if structured_baseline:
        _, expected_config_digest = _render_profile(root)
        metadata = (
            (
                CONTRACT_SCHEMA_FIELD_RE,
                RENDER_CONTRACT_SCHEMA,
                "render contract schema is invalid",
            ),
            (
                RENDER_CONFIG_FIELD_RE,
                RENDER_CONFIG.as_posix(),
                "render configuration path is invalid",
            ),
            (
                RENDER_CONFIG_DIGEST_FIELD_RE,
                expected_config_digest,
                "render configuration digest does not match",
            ),
            (
                NODE_FIELD_RE,
                PINNED_NODE_VERSION,
                "operational Node version is invalid",
            ),
        )
        for pattern, expected_value, diagnostic in metadata:
            values = [
                match.group("value")
                for match in pattern.finditer(text)
            ]
            if values != [expected_value]:
                failures.append(diagnostic)
    if actual != expected:
        if structured_baseline and any(
            row[:3] == expected_row[:3] and row[3] != expected_row[3]
            for row, expected_row in zip(actual, expected)
        ):
            failures.append("render contract digest does not match")
        failures.append(
            "ledger rows do not exactly match the current Mermaid inventory"
        )
    for row in observed:
        if structured_baseline:
            if (
                row["renderer"].strip() != PINNED_RENDERER
                or row["profile"].strip() != RENDER_PROFILE
                or row["visual_review"].strip() != "Pass"
                or not re.fullmatch(r"[0-9a-f]{64}", row["contract_digest"])
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
    if structured_baseline:
        try:
            renderer(blocks, root)
        except (
            OSError,
            ValueError,
            subprocess.CalledProcessError,
            json.JSONDecodeError,
        ) as exc:
            failures.append(f"operational Mermaid rendering failed: {exc}")
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
        supplied_record = str(args.check_record)
        registered = [
            (relative, status)
            for relative, status in RELEASE_LEDGERS.items()
            if supplied_record
            in {
                relative.as_posix(),
                str(relative),
                str((root / relative).resolve()),
            }
        ]
        if len(registered) != 1:
            print(
                "--check-record requires the exact tracked release ledger using "
                "a canonical registered release ledger path",
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
            repository_root=root,
        )
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print(f"Validated {len(blocks)} Mermaid ledger rows in {args.check_record.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
