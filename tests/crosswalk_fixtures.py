"""Reusable repository fixtures for crosswalk validation tests."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import yaml

from tools.crosswalks.io import parse_front_matter


MAPPING_SET_ID = "nist--ai-rmf--1.0--esaf-0.4-alpha--1.0.0"


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
        control_path = self.root / "controls" / "IAM" / "IAM-100.md"
        control_path.parent.mkdir(parents=True, exist_ok=True)
        control_path.write_bytes(
            b"---\nid: IAM-100\nstatus: draft\nversion: 1.0.0\n---\n\n# IAM-100\n"
        )
        catalog = {
            "schema_version": "1.0.0",
            "control_count": 1,
            "controls": [
                {
                    "id": "IAM-100",
                    "version": "1.0.0",
                    "status": "draft",
                    "path": "IAM/IAM-100.md",
                }
            ],
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
        return snapshot

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
