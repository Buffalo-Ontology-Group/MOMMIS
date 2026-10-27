# MOMMIS Evidence Explorer — MVP v2

This version narrows MOMMIS to an HMO-centered research prototype: 18 core interface entities, two molecular identifier entries, and 12 contextual evidence records. It follows Emily Steliotes's T15 proposal: a focused ontology, reuse of MilkOligoDB–GlyCosmos identifiers, a small evidence graph, four competency questions, and a starter for human-validated AI curation.

## Open the interface

Download `preview/mommis-mvp-v2.html` using GitHub's raw download button and open it in a browser. It is a self-contained interactive preview; it does not synchronize with GitHub after downloading.

For the live OWL-backed interface:

```bash
python3 -m venv .venv
.venv/bin/pip install -r server/requirements.txt
.venv/bin/python server/ontology_backend.py --github --branch feature/mommis-mvp-v2
```

Open http://localhost:8000/explorer/ . The backend polls this branch's `ontology/mommis-aligned.owl` every 30 seconds while queried, retains the last valid graph on failed updates, and exposes its current raw OWL at `/api/ontology.owl`. It parses asserted structure, without full imports or DL reasoning. Updating the OWL changes ontology labels/structure in the interface; study records still require separate curation in `explorer/data/mvp.json`.

## What is included

- A clickable evidence landscape grouped by microbial utilization, metabolism, epithelial response and immune endpoints.
- Twelve records from seven cited studies: three carried-forward draft extractions, five mapping-workbook candidates, and four abstract-checked mouse endpoints. None is marked expert-validated. Multiple endpoints are not independent studies.
- 2′-FL and 3-FL GlyTouCan / WURCS identifiers carried forward from the earlier project mapping. No selected 3-FL evidence; no transfer of 2′-FL results.
- Eighteen retained local ontology classes, including prebiotic disposition, the bacterial proliferation pattern, milk-component classes and selected immune concepts. Full-import validation remains outstanding.
- JSON, contextual RDF/Turtle, OWL, SPARQL-query and curation-CSV downloads. Local review notes can be exported; they do not edit GitHub.

The default visualization is an evidence organization, not a proven biological causal path. Oral tolerance, infant exposure, direct host benefit and identifier reconciliation remain visible curation gaps.

## Rebuild and test

```bash
.venv/bin/python scripts/build-mvp.py
npm test
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
npm install --no-save playwright
npx playwright install chromium
node tests/mvp-browser.cjs
```

`queries/*.rq` are executed against `explorer/data/mvp.ttl` during the build. The browser displays saved results, not a live SPARQL endpoint. `scripts/build-mvp.py` builds RDF, result sets, the OWL snapshot and the standalone HTML. Edit the JSON and canonical OWL, then rebuild. Do not rerun historical ontology migration scripts over later curation.

## Version preservation

[PR #2](https://github.com/Buffalo-Ontology-Group/MOMMIS/pull/2), branch `feature/hmo-evidence-explorer`, remains the complete reference version at commit `55097946fe0c3e63f81f8854167e3f1f45382ac6`. The full 5,587-entity / 6,032-assertion corpus and original upload are removed from this branch's active tree and remain available in that version and Git history.

See [MVP scope and rationale](docs/MVP_SCOPE.md), [selection manifest](docs/mvp-selection.json), and [version policy](docs/VERSIONS.md). Future major changes get a new branch and PR, preserving the prior version.
