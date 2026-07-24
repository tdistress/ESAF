from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
GENERATOR_VERSION = "1.0.0"


@dataclass(frozen=True)
class MappingProfile:
    mapping_set_id: str
    snapshot_path: str
    label: str
    direction: str
    expected_count: int


_PROFILE_ROWS = (
    (
        "uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0",
        "Core",
        "external_to_esaf",
        116,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.1.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.1.0",
        "Plus forward",
        "esaf_to_external",
        144,
    ),
    (
        "uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0",
        "crosswalks/mappings/uk-ncsc/cyber-essentials-plus-test-specification/3.2/0.4-alpha/0.2.0",
        "Plus reverse",
        "external_to_esaf",
        144,
    ),
)
PROFILES = {row[0]: MappingProfile(*row) for row in _PROFILE_ROWS}


class GitReader:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def _run(
        self,
        *arguments: str,
        text: bool = False,
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=text,
        )

    def resolve_commit(self, revision: str) -> str:
        if not FULL_SHA.fullmatch(revision):
            raise ValueError(
                "candidate must be a full lowercase 40-character Git SHA"
            )
        try:
            resolved = self._run(
                "rev-parse",
                "--verify",
                f"{revision}^{{commit}}",
                text=True,
            ).stdout.strip()
        except subprocess.CalledProcessError as error:
            raise ValueError("candidate is not an available commit") from error
        if resolved != revision:
            raise ValueError("candidate does not resolve to the exact commit")
        return resolved

    def read_bytes(self, commit: str, path: str) -> bytes:
        if path.startswith("/") or ".." in Path(path).parts or "\\" in path:
            raise ValueError(f"unsafe repository path: {path}")
        try:
            return self._run("show", f"{commit}:{path}").stdout
        except subprocess.CalledProcessError as error:
            raise ValueError(
                f"missing tracked file at candidate: {path}"
            ) from error

    def list_files(self, commit: str, path: str) -> tuple[str, ...]:
        result = self._run(
            "ls-tree",
            "-r",
            "--name-only",
            "-z",
            commit,
            "--",
            path,
        ).stdout
        names = tuple(item.decode("utf-8") for item in result.split(b"\0") if item)
        return tuple(sorted(names))

    def worktree_roots(self) -> tuple[Path, ...]:
        output = self._run("worktree", "list", "--porcelain", "-z").stdout
        roots = []
        for field in output.split(b"\0"):
            if field.startswith(b"worktree "):
                roots.append(Path(field[9:].decode("utf-8")).resolve())
        return tuple(roots)
