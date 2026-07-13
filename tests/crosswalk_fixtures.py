"""Reusable repository fixtures for crosswalk validation tests."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import yaml

from tools.crosswalks.digests import event_digest, snapshot_digest
from tools.crosswalks.io import parse_front_matter


MAPPING_SET_ID = "nist--ai-rmf--1.0--esaf-0.4-alpha--1.0.0"


def valid_event(**overrides: str) -> dict[str, str]:
    """Return a lifecycle event before its event digest is attached."""
    event = {
        "event_id": "approved-1",
        "state": "approved",
        "date": "2026-07-13",
        "actor": "approver-1",
        "reason": "Approved after independent review.",
        "predecessor_id": "",
        "successor_id": "",
        "approval_reference": "APR-001",
        "previous_event_digest": "0" * 64,
    }
    event.update(overrides)
    return event


class CrosswalkFixture:
    """Build minimal crosswalk repository snapshots beneath a temporary root."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.snapshot: Path | None = None
        self.control_commit: str | None = None
        self.commit_valid_control_catalog()

    def _git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    def commit_valid_control_catalog(self, release: str = "0.4-alpha") -> str:
        if not (self.root / ".git").exists():
            self.root.mkdir(parents=True, exist_ok=True)
            self._git("init", "--quiet")
            self._git("config", "user.email", "fixture@example.com")
            self._git("config", "user.name", "Crosswalk Fixture")
        iam_path = self.root / "controls" / "IAM" / "IAM-100.md"
        iam_path.parent.mkdir(parents=True, exist_ok=True)
        iam_path.write_bytes(
            b"---\r\nid: IAM-100\r\nstatus: draft\r\nversion: 1.0.0\r\n---"
            b"\r\n\r\n# IAM-100 caf\xc3\xa9"
        )
        zzz_path = self.root / "controls" / "ZZZ" / "ZZZ-100.md"
        zzz_path.parent.mkdir(parents=True, exist_ok=True)
        zzz_path.write_bytes(
            b"---\nid: ZZZ-100\nstatus: draft\nversion: 2.0.0\n---\n\n# ZZZ-100\n"
        )
        catalog_controls = [
            {
                "id": "ZZZ-100",
                "version": "2.0.0",
                "status": "draft",
                "path": "ZZZ/ZZZ-100.md",
            },
            {
                "id": "IAM-100",
                "version": "1.0.0",
                "status": "draft",
                "path": "IAM/IAM-100.md",
            },
        ]
        catalog = {
            "schema_version": "1.0.0",
            "control_count": len(catalog_controls),
            "controls": catalog_controls,
        }
        (self.root / "controls" / "catalog.json").write_text(
            json.dumps(catalog, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        (self.root / "VERSION.md").write_text(
            f"# ESAF Version\n\nCurrent Version: **{release}**\n",
            encoding="utf-8",
            newline="\n",
        )
        self._git("add", "VERSION.md", "controls")
        self._git(
            "commit", "--quiet", "--allow-empty", "-m", f"Fixture controls {release}"
        )
        self.control_commit = self._git("rev-parse", "HEAD")
        return self.control_commit

    def commit_version_document(self, text: str) -> str:
        (self.root / "VERSION.md").write_text(
            text, encoding="utf-8", newline="\n"
        )
        self._git("add", "VERSION.md")
        self._git("commit", "--quiet", "-m", "Mutate fixture version")
        self.control_commit = self._git("rev-parse", "HEAD")
        return self.control_commit

    def dangling_control_commit(self) -> str:
        return self._git("commit-tree", "HEAD^{tree}", "-m", "Dangling controls")

    def reset_repository(self) -> None:
        if self.control_commit is None:
            raise RuntimeError("fixture control commit is unavailable")
        self._git("reset", "--hard", self.control_commit)
        for tag in self._git("tag", "--list").splitlines():
            if tag:
                self._git("tag", "--delete", tag)
        self.reset_crosswalks()
        self.snapshot = None

    def reset_crosswalks(self) -> None:
        shutil.rmtree(self.root / "crosswalks" / "mappings", ignore_errors=True)
        shutil.rmtree(self.root / "crosswalks" / "registry", ignore_errors=True)

    def write_front_matter(
        self, relative: str, metadata: dict[str, object], body: str
    ) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        yaml_text = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True)
        path.write_text(f"---\n{yaml_text}---\n{body}", encoding="utf-8", newline="\n")
        return path

    def create_valid_snapshot(
        self,
        status: str = "draft",
        complete: bool = True,
        scope_type: str = "complete_publication",
        dispositions: tuple[str, ...] = ("mapped",),
        with_lifecycle: bool = True,
    ) -> Path:
        commit = self.control_commit or self.commit_valid_control_catalog()
        catalog_bytes = subprocess.run(
            ["git", "-C", str(self.root), "show", f"{commit}:controls/catalog.json"],
            check=True,
            capture_output=True,
        ).stdout
        catalog = json.loads(catalog_bytes)
        controls = []
        for control in catalog["controls"]:
            record_bytes = subprocess.run(
                ["git", "-C", str(self.root), "show", f"{commit}:controls/{control['path']}"],
                check=True,
                capture_output=True,
            ).stdout
            controls.append(
                {
                    "id": control["id"],
                    "version": control["version"],
                    "status": control["status"],
                    "path": control["path"],
                    "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
                }
            )
        controls.sort(key=lambda control: str(control["id"]))
        catalog_digest = hashlib.sha256(catalog_bytes).hexdigest()
        snapshot = (
            self.root
            / "crosswalks"
            / "mappings"
            / "nist"
            / "1.0"
            / "0.4-alpha"
            / "1.0.0"
        )
        snapshot.mkdir(parents=True, exist_ok=True)
        self.snapshot = snapshot

        provision_count = len(dispositions) if complete else 2
        provision_ids = [f"EXT-{index}" for index in range(1, provision_count + 1)]
        mapping_set = self._mapping_set(
            status, scope_type, provision_count, commit, catalog_digest
        )
        inventory = {
            "schema_version": "1.0.0",
            "mapping_set_id": MAPPING_SET_ID,
            "scope_type": scope_type,
            "scope_statement": "All declared normative requirements.",
            "source_basis": "Official publication structure.",
            "expected_count": provision_count,
            "provision_ids": provision_ids,
        }
        self.write_front_matter(
            snapshot.relative_to(self.root).as_posix() + "/README.md",
            mapping_set,
            "# Mapping set\n",
        )
        self.write_front_matter(
            snapshot.relative_to(self.root).as_posix() + "/PROVISION_INVENTORY.md",
            inventory,
            "# Provision inventory\n",
        )
        manifest = {
            "schema_version": "1.0.0",
            "esaf_release": "0.4-alpha",
            "source_commit_sha": commit,
            "control_catalog_sha256": catalog_digest,
            "controls": controls,
        }
        (snapshot / "ESAF_CONTROL_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )

        record_status = "draft" if status == "draft" else "reviewed"
        record_dispositions = dispositions if complete else dispositions[:1]
        for index, disposition in enumerate(record_dispositions, 1):
            self.add_record(
                snapshot,
                external_provision_id=f"EXT-{index}",
                record_id=f"ext-{index}",
                status=record_status,
                disposition=disposition,
            )
        if with_lifecycle:
            event = valid_event()
            self._omit_empty_optional_event_fields(event)
            event["event_digest"] = event_digest(event)
            self._write_lifecycle(
                MAPPING_SET_ID,
                snapshot_digest(self.root, snapshot),
                [event],
            )
        return snapshot

    def create_approved_snapshot_with_lifecycle(self, final_state: str) -> Path:
        """Create an approved snapshot and a valid lifecycle chain."""
        snapshot = self.create_valid_snapshot(status="approved", complete=True)
        states = ("approved", "published", "deprecated", "retired")
        events: list[dict[str, str]] = []
        for state in states[: states.index(final_state) + 1]:
            previous = events[-1]["event_digest"] if events else "0" * 64
            event = valid_event(
                event_id=f"{state}-1",
                state=state,
                reason=f"Mapping set {state}.",
                previous_event_digest=previous,
                approval_reference="APR-001" if state == "approved" else "",
                successor_id=(
                    "nist--ai-rmf--1.0--esaf-0.4-alpha--1.0.1"
                    if state == "deprecated"
                    else ""
                ),
            )
            self._omit_empty_optional_event_fields(event)
            event["event_digest"] = event_digest(event)
            events.append(event)
        self._write_lifecycle(MAPPING_SET_ID, snapshot_digest(self.root, snapshot), events)
        return snapshot

    def commit_approved_snapshot(self) -> str:
        self.create_approved_snapshot_with_lifecycle("approved")
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Approved snapshot baseline")
        return self._git("rev-parse", "HEAD")

    def commit_approved_snapshot_with_lifecycle(self) -> str:
        self.create_approved_snapshot_with_lifecycle("approved")
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Approved lifecycle baseline")
        return self._git("rev-parse", "HEAD")

    def commit_unhashable_lifecycle_mapping_set_id(self) -> str:
        self.create_approved_snapshot_with_lifecycle("approved")
        self.set_unhashable_lifecycle_mapping_set_id()
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Malformed lifecycle baseline")
        return self._git("rev-parse", "HEAD")

    def commit_malformed_lifecycle_yaml(self) -> str:
        self.create_approved_snapshot_with_lifecycle("approved")
        lifecycle = self.root / "crosswalks" / "registry" / f"{MAPPING_SET_ID}.md"
        lifecycle.write_bytes(b"---\nmapping_set_id: [\n---\n# Broken lifecycle\n")
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Unparseable lifecycle baseline")
        return self._git("rev-parse", "HEAD")

    def commit_lifecycle_missing_closing_delimiter(self) -> str:
        self.create_approved_snapshot_with_lifecycle("approved")
        lifecycle = self.root / "crosswalks" / "registry" / f"{MAPPING_SET_ID}.md"
        valid = lifecycle.read_bytes()
        lifecycle.write_bytes(self._without_closing_delimiter(valid))
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Unclosed lifecycle baseline")
        baseline = self._git("rev-parse", "HEAD")
        lifecycle.write_bytes(valid)
        return baseline

    def commit_lifecycle_with_empty_events(self) -> str:
        self.create_approved_snapshot_with_lifecycle("approved")
        lifecycle = self.root / "crosswalks" / "registry" / f"{MAPPING_SET_ID}.md"
        valid = lifecycle.read_bytes()
        metadata, body = parse_front_matter(lifecycle)
        metadata["events"] = []
        self.write_front_matter(
            lifecycle.relative_to(self.root).as_posix(), metadata, body
        )
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Empty-event lifecycle baseline")
        baseline = self._git("rev-parse", "HEAD")
        lifecycle.write_bytes(valid)
        return baseline

    def commit_snapshot_readme_missing_closing_delimiter(self) -> str:
        snapshot = self.create_approved_snapshot_with_lifecycle("approved")
        readme = snapshot / "README.md"
        valid = readme.read_bytes()
        readme.write_bytes(self._without_closing_delimiter(valid))
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Unclosed snapshot baseline")
        baseline = self._git("rev-parse", "HEAD")
        readme.write_bytes(valid)
        return baseline

    def commit_schema_invalid_snapshot_readme(self) -> str:
        snapshot = self.create_approved_snapshot_with_lifecycle("approved")
        readme = snapshot / "README.md"
        valid = readme.read_bytes()
        metadata, body = parse_front_matter(readme)
        metadata["schema_version"] = "invalid"
        self.write_front_matter(readme.relative_to(self.root).as_posix(), metadata, body)
        self._git("add", "crosswalks")
        self._git("commit", "--quiet", "-m", "Schema-invalid snapshot baseline")
        baseline = self._git("rev-parse", "HEAD")
        readme.write_bytes(valid)
        return baseline

    def commit_malformed_snapshot_readme(self, mutation: str) -> str:
        snapshot = self.create_approved_snapshot_with_lifecycle("approved")
        readme = snapshot / "README.md"
        raw = readme.read_bytes()
        mutations = {
            "invalid_utf8": b"\xff",
            "bom": b"\xef\xbb\xbf" + raw,
            "crlf": raw.replace(b"\n", b"\r\n"),
            "missing_front_matter": b"# Missing front matter\n",
        }
        malformed = mutations[mutation]
        readme.write_bytes(malformed)
        self._git("add", "crosswalks")
        blob = subprocess.run(
            ["git", "-C", str(self.root), "hash-object", "-w", "--stdin"],
            input=malformed,
            check=True,
            capture_output=True,
        ).stdout.decode("ascii").strip()
        self._git(
            "update-index",
            "--cacheinfo",
            "100644",
            blob,
            readme.relative_to(self.root).as_posix(),
        )
        self._git("commit", "--quiet", "-m", f"Malformed snapshot baseline {mutation}")
        return self._git("rev-parse", "HEAD")

    @staticmethod
    def _without_closing_delimiter(raw: bytes) -> bytes:
        delimiter = b"---\n"
        closing = raw.find(delimiter, len(delimiter))
        if closing < 0:
            raise ValueError("fixture front matter has no closing delimiter")
        return raw[:closing] + raw[closing + len(delimiter) :]

    def mutate_approved_record(self) -> None:
        path = self._record()
        path.write_bytes(path.read_bytes() + b"\nApproved content was rewritten.\n")

    def rewrite_snapshot_and_registry_digest(self) -> None:
        self.mutate_approved_record()
        lifecycle = self._lifecycle()
        lifecycle["snapshot_digest"] = snapshot_digest(self.root, self._snapshot())
        self._write_lifecycle_metadata(lifecycle)

    def rewrite_prior_event_and_rehash_chain(self) -> None:
        lifecycle = self._lifecycle()
        events = lifecycle["events"]
        events[0]["reason"] = "Rewritten approval reason."
        events[0]["event_digest"] = event_digest(events[0])
        self._write_lifecycle_metadata(lifecycle)

    def reorder_lifecycle_events(self) -> None:
        self._append_lifecycle_state("published")
        lifecycle = self._lifecycle()
        lifecycle["events"] = list(reversed(lifecycle["events"]))
        self._write_lifecycle_metadata(lifecycle)

    def duplicate_lifecycle_event(self) -> None:
        lifecycle = self._lifecycle()
        duplicate = dict(lifecycle["events"][0])
        duplicate["previous_event_digest"] = lifecycle["events"][-1]["event_digest"]
        duplicate["event_digest"] = event_digest(duplicate)
        lifecycle["events"].append(duplicate)
        self._write_lifecycle_metadata(lifecycle)

    def skip_published_transition(self) -> None:
        self._append_lifecycle_state(
            "deprecated",
            successor_id="nist--ai-rmf--1.0--esaf-0.4-alpha--1.0.1",
        )

    def publish_unapproved_snapshot(self) -> None:
        self._mutate_mapping_set(lambda value: value.__setitem__("status", "reviewed"))
        self._append_lifecycle_state("published")

    def publish_second_active_version(self) -> None:
        self._append_lifecycle_state("published")
        source = self._snapshot()
        target = source.parent / "1.0.1"
        shutil.copytree(source, target)
        second_id = "nist--ai-rmf--1.0--esaf-0.4-alpha--1.0.1"
        for name in ("README.md", "PROVISION_INVENTORY.md", "ext-1.md"):
            path = target / name
            metadata, body = parse_front_matter(path)
            metadata["mapping_set_id"] = second_id
            if name == "README.md":
                metadata["mapping_set_version"] = "1.0.1"
            self.write_front_matter(path.relative_to(self.root).as_posix(), metadata, body)
        events: list[dict[str, str]] = []
        for state in ("approved", "published"):
            event = valid_event(
                event_id=f"{state}-2",
                state=state,
                reason=f"Second mapping set {state}.",
                approval_reference="APR-002" if state == "approved" else "",
                previous_event_digest=(events[-1]["event_digest"] if events else "0" * 64),
            )
            self._omit_empty_optional_event_fields(event)
            event["event_digest"] = event_digest(event)
            events.append(event)
        self._write_lifecycle(second_id, snapshot_digest(self.root, target), events)

    def deprecate_without_successor_or_explanation(self) -> None:
        self._append_lifecycle_state("published")
        self._append_lifecycle_state("deprecated", reason="", successor_id="")

    def set_stale_snapshot_digest(self) -> None:
        lifecycle = self._lifecycle()
        lifecycle["snapshot_digest"] = "0" * 64
        self._write_lifecycle_metadata(lifecycle)

    def refresh_lifecycle_snapshot_digest(self) -> None:
        lifecycle = self._lifecycle()
        lifecycle["snapshot_digest"] = snapshot_digest(self.root, self._snapshot())
        self._write_lifecycle_metadata(lifecycle)

    def set_unhashable_lifecycle_event_id(self) -> None:
        self._mutate_lifecycle(
            lambda value: value["events"][0].__setitem__("event_id", [])
        )

    def set_unhashable_lifecycle_mapping_set_id(self) -> None:
        self._mutate_lifecycle(
            lambda value: value.__setitem__("mapping_set_id", [])
        )

    def _append_lifecycle_state(self, state: str, **overrides: str) -> None:
        lifecycle = self._lifecycle()
        events = lifecycle["events"]
        values = {
            "event_id": f"{state}-{len(events) + 1}",
            "state": state,
            "reason": f"Mapping set {state}.",
            "approval_reference": "",
            "previous_event_digest": events[-1]["event_digest"],
        }
        values.update(overrides)
        event = valid_event(**values)
        self._omit_empty_optional_event_fields(event)
        event["event_digest"] = event_digest(event)
        events.append(event)
        self._write_lifecycle_metadata(lifecycle)

    def _write_lifecycle(
        self, mapping_set_id: str, digest: str, events: list[dict[str, str]]
    ) -> None:
        self.write_front_matter(
            f"crosswalks/registry/{mapping_set_id}.md",
            {
                "schema_version": "1.0.0",
                "mapping_set_id": mapping_set_id,
                "snapshot_digest": digest,
                "events": events,
            },
            "# Lifecycle record\n",
        )

    @staticmethod
    def _omit_empty_optional_event_fields(event: dict[str, str]) -> None:
        for field in ("predecessor_id", "successor_id", "approval_reference"):
            if not event.get(field):
                event.pop(field, None)

    def _lifecycle(self) -> dict[str, object]:
        metadata, _ = parse_front_matter(
            self.root / "crosswalks" / "registry" / f"{MAPPING_SET_ID}.md"
        )
        return metadata

    def _write_lifecycle_metadata(self, metadata: dict[str, object]) -> None:
        mapping_set_id = str(metadata["mapping_set_id"])
        self.write_front_matter(
            f"crosswalks/registry/{mapping_set_id}.md",
            metadata,
            "# Lifecycle record\n",
        )

    def _mutate_lifecycle(self, mutation: object) -> None:
        metadata = self._lifecycle()
        mutation(metadata)  # type: ignore[operator]
        self.write_front_matter(
            f"crosswalks/registry/{MAPPING_SET_ID}.md",
            metadata,
            "# Lifecycle record\n",
        )

    def add_record(
        self,
        snapshot: Path,
        external_provision_id: str,
        record_id: str,
        status: str = "draft",
        disposition: str = "mapped",
    ) -> Path:
        record: dict[str, object] = {
            "schema_version": "1.0.0",
            "record_id": record_id,
            "mapping_set_id": MAPPING_SET_ID,
            "status": status,
            "external_provision_id": external_provision_id,
            "granularity": "requirement",
            "context": {
                "mode": "paraphrase",
                "summary": f"A summary of {external_provision_id}.",
            },
            "source_locator": {
                "official_url": f"https://example.com/standard#{record_id}",
                "locator": external_provision_id,
            },
            "disposition": disposition,
            "relationships": [self._relationship()] if disposition == "mapped" else [],
            "mapper": {"id": "mapper-1", "date": "2026-07-13"},
            "change_history": [
                {"version": "1.0.0", "date": "2026-07-13", "change": "Initial version"}
            ],
        }
        if disposition != "mapped":
            record["negative_rationale"] = "No direct relationship was identified."
        if status == "reviewed":
            record["reviewer"] = self._reviewer()
        relative = snapshot.relative_to(self.root).as_posix() + f"/{record_id}.md"
        return self.write_front_matter(relative, record, f"# {external_provision_id}\n")

    @staticmethod
    def _reviewer() -> dict[str, object]:
        return {
            "id": "reviewer-1",
            "qualification": "Independent subject-matter reviewer",
            "date": "2026-07-13",
            "authorized_source_access": True,
            "findings_disposition": "All findings resolved",
        }

    @staticmethod
    def _relationship() -> dict[str, object]:
        return {
            "esaf_control_id": "IAM-100",
            "esaf_control_version": "1.0.0",
            "relationship": "supports",
            "direction": "external_to_esaf",
            "coverage": "partial",
            "confidence": "high",
            "rationale": "The outcomes overlap.",
            "conditions": ["The declared scope applies."],
            "expected_evidence": ["Approved assessment record"],
            "known_gaps": ["Implementation remains organization-specific."],
        }

    def _mapping_set(
        self,
        status: str,
        scope_type: str,
        inventory_count: int,
        commit: str,
        catalog_digest: str,
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "schema_version": "1.0.0",
            "mapping_set_id": MAPPING_SET_ID,
            "authority": {"id": "nist", "name": "NIST"},
            "publication": {"id": "ai-rmf", "name": "AI Risk Management Framework"},
            "source_version": {"id": "1.0", "label": "1.0"},
            "esaf_release": {
                "id": "0.4-alpha",
                "label": "ESAF 0.4-alpha",
                "source_commit_sha": commit,
                "control_catalog_sha256": catalog_digest,
                "control_manifest_path": "ESAF_CONTROL_MANIFEST.json",
            },
            "mapping_set_version": "1.0.0",
            "status": status,
            "source": {
                "official_url": "https://example.com/standard",
                "publication_date": "2023-01-26",
                "access_class": "public",
                "licensing_note": "Public source; derivative analysis only.",
            },
            "publication_rights": {
                "basis": "Documented publication review",
                "permitted_elements": ["identifiers", "paraphrases"],
                "prohibited_elements": ["titles"],
                "restrictions": "No verbatim requirements.",
                "approved": True,
                "reviewer_id": "rights-reviewer",
                "review_date": "2026-07-13",
            },
            "scope": {
                "type": scope_type,
                "statement": "All declared normative requirements.",
                "inventory_count": inventory_count,
                "default_granularity": "requirement",
            },
            "mapper": {
                "id": "mapper-1",
                "qualification": "Qualified mapper",
                "date": "2026-07-13",
                "authorized_source_access": True,
            },
            "findings": [],
            "change_history": [
                {"version": "1.0.0", "date": "2026-07-13", "change": "Initial version"}
            ],
        }
        if status in {"reviewed", "approved"}:
            value["reviewer"] = self._reviewer()
        if status == "approved":
            value["approver"] = {"id": "approver-1", "date": "2026-07-13"}
        return value

    def mutate_control_after_snapshot(self, snapshot: Path) -> None:
        path = self.root / "controls" / "IAM" / "IAM-100.md"
        path.write_bytes(path.read_bytes() + b"\nCurrent-tree substitution.\n")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self._mutate_manifest(
            lambda value: value["controls"][0].__setitem__("record_sha256", digest)
        )

    def set_unreachable_commit(self) -> None:
        unreachable = "f" * 40
        self._mutate_mapping_set(
            lambda value: value["esaf_release"].__setitem__("source_commit_sha", unreachable)  # type: ignore[union-attr]
        )
        self._mutate_manifest(
            lambda value: value.__setitem__("source_commit_sha", unreachable)
        )

    def set_wrong_esaf_release(self) -> None:
        self._mutate_mapping_set(
            lambda value: value["esaf_release"].__setitem__("id", "9.9")  # type: ignore[union-attr]
        )
        self._mutate_manifest(lambda value: value.__setitem__("esaf_release", "9.9"))

    def point_tag_to_other_commit(self) -> None:
        self._git("commit", "--quiet", "--allow-empty", "-m", "Other commit")
        self._git("tag", "fixture-release")
        self._mutate_mapping_set(
            lambda value: value["esaf_release"].__setitem__("tag_alias", "fixture-release")  # type: ignore[union-attr]
        )
        self._mutate_manifest(lambda value: value.__setitem__("tag_alias", "fixture-release"))

    def alter_catalog_digest(self) -> None:
        digest = "0" * 64
        self._mutate_mapping_set(
            lambda value: value["esaf_release"].__setitem__("control_catalog_sha256", digest)  # type: ignore[union-attr]
        )
        self._mutate_manifest(
            lambda value: value.__setitem__("control_catalog_sha256", digest)
        )

    def alter_control_record_digest(self) -> None:
        self._mutate_manifest(
            lambda value: value["controls"][0].__setitem__("record_sha256", "0" * 64)
        )

    def reference_unknown_control(self) -> None:
        self._mutate_record(
            lambda value: value["relationships"][0].__setitem__("esaf_control_id", "IAM-999")
        )

    def inject_and_reference_unknown_control(self) -> None:
        self.reference_unknown_control()

        def mutate(value: dict[str, object]) -> None:
            injected = dict(value["controls"][0])  # type: ignore[index]
            injected["id"] = "IAM-999"
            value["controls"].append(injected)  # type: ignore[union-attr]

        self._mutate_manifest(mutate)

    def set_wrong_control_version(self) -> None:
        self._mutate_record(
            lambda value: value["relationships"][0].__setitem__("esaf_control_version", "9.9.9")
        )

    def omit_manifest_control(self) -> None:
        self._mutate_manifest(lambda value: value.__setitem__("controls", []))

    def duplicate_mapping_set_id(self) -> None:
        snapshot = self._snapshot()
        duplicate = self.root / "crosswalks" / "mappings" / "other" / "1.0" / "1.0" / "1.0.0"
        shutil.copytree(snapshot, duplicate)

    def duplicate_record_id(self) -> None:
        shutil.copy2(self._record(), self._snapshot() / "duplicate.md")

    def duplicate_external_provision_id(self) -> None:
        self.add_record(
            self._snapshot(), "EXT-1", "ext-2", status="reviewed", disposition="mapped"
        )

    def mismatch_snapshot_path(self) -> None:
        source = self._snapshot()
        target = source.parent / "1.0.1"
        source.rename(target)
        self.snapshot = target

    def mismatch_inventory_scope_type(self) -> None:
        self._mutate_inventory(lambda value: value.__setitem__("scope_type", "declared_subset"))

    def mismatch_inventory_scope_statement(self) -> None:
        self._mutate_inventory(lambda value: value.__setitem__("scope_statement", "Different scope."))

    def mismatch_mapping_set_inventory_count(self) -> None:
        self._mutate_mapping_set(lambda value: value["scope"].__setitem__("inventory_count", 2))  # type: ignore[union-attr]

    def mismatch_inventory_expected_count(self) -> None:
        self._mutate_inventory(lambda value: value.__setitem__("expected_count", 2))

    def add_auxiliary_file(self) -> None:
        (self._snapshot() / "NOTES.txt").write_text("notes\n", encoding="utf-8", newline="\n")

    def add_nested_directory(self) -> None:
        (self._snapshot() / "nested").mkdir()

    def add_symbolic_link(self) -> None:
        (self._snapshot() / "linked.md").symlink_to(self._record())

    def symlinks_supported(self) -> bool:
        probe_target = self.root / "symlink-target"
        probe_link = self.root / "symlink-link"
        probe_target.write_text("probe", encoding="utf-8")
        try:
            probe_link.symlink_to(probe_target)
            return probe_link.is_symlink()
        except OSError:
            return False
        finally:
            if probe_link.is_symlink():
                probe_link.unlink()
            probe_target.unlink(missing_ok=True)

    def remove_granularity_exception(self) -> None:
        self._mutate_record(lambda value: value.__setitem__("granularity", "clause"))

    def remove_mapped_relationships(self) -> None:
        self._mutate_record(lambda value: value.__setitem__("relationships", []))

    def add_relationship_to_negative(self) -> None:
        def mutate(value: dict[str, object]) -> None:
            value["disposition"] = "no_direct_mapping"
            value["negative_rationale"] = "No direct relationship was identified."

        self._mutate_record(mutate)

    def remove_negative_rationale(self) -> None:
        def mutate(value: dict[str, object]) -> None:
            value["disposition"] = "no_direct_mapping"
            value["relationships"] = []

        self._mutate_record(mutate)

    def duplicate_control_direction_leg(self) -> None:
        def mutate(value: dict[str, object]) -> None:
            value["relationships"].append(dict(value["relationships"][0]))  # type: ignore[union-attr,index]

        self._mutate_record(mutate)

    def make_mapper_reviewer_identical(self) -> None:
        def mutate(value: dict[str, object]) -> None:
            value["reviewer"]["id"] = value["mapper"]["id"]  # type: ignore[index]

        self._mutate_mapping_set(mutate)

    def remove_review_metadata(self) -> None:
        self._mutate_record(lambda value: value.pop("reviewer"))

    def set_unsafe_child_status(self) -> None:
        self._mutate_record(lambda value: value.__setitem__("status", "draft"))

    def make_approved_snapshot_empty(self) -> None:
        for path in self._snapshot().glob("*.md"):
            if path.name not in {"README.md", "PROVISION_INVENTORY.md"}:
                path.unlink()

    def add_open_finding(self) -> None:
        self._set_finding("Important", "open")

    def accept_important_finding(self) -> None:
        self._set_finding("Important", "accepted")

    def remove_rights_approval(self) -> None:
        def mutate(value: dict[str, object]) -> None:
            value["publication_rights"].pop("approved")  # type: ignore[union-attr]

        self._mutate_mapping_set(mutate)

    def add_unpermitted_paraphrase(self) -> None:
        def mutate(value: dict[str, object]) -> None:
            rights = value["publication_rights"]
            rights["permitted_elements"] = ["identifiers"]  # type: ignore[index]
            rights["prohibited_elements"] = ["titles", "paraphrases"]  # type: ignore[index]

        self._mutate_mapping_set(mutate)

    def break_local_link(self) -> None:
        path = self._record()
        path.write_text(
            path.read_text(encoding="utf-8") + "\n[Missing](missing.md)\n",
            encoding="utf-8",
            newline="\n",
        )

    def add_reviewed_drafting_marker(self) -> None:
        path = self._record()
        path.write_text(
            path.read_text(encoding="utf-8") + "\nTODO: resolve wording\n",
            encoding="utf-8",
            newline="\n",
        )

    def write_utf8_bom(self) -> None:
        path = self._record()
        path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())

    def write_crlf(self) -> None:
        path = self._record()
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))

    def write_encoding_corruption_signature(self) -> None:
        path = self._record()
        path.write_text(
            path.read_text(encoding="utf-8") + "\nPossible corruption: cafÃ©\n",
            encoding="utf-8",
            newline="\n",
        )

    def break_inventory_local_link(self) -> None:
        self._append_inventory_body("\n[Missing](missing-inventory.md)\n")

    def add_inventory_drafting_marker(self) -> None:
        self._append_inventory_body("\nTODO: resolve inventory wording\n")

    def write_inventory_encoding_corruption_signature(self) -> None:
        self._append_inventory_body("\nPossible corruption: cafÃ©\n")

    def _set_finding(self, severity: str, status: str) -> None:
        finding: dict[str, object] = {
            "finding_id": "finding-1",
            "affected_record_ids": ["ext-1"],
            "severity": severity,
            "status": status,
            "description": "A review finding.",
            "disposition": "The finding was dispositioned.",
        }
        if status in {"resolved", "accepted"}:
            finding["resolver_or_acceptor"] = "approver-1"
            finding["disposition_date"] = "2026-07-13"
        if status == "accepted":
            finding["acceptance_rationale"] = "Within approved tolerance."
        self._mutate_mapping_set(lambda value: value.__setitem__("findings", [finding]))

    def _mutate_mapping_set(self, mutation: object) -> None:
        self._mutate_front_matter(self._snapshot() / "README.md", mutation)

    def _mutate_inventory(self, mutation: object) -> None:
        self._mutate_front_matter(self._snapshot() / "PROVISION_INVENTORY.md", mutation)

    def _mutate_record(self, mutation: object) -> None:
        self._mutate_front_matter(self._record(), mutation)

    def _mutate_manifest(self, mutation: object) -> None:
        path = self._snapshot() / "ESAF_CONTROL_MANIFEST.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        mutation(value)  # type: ignore[operator]
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    def _mutate_front_matter(self, path: Path, mutation: object) -> None:
        metadata, body = parse_front_matter(path)
        mutation(metadata)  # type: ignore[operator]
        self.write_front_matter(path.relative_to(self.root).as_posix(), metadata, body)

    def _append_inventory_body(self, addition: str) -> None:
        path = self._snapshot() / "PROVISION_INVENTORY.md"
        metadata, body = parse_front_matter(path)
        self.write_front_matter(
            path.relative_to(self.root).as_posix(), metadata, body + addition
        )

    def _snapshot(self) -> Path:
        if self.snapshot is None:
            raise RuntimeError("create_valid_snapshot must be called first")
        return self.snapshot

    def _record(self) -> Path:
        return sorted(
            path
            for path in self._snapshot().glob("*.md")
            if path.name not in {"README.md", "PROVISION_INVENTORY.md"}
        )[0]
