# Task 1 report: reviewed validation policy

## Scope completed

- Deleted `tools/validation-plans.json`; planner command definitions and path-routing rules are no longer read from candidate-controlled JSON.
- Added frozen in-memory `ValidationPolicy` records and reviewed immutable `COMMAND_CATALOG`, `ROUTING_RULES`, `PUBLICATION_COMMAND_IDS`, and `PROOF_COMMAND_IDS` constants in `tools/plan_validation.py`.
- Added `validate_policy(policy)` to fail closed on malformed in-memory command and route records before planning.
- Kept the command catalog fixed, including `git diff --check {base} {candidate}`, link validation with `--check`, and qualified-review proof validation with `--check --candidate-sha {candidate}`.
- Made publication selection consume the separately declared ordered publication IDs.
- Updated planner tests to construct synthetic `ValidationPolicy` instances, reject invalid policy records, and lock the reviewed catalog, publication order, proof IDs, and argv templates.

## TDD evidence

The focused suite was run immediately after the new tests were added and before the implementation. It failed at import with:

```text
ImportError: cannot import name 'COMMAND_CATALOG' from 'tools.plan_validation'
```

This was the expected red state because the JSON-backed implementation did not yet provide the reviewed in-memory policy API.

## Verification

```text
python -B -m unittest tests/test_plan_validation.py -v
Ran 14 tests ... OK

python tools/validate_test_shards.py --check
profile_validation: 1
qualified_review_evidence: 1
mapping_review_bundle: 1
remaining: 31
total tracked: 34
```

`git diff --check` also completed without whitespace errors.

## Scope boundary and follow-up

The full repository suite is intentionally deferred to the final hardening task because Task 4 will update the workflow/foundation references that still name the deleted policy file. Existing untracked Python cache directories were preserved and not staged.

## Round 1 review resolution

The static catalog regression test now asserts the entire ordered `COMMAND_CATALOG` identifier sequence and a hand-authored exact argv tuple for every command identifier. It retains explicit denial of generic `qualified-review` and `mapping-review` commands and also denies the known stateful/human-evidence/arbitrary-input command identifiers.

A mutation check temporarily inserted a generic `mapping-review` command that invoked `tools/build_mapping_review_bundle.py --output temporary`. The focused catalog test failed at the exact ordered identifier assertion, proving that any added command—including a stateful, human-evidence, or arbitrary-input command—fails the contract. The temporary mutation was removed before final verification.
