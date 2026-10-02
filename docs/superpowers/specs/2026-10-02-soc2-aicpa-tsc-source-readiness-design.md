# SOC 2 Trust Services Criteria source-readiness design

## Purpose

Determine whether ESAF can identify, inventory, and later map the AICPA Trust
Services Criteria used in SOC 2 within authorized access and publication
boundaries. This is a readiness decision only. It does not authorize mapping
records, source-derived provision inventories, snapshots, registry entries, or
catalog changes.

## Scope and source identity

The candidate source is the AICPA's **2017 Trust Services Criteria (With
Revised Points of Focus – 2022)**, published on the AICPA & CIMA resource page
on 2023-09-30. The title's `2017` identifies the criteria edition; `2022`
identifies the revised Points of Focus. The AICPA page describes the criteria
as covering security, availability, processing integrity, confidentiality,
and privacy and marks the downloadable PDF as requiring a free account.

The readiness work shall distinguish the Trust Services Criteria from the
separate 2018 SOC 2 Description Criteria (with revised implementation guidance
– 2022), practitioner guides, attestation standards, example reports, and
other materials. Those sources are excluded from any proposed provision
population unless a later design explicitly expands scope.

The only proposed future mapping direction is `esaf_to_external`. Any future
candidate shall state its full-criteria scope and finest publishable
identifier granularity after authorized source access and permission are
verified. No source-derived provision inventory or positive feasibility probe
is permitted while the source access and publication-rights gates are blocked.

## Evidence model and rights boundary

The package shall use the established source oracle, rights review, mechanical
readiness matrix, deterministic decision renderer, crosswalk landing page,
and issue traceability pattern. It shall not add a parallel registry or any
mapping artifact while the derived decision is `HOLD` or `NO_GO`.

The public AICPA resource page identifies the publication and says it is
available after free-account access. The AICPA site Terms & Conditions observed
for this review restrict copying, modification, distribution, public use, and
derivative works absent written consent, and object to text/data mining and
scraping. The resource page identifies the download as including copyright
information, but the document-specific notice has not been inspected. These
observations do not determine the scope of any license attached to the PDF or
any statutory exception. The package shall therefore fail closed: no source
text, close paraphrases, provision identifiers, structural inventory, or
derivative mapping analysis will be published until an independent reviewer
verifies document-specific terms and any needed written permission for ESAF's
repository, generated publications, and downstream redistribution model.

Bibliographic source identity and official hyperlinks shall be kept separate
from ESAF-1600 mapping field classes. The rights review must explicitly
determine whether even the proposed metadata field classes are appropriate to
publish; no blanket reuse license is inferred from free-account access.

## Mechanical readiness decision

The closed matrix shall evaluate these ordered gates:

1. `source_identity_and_drift`;
2. `authorized_source_artifact`;
3. `publication_rights`;
4. `provision_inventory`;
5. `semantic_and_normative_feasibility`;
6. `esaf_1600_and_schema_fit`;
7. `mapper_and_reviewer_readiness`; and
8. `overclaiming_controls`.

Each gate is `PASS` or `BLOCKED` and cites evidence. Each blocked gate has at
least one blocker with an owner, missing evidence, reconsideration trigger,
and deterministic re-entry test. Schema 1.0.0 cannot emit `GO`: its boolean
feasibility flag and reviewer requirements do not encode digest-bound probe
evidence or exact-candidate reviewer attestations. The renderer shall reject
an otherwise all-PASS matrix until a reviewed schema adds and validates those
machine-readable evidence records, along with affirmative source and rights
evidence. Once supported, `GO` may be derived only when every gate passes,
blockers are empty, the feasibility probe is evidenced, and no Critical or
Important findings remain. Otherwise it derives `HOLD`
when at least one complete blocker remains and every blocked gate has a
credible reconsideration trigger and re-entry test. It derives `NO_GO` when
evidence establishes that at least one required gate is conclusively
unachievable for this exact scope, even if other blockers are also present.
The renderer shall reject a `HOLD` matrix containing a terminal blocker and
shall reject a `NO_GO` matrix without one, so the dispositions are mutually
exclusive. A narrower or materially changed scope requires a revised design
and a new readiness decision.

The expected current result is `HOLD`: the downloadable source bytes and
document-specific notice have not been inspected, written publication
permission for public derivative analysis is not evidenced, no authorized
provision inventory or positive probe exists, and qualified named mapping and
independent review personnel are not identified.

## Nonclaims and reconsideration

The package shall state that no SOC 2 mapping artifact or provision inventory
exists and shall not claim AICPA approval, authorization, endorsement,
certification, compliance, equivalence, coverage, assurance, or legal
sufficiency. It shall distinguish readiness status from an attestation
engagement or SOC report.

Reconsideration requires an authorized person to obtain the exact source and
document-specific terms; an independent rights reviewer to approve every
proposed field class and publication channel, including written permission
where needed; a complete reconciled inventory at an authorized granularity;
a positive ESAF normative-feasibility probe; named qualified mapper and
independent exact-candidate reviewers; and a refreshed matrix with digest-bound
feasibility and exact-candidate reviewer attestations and no open Critical or
Important findings. A later `GO` only authorizes a separate
mapping candidate and does not itself approve a mapping.

## Deliverables

- Source identity and evidence oracle.
- Independent publication-rights review, committed before derivative decision
  analysis.
- Mechanical readiness matrix and generated GO/HOLD/NO_GO review.
- `crosswalks/soc-2.md` readiness landing page and issue traceability record.
- Focused tests, deterministic renderer, CI and documentation wiring.
- Project backlog synchronization for the new unmilestoned GitHub Issue #219.

No files shall be added under `crosswalks/mappings/` or `crosswalks/registry/`,
and `crosswalks/catalog.json` shall remain unchanged while the decision is
`HOLD` or `NO_GO`.
