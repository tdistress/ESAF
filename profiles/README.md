# ESAF-1800 Profiles

The normative [ESAF-1800 profile contract](ESAF-1800.md) defines how industry,
jurisdiction, and risk profiles tailor the core ESAF baseline without changing
control meanings.

## Profile index

| Profile | Version | Status |
|---|---|---|
| [United Kingdom jurisdiction profile](uk/0.1.0/README.md) | 0.1.0 | Draft |

## Shared assessment semantics

Each profile shall reuse the determinations, evidence-quality attributes,
assessment-result contract, and maturity levels defined by
[ESAF-1500](../assessment/ESAF-1500.md). A profile may add stricter evidence
or maturity criteria, but shall not weaken cumulative prerequisites, shall not
treat maturity as conformance, and shall not define a profile-local replacement maturity scale.

## Editing profiles

Create or edit versioned profile packages only under
`profiles/<profile-domain>/<version>/`, where the profile domain identifies
the jurisdiction, industry, sector, or risk context. Package changes shall
preserve the component structure and identifiers defined by ESAF-1800 and its
schemas. Manifest component values are package-relative component paths;
component `$schema` values are document-relative schema locators.

`proposed` remains a valid earlier lifecycle state. A profile shall not advance
beyond Draft until the applicable technical, editorial, scope, and
overclaiming reviews and publication gates are complete. Profiles shall not
claim compliance, certification, equivalence, endorsement, legal sufficiency,
external approval, or production readiness.

Validate profile contract, schema, package, or index changes from the
repository root:

```shell
python tools/validate_profiles.py --check
```
