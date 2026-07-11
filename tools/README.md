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
