# Task 6 report: bounded Mermaid rendering

## Result

Implemented a deterministic 60-second per-diagram timeout for the Mermaid CLI
subprocess in `tools/mermaid_inventory.py`. A renderer timeout now removes the
block's PNG output and raises `ValueError` with the stable input identifier and
timeout value. The normal successful-render and nonzero-exit paths are
unchanged.

No Mermaid version pin, Puppeteer launch configuration, or root package
artifact was modified.

## Test-driven development record

1. Added `test_operational_renderer_removes_partial_output_after_timeout`.
   It uses the first ten discovered blocks so that block 10 retains the stable
   identifier `010-ARC-P140-5`, has the external Mermaid subprocess create a
   partial PNG, and then raises `subprocess.TimeoutExpired`.
2. Ran the focused test before the implementation. It failed because the
   unhandled `subprocess.TimeoutExpired` escaped from `render_mermaid_blocks`.
3. Added `RENDER_TIMEOUT_SECONDS = 60`, passed it only to the Mermaid CLI
   `subprocess.run` call, and translated the exception to the project error
   family after removing the partial PNG.
4. Re-ran the focused test successfully. The test verifies the exact concise
   error `010-ARC-P140-5 render timed out after 60 seconds` and verifies that
   the partial output no longer exists.

## Validation evidence

- `python -B -m unittest tests.test_mermaid_inventory.MermaidInventoryTests.test_operational_renderer_removes_partial_output_after_timeout -v`
  - Passed: 1 test.
- `python -B -m unittest tests.test_mermaid_inventory -v`
  - Passed: 32 tests.
- Required private-runtime Mermaid gate:

  ```powershell
  $runtimeRoot='C:\Users\phrea\AppData\Local\Temp\esaf-mermaid-runtime-node-22.23.1-20260808'
  $env:PATH="$runtimeRoot\bin;$runtimeRoot\node-v22.23.1-win-x64;$env:PATH"
  $env:ESAF_MERMAID_PUPPETEER_CONFIG='tools/mermaid-puppeteer-ci.json'
  python -B tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
  ```

  - Passed: `Validated 23 Mermaid ledger rows ...`.
  - The historical block-010 deadlock did not reproduce in this execution.
- `git diff --check`
  - Passed.
- Full-suite attempt: `python -B -m unittest discover -s tests -v` was first
  limited by the interactive 60-second command cap, then continued in a
  background runner. It exposed failures/errors in existing
  `test_v05_beta_release_evidence.V05LocalValidationRunnerTests` before the
  run was stopped; those tests exercise repository cleanliness and validation
  runner protocol rather than Mermaid rendering. This task does not claim a
  passing full-suite result.

## Cache and workspace state

The following untracked cache directories were already present before Task 6
work and were preserved as user-created workspace artifacts:

- `tools/__pycache__/`
- `tools/crosswalks/__pycache__/`

No additional cache directory was intentionally created; Python validation
commands used `-B` and `PYTHONDONTWRITEBYTECODE=1` where applicable.

## Concern

The 60-second timeout guarantees a bounded renderer subprocess wait, but the
real private-runtime gate happened to pass without reproducing the known
Chrome deadlock. The deterministic regression test provides the direct timeout
and partial-artifact coverage for that failure mode.
