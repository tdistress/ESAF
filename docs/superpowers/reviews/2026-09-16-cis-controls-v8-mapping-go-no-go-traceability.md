# CIS Controls Version 8 mapping go/no-go traceability (Issue #206)

## Decisions

- `I206-D1`: Pin CIS Controls Version 8 (v8) public source identity (landing, free registration download, Navigator inventory source) and record Version 8.1 as an adjacent unpinned iterative update.
- `I206-D2`: Record publication-rights HOLD under CC BY-NC-ND 4.0: permit identifiers, titles, structural inventory, and official links; prohibit paraphrases and derivative mapping analysis without CIS commercial-use approval.
- `I206-D3`: Publish a complete 153-identifier Safeguard inventory with canonical digest derived from the official public CIS Controls Navigator v8; do not commit CIS PDF/Excel package bytes.
- `I206-D4`: Record mechanical readiness decision `HOLD` because publication rights and mapper/independent reviewers are blocked.
- `I206-D5`: Freeze generated crosswalk catalog counts at 3 / 404 / 81 / 325 with CIS Controls mapping artifacts at `0`.

## Artifacts

- `I206-A1`: `docs/superpowers/reviews/2026-09-16-cis-controls-v8-publication-rights-review.md`
- `I206-A2`: `docs/superpowers/specs/2026-09-16-cis-controls-v8-source-readiness-oracle.json`
- `I206-A3`: `docs/superpowers/specs/2026-09-16-cis-controls-v8-safeguard-inventory.json`
- `I206-A4`: `docs/superpowers/specs/2026-09-16-cis-controls-v8-mapping-readiness-matrix.json`
- `I206-A5`: `docs/superpowers/reviews/2026-09-16-cis-controls-v8-mapping-go-no-go-review.md`
- `I206-A6`: `crosswalks/cis-controls.md`

## Boundaries

- `I206-B1`: Do not create CIS Controls mapping records, snapshots, registry entries, or catalog increments while HOLD.
- `I206-B2`: Do not close Issue #55 or Issue #60.
- `I206-B3`: Do not claim CIS approval, endorsement, certification, equivalence, compliance, or assurance.
