> MVP v2 note: the active module now retains 18 local classes. Historical notes below describe PR #2. Use the root README and docs/MVP_SCOPE.md for the current launch instructions, scope and branch.

# MOMMIS ontology backend

The canonical editable ontology is **`ontology/mommis-aligned.owl`**. The backend parses this OWL RDF/XML file and exposes its named classes, labels, asserted parents, equivalence expressions, and review notes at `/api/ontology`. The browser's **Ontology** tab uses that API. There is no separate manually maintained class table.

## Start locally, following GitHub edits

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r server/requirements.txt
.venv/bin/python server/ontology_backend.py --github
```

Open **http://localhost:8000/explorer/**. Leave the server running.

The default tracked branch is `feature/hmo-evidence-explorer` (PR #2). Edit `ontology/mommis-aligned.owl` on that branch, or save it in Protégé and commit/upload the edited file. Do not regenerate it with the one-time legacy alignment script after making new edits: that script rebuilds the earlier draft from archived inputs.

While the page is open, the interface requests an update every 30 seconds. The backend checks GitHub at most once per 30 seconds, replaces its in-memory ontology after successful parsing, and returns the new fingerprint and class data. GitHub/network caching can delay visibility; this is polling, not an instantaneous webhook. No backend restart is needed for OWL changes. If no page is open, it refreshes on the next request.

When PR #2 is merged, start with:

```sh
.venv/bin/python server/ontology_backend.py --github --branch main
```

For local Protégé edits before uploading, omit `--github`; the same refresh cycle reads the local OWL file instead. GitHub mode uses GitHub as the source of truth and does not upload local edits.

## Validation and fallback

The API validates RDF/XML parsing plus ontology/class declarations; rejects oversized files and XML entity declarations; and does not dereference ontology imports. It is not a full OWL DL validator or reasoner. If an update fails, it returns the last successfully parsed ontology with `status: stale` and an error displayed by the UI. At first startup, the checked-out local OWL file is the fallback if GitHub cannot be reached; it is explicitly marked stale. If neither version is usable, the API returns 503.

The server binds to localhost only and performs no GitHub writes. There is no hosted deployment yet. Editing GitHub updates a running GitHub-connected backend; it cannot update a downloaded offline file or a stopped server.

## Offline preview and derived files

The portable `preview/mommis-explorer.html` embeds an OWL-derived snapshot and always labels it offline. A simple static server falls back to `explorer/data/ontology.json` with the same snapshot label. These files do not claim to be live.

Regenerate after changing the canonical OWL:

```sh
.venv/bin/python scripts/build-ontology-snapshot.py
npm run build:standalone
cp dist/mommis-explorer.html preview/mommis-explorer.html
```

The snapshot script also refreshes `ontology/mommis-aligned.ttl` from the canonical OWL. Edit the OWL only; Turtle, JSON and standalone HTML are derived exports. Commit regenerated files when distributing an offline preview. The live API needs no rebuild.

## Scope

The backend reads ontology structure. Existing evidence records and personal notes remain separate; no assertion is approved, no clinical inference is made, and no evidence-to-class equivalence is inferred automatically. Further evidence integration requires reviewed mappings. The display handles named parents, intersections, unions, and basic property restrictions; other OWL expressions are explicitly marked as not displayed. Imports and complete logical reasoning are outside this iteration.

Tests: `python3 tests/test_ontology_backend.py` (requires server dependencies).
