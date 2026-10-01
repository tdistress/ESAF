# NIST AI RMF 1.0 owner-risk people-gate disposition

**Date:** 2026-10-01  
**Decision type:** `owner_risk_acceptance`  
**Applies to:** NIST AI RMF 1.0 mapping readiness people gate only  
**Lifecycle limitation:** Draft mapping authorship only

## Owner decision

The ESAF repository owner directed that independent qualified reviewers are
not required for NIST AI RMF readiness clearance because the framework is a
well-established public source, selected Approach 1 (owner-risk Draft path),
and authorized commit, push, and merge to complete the work.

This disposition clears readiness blocker `NIST-AI-RMF-READINESS-B001` for
the purpose of deriving matrix `GO` and authorizing a separate Draft
`esaf_to_external` mapping candidate. It does not complete qualified review.

## Named mapper

- Mapper identity: `esaf-project-owner` (ESAF Project Maintainer / repository
  owner)
- Authorized source access: yes (public NIST.AI.100-1 PDF)
- Experience basis: ESAF-1600 crosswalk method and public NIST AI RMF 1.0 Core

## Deferred qualified review

Independent seats for `nist_ai_rmf_subject_matter`,
`esaf_specification_and_mapping`, `publication_rights` (mapping-candidate
reaffirmation), and `security_and_overclaiming` remain unfilled.
`qualified_review_status: deferred`.

Self-review remains prohibited for any future advancement to `reviewed` or
`approved`. ESAF-1600 still requires a mapper-distinct qualified reviewer
before those lifecycle states.

## Claims not made

- qualified review
- NIST approval or endorsement
- compliance, certification, equivalence, assurance
- production readiness
- closure of Issues #55 or #60

## Reconsideration

A later owner or governance decision may require naming independent reviewers
and completing exact-SHA inventory/specification and security/overclaiming
reviews before any lifecycle advance beyond Draft.
