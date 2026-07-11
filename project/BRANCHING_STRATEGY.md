# Branching Strategy

`main` contains approved publication states. Changes are proposed through short-lived branches and pull requests.

## Branch naming

- `agent/<topic>` for changes prepared by an automation or coding agent.
- `feature-<topic>` for contributor-authored features.
- `fix-<topic>` for corrections.
- `release-<version>` for release stabilization when required.
- `research-<topic>` for exploratory work that is not yet proposed for inclusion.

Long-lived workstream branches are discouraged. Existing historical branches may remain until their content is reviewed and merged or closed.

## Merge policy

Every change to `main` should use a pull request, pass editorial checks, and preserve a clear audit trail. Feature branches should be deleted after merge.
