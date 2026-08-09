# Task 8 report: terminate timed-out Mermaid process trees

## Result

Replaced the Mermaid CLI's per-block `subprocess.run` call with a narrowly
scoped `_run_renderer` helper using `subprocess.Popen` and a 60-second
`communicate` timeout. On Windows, a timeout now invokes
`taskkill /PID <renderer-pid> /T /F` with captured output and `check=False` to
terminate only the timed-out renderer's process tree. It then drains renderer
pipes with a separate bounded five-second `communicate` call, removes the
partial PNG, and raises the pre-existing stable block-specific timeout error.

`taskkill` errors, including a nonzero result and a bounded taskkill timeout,
do not replace the renderer timeout. Successful rendering does not invoke
`taskkill`, and the existing pinned renderer, Node version, Puppeteer launch
configuration, and Mermaid command arguments are unchanged. No package or
user-created installation artifact was changed.

## Test-driven development record

1. Replaced the prior `subprocess.run` timeout test with fake-`Popen`
   behavioral coverage. The test creates a partial PNG, makes the first
   `communicate(timeout=60)` raise `TimeoutExpired`, and requires the exact
   `taskkill /PID 4242 /T /F` invocation, bounded pipe drain, partial-output
   removal, stable error, and no second renderer process.
2. Added a second fake-`Popen` test in which taskkill returns exit code 1. It
   verifies the same stable `001-ARC-P110-1 render timed out after 60 seconds`
   validation error remains observable.
3. Updated the success/configuration test to require `Popen`, retain the
   tracked no-sandbox configuration assertion, and prove successful rendering
   makes no taskkill call.
4. Before production edits, the three focused tests failed as expected because
   `render_mermaid_blocks` still invoked `subprocess.run` for the renderer;
   the fakes reported that renderer execution shall use `Popen` and that the
   expected taskkill command was absent.
5. Implemented `_run_renderer` and reran the focused module successfully.

## Validation evidence

- `python -m unittest tests.test_mermaid_inventory -v`
  - Passed: 33 tests.
- Private runtime Mermaid record gate:

  ```powershell
  $runtimeRoot='C:\Users\phrea\AppData\Local\Temp\esaf-mermaid-runtime-node-22.23.1-20260808'
  $env:PATH="$runtimeRoot\bin;$runtimeRoot\node-v22.23.1-win-x64;$env:PATH"
  $env:ESAF_MERMAID_PUPPETEER_CONFIG='tools/mermaid-puppeteer-ci.json'
  python -B tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md
  ```

  - Passed: `Validated 23 Mermaid ledger rows ...` in 36.3 seconds.
- `git diff --check`
  - Passed.
- `python -B -m unittest discover -s tests -v`
  - Did not complete: the command exceeded the 184-second execution bound
    without captured test output. This report does not claim a full-suite pass.

## Workspace state and concerns

- Pre-existing untracked cache directories were preserved:
  `tests/__pycache__/`, `tools/__pycache__/`, and
  `tools/crosswalks/__pycache__/`.
- The private-runtime gate did not reproduce a renderer timeout; deterministic
  fake-process coverage directly exercises the cleanup branch.
- The full test suite needs a longer-running environment or diagnosis before a
  whole-suite success claim can be made.
