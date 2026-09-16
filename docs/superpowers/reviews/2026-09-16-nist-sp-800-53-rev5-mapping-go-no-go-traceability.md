# NIST SP 800-53 Rev. 5 mapping go/no-go traceability (Issue #194)

## Decisions

- `I194-D1`: Pin NIST.SP.800-53r5 / SP 800-53 Rev. 5 public PDF identity (SHA-256, byte length, page count, publication date) and OSCAL catalog 5.2.0 inventory source digest.
- `I194-D2`: Record publication-rights PASS for all six ESAF-1600 field classes under U.S. government work / NIST technical-series practice.
- `I194-D3`: Publish a complete 1196-identifier control and enhancement inventory with canonical digest.
- `I194-D4`: Record mechanical readiness decision `HOLD` because mapper and independent reviewers are unnamed.
- `I194-D5`: Freeze generated crosswalk catalog counts at 3 / 404 / 81 / 325 with NIST SP 800-53 mapping artifacts at `0`.

## Artifacts

- `I194-A1`: `docs/superpowers/reviews/2026-09-16-nist-sp-800-53-publication-rights-review.md`
- `I194-A2`: `docs/superpowers/specs/2026-09-16-nist-sp-800-53-source-readiness-oracle.json`
- `I194-A3`: `docs/superpowers/specs/2026-09-16-nist-sp-800-53-rev5-control-inventory.json`
- `I194-A4`: `docs/superpowers/specs/2026-09-16-nist-sp-800-53-mapping-readiness-matrix.json`
- `I194-A5`: `docs/superpowers/reviews/2026-09-16-nist-sp-800-53-rev5-mapping-go-no-go-review.md`
- `I194-A6`: `crosswalks/nist-sp-800-53.md`

## Boundaries

- `I194-B1`: Do not create NIST SP 800-53 mapping records, snapshots, registry entries, or catalog increments while HOLD.
- `I194-B2`: Do not close Issue #55 or Issue #60.
- `I194-B3`: Do not claim NIST approval, endorsement, certification, equivalence, compliance, or assurance.
