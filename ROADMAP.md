# ESAF Roadmap

**Status:** Working Draft

**Version:** 0.9-rc1

## 0.9-rc1 delivery sequence

`v0.9-rc1` is the bounded Working Draft release candidate. Delivery order:

1. close validation-harness Phase 2 performance work;
2. author ESAF-1300, ESAF-1400, and ESAF-1700 Working Draft foundations;
3. complete one public-source crosswalk readiness package, defaulting to NIST
   AI RMF unless the owner selects another public source; and
4. close ordinary `v0.9-rc1` publication gates on the exact candidate.

Deferred mapping assurance remains tracked after beta through issue 55 and does
not stop later engineering work. HITRUST readiness remains separately gated
through issue 60. The Phase 4, Phase 5, and Phase 6 lists remain long-term
direction, not `v0.9-rc1` exit criteria.

Publication remains conditional on the remote annotated `v0.9-rc1` tag
resolving to the exact validated merged commit. The tag has not been created,
and the post-merge gate remains open.

## 0.5-beta delivery sequence

The `v0.5-beta` Working Draft was published on 2026-08-01 through the
annotated `v0.5-beta` tag at
`255f8806917aaf8c6a2441152b4638fc9fd2bfda`. It records a coordinated
owner-risk disposition for the three Draft UK mapping sets, the minimum shared
assessment foundation, one pilot profile, and the priority-mapping decision.
Deferred mapping assurance remains tracked after beta through issue 55 and does
not stop later engineering work. Publication does not change any control,
architecture, profile, mapping-set, or mapping-record lifecycle state. The
Phase 4 and Phase 5 lists remain long-term direction, not `v0.5-beta` exit
criteria.

## Phase 0 - Foundation

- Stable repository structure and contribution workflow
- Project charter, governance, style, terminology, and release conventions
- Enterprise AI lifecycle and control taxonomy decisions

## Phase 1 - Enterprise Standard

- ESAF-1000 management system and operating model
- Protect AI, Utilize AI, and Govern AI normative requirements
- Lifecycle gates, governance artifacts, roles, and decision rights

## Phase 2 - Control Catalog

- Sixteen control families and their objectives
- Normative controls, enhancements, evidence, assessment procedures, and metrics
- Risk-tiered baseline profiles

## Phase 3 - Reference Architecture

- Architecture method, principles, trust zones, selection, pattern contract, overlays, and decision records
- Enterprise AI platform and gateway
- RAG, agentic AI, private model, enterprise copilot, AI integration services, and observability patterns
- Trust boundaries, security overlays, and implementation decision records

## Phase 4 - Standards Crosswalk

- NIST AI RMF, NIST CSF, NIST SP 800-53, ISO/IEC 42001, and ISO/IEC 27001
- PCI DSS, HITRUST CSF, UK Cyber Essentials, SOC 2, and CIS Controls
- OWASP AI guidance, MITRE ATLAS, privacy, and sector obligations

## Phase 5 - Industry Profiles

- Healthcare, financial services, critical infrastructure, retail, government, manufacturing, media, UK, and EU profiles

## Phase 6 - Assessment Toolkit

- Capability and control maturity models
- Assessment workbook, evidence catalog, audit checklist, and governance templates

Release criteria and milestone definitions are maintained in `project/`.
