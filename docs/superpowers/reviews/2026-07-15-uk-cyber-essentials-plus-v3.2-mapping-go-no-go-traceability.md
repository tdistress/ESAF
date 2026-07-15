# Cyber Essentials Plus v3.2 Mapping Feasibility Traceability

**Status:** Pending exact-head reviews

**Scope:** Design-only feasibility decisions for two separate directions between ESAF 0.4-alpha and the pinned public NCSC *Cyber Essentials Plus Test Specification* v3.2. No mapping snapshot, relationship record, implementation authorization, certification claim, or current-operational-scheme completeness claim exists.

## Source inventory and rights sequencing

The repaired source-inventory traceability records the locked oracle at SHA-256 `8a6ad659394130c360205aa8a693b812f6c3a6778bc1395cd93ac6187f8386bc`. Commit `c69541278d19eec50f00e2c6f93cdf536c3fbc58` corrected that identity and added an executable LF-normalized digest check; the check passes against the current oracle.

The mapping-feasibility rights record is `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-rights-re-attestation.md` at commit `4207e1c1e8ff9f743274ebb4b626210cca053458`. The record identifies Codex Mapping Feasibility Rights Reviewer R1, the same locked oracle digest, the prior rights commit `6add413fc7a8a6330cf16dc5d12e3b9b85aa34e6`, all eight approved field classes, and an unconditional `approved` disposition. Git ancestry verification returned exit 0, and the record commit changes only the rights record.

## Independent analysis and sealed reconciliation

| Direction | Analyst | Prompt SHA-256 | Receipt UTC | Accepted payload reference | Direction-content SHA-256 |
|---|---|---|---|---|---|
| `esaf_to_external` | Codex CE Plus ESAF-to-External Analyst A16 | `f0abf7998ae59c8389eede5097858a7237a51f0926a34e246d1403be64f05c4b` | `2026-07-15T22:14:39.268Z` | `sha256:9f5ecd41820be2b17f98fade7b4dc6254e5c960b12fdef51ee970c39285797fb` | `2fe23149dff33bd845effd81fe69d751f7b75946d7736b252d538a537feffb6f` |
| `external_to_esaf` | Codex CE Plus External-to-ESAF Analyst B16 | `64ef5de20ccfbafb67a897d86e968c71eb7b3a6a9e0cfb814c07c57a967bb145` | `2026-07-15T22:16:07.597Z` | `sha256:818859cb096f0cc78c1f9802d7aa9474f7d99c1ded454ccdedade09cf646bc27` | `be72787699d075863d0e5f18c59e2085b160dda7d31eb9baa291319d989290df` |

The common-input SHA-256 is `7bfa465fdeb980a88b6e3456ebd1939ee8a32ea72df58f7bf04a402b19eca6f4`. Both sibling analysts were dispatched concurrently with `fork_turns="none"`. Their final responses returned only through the private controller mailbox, inaccessible to the sibling; the controller withheld the first response until both were received. Each accepted submission attests `no_output_file_attestation: true` and `no_sibling_content_attestation: true`. The fail-closed fallback required separate principals or containers or a stop if those mailbox semantics were unavailable.

Codex CE Plus Mapping Feasibility Reconciler R16 accepted both sealed direction-local submissions without alteration. The `esaf_to_external` validation is `ACCEPTED` with evidence references `sha256:9f5ecd41820be2b17f98fade7b4dc6254e5c960b12fdef51ee970c39285797fb` and `sha256:2fe23149dff33bd845effd81fe69d751f7b75946d7736b252d538a537feffb6f`. The `external_to_esaf` validation is `ACCEPTED` with evidence references `sha256:818859cb096f0cc78c1f9802d7aa9474f7d99c1ded454ccdedade09cf646bc27` and `sha256:be72787699d075863d0e5f18c59e2085b160dda7d31eb9baa291319d989290df`. Post-seal changes are prohibited, the packaging disposition is `accepted`, and both direction-content digests above were recomputed from the packaged matrix.

## Derived coverage and decisions

| Direction | Probes | Groups | Kinds | Actors | Special scenarios |
|---|---:|---:|---:|---:|---:|
| `esaf_to_external` | 2 | 10 of 10 | 7 of 7 | 5 of 5 | 9 of 9 |
| `external_to_esaf` | 7 | 10 of 10 | 7 of 7 | 5 of 5 | 9 of 9 |

| Direction | Ordered gates | Positive probes | Disposition | Authorized next activity |
|---|---|---|---|---|
| `esaf_to_external` | `source=PASS`, `rights=PASS`, `semantic=PASS`, `normative_basis=PASS`, `schema=PASS`, `overclaiming=PASS`, `utility=PASS` | `esaf-ext-t5-006-privileged-access` | `GO` | Design the Cyber Essentials Plus v3.2 `esaf_to_external` mapping. |
| `external_to_esaf` | `source=PASS`, `rights=PASS`, `semantic=PASS`, `normative_basis=PASS`, `schema=PASS`, `overclaiming=PASS`, `utility=PASS` | `external-iam130-t5-006` | `GO` | Design the Cyber Essentials Plus v3.2 `external_to_esaf` mapping. |

Both `GO` decisions authorize only later direction-specific design work. They do not authorize mapping implementation or create a mapping.

## Changed files and command results

This publication step changes exactly:

- `crosswalks/uk-cyber-essentials.md`
- `docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-traceability.md`
- `project/BACKLOG.md`
- `tests/test_release_metadata.py`
- `tests/test_uk_cyber_essentials_plus_v32_mapping_go_no_go.py`

Test-first evidence: `python -m unittest tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go tests.test_release_metadata -v` ran 54 tests with exactly two expected failures, one for the absent landing-page publication and one for the absent disposition-authorized backlog entries. No other test failed.

| Command | Result |
|---|---|
| `python -m unittest tests.test_uk_cyber_essentials_plus_v32_traceability tests.test_uk_cyber_essentials_plus_v32_mapping_go_no_go tests.test_render_ce_plus_mapping_go_no_go tests.test_release_metadata -v` | 61 tests passed |
| `python tools/render_ce_plus_mapping_go_no_go.py --matrix docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json --output docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md --check` | exited 0; rendered review is current |
| `git diff --check` | exited 0 |

Independent specification/methodology and security/overclaiming reviews remain required on one immutable exact head; their identities and integration evidence belong outside this non-self-referential record.
