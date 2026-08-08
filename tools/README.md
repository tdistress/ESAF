# Tooling

Validation, publication, assessment, and repository-maintenance tools will be maintained here. Generated artifacts should not replace authoritative Markdown sources.

## Time-budgeted validation

Use the planner to choose useful local work for the current change. It compares
the specified base and candidate commits, reports the resolved SHAs, and lists
the commands selected for each tier:

```powershell
python tools/plan_validation.py --base origin/main --candidate HEAD
```

The planner has three tiers.

- `quick` is a short preflight for a small work window. It checks the diff,
  verifies the shard manifest, and selects any directly affected checks.
- `standard` adds the relevant domain validator or complete test shard. It is
  useful before handing off a focused change or when there is time to follow a
  problem within one area.
- `publication` is for a frozen candidate. It includes the required complete
  local gates, publication rendering and link checks, exact-SHA proof where it
  applies, and independent review before a pull request, merge, or release.

The duration labels printed by the planner are planning aids based on observed
runs, not promises. Unknown, renamed, deleted, or cross-cutting paths, such as
workflow and validation-tool changes, escalate to `publication`. Required CI
remains authoritative. A passing `quick` or `standard` run neither replaces a
complete pull-request or publication gate nor carries forward after the
candidate SHA changes.

To run all manifest-defined shards concurrently during a longer local session:

```powershell
python tools/run_test_shards.py --all --parallel --durations 50
```

The existing sequential `--all` mode remains available when its ordered output
is more useful for diagnosis. Parallel mode waits for every selected shard and
reports each result.

## Assessment validation

Validate the ESAF-1500 schemas, tracked fictional examples, references, final
states, maturity prerequisites, component roll-ups, and non-claim boundaries:

```shell
python tools/validate_assessment.py --check
```

The validator does not score organizations.

## Profile validation

Validate ESAF-1800 schemas, Draft profile packages, control selections,
traceability, lifecycle-bound external references, and non-claim boundaries:

```shell
python tools/validate_profiles.py --check
```

The validator fails closed on malformed, incomplete, or semantically invalid
packages. It does not establish legal sufficiency, external-scheme assurance,
or production readiness.

Versioned packages reside at `profiles/<profile-domain>/<version>/`, where the
profile domain identifies the jurisdiction, industry, sector, or risk context.
Manifest component values are package-relative component paths; component
`$schema` values are document-relative schema locators.
Each package's `PROFILE.md` is the authoritative instance record. The
validator requires every adjacent derived JSON component to match its named
Markdown JSON block exactly.

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

## PCI DSS readiness validation

Validate the closed PCI DSS readiness matrix, derive the GO/HOLD decision, and
require the generated review to match without rewriting it:

```shell
python tools/render_pci_dss_mapping_go_no_go.py --check
```

The current decision is `HOLD`. This validation does not download or accept the
protected source, create a provision inventory or mapping, or assert compliance,
certification, equivalence, endorsement, authorization, coverage, or legal
sufficiency.

## Architecture validation

Validate the ESAF-1200 foundation, pattern registry, pattern metadata and structure, links, control references, placeholders, and text encoding:

```shell
python tools/validate_test_shards.py --check
python tools/run_test_shards.py --all --durations 50
python tools/validate_architectures.py
```

CI runs the same four manifest-defined shards in separate jobs and publishes one
aggregate required check.

Architecture validation requires linked pattern records to match registry status, contain the complete pattern contract, and reference existing ESAF controls. It intentionally checks structural rules only. Technical reviewers remain responsible for the correctness of architecture decisions, diagrams, control allocation, and implementation guidance.

## Release-gate validation

Validate the authoritative 0.4-alpha record and the current v0.5-beta
readiness record without changing files:

```shell
python tools/release_gates.py --check
python tools/v05_beta_release_gates.py --check
python -m tools.v05_beta_release_evidence --help
```

Use module invocation for the v0.5 evidence collector. The help command does
not fetch GitHub evidence. Operational collection requires the authenticated
resource identifiers and exact values documented by the command.

