# ESAF-1600 Crosswalk Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the normative, machine-validatable ESAF-1600 crosswalk foundation without adding substantive PCI DSS, HITRUST CSF, or UK Cyber Essentials mappings.

**Architecture:** Authoritative crosswalk snapshots remain Markdown with YAML front matter. A focused `tools/crosswalks/` package parses and validates snapshot, provision, manifest, and lifecycle contracts; the thin `tools/validate_crosswalks.py` CLI writes or checks deterministic JSON and Markdown catalogs. Approved snapshots are bound to immutable Git control manifests and protected by complete-file and append-only-history checks.

**Tech Stack:** Python 3.13 standard library, PyYAML 6.x, jsonschema 4.x, Markdown/YAML, JSON Schema Draft 2020-12, Git, GitHub Actions, `unittest`.

## Global Constraints

- Markdown is authoritative; generated JSON and Markdown catalogs shall not be edited directly.
- Do not add substantive external mapping assertions or reproduce external requirement text in this milestone.
- Relationship, direction, coverage, and confidence are separate dimensions; `equivalent`, `satisfies`, `certifies`, and compliance conclusions are prohibited.
- Provision records are requirement-level unless a clause/domain exception is explicitly justified.
- Draft snapshots may be incomplete; reviewed and approved snapshots shall exactly match their inventories.
- Approved snapshots are immutable and version-bound; lifecycle changes occur only in the append-only registry.
- Every snapshot pins a mandatory 40-character ESAF commit SHA; an optional tag is a display alias only.
- Snapshot source-derived content requires prior publication-rights approval by a reviewer different from the mapper.
- Use only dependencies already declared in `requirements-dev.txt`.
- Set `PYTHONDONTWRITEBYTECODE=1` for every Python validation command.
- Keep the initial generated catalog empty and explicit: zero mapping sets were assessed.
- Every task ends in a reviewable commit and leaves all focused tests passing.

---

## File and interface map

### Authoritative and generated content

- `crosswalks/ESAF-1600.md` — normative methodology.
- `crosswalks/MAPPING_SET_TEMPLATE.md` — mapping-set metadata and narrative contract.
- `crosswalks/PROVISION_INVENTORY_TEMPLATE.md` — declared assessment-universe contract.
- `crosswalks/CROSSWALK_TEMPLATE.md` — provision and directional-leg contract.
- `crosswalks/LIFECYCLE_RECORD_TEMPLATE.md` — lifecycle and digest contract.
- `crosswalks/schema/*.schema.json` — five metadata schemas.
- `crosswalks/mappings/` — authoritative versioned snapshots; initially empty except `.gitkeep` if needed.
- `crosswalks/registry/` — authoritative append-only lifecycle records; initially empty except `.gitkeep` if needed.
- `crosswalks/catalog.json` and `crosswalks/CATALOG.md` — deterministic generated views.

### Validation package

- `tools/crosswalks/io.py` — front-matter parsing, Markdown links, encoding, path helpers.
- `tools/crosswalks/schemas.py` — schema loading and deterministic schema-error formatting.
- `tools/crosswalks/manifest.py` — Git object reads and control-manifest regeneration.
- `tools/crosswalks/digests.py` — snapshot and lifecycle digest algorithms.
- `tools/crosswalks/validation.py` — repository-aware semantic validation and immutable-baseline comparison.
- `tools/crosswalks/catalog.py` — deterministic machine and human catalog rendering.
- `tools/validate_crosswalks.py` — `--check`, `--write`, and optional `--baseline-ref` CLI.

### Tests

- `tests/crosswalk_fixtures.py` — reusable temporary-repository fixture builder.
- `tests/test_crosswalk_schemas.py` — schema and parser contracts.
- `tests/test_validate_crosswalks.py` — semantic, provenance, lifecycle, mutation, and CLI contracts.
- `tests/test_esaf_1600_foundation.py` — normative-document, migration, and landing-page invariants.

---

### Task 1: Define schemas and Markdown parsing

**Files:**
- Create: `crosswalks/schema/mapping-set.schema.json`
- Create: `crosswalks/schema/provision-inventory.schema.json`
- Create: `crosswalks/schema/mapping-record.schema.json`
- Create: `crosswalks/schema/lifecycle-record.schema.json`
- Create: `crosswalks/schema/esaf-control-manifest.schema.json`
- Create: `tools/crosswalks/__init__.py`
- Create: `tools/crosswalks/io.py`
- Create: `tools/crosswalks/schemas.py`
- Create: `tests/test_crosswalk_schemas.py`

**Interfaces:**
- Produces: `parse_front_matter(path: Path) -> tuple[dict[str, object], str]`
- Produces: `load_schemas(root: Path) -> dict[str, Draft202012Validator]`
- Produces: `schema_errors(validator, value, relative_path) -> list[str]`
- Consumes: PyYAML and `jsonschema.Draft202012Validator`.

- [ ] **Step 1: Write failing parser and schema tests**

```python
class CrosswalkSchemaTests(unittest.TestCase):
    def test_parse_front_matter_returns_metadata_and_body(self) -> None:
        path = self.root / "record.md"
        path.write_text("---\nrecord_id: req-1\n---\n# Record\n", encoding="utf-8")
        metadata, body = parse_front_matter(path)
        self.assertEqual(metadata["record_id"], "req-1")
        self.assertEqual(body, "# Record\n")

    def test_mapping_schema_rejects_prohibited_relationship(self) -> None:
        record = valid_record("draft", "mapped", "requirement")
        record["relationships"][0]["relationship"] = "equivalent"
        errors = schema_errors(self.validators["mapping-record"], record, "record.md")
        self.assertTrue(any("equivalent" in error for error in errors))
```

Add these table-driven boundary tests in the same module. `delete_path`, `set_path`, and `add_unexpected_property` copy the instance before mutation; path components use dotted notation and numeric array indexes.

