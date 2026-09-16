# Draft United Kingdom Jurisdiction Profile 0.2.0

**Profile ID:** `uk--jurisdiction-profile--0.2.0`

**Lifecycle:** Draft

**Target ESAF release:** `v0.16-draft`

This README is the authoritative package-level statement of purpose,
applicability, use, and limitations under ESAF-1800. The complete control
selections, risks, overlays, evidence expectations, and external references
are authoritative in [PROFILE.md](PROFILE.md). The adjacent JSON files are
deterministic schema-governed representations of those Markdown blocks; any
difference shall fail validation.

Version `0.2.0` is a bounded Draft deepen of
[`0.1.0`](../0.1.0/README.md). Control meanings, selection statuses, overlays,
and lifecycle-only UK mapping identity are preserved. The profile version and
the target ESAF release remain separate identifiers.

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

### Informative applicability-condition guidance

Each applicability condition is an independent factual question. Operators
should answer the exact question recorded in `profile.json` and retain the
stated resolution evidence. Informative clarifications for common misreads:

- Organizational domicile, incorporation, or headquarters location does not
  activate this profile by itself; United Kingdom deployment or operation does.
- External-provider use does not by itself establish an external AI service
  integration or a material E1 through E4 dependency.
- A downloaded or otherwise acquired external model without a live service
  integration does not satisfy the external AI service-integration condition.
- Generic internet exposure does not by itself establish an internet-reachable
  API or an internet-reachable AI-use interface or workflow.
- An administration-only console or path does not satisfy the
  internet-reachable AI application-interface condition and remains covered by
  the separate exposed-boundary IAM and infrastructure chain.
- Software intake does not establish model, application-artifact,
  infrastructure-dependency, or callable-tool use, and an unsupported
  technology does not by itself establish that a model is unsupported or that
  a capability must be retired.

These clarifications are informative operator guidance. They do not add,
remove, or reinterpret ESAF control meanings.

## Companion surfaces for operators

This profile reuses shared ESAF-1500 assessment semantics and points operators
to companion manuals and Draft toolkit packs for practice. Companion material
does not import mapping outcomes and does not change this profile's selections:

- [ESAF-1500 assessment guide](../../assessment/ESAF-1500.md)
- [Assessment toolkit index](../../assessment/README.md)
- [Assessment workbook](../../assessment/workbook/README.md)
- [Evidence catalog](../../assessment/evidence-catalog/README.md)
- [Audit checklist](../../assessment/audit-checklist/README.md)
- [ESAF-1300 governance manual](../../governance/ESAF-1300.md)
- [ESAF-1400 implementation guide](../../implementation/ESAF-1400.md)
- [ESAF-1700 data model](../../data-model/ESAF-1700.md)
- [Governance templates](../../templates/README.md)

## How to use the package

1. Confirm and evidence the United Kingdom deployment or operating basis.
2. Record the assessed system boundary and supporting dependencies.
3. Verify that the control-catalog schema version and SHA-256 pin, and every
   control record's version, lifecycle status, path, and SHA-256 pin, in the
   authoritative `profile.json` block in `PROFILE.md` match the catalog and
   control Markdown.
4. Answer the boolean conditions in `profile.json` using the specified
   resolution evidence and the informative applicability guidance above.
5. Resolve `required` and activated `conditional` selections from the
   authoritative `control-selections.json` block in `PROFILE.md`.
6. Apply the relevant overlays and evidence expectations.
7. Gather and evaluate evidence under ESAF-1500 using the declared
   `evidence_types`, preserving scope, period, methods, limitations, and
   determinations. Consult the ESAF-1500 toolkit packs linked above for
   evidence-type and quality evaluation practice.
8. Report this profile identifier, version, and Draft lifecycle with the
   assessment result.

`not_selected` means that this profile adds no profile-level selection. It
does not alter the underlying ESAF requirement. The profile-local control
status also does not determine an ESAF-1500 assessment determination.

Every evidence expectation evaluates all seven ESAF-1500 evidence-quality
attributes. The attributes listed in an expectation are profile-specific
emphases and do not replace the complete ESAF-1500 evaluation.

## Source boundary

The package is original ESAF synthesis. Its permitted source boundary is the
ESAF library and pinned lifecycle metadata only from the three exact United
Kingdom Cyber Essentials mapping registry records in
`external-references.json`. Substantive mapping content remains excluded,
including relationships, external outcomes, evidence, and interpretations.
Composition with ESAF-1600 is therefore limited to exact mapping identity,
registry location, Draft editorial status, empty registry lifecycle history,
and qualified-review dependency; it does not create relationship legs.
All content and interpretations from other or unpinned external mappings are
also excluded. Other United Kingdom laws, regulations, sector rules, and
guidance are outside this profile.

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
