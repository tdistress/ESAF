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

The mapping set remains draft. All 91 referenced ESAF controls are draft version 0.1.0 and are pinned to the ESAF 0.4-alpha source baseline. No relationship has been independently reviewed or approved, and qualified human review is required before any lifecycle transition. The crosswalk describes analytical contributions from ESAF controls to individual provisions; it does not establish certification, compliance, equivalence, a compliance percentage, legal sufficiency, or implementation effectiveness.

## Cyber Essentials Plus roadmap

Cyber Essentials Plus will be analyzed as a separate, source-versioned mapping set because its assurance and testing purpose differs from the core requirements mapped here. No Plus testing outcome is inferred from this core draft.
