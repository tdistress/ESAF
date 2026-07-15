# UK Cyber Essentials Crosswalk

**Status:** Draft mapping in development

This work maps ESAF 0.4-alpha controls to the UK National Cyber Security Centre (NCSC) publication *Cyber Essentials: Requirements for IT Infrastructure v3.3*. The mapping set is limited to Cyber Essentials core. Cyber Essentials Plus has a distinct assurance purpose and will use a separate, source-versioned mapping set.

The [authoritative draft snapshot](mappings/uk-ncsc/cyber-essentials-requirements-for-it-infrastructure/3.3/0.4-alpha/0.1.0/README.md) contains the provision-level records. The [generated crosswalk catalog](CATALOG.md) provides the repository-wide derived view.

## Source and publication rights

- Authority: UK National Cyber Security Centre
- Publication: *Cyber Essentials: Requirements for IT Infrastructure v3.3*
- Publication date: 2026-04-27
- Official source: <https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf>
- Source accessed: 2026-07-13
- PDF SHA-256: `e5a857de99cba9e1c0e3d2c9ac5d626edf7215e1c5b906fc18b4ef1a34684923`

Source material is Crown copyright and is reused under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). This project attributes the NCSC, does not reproduce government logos or third-party material, and does not imply NCSC endorsement or official status. Mapping records use original paraphrases and official links rather than copied requirement text.

## Provision inventory

The complete-publication inventory contains 116 independently testable provisions from sections D and E. The identifiers shown below are ESAF-assigned atomic provision locators; they are not identifiers published or endorsed by the NCSC.

| Group | Record range | Count |
|---|---|---:|
| D. Scope | `ce33-d-001` through `ce33-d-044` | 44 |
| E.1 Firewalls | `ce33-e1-001` through `ce33-e1-012` | 12 |
| E.2 Secure Configuration | `ce33-e2-001` through `ce33-e2-012` | 12 |
| E.3 Security Update Management | `ce33-e3-001` through `ce33-e3-007` | 7 |
| E.4 User Access Control | `ce33-e4-001` through `ce33-e4-029` | 29 |
| E.5 Malware Protection | `ce33-e5-001` through `ce33-e5-012` | 12 |
| **Total** |  | **116** |

The inventory includes prescriptive scope classifications and independently testable requirements. It excludes definitions, aims, examples, explanatory introductions, information boxes, backup guidance in section C, zero-trust guidance in section F, and statements expressly identified as non-mandatory guidance.

## Draft mapping results

The 116 provision records contain 41 forward-only relationship legs and 76 no-direct-mapping dispositions. Relationship legs describe limited contributions from individual ESAF controls; several legs do not combine into a claim that a Cyber Essentials provision has been met.

Prominent gaps include:

- mandatory firewall deployment, default-deny behavior, and the full set of firewall administration outcomes;
- exact password length, blocklist, throttling, and lockout thresholds;
- the fixed 14-day security-update deadline and its precise vendor, severity, and scoring triggers; and
- endpoint malware protection, anti-malware configuration, and application allowlisting outside the narrow AI application and integration contributions recorded in the snapshot.

## Draft-control boundary

The mapping set remains draft. The pinned baseline contains 91 draft controls v0.1.0; 41 legs reference 16 distinct controls. All provision records and relationship legs remain draft. Independent technical review of the candidate does not constitute qualified Cyber Essentials scheme review or lifecycle approval. Qualified human review is required before any lifecycle transition. The crosswalk describes analytical contributions from ESAF controls to individual provisions; it does not establish certification, compliance, equivalence, a compliance percentage, legal sufficiency, or implementation effectiveness.

## Cyber Essentials Plus v3.2 public-source inventory

Cyber Essentials core v3.3 and Cyber Essentials Plus v3.2 are separate, source-versioned artifacts. Core v3.3 defines protection requirements; the public Plus v3.2 specification defines assessment procedures and assurance activities. Neither inventory supplies or supersedes the other.

The [reconciled Plus v3.2 public-source provision oracle](../docs/superpowers/specs/2026-07-14-uk-cyber-essentials-plus-v3.2-provision-oracle.json) contains 144 provisions derived from its locked records and section ledger. Its complete-publication status means complete only for the pinned public v3.2 specification under the recorded atomization rule. It is not a complete inventory of the current operational Cyber Essentials Plus scheme, Delivery Partner methodology, or certification process.

Official NCSC sources and byte identities are:

- resource page: <https://www.ncsc.gov.uk/cyberessentials/resources>;
- canonical PDF: <https://www.ncsc.gov.uk/sites/default/files/2026-05/cyber-essentials-plus-test-specification-v3-2%20english.pdf>, 424,226 bytes, SHA-256 `2adf2703dec3b581e13e39c6a1de230bb1bce6d85f1158bb1eb53108e28596e8`; and
- legacy official PDF: <https://www.ncsc.gov.uk/files/cyber-essentials-plus-test-specification-v3-2.pdf>, 419,191 bytes, SHA-256 `d334c717597a01fab7a362377b7b04c8449568052ed1c4cf48837f6fb3aca694`.

The NCSC material is Crown copyright and is reused under the Open Government Licence v3.0 with attribution. The rights re-attestation confirms that the oracle remains within that approved publication basis and contains no IASME-derived structure or text.

There is 2026 operational context outside this source boundary: NCSC publishes core v3.3 while the public Plus test specification remains v3.2, and separate 2026 operational changes are not consolidated into the public v3.2 PDF. Those changes are context only and are not part of the 144-provision universe.

No Cyber Essentials Plus mapping snapshot exists. The oracle does not establish certification, compliance, equivalence, current-scheme completeness, or any Plus testing outcome.

## Cyber Essentials Plus v3.2 mapping feasibility

The [canonical feasibility matrix](../docs/superpowers/specs/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-feasibility-matrix.json) and [rendered decision record](../docs/superpowers/reviews/2026-07-15-uk-cyber-essentials-plus-v3.2-mapping-go-no-go-review.md) record these directional dispositions: `esaf_to_external`: **GO** and `external_to_esaf`: **GO**. No Cyber Essentials Plus mapping exists. `GO` authorizes design only; it does not authorize mapping implementation.

These decisions apply only to the pinned public Cyber Essentials Plus v3.2 specification. They do not establish completeness for the current operational Cyber Essentials Plus scheme or change the source and assurance boundaries above.
