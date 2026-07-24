# Qualified Reviewer Attestation

An unsigned blank form is not review evidence.

| Field | Value |
|---|---|
| Reviewer identity | `[REQUIRED]` |
| Organization | `[REQUIRED]` |
| Verification locator | `[REQUIRED]` |
| Mapping-set identifier | `[REQUIRED]` |
| Candidate commit SHA | `[REQUIRED: 40 lowercase hexadecimal characters]` |
| Package-manifest SHA-256 | `[REQUIRED]` |
| Review role | `[REQUIRED: Specification and inventory review / Security and overclaiming review]` |
| Scheme qualification | `[REQUIRED]` |
| ESAF or mapping qualification | `[REQUIRED]` |
| Authorized source access | `[REQUIRED: Yes / No]` |
| Independence from mapper | `[REQUIRED: Yes / No]` |
| Conflicts of interest | `[REQUIRED: Yes / No; describe or state none]` |
| Signature | `[REQUIRED]` |
| Date | `[REQUIRED: YYYY-MM-DD]` |

I attest that I have authorized source access: Yes / No.

I attest that I am independent from the mapper: Yes / No.

I attest that conflicts of interest have been disclosed: Yes / No.

I understand that this review does not establish certification, compliance,
equivalence, endorsement, or assurance beyond the relationships expressly
recorded in the mapping snapshot.
