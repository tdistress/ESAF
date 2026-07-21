# Cyber Essentials Plus v3.2 structured reverse-observation design

## Status and scope

This design replaces free-form external-observation inference in the exact `uk-ncsc--cyber-essentials-plus-test-specification--3.2--esaf-0.4-alpha--0.2.0` reverse-evidence profile. It changes the authoring and validation contract for the 31 existing positive records without changing any mapping disposition, target control, relationship type, coverage, confidence, or provenance.

Task 5 content is outside this change. The Task 6 README refresh remains deferred.

## Problem

Free-form prose cannot be made fail-closed with a maintainable synonym blacklist. Reporting phrases such as “the dated assessment result records that” can make tool use, execution, authorization, or other procedure activity look like a security result even when the asserted fact contains no security or configuration outcome.

The reverse profile therefore needs a closed observation language. Unknown subjects, predicates, results, result kinds, provision bindings, control bindings, and date-boundary forms must fail by default.

## Canonical observation contract

Text immediately after `External observation:` shall be one canonical compact JSON object followed by a period. The object shall contain exactly these eight string fields, serialized with sorted keys and compact separators:

| Field | Contract |
| --- | --- |
| `assessment_date_boundary` | Exact value `assessment_date_required`. |
| `control_id` | Exact ESAF control ID cited by the relationship leg. |
| `evidence_date_boundary` | Exact value `evidence_date_required`. |
| `predicate` | Closed leg-profile measurement dimension or status question; it shall not encode the observed answer. |
| `provision_id` | Exact external provision ID of the containing record. |
| `result_kind` | Closed outcome-neutral measurement family compatible with the cited ESAF control. |
| `result_type` | Closed recorded-result representation such as `recorded_boolean`, `recorded_comparison`, `recorded_threshold`, or `recorded_duration`; it shall not encode the recorded answer. |
| `subject` | Closed outcome-neutral security, authentication, evidence, vulnerability, or configuration measurement subject. |

The existing prose markers remain mandatory and unchanged:

1. `Supported ESAF outcome: <control-id> ...`
2. `Conditions only narrow this supported claim; they do not create either outcome.`

Canonical JSON is human-readable, deterministic, and consistent with the profile’s existing canonical-JSON condition checklist.

All four semantic fields—`result_kind`, `subject`, `predicate`, and `result_type`—describe only the measurement schema. They shall not contain pass/fail, true/false, compliant/noncompliant, certified/uncertified, success/failure, equivalent/not-equivalent, or close morphological variants. For a threshold measurement, severity classifications such as `high_risk` and `low_risk` encode the measured answer and are likewise prohibited in every semantic field. Validation shall tokenize semantic identifiers on underscores, hyphens, and other non-alphanumeric boundaries and reject the closed answer-bearing token families and contextual severity classifications, not arbitrary substrings; for example, `password` remains valid. This prohibition applies across field boundaries so an answer cannot be smuggled into a subject, kind, predicate, or result type.

## Source-versioned relationship-leg registry

The exact profile shall own an isolated registry module under `tools/crosswalks/`. Its key is the pair `(provision_id, control_id)`, including the cited control ID, and it shall bind every allowed positive relationship leg to exactly one four-field semantic profile of:

- result kind;
- concrete subject;
- controlled predicate; and
- recorded-result type.

The registry declaration shall retain its entry sequence long enough to reject duplicate `(provision_id, control_id)` pairs before constructing the lookup map. This permits a provision to have multiple valid legs while preventing duplicate profiles for the same leg.

Validation shall first bind the JSON `provision_id` and `control_id` to the record and relationship leg, then require all four semantic registry values to match the source-versioned leg profile exactly. A value permitted for another provision, another control, or another leg shall not be accepted.

The registry shall not treat mere tool, scanner, or utility use; tool-use authorization, selection, or invocation; actor procedure activity; execution of an assessment procedure; or assessment-procedure performance as an observation when it lacks an independently defined security or control measurement. Those administrative or procedural facts are insufficient by themselves. A tool-produced result remains valid when the structured subject and predicate define the concrete security measurement, and a control measurement such as required configuration-change approval remains valid when it directly measures the control rather than merely authorizing tool use. Tool identity belongs in expected evidence and provenance.

