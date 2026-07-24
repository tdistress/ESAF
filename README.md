# Enterprise Secure AI Framework (ESAF)

> An open enterprise standard for the secure governance, architecture, adoption, and operation of artificial intelligence.

![Status](https://img.shields.io/badge/status-Working%20Draft-blue)
![Version](https://img.shields.io/badge/version-0.4--alpha-orange)

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
| ESAF-1300 | Governance Manual | `governance/` |
| ESAF-1400 | Implementation Guide | `implementation/` |
| [ESAF-1500](assessment/ESAF-1500.md) | Assessment Guide | [assessment/ESAF-1500.md](assessment/ESAF-1500.md) |
| ESAF-1600 | Standards Crosswalk | `crosswalks/` |
| ESAF-1700 | Enterprise AI Data Model | `data-model/` |
| ESAF-1800 | Industry Profiles | `profiles/` |

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

See [the roadmap](ROADMAP.md), [project charter](PROJECT_CHARTER.md), [governance model](GOVERNANCE.md), [style guide](STYLE_GUIDE.md), and [contribution guide](CONTRIBUTING.md).

## Contributing

Contributions from enterprise architecture, AI engineering, cybersecurity, governance, risk, compliance, privacy, law, operations, audit, academia, and regulated industries are welcome. Open an issue before proposing significant normative or structural changes.

## License

Licensing is not yet finalized. See [LICENSE](LICENSE) before using or redistributing project content.
