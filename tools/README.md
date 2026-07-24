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

## Release-gate validation

Validate the authoritative 0.4-alpha readiness record without changing files:

```shell
python tools/release_gates.py --check
```

Exact candidate, approval, merge, and tag SHAs remain in GitHub evidence and an
external temporary JSON file; they are never written into the tracked record.

## Mermaid publication rendering

Inventory every tracked Mermaid block and write temporary renderer inputs beneath the system temporary directory, outside the repository:

```powershell
$renderDirectory = python -c "import tempfile; print(tempfile.mkdtemp(prefix='esaf-v04-mermaid-'))"
python tools/mermaid_inventory.py --output-dir $renderDirectory --write
```

Render each input with `@mermaid-js/mermaid-cli@11.16.0`, then record parse and readability dispositions in the tracked release ledger. Parser success does not replace visual review.

## Qualified mapping review packages

Generate one reviewer package from an exact commit.
Supply a new output path that does not already exist and is outside every Git
worktree:

```powershell
$candidate = git rev-parse HEAD
$output = Join-Path ([System.IO.Path]::GetTempPath()) "esaf-uk-review-core"
python tools/build_mapping_review_bundle.py `
  --commit $candidate `
  --mapping-set-id uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0 `
  --output $output
```

Repeat with each allowlisted mapping-set identifier and a distinct new output
path. Preserve the exact commit and printed manifest SHA-256 in the review
record.

The package contains tracked ESAF mapping evidence, referenced controls,
schemas, protocol, and blank worksheets. It does not include the external source document. Reviewers obtain authorized access independently. Package generation does not change Draft lifecycle state or constitute qualified review.
