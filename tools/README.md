# Tooling

Validation, publication, assessment, and repository-maintenance tools will be maintained here. Generated artifacts should not replace authoritative Markdown sources.

## Control catalog validation

Install the development dependencies and validate the catalog:

```shell
python -m pip install --requirement requirements-dev.txt
python tools/validate_controls.py --check
```

After an intentional control-source change, regenerate the derived catalog files and then validate them:

```shell
python tools/validate_controls.py --write
python tools/validate_controls.py --check
```

The validator enforces metadata schema conformance, identifier and family consistency, objective coverage, required sections, assessment syntax, related-control resolution, numbering, family indexes, and generated-output currency. Markdown control files remain authoritative.

## Crosswalk validation

After an intentional authoritative crosswalk change, validate the records and rewrite the deterministic human- and machine-readable catalogs:

```shell
python tools/validate_crosswalks.py --write
```

Check authoritative records and require generated outputs to be present and current without rewriting them:

```shell
python tools/validate_crosswalks.py --check
```

When a trusted comparison commit is available, also enforce approved-snapshot immutability and append-only lifecycle history:

```shell
python tools/validate_crosswalks.py --check --baseline-ref <trusted-commit>
```

Historical control-manifest regeneration and `--baseline-ref` comparison require full Git history. Continuous-integration and local review checkouts shall fetch complete history before running these modes; a shallow checkout is insufficient.

## Architecture validation

Validate the ESAF-1200 foundation, pattern registry, pattern metadata and structure, links, control references, placeholders, and text encoding:

```shell
python -m unittest discover -s tests -v
python tools/validate_architectures.py
```

Architecture validation requires linked pattern records to match registry status, contain the complete pattern contract, and reference existing ESAF controls. It intentionally checks structural rules only. Technical reviewers remain responsible for the correctness of architecture decisions, diagrams, control allocation, and implementation guidance.
