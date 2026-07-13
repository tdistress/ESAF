# Provision inventory authoring template

These two YAML documents are non-authoritative examples. Use exactly one scope model in an authoritative `PROVISION_INVENTORY.md`; rights metadata remains in the mapping-set record.

## Complete-publication scope

```yaml
schema_version: 1.0.0
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.0
scope_type: complete_publication
scope_statement: Every provision in the non-authoritative example publication is inventoried.
source_basis: Official example publication structure; identifiers may be published under the recorded rights review.
expected_count: 4
provision_ids:
  - EX-1.1
  - EX-1.2
  - EX-2.1(a)
  - EX-3.1
```

## Declared-subset scope

```yaml
schema_version: 1.0.0
mapping_set_id: example-authority--example-standard--2026.1--esaf-0.5-beta--1.0.1
scope_type: declared_subset
scope_statement: Only the governance chapter identified as EX-1 is assessed; this is not publication-wide coverage.
source_basis: Official example chapter inventory; identifiers may be published under the recorded rights review.
expected_count: 2
provision_ids:
  - EX-1.1
  - EX-1.2
```