Release collection performs read-only clean-worktree and Python-cache
preflight checks before expensive commands, reports command durations and a
bounded output tail on failure, and retains the final clean-worktree and cache
results in release evidence. Taggable collection reuses candidate results only
after valid closure evidence binds the canonical results to the exact candidate
SHA and closure base; merge-head validation and fresh GitHub acquisition remain
mandatory.

Exact candidate, approval, merge, and tag SHAs remain in GitHub evidence and
an external temporary JSON file until durable publication evidence exists.

## Mermaid publication rendering

Inventory every tracked Mermaid block and write temporary renderer inputs beneath the system temporary directory, outside the repository:

```powershell
$renderDirectory = python -c "import tempfile; print(tempfile.mkdtemp(prefix='esaf-v04-mermaid-'))"
python tools/mermaid_inventory.py --output-dir $renderDirectory --write
```

Render each input with `@mermaid-js/mermaid-cli@11.16.0`, then record parse and readability dispositions in the tracked release ledger. Parser success does not replace visual review.

The v0.5 baseline validator requires the pinned renderer on `PATH` and renders
every block into a temporary directory:

```powershell
npm install --global @mermaid-js/mermaid-cli@11.16.0
python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
```

The v0.5 ledger records a render-contract digest, not a PNG digest. The
contract hashes canonical JSON containing the exact Mermaid source and digest,
diagram identity and type, pinned renderer and Node versions, render options,
and the complete `tools/mermaid-render-config.json` object. The validator
recomputes that contract and also requires all 23 operational renders to
succeed. Temporary PNG byte hashes are not a durable repository invariant
because browser rasterization can change antialiased pixels. The named visual
review remains a separate human attestation.

## Qualified mapping review packages

Qualified-review evidence is a two-stage, human-operated process. Create every
package, campaign directory, archive, seal record, and completed review record
outside every Git worktree, in an externally managed location whose retention
owner can preserve it. That location shall not be a Git repository, a path
inside a repository worktree, a symbolic-link or junction alias to one, or a
temporary location that cannot retain the final immutable record.

The candidate commit must equal the current clean HEAD of this module checkout.
A failed assembly can leave an owned hidden sibling staging directory; the
caller destination remains unpublished.

A campaign root contains the canonical `REVIEW_EVIDENCE.json` manifest and
only the package, attestation, and completed-worksheet files referenced by its
canonical relative paths. Keep the Draft and final-confirmation campaign roots
separate. The Draft seal record is written beside, not inside, the sealed
Draft campaign root; the deterministic ZIP archive and its immutable locator
are likewise external evidence.

Never commit the external source document, a completed attestation, a
completed worksheet, `REVIEW_EVIDENCE.json`, a campaign archive, or a seal
record. Git contains only the blank templates, schemas, protocol, and
automation. In particular, do not use a generated review package to
redistribute an authorized source document.
Each role attestation must include the reviewer’s separate
source-content-exclusion signature. Keep single-line reviewer prose to 512
characters or fewer, use locators instead of source excerpts, and record the
exact checksum and locator sets derived from the candidate package.

### Draft package and campaign

Generate one Draft reviewer package from the exact clean candidate commit.
Supply a distinct new output path outside every Git worktree for each
allowlisted mapping-set identifier. Each call shall use a new output path that
does not already exist:

```powershell
$draftCandidate = git rev-parse HEAD
$draftPackage = Join-Path $env:USERPROFILE "ESAF-review-evidence\draft-core-package"
python tools/build_mapping_review_bundle.py --candidate-state draft `
  --commit $draftCandidate `
  --mapping-set-id uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0 `
  --output $draftPackage
```

Record the exact candidate SHA and printed package-manifest SHA-256 in the
external campaign. The package contains repository evidence and blank forms;
it does not include the external source document. Reviewers obtain authorized
source access independently.

After the qualified human reviewers complete the two roles, validate the
external Draft campaign without rewriting it:

```powershell
$draftCampaign = Join-Path $env:USERPROFILE "ESAF-review-evidence\draft-campaign"
python tools/validate_qualified_review_evidence.py --check `
  --candidate $draftCandidate `
  --evidence-root $draftCampaign
