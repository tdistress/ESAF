# Security and Overclaiming Review Worksheet

## Review identification

| Field | Value |
|---|---|
| Mapping-set identifier | `[REQUIRED]` |
| Candidate commit SHA | `[REQUIRED: 40 lowercase hexadecimal characters]` |
| Package-manifest SHA-256 | `[REQUIRED]` |
| Reviewer identity | `[REQUIRED]` |
| Attestation locator | `[REQUIRED]` |
| Review date | `[REQUIRED: YYYY-MM-DD]` |
| Coverage | `[REQUIRED]` |

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
- nonclaims, including certification, compliance, equivalence, endorsement,
  and assurance.

## Findings

| Finding ID | Affected record IDs | Severity | Description | Evidence | Required action | Status | Disposition |
|---|---|---|---|---|---|---|---|
| `[REQUIRED OR NONE]` |  | Critical / Important / Minor |  |  |  | open / resolved / accepted |  |

## Overall conclusion

Select exactly one: `pass`, `pass_after_correction`, or `stop`.
