# Specification and Inventory Review Worksheet

## Review identification

| Field | Value |
|---|---|
| Mapping-set identifier | `[REQUIRED]` |
| Candidate commit SHA | `[REQUIRED: 40 lowercase hexadecimal characters]` |
| Package-manifest SHA-256 | `[REQUIRED]` |
| Reviewer identity | `[REQUIRED]` |
| Attestation locator | `[REQUIRED]` |
| Review role | `Specification and inventory review` |
| Review date | `[REQUIRED: YYYY-MM-DD]` |
| Coverage summary | `[REQUIRED]` |
| Review method | `[REQUIRED]` |
| Provision coverage | `[REQUIRED: population and identifiers reviewed]` |
| Mapping-record coverage | `[REQUIRED: population and identifiers reviewed]` |

## Review scope

Make and record an explicit determination for each of:

- source identity, version, checksum, and official locator;
- Publication rights;
- Provision population;
- provision identifiers;
- provision hierarchy;
- provision granularity;
- provision coverage;
- predecessor integrity;
- absence of omitted, duplicated, invented, or wrong-version provisions;
- record, catalog, and registry agreement; and
- change history.

## Findings

Critical and Important findings cannot be accepted and must be resolved.
Only Minor findings may be accepted, with a named acceptor, acceptance
rationale, and disposition date.

| Finding ID | Affected record IDs | Severity | Description | Evidence | Required action | Status | Disposition | Resolver or acceptor | Disposition date | Acceptance rationale |
|---|---|---|---|---|---|---|---|---|---|---|
| `[REQUIRED OR NONE]` |  | Critical / Important / Minor |  |  |  | open / resolved / accepted (Minor only) |  |  | YYYY-MM-DD |  |

## Overall conclusion

Select exactly one: `pass`, `pass_after_correction`, or `stop`.

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
