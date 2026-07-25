# Draft United Kingdom Jurisdiction Profile 0.1.0

**Profile ID:** `uk--jurisdiction-profile--0.1.0`

**Lifecycle:** Draft

**Target ESAF release:** `v0.5-beta`

## Purpose and applicability

This Draft profile applies to AI systems deployed or operated in the United
Kingdom, regardless of organizational domicile. Incorporation, headquarters,
or domicile alone does not determine applicability.

The assessed boundary includes the AI system and business purpose, included
and excluded components, supporting infrastructure and services, suppliers,
shared-responsibility boundaries, applicable condition answers and their
evidence, assumptions, limitations, and unresolved scope questions. Users
shall record the United Kingdom deployment or operating basis and retain the
evidence used to resolve each applicable condition.

## How to use the package

1. Confirm and evidence the United Kingdom deployment or operating basis.
2. Record the assessed system boundary and supporting dependencies.
3. Answer the boolean conditions in `profile.json` using the specified
   resolution evidence.
4. Resolve `required` and activated `conditional` selections in
   `control-selections.json`.
5. Apply the relevant overlays and evidence expectations.
6. Gather and evaluate evidence under ESAF-1500, preserving scope, period,
   methods, limitations, and determinations.
7. Report this profile identifier, version, and Draft lifecycle with the
   assessment result.

Each condition shall be answered independently from its exact factual
question. A broader fact does not supply a narrower one: external-provider use
does not by itself establish an external AI service integration or a material
E1 through E4 dependency. A downloaded or otherwise acquired external model
without a live service integration does not satisfy the external AI
service-integration condition. Generic internet exposure does not by itself
establish an internet-reachable API or an internet-reachable AI-use interface
or workflow. An administration-only console or path does not satisfy the
internet-reachable AI application-interface condition and remains covered by
the separate exposed-boundary IAM and infrastructure chain. Software intake
does not establish model, application-artifact, infrastructure-dependency, or
callable-tool use, and an unsupported technology does not by itself establish
that a model is unsupported or that a capability must be retired.

`not_selected` means that this pilot adds no profile-level selection. It does
not alter the underlying ESAF requirement. The profile-local control status
also does not determine an ESAF-1500 assessment determination.

Every evidence expectation evaluates all seven ESAF-1500 evidence-quality
attributes. The attributes listed in an expectation are profile-specific
emphases and do not replace the complete ESAF-1500 evaluation.

## Source boundary

The package is original ESAF synthesis. Its permitted source boundary is the
ESAF library and pinned lifecycle metadata only from the three exact United
Kingdom Cyber Essentials mapping registry records in
`external-references.json`. Substantive mapping content remains excluded,
including relationships, external outcomes, evidence, and interpretations.
All content and interpretations from other or unpinned external mappings are
also excluded. Other United Kingdom laws, regulations, sector rules, and
guidance are outside this pilot.

## Draft limitations and non-claims

This Draft profile does not establish legal sufficiency.
It does not establish compliance.
It does not establish certification.
It does not establish equivalence.
It does not establish endorsement.
It does not establish external approval.
It does not establish production readiness.

This profile does not define the scope of Cyber Essentials or any legal or
regulatory regime. It does not implement or certify Cyber Essentials, complete
qualified review of a mapping set, or advance a referenced mapping beyond its
recorded state. Each listed mapping snapshot has Draft editorial status and an
empty registry lifecycle-event history. Mapping snapshot editorial status and
governed registry lifecycle state remain separate; a change to either requires
an explicit profile update before reliance. Core ESAF controls are not replaced,
waived, weakened, narrowed, or made optional by this profile.

An assessment remains valid only for its recorded system boundary, evidence,
methods, limitations, and time period. ESAF-1500 maturity and control
determinations remain separate and retain their shared meanings.