Registry construction and integrity validation shall audit all four semantic values under the same outcome-neutral rules as claim validation. It shall reject an answer-bearing value regardless of which semantic field contains it, including a threshold profile whose result classification is disguised as a subject, kind, predicate, or result type.

Markdown records remain authoritative for mapping decisions. The registry is only a source-versioned validation allowlist and shall not create, infer, or override a relationship. For this exact mapping set, registry keys shall equal the complete set of mapped `(provision_id, control_id)` relationship legs. Integrity validation shall reject missing mapped legs, orphan keys, keys for negative or unimplemented provisions, and duplicate declarations.

## Validator behavior

For mapped records in this exact profile, validation shall:

1. isolate the text between `External observation:` and `Supported ESAF outcome:`;
2. require exactly one terminal period around a canonical compact JSON object;
3. parse JSON without accepting duplicate or extra fields;
4. require all eight values to be nonempty strings;
5. require the two exact date-boundary literals;
6. require exact record provision and relationship control bindings;
7. resolve the exact `(provision_id, control_id)` leg in the source-versioned registry;
8. require the registry result kind, subject, predicate, and recorded-result type to match exactly;
9. reject value-bearing or assurance-bearing terms and their close variants in every semantic field; and
10. continue applying the existing supported-outcome, conditions-only-narrow, condition-evidence, prohibited-inference, population-boundary, and manifest-provenance contracts.

Snapshot validation shall independently compare the registry key set with the authoritative mapped-leg set. Each leg of a valid multi-leg record is validated through its own pair key. Existing duplicate relationship-pair validation remains mandatory.

The superseded free-form observation predicate, activity detection, tool blacklist, and date-word inference shall be removed. There shall be one observation-validation path.

## Record migration

All 31 existing positives shall receive their registry-derived canonical JSON observation. Their nine prohibited-inference entries shall bind the exact JSON observation and cited ESAF control outcome.

Existing expected-evidence prose remains the human-readable gloss and retains tool identity only as evidence/provenance where applicable. Generated catalog output and the lifecycle digest shall be regenerated. No negative record or mapping decision changes.

## Test contract

Regression tests shall prove fail-closed behavior for:

- all reviewer tool/activity synonyms and prior active, passive, and nominal variants after prohibition rebinding;
- malformed, non-object, duplicate-key, extra-field, missing-field, non-string, and noncanonical structured claims;
- tool or actor activity used as the subject, predicate, result type, or result kind;
- unknown registry values;
- incompatible result-kind/control and provision/control profile combinations;
- wrong provision ID, relationship control ID, assessment-date boundary, and evidence-date boundary;
- value-bearing or assurance-bearing terms smuggled through each semantic field, including `high_risk` and `low_risk` severity classifications in every field of a threshold profile during registry audit;
- a valid multi-leg record, a duplicate relationship pair, and an incompatible pair;
- registry declarations or key sets with a duplicate, missing mapped leg, orphan, negative-provision, or unimplemented-provision entry;
- supported-outcome marker drift and existing condition/prohibition failures; and
- a valid tool-produced concrete authentication/configuration result whose tool identity appears only in evidence; and
- a valid configuration-change approval measurement, proving that the tool-use authorization exclusion does not categorically reject independently defined control measurements.

The focused profile test shall also validate all persisted positives through the production validator.

## Task 5 extension rule

Task 5 may add a registry entry only after its own provision-level analysis justifies a positive relationship leg. Each new positive leg shall add one exact `(provision_id, control_id)` profile and fail-first tests for its canonical observation. Another leg for the same provision requires its own independent profile. Unknown Task 5 legs remain negative or fail closed; the validator shall never infer or synthesize a profile from free-form text, nearby provisions, another leg, or control-level similarity.
