# Enterprise Secure AI Framework (ESAF)

> An open enterprise standard for the secure governance, architecture, adoption, and operation of artificial intelligence.

![Status](https://img.shields.io/badge/status-Working%20Draft-blue)
![Version](https://img.shields.io/badge/version-0.9--rc1-orange)

## Vision

Artificial intelligence is becoming foundational to modern enterprises, but organizations still lack a single vendor-neutral standard connecting governance, cybersecurity, architecture, risk, operations, assurance, and business adoption.

ESAF is designed to fill that gap. Its design philosophy is simple: build a framework organizations can implement, not merely read.

## Core pillars
We are utilizing and aligning with the three pillars of the SANS Secure AI Blueprint:

- **Protect AI** secures AI systems, models, infrastructure, identities, data, applications, and autonomous agents.
- **Utilize AI** enables responsible, secure, and measurable enterprise adoption.
- **Govern AI** establishes oversight, accountability, risk management, compliance, and continuous assurance.

## Enterprise AI lifecycle

```text
Strategy -> Ideation -> Business Case -> Risk Classification
-> Architecture -> Data Readiness -> Model Selection -> Development
-> Validation -> Approval -> Deployment -> Operations -> Monitoring
-> Continuous Improvement -> Retirement
```

Every requirement, control, architecture, assessment, and governance artifact will map to one or more lifecycle stages.

## Publication set

| ID | Publication | Repository location |
|---|---|---|
| ESAF-1000 | Enterprise Standard | `framework/` |
| ESAF-1100 | Control Catalog | `controls/` |
| ESAF-1200 | Reference Architecture | `architectures/` |
| [ESAF-1300](governance/ESAF-1300.md) | Governance Manual | [governance/ESAF-1300.md](governance/ESAF-1300.md) |
| [ESAF-1400](implementation/ESAF-1400.md) | Implementation Guide | [implementation/ESAF-1400.md](implementation/ESAF-1400.md) |
| [ESAF-1500](assessment/ESAF-1500.md) | Assessment Guide | [assessment/ESAF-1500.md](assessment/ESAF-1500.md) |
| ESAF-1600 | Standards Crosswalk | `crosswalks/` |
| [ESAF-1700](data-model/ESAF-1700.md) | Enterprise AI Data Model | [data-model/ESAF-1700.md](data-model/ESAF-1700.md) |
| [ESAF-1800](profiles/ESAF-1800.md) | Industry, jurisdiction, and risk profiles | [profiles/ESAF-1800.md](profiles/ESAF-1800.md) |

The current profile package is the [Draft United Kingdom jurisdiction pilot](profiles/uk/0.1.0/README.md).

## Standards alignment

ESAF is intended to complement and map to recognized sources including NIST AI RMF, NIST CSF 2.0, NIST SP 800-53, ISO/IEC 42001, ISO/IEC 27001, ISO/IEC 23894, CIS Controls, OWASP guidance, MITRE ATLAS, PCI DSS, HITRUST CSF, SOC 2, UK Cyber Essentials, HIPAA, GDPR, and DORA.

Mappings indicate alignment and traceability; they do not by themselves establish compliance or certification.

## Repository map

```text
.github/          GitHub contribution and review configuration
framework/        ESAF-1000 normative enterprise standard
controls/         ESAF-1100 control catalog
architectures/    ESAF-1200 reference architectures
governance/       ESAF-1300 governance manual
implementation/   ESAF-1400 implementation guide
assessment/       ESAF-1500 assessment guide
crosswalks/       ESAF-1600 standards mappings
data-model/       ESAF-1700 canonical governance data model
profiles/         ESAF-1800 industry and jurisdiction profiles
templates/        Reusable governance and implementation artifacts
examples/         Non-normative worked examples
diagrams/         Editable figure sources and exports
docs/             Documentation-site entry points
tools/            Validation, publication, and assessment tooling
project/          Management of the ESAF initiative itself
```

## Project status

ESAF is a **working draft**. Content may change before Version 1.0 and shall not be represented as an approved certification scheme.

Publication of `v0.9-rc1` remains conditional on the remote annotated tag
resolving to the exact validated merged commit. The tag has not been created,
and this closure candidate does not approve publication.

See [the roadmap](ROADMAP.md), [project charter](PROJECT_CHARTER.md), [governance model](GOVERNANCE.md), [style guide](STYLE_GUIDE.md), and [contribution guide](CONTRIBUTING.md).

## Contributing

We are always seeking partners and qualified assessors to review controls and crosswalks to ensure the accuracy of this framework.

Contributions from enterprise architecture, AI engineering, cybersecurity, governance, risk, compliance, privacy, law, operations, audit, academia, and regulated industries are welcome. Open an issue before proposing significant normative or structural changes.

## License

Original ESAF standards content is licensed under [Creative Commons Attribution 4.0 International](LICENSE) (CC BY 4.0). Software and implementation assets identified in [LICENSE_SCOPE.md](LICENSE_SCOPE.md) are licensed under the [Apache License 2.0](LICENSES/Apache-2.0.txt).

See the [copyright and attribution notice](NOTICE), [third-party notices](THIRD_PARTY_NOTICES.md), and [ESAF name and marks policy](TRADEMARKS.md). Separately identified third-party material remains under its stated terms.
