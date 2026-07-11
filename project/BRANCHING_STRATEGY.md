# Branching Strategy

ESAF uses a lightweight GitHub Flow model.

- `main` contains the current accepted project state.
- Short-lived branches use `feature/<topic>`, `fix/<topic>`, or `editorial/<topic>`.
- Release stabilization branches use `release/<version>` only when needed.
- Pull requests are required for substantive changes.
- Branches are deleted after merge.

Avoid permanent workstream branches. Tags identify published versions, for example `v0.1-alpha`, `v0.9-rc1`, and `v1.0.0`.

