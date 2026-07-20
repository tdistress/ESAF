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
| `predicate` | Closed provision-profile predicate describing the controlled state or measurement. |
| `provision_id` | Exact external provision ID of the containing record. |
| `result` | Closed recorded-result type such as `recorded_boolean`, `recorded_comparison`, `recorded_threshold`, or `recorded_duration`; it shall not invent a pass/fail value. |
| `result_kind` | Closed result family compatible with the cited ESAF control. |
| `subject` | Closed concrete security, authentication, evidence, vulnerability, or configuration subject. |

The existing prose markers remain mandatory and unchanged:

1. `Supported ESAF outcome: <control-id> ...`
2. `Conditions only narrow this supported claim; they do not create either outcome.`

Canonical JSON is human-readable, deterministic, and consistent with the profile’s existing canonical-JSON condition checklist.

## Source-versioned provision registry

The exact profile shall own an isolated registry module under `tools/crosswalks/`. The registry shall bind every allowed positive external provision ID to exactly one tuple of:

- cited control ID;
- result kind;
- concrete subject;
- controlled predicate; and
- recorded-result type.

Validation shall first bind the JSON `provision_id` and `control_id` to the record and relationship, then require all five registry values to match the source-versioned profile entry exactly. A value permitted for another provision or another control shall not be accepted.

The registry contains no tool, scanner, utility, actor-action, authorization, selection, invocation, execution-procedure, or assessment-performance subjects or outcomes. A tool-produced result remains valid when the structured subject and predicate are the concrete security outcome; tool identity belongs in expected evidence and provenance.

## Validator behavior

For mapped records in this exact profile, validation shall:

1. isolate the text between `External observation:` and `Supported ESAF outcome:`;
2. require exactly one terminal period around a canonical compact JSON object;
3. parse JSON without accepting duplicate or extra fields;
4. require all eight values to be nonempty strings;
5. require the two exact date-boundary literals;
6. require exact record provision and relationship control bindings;
7. resolve the provision in the source-versioned registry;
8. require the registry control, result kind, subject, predicate, and recorded-result type to match exactly; and
9. continue applying the existing supported-outcome, conditions-only-narrow, condition-evidence, prohibited-inference, population-boundary, and manifest-provenance contracts.

The superseded free-form observation predicate, activity detection, tool blacklist, and date-word inference shall be removed. There shall be one observation-validation path.

## Record migration

All 31 existing positives shall receive their registry-derived canonical JSON observation. Their nine prohibited-inference entries shall bind the exact JSON observation and cited ESAF control outcome.

Existing expected-evidence prose remains the human-readable gloss and retains tool identity only as evidence/provenance where applicable. Generated catalog output and the lifecycle digest shall be regenerated. No negative record or mapping decision changes.

## Test contract

Regression tests shall prove fail-closed behavior for:

- all reviewer tool/activity synonyms and prior active, passive, and nominal variants after prohibition rebinding;
- malformed, non-object, duplicate-key, extra-field, missing-field, non-string, and noncanonical structured claims;
- tool or actor activity used as the subject, predicate, result, or result kind;
- unknown registry values;
- incompatible result-kind/control and provision/profile combinations;
- wrong provision ID, relationship control ID, assessment-date boundary, and evidence-date boundary;
- supported-outcome marker drift and existing condition/prohibition failures; and
- a valid tool-produced concrete authentication/configuration result whose tool identity appears only in evidence.

The focused profile test shall also validate all persisted positives through the production validator.

## Task 5 extension rule

Task 5 may add a registry entry only after its own provision-level analysis produces a positive mapping decision. Each new positive shall add one exact provision/control/result profile and fail-first tests for its canonical observation. Unknown Task 5 provisions remain negative or fail closed; the validator shall never infer or synthesize a profile from free-form text, nearby provisions, or control-level similarity.
