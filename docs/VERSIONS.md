# Major-version policy

Emily requested separate versions on 27 October 2026 so major reductions or redesigns remain reversible and reviewable.

| Version | Branch | Reference |
|---|---|---|
| v1: broad evidence / corpus explorer | `feature/hmo-evidence-explorer` | PR #2; baseline `55097946fe0c3e63f81f8854167e3f1f45382ac6` |
| v2: focused HMO MVP | `feature/mommis-mvp-v2` | [PR #3](https://github.com/Buffalo-Ontology-Group/MOMMIS/pull/3) |

For future major updates, create a new numbered branch from the selected prior commit and a separate draft PR. Record its parent version, scope changes and omissions. Leave previous PRs and branches intact. Never force-push, delete, close, or merge a reference version as part of a redesign unless Emily explicitly requests it. Small fixes within one version may update that version's PR.

This version is an alternative to PR #2, based on the same work, not a request to merge both independently. Neither PR is merged automatically.

## v3 — original-evidence-first MVP

Branch: `feature/mommis-mvp-v3`. Parent: PR #3 commit `6360a88b097bee5a4dd8349e302874ec5a2101ce`. Evidence source: PR #2 commit `55097946fe0c3e63f81f8854167e3f1f45382ac6`. Replaces v2's nine added records with seven original corpus records, preserving E001–E003. New C-prefixed IDs refer to original edge IDs; retired E004–E012 are not repurposed. Browser review notes are kept in a separate v3 store. Earlier notes remain with v2.
