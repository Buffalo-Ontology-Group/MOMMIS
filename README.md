# MOMMIS Evidence Explorer — MVP v3

This version follows the original-evidence-first workflow: **10 selected records from PR #2, 14 core interface entities and two molecular identities**. It replaces the nine v2 additions with seven original corpus records, keeping the original three contextual pilot extractions. No new literature search was used.

## Open the interface

Download `preview/mommis-mvp-v3.html` with GitHub's raw download button and open it in a browser. The clickable map, source inspector, molecular identifiers, OWL inspection, four query demonstrations and exports work offline. Original excerpts, page references, edge IDs and imported status are visible for every selected corpus record. Corpus source links open the archived extraction, not the cited PDFs.

For the live OWL-backed interface:

```bash
python3 -m venv .venv
.venv/bin/pip install -r server/requirements.txt
.venv/bin/python server/ontology_backend.py --github --branch feature/mommis-mvp-v3
```

Open http://localhost:8000/explorer/ . The backend checks this branch's OWL every 30 seconds while queried. Invalid updates retain the last valid graph. The offline HTML does not synchronize. OWL changes update ontology inspection; evidence curation remains a separate edit to `explorer/data/mvp.json`.

## Scientific boundaries

Eight cited source documents include reviews; this is not a count of independent studies. Three pilot records remain draft extractions, and seven corpus records remain unverified even when their imported status says accepted. Missing comparator, dose and model details are explicit. The negative piglet result in C4121 is retained. Oral tolerance remains an evidence gap.

The focused ontology and its prebiotic-disposition pattern are unchanged from v2: 18 local classes, 13 external named declarations, no full upstream import closure. No corpus effects are promoted to universal OWL axioms. 3-FL is mentioned only in C5653's unresolved two-glycan context; it does not inherit other 2′-FL evidence.

## Rebuild and verify

```bash
.venv/bin/python scripts/build-mvp.py
npm test
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
npm install --no-save playwright@1.56.1
npx playwright install chromium
node tests/mvp-browser.cjs
```

Build outputs: contextual RDF/Turtle, saved results from `queries/*.rq`, OWL snapshot and standalone HTML. The browser displays saved SPARQL results. Source-provenance tests compare selected records with pinned PR #2 Git objects; a full repository clone is required for that check. The curation CSV includes original extracted wording but leaves exact verified passages and gold labels empty.

## Versions

[PR #2](https://github.com/Buffalo-Ontology-Group/MOMMIS/pull/2) retains the full corpus. [PR #3](https://github.com/Buffalo-Ontology-Group/MOMMIS/pull/3) retains the first focused MVP. This is a separate v3 branch and draft PR; earlier versions are not modified, closed or merged.

See [selection rationale](docs/MVP_SCOPE.md), [selection manifest](docs/mvp-selection.json) and [version policy](docs/VERSIONS.md).
