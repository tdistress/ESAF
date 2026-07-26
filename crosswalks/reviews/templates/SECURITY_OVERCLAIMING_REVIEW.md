# Security and Overclaiming Review Worksheet

## Review identification

| Field | Value |
|---|---|
| Mapping-set identifier | `[REQUIRED]` |
| Candidate commit SHA | `[REQUIRED: 40 lowercase hexadecimal characters]` |
| Package root | `[REQUIRED: canonical relative path]` |
| Package manifest path | `[REQUIRED: canonical relative path]` |
| Package-manifest SHA-256 | `[REQUIRED: 64 lowercase hexadecimal characters]` |
| Package immutable locator | `[REQUIRED: immutable HTTPS URL or urn:sha256 locator]` |
| Package retention owner | `[REQUIRED]` |
| Reviewer identity | `[REQUIRED]` |
| Attestation path | `[REQUIRED: canonical relative path]` |
| Attestation immutable locator | `[REQUIRED: immutable HTTPS URL or urn:sha256 locator]` |
| Attestation retention owner | `[REQUIRED]` |
| Attestation SHA-256 | `[REQUIRED: 64 lowercase hexadecimal characters]` |
| Worksheet path | `[REQUIRED: canonical relative path]` |
| Worksheet immutable locator | `[REQUIRED: immutable HTTPS URL or urn:sha256 locator]` |
| Worksheet retention owner | `[REQUIRED]` |
| Review role | `Security and overclaiming review` |
| Review date | `[REQUIRED: YYYY-MM-DD]` |
| Coverage summary | `[REQUIRED]` |
| Review method | `[REQUIRED]` |
| Provision coverage | `[REQUIRED: population and identifiers reviewed]` |
| Mapping-record coverage | `[REQUIRED: population and identifiers reviewed]` |

Every table value shall be single-line text without an unescaped pipe
character. Do not add, remove, duplicate, or reorder rows.

## Review scope

Verify:

- relationship direction and type;
- coverage and confidence;
- conditions;
- expected evidence;
- known gaps;
- `no_direct_mapping`;
- `prerequisite`;
- `partially_supports`;
- normative-text basis; and
- that conditions cannot create a missing external outcome;
- that implementation guidance or adjacent capabilities cannot replace
  normative requirements; and
- nonclaims, including certification, compliance, equivalence, endorsement,
  and assurance.

## Findings

Critical and Important findings cannot be accepted and must be resolved.
Only Minor findings may be accepted, with a named acceptor, acceptance
rationale, and disposition date.

| Finding ID | Affected record IDs | Severity | Description | Evidence | Required action | Status | Disposition | Resolver or acceptor | Disposition date | Acceptance rationale |
|---|---|---|---|---|---|---|---|---|---|---|
| `[REQUIRED OR NONE]` |  | Critical / Important / Minor |  |  |  | open / resolved / accepted (Minor only) |  |  | YYYY-MM-DD |  |

## Overall conclusion

| Field | Value |
|---|---|
| Overall conclusion | `[REQUIRED: pass / pass_after_correction / stop]` |
| Post-correction candidate SHA | `[REQUIRED for pass_after_correction; otherwise Not applicable]` |
| Reviewer metadata findings disposition | `[REQUIRED: concise disposition of all findings]` |

## Worksheet signature

| Field | Value |
|---|---|
| Reviewer signature | `[REQUIRED]` |
| Signature date | `[REQUIRED: YYYY-MM-DD]` |
| Signed worksheet SHA-256 | `[REQUIRED: digest of the completed signed worksheet]` |

Digest procedure: encode the completed worksheet as UTF-8 without BOM and LF
line endings after all other fields, including the reviewer signature and
signature date, are final. For the digest calculation, remove the entire
`| Signed worksheet SHA-256 |` table row, including its terminating LF, and
hash every remaining byte with SHA-256. Record the lowercase hexadecimal
digest in that row; verification repeats the same exclusion. No non-excluded
byte may change after the digest is recorded.
