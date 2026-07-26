# Qualified Reviewer Attestation

An unsigned blank form is not review evidence.

| Field | Value |
|---|---|
| Reviewer identity | `[REQUIRED]` |
| Organization | `[REQUIRED]` |
| Verification locator | `[REQUIRED]` |
| Mapping-set identifier | `[REQUIRED]` |
| Candidate commit SHA | `[REQUIRED: 40 lowercase hexadecimal characters]` |
| Package root | `[REQUIRED: canonical relative path]` |
| Package manifest path | `[REQUIRED: canonical relative path]` |
| Package-manifest SHA-256 | `[REQUIRED: 64 lowercase hexadecimal characters]` |
| Package immutable locator | `[REQUIRED: immutable HTTPS URL or urn:sha256 locator]` |
| Package retention owner | `[REQUIRED]` |
| Attestation path | `[REQUIRED: canonical relative path]` |
| Attestation immutable locator | `[REQUIRED: immutable HTTPS URL or urn:sha256 locator]` |
| Attestation retention owner | `[REQUIRED]` |
| Review role | `[REQUIRED: Specification and inventory review / Security and overclaiming review]` |
| Publication identity | `[REQUIRED]` |
| Exact source version | `[REQUIRED]` |
| Official URL | `[REQUIRED]` |
| Source checksum(s) | `[REQUIRED]` |
| Source locator(s) | `[REQUIRED: include every additional locator used]` |
| Publication-rights basis | `[REQUIRED]` |
| Permitted elements | `[REQUIRED]` |
| Prohibited elements | `[REQUIRED: list or state none]` |
| Restrictions | `[REQUIRED]` |
| Qualification | `[REQUIRED: state Scheme qualification and ESAF or mapping qualification]` |
| Authorized source access | `[REQUIRED: Yes / No]` |
| Independence from mapper | `[REQUIRED: Yes / No]` |
| Conflicts of interest | `[REQUIRED: Yes / No; describe or state none]` |
| Conflict disposition | `[REQUIRED: resolved disposition and authority]` |
| Project-owner eligibility acceptance | `[REQUIRED: Accepted / Rejected]` |
| Project-owner dual-role acceptance | `[REQUIRED: Yes / No / Not applicable]` |
| Project-owner identity | `[REQUIRED]` |
| Project-owner signature | `[REQUIRED]` |
| Project-owner acceptance date | `[REQUIRED: YYYY-MM-DD]` |
| Signature | `[REQUIRED]` |
| Date | `[REQUIRED: YYYY-MM-DD]` |

Every table value shall be single-line text without an unescaped pipe
character. Do not add, remove, duplicate, or reorder rows.

I attest that I had authorized access to the exact publication identity,
source version, official URL, source checksum(s), and source locator(s)
recorded above: Yes / No.

I attest that my access and use comply with the recorded publication-rights
basis, permitted elements, prohibited elements, and restrictions: Yes / No.

I attest that I am independent from the mapper: Yes / No.

I attest that conflicts of interest and their disposition have been fully
disclosed: Yes / No.

I understand that this review does not establish certification, compliance,
equivalence, endorsement, or assurance beyond the relationships expressly
recorded in the mapping snapshot.
