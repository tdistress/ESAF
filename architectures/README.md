# ESAF-1200 Reference Architecture

ESAF-1200 defines vendor-neutral architecture methods and reusable patterns for implementing the requirements of ESAF-1000 and the controls of ESAF-1100.

## Foundation

- [`ESAF-1200.md`](ESAF-1200.md) defines the normative architecture method.
- [`PRINCIPLES.md`](PRINCIPLES.md) defines durable architecture principles.
- [`TRUST_ZONES.md`](TRUST_ZONES.md) defines logical trust zones and boundary-crossing requirements.
- [`PATTERN_SELECTION.md`](PATTERN_SELECTION.md) defines pattern selection and tailoring.
- [`ARCHITECTURE_TEMPLATE.md`](ARCHITECTURE_TEMPLATE.md) defines the required pattern record.
- [`patterns/`](patterns/README.md) maintains the pattern registry.
- [`overlays/`](overlays/README.md) defines reusable risk, deployment, and obligation overlays.
- [`decisions/`](decisions/README.md) maintains architecture decision records.

## Initial pattern queue

The initial library covers enterprise AI platforms and gateways, enterprise copilots, retrieval-augmented generation, agentic and multi-agent AI, private model deployment, AI integration services, and AI observability. Each pattern is delivered through an independently reviewable change.

Product-specific configuration belongs in ESAF-1400. Crosswalk assertions belong in ESAF-1600. A reference pattern does not establish conformance with ESAF or an external standard.
