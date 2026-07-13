# Provision mapping authoring template

All YAML documents below are non-authoritative examples. They demonstrate record shape and analytical distinctions; they do not map a real external publication.

## Requirement-level mapped record with asymmetric directions

```yaml
schema_version: 1.0.0
record_id: ex-1-1
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.0
status: draft
external_provision_id: EX-1.1
granularity: requirement
context:
  mode: paraphrase
  summary: The example provision assigns governance responsibility.
source_locator:
  official_url: https://example.com/example-standard#ex-1-1
  locator: EX-1.1
disposition: mapped
relationships:
  - esaf_control_id: GOV-100
    esaf_control_version: 1.0.0
    relationship: supports
    direction: esaf_to_external
    coverage: partial
    confidence: high
    rationale: The ESAF control directly contributes governance evidence to the example outcome.
    conditions:
      - The control is implemented across the assessed scope.
    expected_evidence:
      - Approved governance charter
    known_gaps:
      - The example provision also expects source-specific responsibilities.
  - esaf_control_id: GOV-100
    esaf_control_version: 1.0.0
    relationship: informs
    direction: external_to_esaf
    coverage: contextual
    confidence: medium
    rationale: The example provision provides context for assigning the ESAF control owner.
    conditions:
      - The external publication applies to the organization.
    expected_evidence:
      - Responsibility assignment record
    known_gaps:
      - The provision does not address the full ESAF governance outcome.
mapper:
  id: mapper-1
  date: "2026-07-13"
change_history:
  - version: 1.0.0
    date: "2026-07-13"
    change: Created the non-authoritative mapped example.
```

## Controlled clause-level exception

```yaml
schema_version: 1.0.0
record_id: ex-2-1-a
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.0
status: draft
external_provision_id: EX-2.1(a)
granularity: clause
granularity_exception: The example publication provides no independently addressable requirement below this clause.
context:
  mode: identifier_only
  omission_rationale: The example rights boundary permits identifiers but not a provision summary.
source_locator:
  official_url: https://example.com/example-standard#ex-2-1-a
  locator: EX-2.1(a)
disposition: mapped
relationships:
  - esaf_control_id: IAM-100
    esaf_control_version: 1.0.0
    relationship: partially_supports
    direction: esaf_to_external
    coverage: narrow
    confidence: medium
    rationale: The ESAF control addresses one identifiable element of the clause.
    conditions:
      - Identity scope matches the assessed system boundary.
    expected_evidence:
      - Authentication configuration record
    known_gaps:
      - Other clause elements require separate controls.
mapper:
  id: mapper-1
  date: "2026-07-13"
change_history:
  - version: 1.0.0
    date: "2026-07-13"
    change: Created the non-authoritative clause example.
```

## No direct mapping

```yaml
schema_version: 1.0.0
record_id: ex-1-2
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.0
status: draft
external_provision_id: EX-1.2
granularity: requirement
context:
  mode: paraphrase
  summary: The example provision addresses a source-specific administrative outcome.
source_locator:
  official_url: https://example.com/example-standard#ex-1-2
  locator: EX-1.2
disposition: no_direct_mapping
relationships: []
negative_rationale: No ESAF control directly addresses the source-specific outcome; omission is recorded as an assessed gap.
mapper:
  id: mapper-1
  date: "2026-07-13"
change_history:
  - version: 1.0.0
    date: "2026-07-13"
    change: Created the non-authoritative gap example.
```

## Out of declared scope

```yaml
schema_version: 1.0.0
record_id: ex-3-1
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.0
status: draft
external_provision_id: EX-3.1
granularity: requirement
context:
  mode: identifier_only
  omission_rationale: Only the identifier is necessary to substantiate the scope assessment.
source_locator:
  official_url: https://example.com/example-standard#ex-3-1
  locator: EX-3.1
disposition: out_of_scope
relationships: []
negative_rationale: The provision concerns a product class excluded by the mapping set's documented assessment boundary.
mapper:
  id: mapper-1
  date: "2026-07-13"
change_history:
  - version: 1.0.0
    date: "2026-07-13"
    change: Created the non-authoritative scope example.
```