```

Only a report with `evidence_valid: true` and `transition_ready: true` can
support the later authorized Draft-to-reviewed transition. A valid `stop`
conclusion may have `evidence_valid: true` while readiness remains false; it
preserves the evidence and blocks the transition. Stop rather than proceeding
when eligibility, independence, source access, source/version or digest,
candidate SHA, campaign linkage, template completion, or seal integrity is
invalid, or when Critical or Important findings remain open. Automation does
not convert a `stop` into approval or a lifecycle transition.

### Seal the Draft campaign

When the completed Draft campaign validates, seal its exact bytes
deterministically. First reserve the immutable archive locator, then supply it
to the sealing command. The CLI remains offline and does not upload either
file. It atomically writes the deterministic `CAMPAIGN_ARCHIVE.zip` and its
`CAMPAIGN_SEAL.json` together in the new external output directory:

```powershell
$draftSealDirectory = Join-Path $env:USERPROFILE "ESAF-review-evidence\draft-seal"
$draftArchiveLocator = "https://evidence.example.invalid/esaf-draft.zip?version=1"
python tools/seal_qualified_review_campaign.py --candidate $draftCandidate `
  --evidence-root $draftCampaign `
  --output-directory $draftSealDirectory `
  --archive-locator $draftArchiveLocator
```

Success means that the archive and seal have been locally materialized. It
does not establish upload, durable retention, or external verification. Upload
the exact, unmodified `CAMPAIGN_ARCHIVE.zip` bytes to the locator already
recorded in the seal, then verify the durable object's SHA-256 and byte length
against the seal. An upload failure, absence, or mismatch leaves the local
seal unpublished and unusable. The operator may publish or rely on the seal
only after successful verification.

Preserve the seal record in the external evidence system, then record its
SHA-256, durable locator, and completion of archive upload verification in the
external issue or pull-request evidence record. Both generated files remain
outside the sealed campaign root and every Git worktree. Do not modify any
campaign or archive byte after sealing. A changed archive byte or locator
requires a new output directory and a newly materialized pair.
The output directory’s complete ancestor chain must remain available and
unaliased. The sealer holds OS directory handles or descriptors through atomic
publication and fails closed when anchored no-replace publication is
unavailable.

### Reviewed package and final confirmation

After the authorized transition, generate reviewed packages from the exact
reviewed candidate, with a distinct external output path for each mapping set:

```powershell
$reviewedCandidate = git rev-parse HEAD
$reviewedPackage = Join-Path $env:USERPROFILE "ESAF-review-evidence\reviewed-core-package"
python tools/build_mapping_review_bundle.py --candidate-state reviewed `
  --commit $reviewedCandidate `
  --mapping-set-id uk-ncsc--cyber-essentials-requirements-for-it-infrastructure--3.3--esaf-0.4-alpha--0.1.0 `
  --output $reviewedPackage
```

The separate `final_reviewed_confirmation` campaign shall recursively confirm
the preserved Draft campaign by its campaign identifier, candidate SHA,
manifest digest, seal-record digest, external seal record, and deterministic
archive. Validate it with the Draft inputs:

```powershell
$finalCampaign = Join-Path $env:USERPROFILE "ESAF-review-evidence\final-confirmation"
$draftSealRecord = Join-Path $draftSealDirectory "CAMPAIGN_SEAL.json"
$draftArchive = Join-Path $draftSealDirectory "CAMPAIGN_ARCHIVE.zip"
python tools/validate_qualified_review_evidence.py --check `
  --candidate $reviewedCandidate `
  --evidence-root $finalCampaign `
  --draft-evidence-root $draftCampaign `
  --draft-seal-record $draftSealRecord `
  --draft-archive $draftArchive
```

Only final evidence with `evidence_valid: true` and `merge_ready: true` can
support merge. The validator checks schemas, bytes, hashes, paths, linkage,
and readiness rules. It cannot establish human identity, reviewer
qualification, source authorization, signature effect, the truth of human
review conclusions, non-infringement of human-authored prose, approval, or
compliance. Those remain human decisions recorded in the protected external
evidence system, never Git.
The validator checks the signed source-content-exclusion assertion but cannot
establish its truth, non-infringement, or legal effect.