```python
SCHEMA_VARIANTS = (
    ("mapping-set", valid_mapping_set("draft")),
    ("mapping-set", valid_mapping_set("reviewed")),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True)),
    ("provision-inventory", valid_inventory("complete_publication")),
    ("provision-inventory", valid_inventory("declared_subset")),
    ("mapping-record", valid_record("draft", "mapped", "requirement")),
    ("mapping-record", valid_record("reviewed", "mapped", "clause")),
    ("mapping-record", valid_record("reviewed", "no_direct_mapping", "requirement")),
    ("mapping-record", valid_record("reviewed", "out_of_scope", "domain")),
    ("lifecycle-record", valid_lifecycle("retired")),
    ("esaf-control-manifest", valid_manifest()),
)

REQUIRED_PATHS = {
    "mapping-set": (
        "schema_version", "mapping_set_id", "authority", "authority.id", "authority.name",
        "publication", "publication.id", "publication.name", "source_version",
        "source_version.id", "source_version.label", "esaf_release", "esaf_release.id",
        "esaf_release.label", "esaf_release.source_commit_sha",
        "esaf_release.control_catalog_sha256", "esaf_release.control_manifest_path",
        "mapping_set_version", "status", "source", "source.official_url",
        "source.access_class", "source.licensing_note", "publication_rights",
        "publication_rights.basis", "publication_rights.permitted_elements",
        "publication_rights.prohibited_elements", "publication_rights.restrictions",
        "publication_rights.approved", "publication_rights.reviewer_id",
        "publication_rights.review_date", "scope", "scope.type", "scope.statement",
        "scope.inventory_count", "scope.default_granularity", "mapper", "mapper.id",
        "mapper.qualification", "mapper.date", "mapper.authorized_source_access",
        "findings", "change_history", "change_history.0.version",
        "change_history.0.date", "change_history.0.change",
    ),
    "provision-inventory": (
        "schema_version", "mapping_set_id", "scope_type", "scope_statement",
        "source_basis", "expected_count", "provision_ids",
    ),
    "mapping-record": (
        "schema_version", "record_id", "mapping_set_id", "status",
        "external_provision_id", "granularity", "context", "context.mode",
        "source_locator", "source_locator.official_url", "source_locator.locator",
        "disposition", "relationships", "mapper", "mapper.id", "mapper.date",
        "change_history", "change_history.0.version", "change_history.0.date",
        "change_history.0.change",
    ),
    "lifecycle-record": (
        "schema_version", "mapping_set_id", "snapshot_digest", "events",
        "events.0.event_id", "events.0.state", "events.0.date", "events.0.actor",
        "events.0.reason", "events.0.previous_event_digest", "events.0.event_digest",
    ),
    "esaf-control-manifest": (
        "schema_version", "esaf_release", "source_commit_sha",
        "control_catalog_sha256", "controls", "controls.0.id", "controls.0.version",
        "controls.0.status", "controls.0.path", "controls.0.record_sha256",
    ),
}

CONDITIONAL_REQUIRED_PATHS = (
    ("mapping-set", valid_mapping_set("reviewed"), "reviewer"),
    ("mapping-set", valid_mapping_set("reviewed"), "reviewer.id"),
    ("mapping-set", valid_mapping_set("reviewed"), "reviewer.qualification"),
    ("mapping-set", valid_mapping_set("reviewed"), "reviewer.date"),
    ("mapping-set", valid_mapping_set("reviewed"), "reviewer.authorized_source_access"),
    ("mapping-set", valid_mapping_set("reviewed"), "reviewer.findings_disposition"),
    ("mapping-set", valid_mapping_set("approved"), "reviewer"),
    ("mapping-set", valid_mapping_set("approved"), "reviewer.id"),
    ("mapping-set", valid_mapping_set("approved"), "reviewer.qualification"),
    ("mapping-set", valid_mapping_set("approved"), "reviewer.date"),
    ("mapping-set", valid_mapping_set("approved"), "reviewer.authorized_source_access"),
    ("mapping-set", valid_mapping_set("approved"), "reviewer.findings_disposition"),
    ("mapping-set", valid_mapping_set("approved"), "approver"),
    ("mapping-set", valid_mapping_set("approved"), "approver.id"),
    ("mapping-set", valid_mapping_set("approved"), "approver.date"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.finding_id"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.affected_record_ids"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.severity"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.status"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.description"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.disposition"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.resolver_or_acceptor"),
    ("mapping-set", valid_mapping_set("approved", with_resolved_finding=True), "findings.0.disposition_date"),
    ("mapping-record", valid_record("reviewed", "mapped", "requirement"), "reviewer"),
    ("mapping-record", valid_record("reviewed", "mapped", "requirement"), "reviewer.id"),
    ("mapping-record", valid_record("reviewed", "mapped", "requirement"), "reviewer.qualification"),
    ("mapping-record", valid_record("reviewed", "mapped", "requirement"), "reviewer.date"),
    ("mapping-record", valid_record("reviewed", "mapped", "requirement"), "reviewer.authorized_source_access"),
    ("mapping-record", valid_record("reviewed", "mapped", "requirement"), "reviewer.findings_disposition"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "context.summary"),
    ("mapping-record", valid_identifier_only_record(), "context.omission_rationale"),
    ("mapping-record", valid_record("draft", "mapped", "clause"), "granularity_exception"),
    ("mapping-record", valid_record("draft", "no_direct_mapping", "requirement"), "negative_rationale"),
    ("mapping-record", valid_record("draft", "out_of_scope", "requirement"), "negative_rationale"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.esaf_control_id"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.esaf_control_version"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.relationship"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.direction"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.coverage"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.confidence"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.rationale"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.conditions"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.expected_evidence"),
    ("mapping-record", valid_record("draft", "mapped", "requirement"), "relationships.0.known_gaps"),
)

ENUM_CASES = (
    ("mapping-set", "status", ("draft", "reviewed", "approved")),
    ("mapping-set", "source.access_class", ("public", "restricted", "licensed")),
    ("mapping-set", "publication_rights.permitted_elements.0", ("identifiers", "titles", "structural_inventory", "paraphrases", "derivative_mapping_analysis", "official_links")),
    ("mapping-set", "publication_rights.prohibited_elements.0", ("identifiers", "titles", "structural_inventory", "paraphrases", "derivative_mapping_analysis", "official_links")),
    ("mapping-set", "scope.type", ("complete_publication", "declared_subset")),
    ("mapping-set", "scope.default_granularity", ("requirement", "clause", "domain")),
    ("mapping-record", "status", ("draft", "reviewed")),
    ("mapping-record", "granularity", ("requirement", "clause", "domain")),
    ("mapping-record", "context.mode", ("paraphrase", "identifier_only")),
    ("mapping-record", "disposition", ("mapped", "no_direct_mapping", "out_of_scope")),
    ("mapping-record", "relationships.0.relationship", ("supports", "partially_supports", "complements", "prerequisite", "informs")),
    ("mapping-record", "relationships.0.direction", ("esaf_to_external", "external_to_esaf")),
    ("mapping-record", "relationships.0.coverage", ("substantial", "partial", "narrow", "contextual")),
    ("mapping-record", "relationships.0.confidence", ("high", "medium", "low")),
    ("mapping-set", "findings.0.severity", ("Critical", "Important", "Minor")),
    ("mapping-set", "findings.0.status", ("open", "resolved", "accepted")),
    ("lifecycle-record", "events.0.state", ("approved", "published", "deprecated", "retired")),
    ("esaf-control-manifest", "controls.0.status", ("proposed", "draft", "approved", "published", "deprecated", "retired")),
)

def test_every_required_property_boundary(self) -> None:
    for schema_name, instance in SCHEMA_VARIANTS:
        for path in REQUIRED_PATHS[schema_name]:
            with self.subTest(schema=schema_name, path=path):
                self.assertTrue(path_exists(instance, path), f"fixture missing required path {path}")
                mutated = delete_path(instance, path)
                self.assertTrue(schema_errors(self.validators[schema_name], mutated, schema_name))
    for schema_name, instance, path in CONDITIONAL_REQUIRED_PATHS:
        with self.subTest(schema=schema_name, path=path):
            mutated = delete_path(instance, path)
            self.assertTrue(schema_errors(self.validators[schema_name], mutated, schema_name))

def test_every_schema_variant_is_valid(self) -> None:
    for schema_name, instance in SCHEMA_VARIANTS:
        with self.subTest(schema=schema_name, status=instance.get("status")):
            self.assertEqual(schema_errors(self.validators[schema_name], instance, schema_name), [])

def test_every_enum_accepts_declared_values_and_rejects_unknown(self) -> None:
    for schema_name, path, values in ENUM_CASES:
        for value in values:
            instance = valid_instance_for_enum(schema_name, path, value)
            self.assertEqual(schema_errors(self.validators[schema_name], instance, schema_name), [])
        invalid = valid_instance_for_enum(schema_name, path, values[0])
        set_path(invalid, path, "not-a-declared-value")
        self.assertTrue(schema_errors(self.validators[schema_name], invalid, schema_name))

def test_additional_properties_are_rejected_at_every_object_boundary(self) -> None:
    for schema_name, instance in SCHEMA_VARIANTS:
        for path in object_paths(instance):
            with self.subTest(schema=schema_name, path=path):
                mutated = add_unexpected_property(instance, path)
                self.assertTrue(schema_errors(self.validators[schema_name], mutated, schema_name))

def test_schema_conditional_matrix(self) -> None:
    cases = (
        ("mapping-set", valid_accepted_minor_finding(), "remove_finding_acceptor", "resolver_or_acceptor"),
        ("mapping-set", valid_accepted_minor_finding(), "remove_finding_disposition_date", "disposition_date"),
        ("mapping-set", valid_accepted_minor_finding(), "remove_acceptance_rationale", "acceptance_rationale"),
        ("mapping-set", valid_resolved_finding(), "remove_finding_resolver", "resolver_or_acceptor"),
        ("mapping-set", valid_resolved_finding(), "remove_finding_disposition_date", "disposition_date"),
        ("mapping-record", valid_identifier_only_record(), "add_context_summary", "summary"),
        ("mapping-record", valid_record("draft", "mapped", "requirement"), "add_omission_rationale", "omission_rationale"),
        ("mapping-record", valid_record("draft", "mapped", "requirement"), "empty_relationships", "relationships"),
        ("mapping-record", valid_record("draft", "no_direct_mapping", "requirement"), "add_relationship", "relationships"),
        ("mapping-record", valid_record("draft", "out_of_scope", "requirement"), "add_relationship", "relationships"),
        ("mapping-record", valid_record("draft", "mapped", "requirement"), "empty_conditions", "conditions"),
        ("mapping-record", valid_record("draft", "mapped", "requirement"), "empty_expected_evidence", "expected_evidence"),
        ("mapping-record", valid_record("draft", "mapped", "requirement"), "empty_known_gaps", "known_gaps"),
        ("mapping-record", valid_record("draft", "mapped", "requirement"), "duplicate_conditions", "unique"),
    )
    for schema_name, instance, mutation, expected in cases:
        with self.subTest(schema=schema_name, mutation=mutation):
            mutated = apply_schema_mutation(instance, mutation)
            self.assertIn(expected, "\n".join(schema_errors(self.validators[schema_name], mutated, schema_name)))

def test_every_array_constraint_is_exercised(self) -> None:
    for schema_name, path, min_items, unique_items in constrained_array_paths(self.schema_documents):
        instance = valid_instance_for_array_path(schema_name, path)
        if min_items:
            mutated = set_path_copy(instance, path, [])
            self.assertTrue(schema_errors(self.validators[schema_name], mutated, schema_name))
        if unique_items:
            value = get_path(instance, path)
            mutated = set_path_copy(instance, path, [value[0], value[0]])
            self.assertTrue(schema_errors(self.validators[schema_name], mutated, schema_name))
```

