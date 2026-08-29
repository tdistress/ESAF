# Validation harness bundle hot-path implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or executing-plans.

**Goal:** Land Issue #90 bundle mutation-matrix hot path with equivalence proof; leave hosted 40% measurement for post-merge evidence.

**Architecture:** Mirror qualified-review hot path: frozen 16-case inventory, pure schema/state/findings boundaries, narrow matrix tests, opt-in equivalence verifier, retain representative full `assemble_package` coverage.

**Tech Stack:** Python unittest, jsonschema Draft202012Validator, Git SHA binding.

## Status

Implemented on `cursor/bundle-hot-path-7eec`:

- Design: `docs/superpowers/specs/2026-08-29-validation-harness-bundle-hot-path-design.md`
- Inventory digest: `e424ad26f9dba7cda0663194acc10990d73caa4ce0ead486a52b44fb60302aa1`
- Equivalence: `python3 tools/verify_mapping_review_bundle_hot_path_equivalence.py --check --candidate-sha <SHA>`

Remaining after merge: three hosted full-suite timings vs 751s median for Issue #90 closeout.
