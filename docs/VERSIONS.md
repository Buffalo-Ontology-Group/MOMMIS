# Major-version policy

Emily requested separate versions on 27 October 2026 so major reductions or redesigns remain reversible and reviewable.

| Version | Branch | Reference |
|---|---|---|
| v1: broad evidence / corpus explorer | `feature/hmo-evidence-explorer` | PR #2; baseline `55097946fe0c3e63f81f8854167e3f1f45382ac6` |
| v2: focused HMO MVP | `feature/mommis-mvp-v2` | [PR #3](https://github.com/Buffalo-Ontology-Group/MOMMIS/pull/3) |

For future major updates, create a new numbered branch from the selected prior commit and a separate draft PR. Record its parent version, scope changes and omissions. Leave previous PRs and branches intact. Never force-push, delete, close, or merge a reference version as part of a redesign unless Emily explicitly requests it. Small fixes within one version may update that version's PR.

This version is an alternative to PR #2, based on the same work, not a request to merge both independently. Neither PR is merged automatically.