`apply_schema_mutation` implements only the named single-field/list mutations in this table. `constrained_array_paths` recursively follows local `$ref`, `properties`, `items`, `allOf`, `anyOf`, `oneOf`, `if`, `then`, and `else` nodes and yields every array schema containing `minItems` or `uniqueItems`; `valid_instance_for_array_path` selects the first `SCHEMA_VARIANTS` instance containing that path.

- [ ] **Step 2: Run the focused tests and verify the missing-module failure**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_crosswalk_schemas -v`

Expected: FAIL because `tools.crosswalks.io` and schema files do not exist.

- [ ] **Step 3: Implement strict front-matter and schema helpers**

```python
def parse_front_matter(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 byte-order mark is prohibited")
    if b"\r" in raw:
        raise ValueError("CR or CRLF line endings are prohibited")
    text = raw.decode("utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("malformed YAML front matter")
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        raise ValueError("front matter must be a mapping")
    return metadata, parts[2]

def schema_errors(validator, value: object, relative_path: str) -> list[str]:
    errors = []
    for item in sorted(validator.iter_errors(value), key=lambda error: list(error.absolute_path)):
        location = ".".join(str(part) for part in item.absolute_path) or "metadata"
        errors.append(f"{relative_path}: {location}: {item.message}")
    return errors
```

- [ ] **Step 4: Encode the exact schema vocabulary**

Use these required top-level fields and enums:

```text
mapping-set: schema_version, mapping_set_id, authority, publication,
  source_version, esaf_release, mapping_set_version, status, source,
  publication_rights, scope, mapper, findings, change_history
inventory: schema_version, mapping_set_id, scope_type, scope_statement,
  source_basis, expected_count, provision_ids
record: schema_version, record_id, mapping_set_id, status,
  external_provision_id, granularity, context, source_locator,
  disposition, relationships, mapper, change_history
lifecycle: schema_version, mapping_set_id, snapshot_digest, events
manifest: schema_version, esaf_release, source_commit_sha,
  control_catalog_sha256, controls

status(snapshot): draft | reviewed | approved
status(record): draft | reviewed
access_class: public | restricted | licensed
scope_type: complete_publication | declared_subset
granularity: requirement | clause | domain
disposition: mapped | no_direct_mapping | out_of_scope
relationship: supports | partially_supports | complements | prerequisite | informs
direction: esaf_to_external | external_to_esaf
coverage: substantial | partial | narrow | contextual
confidence: high | medium | low
lifecycle state: approved | published | deprecated | retired
finding severity: Critical | Important | Minor
finding status: open | resolved | accepted
context mode: paraphrase | identifier_only
publication element: identifiers | titles | structural_inventory |
  paraphrases | derivative_mapping_analysis | official_links
```

Constrain slugs to `^[a-z0-9]+(?:-[a-z0-9]+)*$`, version identifiers to `^[a-z0-9]+(?:[.-][a-z0-9]+)*$`, three-part versions to `^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$`, SHA-256 values to `^[a-f0-9]{64}$`, commit SHAs to `^[a-f0-9]{40}$`, and dates to `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`. Set `additionalProperties: false` at every object boundary. The mapping-record schema shall contain no source-text or verbatim-requirement field.

Define reviewer/mapper objects with `id`, `qualification`, `date`, and `authorized_source_access`; approvers with `id` and `date`; findings with `finding_id`, `affected_record_ids`, `severity`, `status`, `description`, `disposition`, `resolver_or_acceptor`, `disposition_date`, and `acceptance_rationale`; change-history rows with `version`, `date`, and `change`; context with `mode` plus mutually exclusive `summary` or `omission_rationale`; and relationship legs with every field listed in the approved design. Use schema conditionals so reviewed/approved states require review metadata, approved state requires approval metadata, mapped disposition requires at least one leg, negative dispositions prohibit legs and require `negative_rationale`, and `identifier_only` requires `omission_rationale` while prohibiting `summary`.

The schemas shall use this complete nested field contract; `?` means optional and no unlisted field is permitted:

```text
mapping-set
  schema_version: string
  mapping_set_id: string
  authority: {id: slug, name: string}
  publication: {id: slug, name: string}
  source_version: {id: version-slug, label: string}
  esaf_release:
    {id: version-slug, label: string, source_commit_sha: sha40,
     tag_alias?: string, control_catalog_sha256: sha256,
     control_manifest_path: "ESAF_CONTROL_MANIFEST.json"}
  mapping_set_version: three-part-version
  status: draft | reviewed | approved
  source:
    {official_url: uri, publication_date?: date, access_class: enum,
     licensing_note: string}
  publication_rights:
    {basis: string, permitted_elements: unique publication-element[],
     prohibited_elements: unique publication-element[], restrictions: string,
     approved: true, reviewer_id: string, review_date: date}
  scope:
    {type: complete_publication | declared_subset, statement: string,
     inventory_count: nonnegative-integer,
     default_granularity: requirement | clause | domain}
  mapper:
    {id: string, qualification: string, date: date,
     authorized_source_access: true}
  reviewer?:
    {id: string, qualification: string, date: date,
     authorized_source_access: true, findings_disposition: string}
  approver?: {id: string, date: date}
  findings: finding[]
  predecessor_id?: mapping-set-id
  change_history: change[]

provision-inventory
  schema_version: string
  mapping_set_id: mapping-set-id
  scope_type: complete_publication | declared_subset
  scope_statement: string
  source_basis: string
  expected_count: nonnegative-integer
  provision_ids: unique nonempty string[]

mapping-record
  schema_version: string
  record_id: slug
  mapping_set_id: mapping-set-id
  status: draft | reviewed
  external_provision_id: string
  granularity: requirement | clause | domain
  title?: string
  context:
    {mode: paraphrase | identifier_only, summary?: string,
     omission_rationale?: string}
  source_locator: {official_url: uri, locator: string}
  granularity_exception?: string
  disposition: mapped | no_direct_mapping | out_of_scope
  relationships: relationship-leg[]
  negative_rationale?: string
  mapper: {id: string, date: date}
  reviewer?:
    {id: string, qualification: string, date: date,
     authorized_source_access: true, findings_disposition: string}
  predecessor_record_id?: slug
  change_history: change[]

relationship-leg
  esaf_control_id: ESAF-control-id
  esaf_control_version: three-part-version
  relationship: supports | partially_supports | complements | prerequisite | informs
  direction: esaf_to_external | external_to_esaf
  coverage: substantial | partial | narrow | contextual
  confidence: high | medium | low
  rationale: string
  conditions: nonempty string[]
  expected_evidence: nonempty string[]
  known_gaps: nonempty string[]

finding
  finding_id: slug
  affected_record_ids: unique slug[]
  severity: Critical | Important | Minor
  status: open | resolved | accepted
  description: string
  disposition: string
  resolver_or_acceptor?: string
  disposition_date?: date
  acceptance_rationale?: string

change
  version: three-part-version
  date: date
  change: string

lifecycle-record
  schema_version: string
  mapping_set_id: mapping-set-id
  snapshot_digest: sha256
  events: lifecycle-event[]

lifecycle-event
  event_id: slug
  state: approved | published | deprecated | retired
  date: date
  actor: string
  reason: string
  predecessor_id?: mapping-set-id
  successor_id?: mapping-set-id
  approval_reference?: string
  previous_event_digest: sha256
  event_digest: sha256

control-manifest
  schema_version: string
  esaf_release: string
  source_commit_sha: sha40
  tag_alias?: string
  control_catalog_sha256: sha256
  controls: control-manifest-entry[]

control-manifest-entry
  id: ESAF-control-id
  version: three-part-version
  status: proposed | draft | approved | published | deprecated | retired
  path: controls-relative POSIX path
  record_sha256: sha256
```

Schema conditionals shall additionally require resolver/date for `resolved`, resolver/date/acceptance rationale for `accepted`, clause/domain granularity exceptions, and the exact source-context element in `publication_rights.permitted_elements` (`paraphrases` for summary, `identifiers` for identifier-only). Arrays described as nonempty use `minItems: 1`; identity and enum arrays use `uniqueItems: true`.

- [ ] **Step 5: Run focused tests and commit**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_crosswalk_schemas -v`

Expected: PASS.

```shell
git add crosswalks/schema tools/crosswalks tests/test_crosswalk_schemas.py
git commit -m "Add ESAF-1600 metadata schemas"
```

### Task 2: Build reusable fixtures and snapshot semantic validation

**Files:**
- Create: `tests/crosswalk_fixtures.py`
- Create: `tools/crosswalks/validation.py`
- Create: `tests/test_validate_crosswalks.py`

**Interfaces:**
- Consumes: Task 1 parsing and schema helpers.
- Produces: `ValidationResult(errors: list[str], mapping_sets: list[dict], lifecycle_records: list[dict])`
- Produces: `validate(root: Path, baseline_ref: str | None = None) -> ValidationResult`
- Produces fixture helpers: `create_valid_snapshot(status: str = "draft", complete: bool = True, scope_type: str = "complete_publication", dispositions: tuple[str, ...] = ("mapped",)) -> Path` and `write_front_matter(relative: str, metadata: dict[str, object], body: str) -> Path`.

- [ ] **Step 1: Write valid-state and inventory-boundary tests**

```python
def test_valid_incomplete_draft_is_accepted(self) -> None:
    self.fixture.create_valid_snapshot(status="draft", complete=False)
    self.assertEqual(validate(self.root).errors, [])

def test_incomplete_reviewed_snapshot_is_rejected(self) -> None:
    self.fixture.create_valid_snapshot(status="reviewed", complete=False)
    errors = validate(self.root).errors
    self.assertIn("missing provision record for inventory identifier EXT-2", "\n".join(errors))

def test_record_outside_inventory_is_always_rejected(self) -> None:
    snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
    self.fixture.add_record(snapshot, external_provision_id="EXT-99", record_id="ext-99")
    self.assertIn("not present in provision inventory", "\n".join(validate(self.root).errors))

def test_complete_positive_snapshot_states_are_accepted(self) -> None:
    for status in ("draft", "reviewed", "approved"):
        with self.subTest(status=status):
            self.fixture.reset_crosswalks()
            self.fixture.create_valid_snapshot(status=status, complete=True)
            self.assertEqual(validate(self.root).errors, [])

def test_declared_subset_and_all_dispositions_are_accepted(self) -> None:
    self.fixture.create_valid_snapshot(
        status="reviewed",
        complete=True,
        scope_type="declared_subset",
        dispositions=("mapped", "no_direct_mapping", "out_of_scope"),
    )
    self.assertEqual(validate(self.root).errors, [])
```

- [ ] **Step 2: Run the focused test and verify the missing-validator failure**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_validate_crosswalks -v`

Expected: FAIL because `tools.crosswalks.validation` does not exist.

- [ ] **Step 3: Implement deterministic snapshot discovery and validation**

```python
@dataclass
class ValidationResult:
    errors: list[str]
    mapping_sets: list[dict[str, object]]
    lifecycle_records: list[dict[str, object]]

def snapshot_directories(root: Path) -> list[Path]:
    base = root / "crosswalks" / "mappings"
    return sorted(path.parent for path in base.rglob("README.md")) if base.exists() else []

def validate(root: Path, baseline_ref: str | None = None) -> ValidationResult:
    errors: list[str] = []
    mapping_sets: list[dict[str, object]] = []
    seen_mapping_set_ids: set[str] = set()
    for snapshot in snapshot_directories(root):
        metadata, _ = parse_front_matter(snapshot / "README.md")
        relative = snapshot.relative_to(root).as_posix()
        errors.extend(validate_snapshot(root, snapshot, metadata, seen_mapping_set_ids))
        mapping_sets.append(load_snapshot_model(root, snapshot, metadata))
    return ValidationResult(sorted(set(errors)), mapping_sets, [])
```

`validate_snapshot` shall recompute the mapping-set ID as `authority.id + "--" + publication.id + "--" + source_version.id + "--esaf-" + esaf_release.id + "--" + mapping_set_version`. Its required directory is `crosswalks/mappings/{authority.id}/{source_version.id}/{esaf_release.id}/{mapping_set_version}`. Reject double hyphens inside components, duplicate IDs, path/metadata disagreement, and any file other than `README.md`, `PROVISION_INVENTORY.md`, `ESAF_CONTROL_MANIFEST.json`, or direct-child provision Markdown named exactly `{record_id}.md`; reject every nested directory, symbolic link, and non-regular entry. Require `mapping_set.scope.type == inventory.scope_type`, `mapping_set.scope.statement == inventory.scope_statement`, and `mapping_set.scope.inventory_count == inventory.expected_count`. Compare inventory count and identifiers, enforce record filename/ID/set agreement, require exact completeness for reviewed/approved snapshots, allow draft omissions but no extras, and apply the parent/child state matrix `draft -> draft|reviewed`, `reviewed -> reviewed`, `approved -> reviewed`.

- [ ] **Step 4: Add mutation tests for semantic rules**

```python
def test_snapshot_and_record_mutation_matrix(self) -> None:
    cases = (
        ("duplicate_mapping_set_id", "duplicate mapping-set id"),
        ("duplicate_record_id", "duplicate record id"),
        ("duplicate_external_provision_id", "duplicate external provision identifier"),
        ("mismatch_snapshot_path", "snapshot path disagrees with metadata"),
        ("mismatch_inventory_scope_type", "mapping-set scope type disagrees with provision inventory"),
        ("mismatch_inventory_scope_statement", "mapping-set scope statement disagrees with provision inventory"),
        ("mismatch_mapping_set_inventory_count", "mapping-set inventory count disagrees with provision inventory"),
        ("mismatch_inventory_expected_count", "inventory expected count disagrees with provision identifiers"),
        ("add_auxiliary_file", "unexpected snapshot entry"),
        ("add_nested_directory", "unexpected snapshot entry"),
        ("add_symbolic_link", "unexpected snapshot entry"),
        ("remove_granularity_exception", "non-requirement granularity requires granularity_exception"),
        ("remove_mapped_relationships", "mapped record requires at least one relationship"),
        ("add_relationship_to_negative", "must not contain relationships"),
        ("remove_negative_rationale", "negative disposition requires negative_rationale"),
        ("duplicate_control_direction_leg", "duplicate relationship leg"),
        ("make_mapper_reviewer_identical", "reviewer must differ from mapper"),
        ("remove_review_metadata", "reviewed content requires review metadata"),
        ("set_unsafe_child_status", "invalid snapshot/provision status combination"),
        ("make_approved_snapshot_empty", "approved snapshot requires at least one provision"),
        ("add_open_finding", "open review finding blocks approval"),
        ("accept_important_finding", "Important findings must be resolved"),
        ("remove_rights_approval", "publication-rights approval is required"),
        ("add_unpermitted_paraphrase", "context exceeds permitted publication elements"),
        ("break_local_link", "broken local link"),
        ("add_reviewed_drafting_marker", "unresolved drafting marker"),
        ("write_utf8_bom", "UTF-8 byte-order mark is prohibited"),
        ("write_crlf", "CR or CRLF line endings are prohibited"),
        ("write_encoding_corruption_signature", "possible text-encoding corruption"),
    )
    for mutation, expected in cases:
        with self.subTest(mutation=mutation):
            self.fixture.reset_crosswalks()
            self.fixture.create_valid_snapshot(status="approved", complete=True)
            if mutation == "add_symbolic_link" and not self.fixture.symlinks_supported():
                continue
            getattr(self.fixture, mutation)()
            self.assertIn(expected, "\n".join(validate(self.root).errors))
```

Implement each named fixture mutation as one minimal change to an otherwise valid approved snapshot. `add_unpermitted_paraphrase` changes rights to `identifier_only`/identifiers-only and then adds a summary. `set_unsafe_child_status` places a draft record under a reviewed snapshot. Link and drafting mutations target reviewed content so those gates apply.

- [ ] **Step 5: Implement relationship, review, findings, and rights semantics**

```python
def validate_record(record: dict[str, object], mapping_set: dict[str, object]) -> list[str]:
    errors: list[str] = []
    relationships = record["relationships"]
    disposition = record["disposition"]
    if disposition == "mapped" and not relationships:
        errors.append("mapped record requires at least one relationship")
    if disposition != "mapped" and relationships:
        errors.append(f"{disposition} record must not contain relationships")
    if record["granularity"] != "requirement" and not record.get("granularity_exception"):
        errors.append("non-requirement granularity requires granularity_exception")
    seen_legs: set[tuple[str, str]] = set()
    for leg in relationships:
        key = (leg["esaf_control_id"], leg["direction"])
        if key in seen_legs:
            errors.append(f"duplicate relationship leg {key[0]}/{key[1]}")
        seen_legs.add(key)
    return errors
```

Rights approval is required for every repository snapshot, including drafts. The rights reviewer and mapper must differ. Reviewed records/snapshots require independent reviewer identity, qualification, date, and source-access attestation. Only resolved Critical/Important findings and resolved or formally accepted Minor findings are eligible for approval.

- [ ] **Step 6: Run focused tests and commit**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_validate_crosswalks -v`

Expected: PASS for all snapshot and record semantic tests added in this task.

```shell
git add tools/crosswalks/validation.py tests/crosswalk_fixtures.py tests/test_validate_crosswalks.py
git commit -m "Validate ESAF-1600 snapshot semantics"
```

### Task 3: Generate and verify release-pinned ESAF control manifests

**Files:**
- Create: `tools/crosswalks/manifest.py`
- Modify: `tools/crosswalks/validation.py`
- Modify: `tests/crosswalk_fixtures.py`
- Modify: `tests/test_validate_crosswalks.py`

**Interfaces:**
- Produces: `git_bytes(root: Path, revision: str, path: str) -> bytes`
- Produces: `build_control_manifest(root: Path, commit_sha: str, esaf_release: str, tag_alias: str | None) -> dict[str, object]`
- Produces: `render_manifest(manifest: dict[str, object]) -> str`
- Consumes: `VERSION.md`, `controls/catalog.json`, and control files from the pinned Git object.

- [ ] **Step 1: Write failing immutable-provenance tests**

```python
def test_manifest_regenerates_from_pinned_commit(self) -> None:
    commit = self.fixture.commit_valid_control_catalog(release="0.4-alpha")
    manifest = build_control_manifest(self.root, commit, "0.4-alpha", None)
    self.assertEqual(manifest["source_commit_sha"], commit)
    self.assertEqual(manifest["controls"][0]["id"], "IAM-100")

def test_manifest_rejects_current_tree_substitution(self) -> None:
    snapshot = self.fixture.create_valid_snapshot(status="draft", complete=True)
    self.fixture.mutate_control_after_snapshot(snapshot)
    self.assertIn("manifest differs from regeneration at pinned commit", "\n".join(validate(self.root).errors))
```

- [ ] **Step 2: Verify the focused tests fail before implementation**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_validate_crosswalks -v`

Expected: FAIL because `build_control_manifest` is unavailable.

- [ ] **Step 3: Implement byte-exact Git reads and manifest generation**

```python
def git_bytes(root: Path, revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path}"],
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise ValueError(completed.stderr.decode("utf-8", errors="replace").strip())
    return completed.stdout

def render_manifest(manifest: dict[str, object]) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
```

`build_control_manifest` shall verify the commit exists, read the release from `VERSION.md`, hash the exact `controls/catalog.json` bytes, preserve every catalog control's ID/version/status/path, hash each control file, sort controls by ID, and resolve an optional tag alias with `git rev-parse TAG^{commit}`. The committed manifest must equal `render_manifest(build_control_manifest(...))` byte for byte.

- [ ] **Step 4: Add commit, release, tag, digest, and control-resolution mutations**

```python
def test_manifest_mutation_matrix(self) -> None:
    cases = (
        ("set_unreachable_commit", "pinned commit is unreachable"),
        ("set_wrong_esaf_release", "VERSION.md release mismatch"),
        ("point_tag_to_other_commit", "tag alias does not resolve to pinned commit"),
        ("alter_catalog_digest", "control catalog digest mismatch"),
        ("alter_control_record_digest", "control record digest mismatch"),
        ("reference_unknown_control", "unresolved ESAF control identifier"),
        ("set_wrong_control_version", "ESAF control version mismatch"),
        ("omit_manifest_control", "manifest differs from regeneration at pinned commit"),
    )
    for mutation, expected in cases:
        with self.subTest(mutation=mutation):
            self.fixture.reset_repository()
            self.fixture.create_valid_snapshot(status="draft", complete=True)
            getattr(self.fixture, mutation)()
            self.assertIn(expected, "\n".join(validate(self.root).errors))
```

Do not hardcode 91 controls; fixture manifests derive their expected control population from the fixture catalog.

- [ ] **Step 5: Run focused tests and commit**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_validate_crosswalks -v`

Expected: PASS.

```shell
git add tools/crosswalks/manifest.py tools/crosswalks/validation.py tests/crosswalk_fixtures.py tests/test_validate_crosswalks.py
git commit -m "Bind crosswalks to immutable control manifests"
```

### Task 4: Protect snapshots and lifecycle history

**Files:**
- Create: `tools/crosswalks/digests.py`
- Modify: `tools/crosswalks/validation.py`
- Modify: `tests/crosswalk_fixtures.py`
- Modify: `tests/test_validate_crosswalks.py`

**Interfaces:**
- Produces: `snapshot_digest(root: Path, snapshot: Path) -> str`
- Produces: `event_bytes(event: Mapping[str, str]) -> bytes`
- Produces: `event_digest(event: Mapping[str, str]) -> str`
- Produces: `validate_lifecycle(records) -> list[str]`
- Produces: `validate_baseline(root: Path, baseline_ref: str, current) -> list[str]`
- Produces fixture helpers: `valid_event(**overrides: str) -> dict[str, str]` and `create_approved_snapshot_with_lifecycle(final_state: str) -> Path`.

- [ ] **Step 1: Write digest-vector and mutation tests**

```python
def test_event_digest_uses_fixed_length_prefixed_utf8(self) -> None:
    event = valid_event(
        event_id="evt-001",
        state="approved",
        date="2026-07-13",
        actor="reviewer-1",
        reason="Cafe\u0301",
        predecessor_id="",
        successor_id="",
        approval_reference="APR-001",
        previous_event_digest="0" * 64,
    )
    expected = (
        b"event_id:7:evt-001\n"
        b"state:8:approved\n"
        b"date:10:2026-07-13\n"
        b"actor:10:reviewer-1\n"
        b"reason:5:Caf\xc3\xa9\n"
        b"predecessor_id:0:\n"
        b"successor_id:0:\n"
        b"approval_reference:7:APR-001\n"
        b"previous_event_digest:64:"
        + (b"0" * 64)
        + b"\n"
    )
    self.assertEqual(event_bytes(event), expected)
    self.assertEqual(
        event_digest(event),
        "dce6853af1e45395304b66d057807375f8c0d61e7393a725f4776e9fba00b811",
    )

def test_approved_snapshot_mutation_against_baseline_is_rejected(self) -> None:
    baseline = self.fixture.commit_approved_snapshot()
    self.fixture.mutate_approved_record()
    errors = validate(self.root, baseline_ref=baseline).errors
    self.assertIn("approved snapshot differs from trusted baseline", "\n".join(errors))

def test_positive_lifecycle_states_are_accepted(self) -> None:
    for state in ("approved", "published", "deprecated", "retired"):
        with self.subTest(state=state):
            self.fixture.reset_crosswalks()
            self.fixture.create_approved_snapshot_with_lifecycle(final_state=state)
            self.assertEqual(validate(self.root).errors, [])
```

- [ ] **Step 2: Verify the tests fail before digest implementation**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_validate_crosswalks -v`

Expected: FAIL because digest functions are unavailable.

- [ ] **Step 3: Implement exact snapshot and event digests**

```python
EVENT_FIELDS = (
    "event_id", "state", "date", "actor", "reason",
    "predecessor_id", "successor_id", "approval_reference",
    "previous_event_digest",
)

def event_bytes(event: Mapping[str, str]) -> bytes:
    output = bytearray()
    for field in EVENT_FIELDS:
        value = unicodedata.normalize("NFC", event.get(field, "")).encode("utf-8")
        output.extend(f"{field}:{len(value)}:".encode("ascii"))
        output.extend(value)
        output.extend(b"\n")
    return bytes(output)

def event_digest(event: Mapping[str, str]) -> str:
    return hashlib.sha256(event_bytes(event)).hexdigest()
```

`snapshot_digest` shall enumerate the complete allowed regular-file set, reject every directory/symlink/other entry, hash exact bytes, sort repository-relative POSIX paths, serialize each line as the lowercase digest, two ASCII spaces, the path, and LF, then hash the manifest bytes.

- [ ] **Step 4: Implement lifecycle and trusted-baseline validation**

Enforce `approved -> published -> deprecated -> retired`, one registry record per mapping set, digest agreement, genesis previous digest of 64 zeroes, chained event digests, successor/explanation on deprecation, approved snapshot requirement before publication, and one active published version per authority/publication/source-version/ESAF-release tuple.

For `--baseline-ref`, use `git ls-tree`/`git show` to prove every baseline-approved snapshot is byte-identical and every baseline lifecycle event array is an exact prefix of the candidate. A missing or shallow baseline is an error when approved or lifecycle-managed content exists.

- [ ] **Step 5: Add mutations for coordinated rewrites and lifecycle errors**

```python
def test_lifecycle_and_baseline_mutation_matrix(self) -> None:
    cases = (
        ("rewrite_snapshot_and_registry_digest", "approved snapshot differs from trusted baseline"),
        ("rewrite_prior_event_and_rehash_chain", "baseline lifecycle events are not an exact prefix"),
        ("reorder_lifecycle_events", "invalid lifecycle transition"),
        ("duplicate_lifecycle_event", "duplicate lifecycle event"),
        ("skip_published_transition", "invalid lifecycle transition"),
        ("publish_unapproved_snapshot", "published lifecycle requires approved snapshot"),
        ("publish_second_active_version", "multiple active published mapping sets"),
        ("deprecate_without_successor_or_explanation", "deprecated lifecycle requires successor or explanation"),
        ("set_stale_snapshot_digest", "lifecycle snapshot digest mismatch"),
    )
    for mutation, expected in cases:
        with self.subTest(mutation=mutation):
            self.fixture.reset_repository()
            baseline = self.fixture.commit_approved_snapshot_with_lifecycle()
            getattr(self.fixture, mutation)()
            self.assertIn(expected, "\n".join(validate(self.root, baseline_ref=baseline).errors))
```

- [ ] **Step 6: Run focused tests and commit**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_validate_crosswalks -v`

Expected: PASS, including the supplied fixed canonical bytes and literal SHA-256 digest vector.

```shell
git add tools/crosswalks/digests.py tools/crosswalks/validation.py tests/crosswalk_fixtures.py tests/test_validate_crosswalks.py
git commit -m "Protect crosswalk snapshot and lifecycle history"
```

### Task 5: Generate deterministic catalogs and expose the CLI

**Files:**
- Create: `tools/crosswalks/catalog.py`
- Create: `tools/validate_crosswalks.py`
- Modify: `tools/crosswalks/validation.py`
- Modify: `tests/test_validate_crosswalks.py`
- Create: `crosswalks/catalog.json`
- Create: `crosswalks/CATALOG.md`

**Interfaces:**
- Produces: `build_catalog(result: ValidationResult) -> dict[str, object]`
- Produces: `render_json(catalog: dict[str, object]) -> str`
- Produces: `render_markdown(catalog: dict[str, object]) -> str`
- Produces: `check_outputs(root: Path, catalog: dict[str, object]) -> list[str]`
- CLI: `python tools/validate_crosswalks.py (--check | --write) [--baseline-ref COMMIT]`.

- [ ] **Step 1: Write failing empty-catalog and freshness tests**

```python
def test_empty_catalog_is_explicit_and_deterministic(self) -> None:
    catalog = build_catalog(validate(self.root))
    self.assertEqual(catalog["counts"]["mapping_sets"], 0)
    self.assertIn("No mapping sets have been assessed", render_markdown(catalog))
    self.assertEqual(render_json(catalog), render_json(catalog))

def test_check_reports_stale_generated_output(self) -> None:
    self.fixture.write_generated_catalogs("stale\n", "{}\n")
    catalog = build_catalog(validate(self.root))
    self.assertIn("generated output is missing or stale", "\n".join(check_outputs(self.root, catalog)))

def test_nonempty_catalog_preserves_data_counts_links_and_semantic_order(self) -> None:
    self.fixture.create_mixed_catalog_fixture(
        mapping_set_versions=("0.10.0", "0.2.0"),
        lifecycle_states=("deprecated", "published"),
        dispositions=("mapped", "no_direct_mapping", "out_of_scope"),
        include_both_directions=True,
    )
    result = validate(self.root)
    self.assertEqual(result.errors, [])
    catalog = build_catalog(result)
    self.assertEqual(catalog["counts"]["mapping_sets"], 2)
    self.assertEqual(catalog["counts"]["provisions"], 6)
    self.assertEqual(catalog["counts"]["relationships"], 4)
    self.assertEqual(catalog["counts"]["negative_dispositions"], 4)
    self.assertEqual(catalog["counts"]["by_direction"], {"esaf_to_external": 2, "external_to_esaf": 2})
    self.assertEqual(catalog["counts"]["by_disposition"], {"mapped": 2, "no_direct_mapping": 2, "out_of_scope": 2})
    self.assertEqual(
        [item["metadata"]["mapping_set_version"] for item in catalog["mapping_sets"]],
        ["0.2.0", "0.10.0"],
    )
    for mapping_set in catalog["mapping_sets"]:
        self.assertIn(mapping_set["lifecycle"]["events"][-1]["state"], {"published", "deprecated"})
        mapped = next(item for item in mapping_set["provisions"] if item["metadata"]["disposition"] == "mapped")
        self.assertEqual(
            {leg["direction"] for leg in mapped["metadata"]["relationships"]},
            {"esaf_to_external", "external_to_esaf"},
        )
        self.assertTrue(mapped["path"].endswith(f"{mapped['metadata']['record_id']}.md"))
    first_json = render_json(catalog)
    first_markdown = render_markdown(catalog)
    self.assertEqual(first_json, render_json(catalog))
    self.assertEqual(first_markdown, render_markdown(catalog))
    for heading in (
        "## Active published mapping sets",
        "## Reviewed and draft work",
        "## Deprecated and retired history",
        "## Coverage and gaps",
    ):
        self.assertIn(heading, first_markdown)
```

- [ ] **Step 2: Verify the tests fail before catalog implementation**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_validate_crosswalks -v`

Expected: FAIL because catalog functions and CLI do not exist.

- [ ] **Step 3: Implement complete forward/reverse catalog data**

```python
def render_json(catalog: dict[str, object]) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=True) + "\n"

def render_markdown(catalog: dict[str, object]) -> str:
    lines = [
        "# ESAF Standards Crosswalk Catalog", "",
        "> Generated by `tools/validate_crosswalks.py`. Do not edit directly.", "",
    ]
    if catalog["counts"]["mapping_sets"] == 0:
        lines.extend(["No mapping sets have been assessed or approved.", ""])
    return "\n".join(lines).rstrip() + "\n"
```

The JSON catalog shall include schema version, generated-source declaration, separate counts by editorial/lifecycle/provision state and every mapping dimension, complete snapshot/inventory/provision/leg metadata, negative dispositions, and lifecycle links. Sort by authority, publication, normalized source version, normalized ESAF release, numeric mapping-set version tuple, external provision ID, record ID, control ID, and direction.

Use this exact generated shape:

```text
catalog
  schema_version: "1.0.0"
  generated_from: "crosswalks/mappings/** and crosswalks/registry/*.md"
  counts:
    mapping_sets, provisions, relationships, negative_dispositions: integer
    by_snapshot_status, by_lifecycle_state, by_provision_status,
    by_authority, by_publication, by_source_version, by_esaf_release,
    by_disposition, by_relationship, by_direction, by_coverage,
    by_confidence: sorted string-to-integer objects
  mapping_sets: mapping-set-view[]

mapping-set-view
  path: repository-relative POSIX path
  metadata: complete parsed mapping-set metadata
  inventory: complete parsed inventory metadata
  lifecycle: complete parsed lifecycle metadata or null
  provisions: provision-view[]

provision-view
  path: repository-relative POSIX path
  metadata: complete parsed provision metadata including every directional leg
```

`CATALOG.md` uses the fixed section order `Active published mapping sets`, `Reviewed and draft work`, `Deprecated and retired history`, and `Coverage and gaps`. Each row links the authoritative snapshot or provision. The empty catalog retains all headings and states that no mapping set has been assessed; it never labels an external source mapped or unmapped.

- [ ] **Step 4: Implement CLI modes and deterministic errors**

```python
parser = argparse.ArgumentParser(description=__doc__)
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument("--check", action="store_true")
mode.add_argument("--write", action="store_true")
parser.add_argument("--baseline-ref")
```

`--write` writes only when validation succeeds. `--check` compares exact expected bytes with both generated files. Print sorted errors as `- {path}: {field or rule}: {observed problem}; required: {correction}` and return 1 on any error.

- [ ] **Step 5: Generate the initial empty catalogs and run CLI tests**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_crosswalks.py --write`

Expected: reports 0 mapping sets, 0 provisions, 0 relationships, and 0 negative dispositions.

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_crosswalks.py --check`

Expected: PASS with the same counts.

- [ ] **Step 6: Commit**

```shell
git add tools/crosswalks tools/validate_crosswalks.py tests/test_validate_crosswalks.py crosswalks/catalog.json crosswalks/CATALOG.md
git commit -m "Generate ESAF-1600 crosswalk catalogs"
```

### Task 6: Publish the normative methodology and authoring templates

**Files:**
- Create: `crosswalks/ESAF-1600.md`
- Create: `crosswalks/MAPPING_SET_TEMPLATE.md`
- Create: `crosswalks/PROVISION_INVENTORY_TEMPLATE.md`
- Create: `crosswalks/CROSSWALK_TEMPLATE.md`
- Create: `crosswalks/LIFECYCLE_RECORD_TEMPLATE.md`
- Create: `crosswalks/mappings/.gitkeep`
- Create: `crosswalks/registry/.gitkeep`
- Create: `tests/test_esaf_1600_foundation.py`

**Interfaces:**
- Consumes: exact schema field names and validator semantics from Tasks 1–5.
- Produces: normative and example contracts linked by later repository documentation.

- [ ] **Step 1: Write failing foundation-document tests**

```python
def test_required_foundation_files_exist(self) -> None:
    for relative in REQUIRED_CROSSWALK_FILES:
        self.assertTrue((ROOT / relative).is_file(), relative)

def test_methodology_prohibits_compliance_equivalence(self) -> None:
    text = (ROOT / "crosswalks/ESAF-1600.md").read_text(encoding="utf-8")
    self.assertIn("shall not establish certification, compliance, equivalence, or legal sufficiency", text)

def test_templates_are_outside_mapping_discovery(self) -> None:
    result = validate(ROOT)
    self.assertEqual(result.mapping_sets, [])

def test_lifecycle_template_contains_complete_valid_chain(self) -> None:
    metadata, _ = parse_front_matter(ROOT / "crosswalks/LIFECYCLE_RECORD_TEMPLATE.md")
    self.assertEqual(
        [event["state"] for event in metadata["events"]],
        ["approved", "published", "deprecated", "retired"],
    )
    self.assertEqual(validate_lifecycle([metadata]), [])

def test_mapping_set_template_is_schema_valid(self) -> None:
    metadata, _ = parse_front_matter(ROOT / "crosswalks/MAPPING_SET_TEMPLATE.md")
    self.assertEqual(schema_errors(self.validators["mapping-set"], metadata, "template"), [])

def test_inventory_template_demonstrates_both_scope_types(self) -> None:
    examples = extract_yaml_blocks(ROOT / "crosswalks/PROVISION_INVENTORY_TEMPLATE.md")
    self.assertEqual({item["scope_type"] for item in examples}, {"complete_publication", "declared_subset"})
    for item in examples:
        self.assertEqual(schema_errors(self.validators["provision-inventory"], item, "template"), [])

def test_crosswalk_template_examples_are_schema_valid_and_complete(self) -> None:
    examples = extract_yaml_blocks(ROOT / "crosswalks/CROSSWALK_TEMPLATE.md")
    for item in examples:
        self.assertEqual(schema_errors(self.validators["mapping-record"], item, "template"), [])
    mapped = next(item for item in examples if item["disposition"] == "mapped" and item["granularity"] == "requirement")
    self.assertEqual({leg["direction"] for leg in mapped["relationships"]}, {"esaf_to_external", "external_to_esaf"})
    clause = next(item for item in examples if item["granularity"] == "clause")
    self.assertTrue(clause["granularity_exception"])
    self.assertEqual(
        {item["disposition"] for item in examples},
        {"mapped", "no_direct_mapping", "out_of_scope"},
    )
```

- [ ] **Step 2: Run and verify missing-file failures**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation -v`

Expected: FAIL listing the five missing foundation files.

- [ ] **Step 3: Author ESAF-1600 from the approved design**

Include normative sections for purpose/scope, authority boundaries, record model, repository paths, canonical IDs, completeness, mapping taxonomy, negative dispositions, review/findings, publication rights, manifest provenance, snapshot/event digests, lifecycle, validation, generated catalogs, and adoption disclaimers. Keep implementation examples in templates, not the normative standard.

- [ ] **Step 4: Author schema-valid templates**

Use non-authoritative example identifiers under the repository root, never under `crosswalks/mappings/`. `MAPPING_SET_TEMPLATE.md` uses YAML front matter. `PROVISION_INVENTORY_TEMPLATE.md` contains exactly two fenced YAML documents, one per scope type. `CROSSWALK_TEMPLATE.md` contains fenced YAML records for a requirement-level mapped record with two asymmetric directional legs, a clause-level exception, `no_direct_mapping`, and `out_of_scope`. `LIFECYCLE_RECORD_TEMPLATE.md` uses YAML front matter containing a schema-valid four-event `approved -> published -> deprecated -> retired` chain, predecessor/successor linkage, snapshot digest, previous-event digest chaining, and the frozen canonical Unicode digest vector from Task 4. Template validation parses only these explicitly named files/blocks and does not treat them as repository mapping or lifecycle records.

- [ ] **Step 5: Run focused tests and commit**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation tests.test_crosswalk_schemas -v`

Expected: PASS.

```shell
git add crosswalks/ESAF-1600.md crosswalks/*_TEMPLATE.md crosswalks/mappings/.gitkeep crosswalks/registry/.gitkeep tests/test_esaf_1600_foundation.py
git commit -m "Publish ESAF-1600 methodology foundation"
```

### Task 7: Migrate control mapping authority to ESAF-1600

**Files:**
- Modify: `controls/ESAF-1100.md`
- Modify: `controls/CONTROL_TEMPLATE.md`
- Modify: all 91 control records under the 16 `controls/FAMILY/CONTROL-ID.md` paths
- Create: `tools/migrate_control_mappings.py`
- Modify: `tools/validate_controls.py`
- Modify: `tests/test_esaf_1600_foundation.py`

**Interfaces:**
- Produces one canonical control-section sentence:
  `Authoritative external mappings are maintained in the [ESAF-1600 generated catalog](../../crosswalks/CATALOG.md).`
- Produces: `split_external_mapping(text: str) -> tuple[str, str, str]`
- Produces: `replace_external_mapping(text: str, replacement: str) -> str`
- Consumes the crosswalk generated catalog from Task 5.

- [ ] **Step 1: Write failing migration-invariant tests**

```python
def test_every_control_delegates_external_mapping_authority(self) -> None:
    records = control_record_paths(ROOT)
    self.assertEqual(len(records), len(json.loads((ROOT / "controls/catalog.json").read_text())["controls"]))
    for path in records:
        section = markdown_section(path.read_text(encoding="utf-8"), "External mappings")
        self.assertEqual(section, CANONICAL_EXTERNAL_MAPPING_LINK)

def test_esaf_1100_defers_taxonomy_to_esaf_1600(self) -> None:
    text = (ROOT / "controls/ESAF-1100.md").read_text(encoding="utf-8")
    self.assertNotIn("| equivalent |", text)
    self.assertIn("ESAF-1600 is authoritative", text)

def test_mapping_migration_preserves_every_byte_outside_section(self) -> None:
    before = (
        "# IAM-100 Example\n\n## External mappings\n\nOld text.\n\n"
        "## Change history\n\nHistory.\n"
    )
    prefix, _old, suffix = split_external_mapping(before)
    after = replace_external_mapping(before, CANONICAL_EXTERNAL_MAPPING_LINK)
    new_prefix, new_section, new_suffix = split_external_mapping(after)
    self.assertEqual((new_prefix, new_suffix), (prefix, suffix))
    self.assertEqual(new_section, CANONICAL_EXTERNAL_MAPPING_LINK)
```

- [ ] **Step 2: Verify the migration tests fail against current controls**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation -v`

Expected: FAIL because controls still contain release-specific absence statements.

- [ ] **Step 3: Mechanically replace all control mapping sections**

Implement `tools/migrate_control_mappings.py` with a compiled multiline expression anchored at `^## External mappings$` and the next `^## ` heading. `split_external_mapping` returns the exact prefix, stripped section content, and exact suffix. `replace_external_mapping` reconstructs `prefix + canonical heading/content + suffix` without normalizing the prefix or suffix. Its `--check` mode reports any catalog-derived control whose section differs; its `--write` mode updates only those catalog-derived records. Derive the record set from `controls/catalog.json`; do not hardcode 91 paths.

- [ ] **Step 4: Enforce the durable link in control validation**

```python
EXPECTED_EXTERNAL_MAPPING = (
    "Authoritative external mappings are maintained in the "
    "[ESAF-1600 generated catalog](../../crosswalks/CATALOG.md)."
)

external = section(body, "External mappings")
if external != EXPECTED_EXTERNAL_MAPPING:
    errors.append(f"{relative}: External mappings must delegate to ESAF-1600")
```

Use the equivalent `../crosswalks/CATALOG.md` path in `CONTROL_TEMPLATE.md`, because the template is one directory higher than control records.

- [ ] **Step 5: Run migration, control, and full tests**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation -v`

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/migrate_control_mappings.py --check`

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python tools/validate_controls.py --check`

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover -s tests -v`

Expected: all PASS; control count remains catalog-derived and every non-mapping control byte is unchanged by review.

- [ ] **Step 6: Commit**

```shell
git add controls tools/migrate_control_mappings.py tools/validate_controls.py tests/test_esaf_1600_foundation.py
git commit -m "Delegate control mappings to ESAF-1600"
```

### Task 8: Update project governance and crosswalk landing pages

**Files:**
- Modify: `crosswalks/README.md`
- Modify: `crosswalks/pci-dss.md`
- Modify: `crosswalks/hitrust-csf.md`
- Modify: `crosswalks/uk-cyber-essentials.md`
- Modify: `CONTRIBUTING.md`
- Modify: `project/DECISION_LOG.md`
- Modify: `tools/README.md`
- Modify: `tests/test_esaf_1600_foundation.py`

**Interfaces:**
- Consumes: normative ESAF-1600 and CLI paths.
- Produces: durable contributor, decision, and operational guidance.

- [ ] **Step 1: Add failing governance-document tests**

```python
def test_landing_pages_remain_planned_and_link_methodology(self) -> None:
    for name in ("pci-dss.md", "hitrust-csf.md", "uk-cyber-essentials.md"):
        text = (ROOT / "crosswalks" / name).read_text(encoding="utf-8")
        self.assertIn("**Status:** Planned", text)
        self.assertIn("[ESAF-1600](ESAF-1600.md)", text)

def test_contributing_requires_rights_provenance(self) -> None:
    text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    for phrase in ("publication-rights basis", "authorized source access", "intellectual-property attestation"):
        self.assertIn(phrase, text)
```

- [ ] **Step 2: Verify the focused tests fail before documentation changes**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation -v`

Expected: FAIL on missing methodology links and rights language.

- [ ] **Step 3: Update repository guidance without claiming completed mappings**

Replace `strength` in `crosswalks/README.md` with relationship, direction, coverage, and confidence. Link the standard, templates, generated catalogs, and validation commands. Keep all three priority landing pages `Planned` and explicitly state that no substantive mapping is approved.

Add contribution requirements for source identity/version, publication-rights basis, permitted/prohibited elements, authorized-access attestations, mapper/reviewer independence, and an intellectual-property attestation.

- [ ] **Step 4: Record the eleven accepted ESAF-1600 decisions**

Append `DEC-0015` through `DEC-0025` for: Markdown authority; deterministic derivatives; separate dimensions; explicit negative dispositions; independent review; approved-snapshot immutability; external append-only lifecycle; provision-inventory completeness; release-pinned control manifests; ESAF-1600 taxonomy authority; and restricted-text exclusion/publication-rights recording.

- [ ] **Step 5: Document CLI use and commit**

Add `--write`, `--check`, and `--baseline-ref` examples to `tools/README.md`, including the requirement for full Git history.

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation -v`

Expected: PASS.

```shell
git add crosswalks CONTRIBUTING.md project/DECISION_LOG.md tools/README.md tests/test_esaf_1600_foundation.py
git commit -m "Document ESAF-1600 governance and contribution rules"
```

### Task 9: Integrate crosswalk validation with continuous integration

**Files:**
- Modify: `.github/workflows/catalog-validation.yml`
- Modify: `tests/test_esaf_1600_foundation.py`

**Interfaces:**
- Consumes: `tools/validate_crosswalks.py` CLI.
- Produces: current-tree and trusted-baseline validation on pull requests and protected-branch pushes.

- [ ] **Step 1: Write failing workflow-contract tests**

```python
def test_ci_fetches_history_and_runs_crosswalk_validation(self) -> None:
    workflow = (ROOT / ".github/workflows/catalog-validation.yml").read_text(encoding="utf-8")
    self.assertIn("fetch-depth: 0", workflow)
    self.assertIn("python tools/validate_crosswalks.py --check", workflow)
    self.assertIn("--baseline-ref", workflow)
    self.assertIn('"crosswalks/**"', workflow)
```

- [ ] **Step 2: Verify the workflow test fails**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation -v`

Expected: FAIL because checkout is shallow and crosswalk paths/commands are absent.

- [ ] **Step 3: Add full-history and baseline-aware workflow steps**

```yaml
- name: Check out repository
  uses: actions/checkout@v5
  with:
    fetch-depth: 0
- name: Validate crosswalk catalog
  run: python tools/validate_crosswalks.py --check
- name: Validate crosswalk history on pull request
  if: github.event_name == 'pull_request'
  run: python tools/validate_crosswalks.py --check --baseline-ref "${{ github.event.pull_request.base.sha }}"
- name: Validate crosswalk history on protected-branch push
  if: github.event_name == 'push' && github.event.before != '0000000000000000000000000000000000000000'
  run: python tools/validate_crosswalks.py --check --baseline-ref "${{ github.event.before }}"
```

Add `crosswalks/**`, `tools/crosswalks/**`, and `tools/validate_crosswalks.py` to pull-request and push path filters. Retain all existing control and architecture validation.

- [ ] **Step 4: Run workflow and full repository tests, then commit**

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_esaf_1600_foundation -v`

Run: `$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover -s tests -v`

Expected: PASS.

```shell
git add .github/workflows/catalog-validation.yml tests/test_esaf_1600_foundation.py
git commit -m "Validate ESAF-1600 crosswalks in CI"
```

### Task 10: Perform whole-foundation verification and independent review

**Files:**
- Create: `docs/superpowers/reviews/2026-07-13-esaf-1600-foundation-traceability.md`
- Modify only files required to resolve verified Critical or Important findings.

**Interfaces:**
- Consumes: every prior task deliverable.
- Produces: a review-ready ESAF-1600 foundation branch with recorded validation evidence.

- [ ] **Step 1: Regenerate and verify all derived artifacts**

Run: `$env:PYTHONDWRITEBYTECODE='1'; python tools/validate_crosswalks.py --write`

Run: `$env:PYTHONDWRITEBYTECODE='1'; python tools/validate_crosswalks.py --check`

Expected: zero mapping sets/provisions/relationships/negative dispositions and current generated files.

- [ ] **Step 2: Run every repository gate from a clean process**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s tests -v
python tools/validate_controls.py --check
python tools/validate_architectures.py
python tools/validate_crosswalks.py --check
git diff --check
```

Expected: all commands exit 0; no `__pycache__`, generated cache, or unrelated files appear in `git status --short`.

- [ ] **Step 3: Create and commit the implementation traceability review**

Create `docs/superpowers/reviews/2026-07-13-esaf-1600-foundation-traceability.md` with one row per normative requirement from Sections 5–19 of the approved design and the columns `Spec section`, `Requirement`, `Implementation file/function`, `Focused test`, and `Result`. Every result shall be `Pass`; resolve uncovered requirements before committing the artifact.

```shell
git add docs/superpowers/reviews/2026-07-13-esaf-1600-foundation-traceability.md
git commit -m "Record ESAF-1600 implementation traceability"
```

- [ ] **Step 4: Request independent specification and whole-branch review**

Ask one reviewer to compare implementation against the approved design and another to inspect the complete branch diff for security, provenance, lifecycle, licensing, deterministic-output, and migration defects. Resolve every Critical and Important finding with a regression test before changing implementation.

- [ ] **Step 5: Re-run all gates after the final fix commit**

Repeat the commands from Step 2 after the branch head changes. Record the reviewed head SHA and exact test counts in the pull-request description.

- [ ] **Step 6: Commit final review-driven corrections**

```powershell
$changes = git status --short
$changes
if ($changes | Where-Object { $_ -notmatch '^.. (crosswalks/|controls/|tools/|tests/|docs/superpowers/reviews/|CONTRIBUTING\.md|project/DECISION_LOG\.md|\.github/workflows/catalog-validation\.yml)' }) {
    throw "Unrelated path present; stop before staging"
}
git add -A
git diff --cached --name-only
git commit -m "Harden ESAF-1600 foundation"
```

Skip this commit when review produces no corrections. Push the branch, open a draft pull request, verify the live PR head equals the reviewed SHA, require passing GitHub checks and a clean merge state, then mark the PR ready for review.
