# Task 3 report — timed-out Mermaid cleanup

## Delivered behavior

- Windows renderer timeouts terminate only the timed-out renderer tree with
  `taskkill /PID <pid> /T /F`.
- POSIX renderer invocations start in a dedicated session and timeout cleanup
  terminates that process group with `os.killpg(pid, signal.SIGKILL)`.
- The renderer's post-timeout pipe drain and Windows termination command retain
  the fixed five-second bound.
- Cleanup failures now fail closed with stable messages identifying the rendered
  block and the failed action: process termination, output drain, partial output
  removal, or temporary input cleanup.
- POSIX coverage verifies both the exact five-second post-kill drain and the
  block-specific failure produced when `os.killpg` raises `OSError`.
- Node, Mermaid CLI, Puppeteer configuration, and browser launch flags were not
  changed. No global browser cleanup was added.

## Test-first record

The added POSIX session/process-group test and tightened cleanup-failure
expectations were run before the implementation. The RED run failed because the
previous implementation used `process.kill()` on POSIX and converted all cleanup
failures to an ordinary render timeout. The minimum implementation then made the
focused suite pass. R1 strengthened the POSIX test to record both
`communicate()` calls and assert the post-kill call is exactly five seconds; a
temporary incorrect bound of four seconds failed with observed timeouts
`[60, 4]` before the intended value was restored. R1 also adds the POSIX
`os.killpg(OSError)` regression proving the stable block-specific process-
termination failure.

R2 addresses the Linux CI failure in Windows-oriented test doubles. Those tests
mocked `subprocess.run` as `taskkill` but left the platform predicate host-
dependent, so Linux selected the real POSIX `killpg` branch for synthetic PIDs.
Each Windows-oriented timeout double now explicitly simulates Windows through
`_renderer_runs_on_windows`; POSIX tests explicitly simulate POSIX. The renderer
implementation and its Windows `taskkill` and POSIX `killpg` contracts were not
changed.

## Validation

| Command | Result |
|---|---|
| `python -B -m unittest tests/test_mermaid_inventory.py -v` | Pass — 39 tests |
| `git diff --check` | Pass |
| Targeted Windows-timeout double regressions | Pass - 5 tests |
| `python tools/run_test_shards.py --shard remaining --durations 50` | Completed in 558.244 seconds but failed outside the focused Mermaid module: 1,005 tests, 3 failures, 3 errors, 6 skipped |
| `python tools/mermaid_inventory.py --check-record docs/superpowers/reviews/2026-07-27-v05-beta-mermaid-rendering.md` with `ESAF_MERMAID_PUPPETEER_CONFIG=tools/mermaid-puppeteer-ci.json` | Blocked fail-closed — available `node` is `v24.14.0`, but the gate requires `22.23.1` |

## Concern

The private Node 22.23.1 runtime is not present on this workstation's PATH; the
record gate was therefore not run successfully. The implementation correctly
refused to substitute Node 24.14.0. The untracked `__pycache__` directories were
already present before the final validation; an attempted cleanup was rejected by
the execution policy, and they remain uncommitted.
