# HMO Evidence Explorer — pilot 0.1

A small research interface connecting HMO identity to **study-specific** evidence. It has no runtime dependencies, no backend, no accounts, and no analytics. It runs as static files.

## Run

From the repository root:

```sh
python3 -m http.server 8000
```

Open **http://localhost:8000/explorer/**. A local web server is required because the interface loads `data/pilot.json`; double-clicking `index.html` may fail browser security restrictions.

For a portable demonstration, run `npm run build:standalone` and open `dist/mommis-explorer.html` directly in a browser. That generated file embeds the dataset and code; it does not require a server or network connection except when opening source links. Browser-local notes are specific to the browser/origin and do not synchronize between the standalone and served versions.

## Try it

1. Select E001 to inspect the Bi-26 culture-growth observation and its source location.
2. Choose **Immune endpoints** to inspect E003. The three-HMO mixture, bacterial intervention, mouse model, comparator and interpretation boundary remain visible.
3. Open **Molecular records** and choose 3-FL. Its identifier exists, but the interface correctly shows no evidence records in this pilot.
4. Write a curation note. It autosaves in the current browser when storage is available. Otherwise notes remain in memory for the session. Export the dataset to retain a portable JSON copy.
5. Export RDF for contextual study records, not universal biological axioms.

No notes are sent to Drive or GitHub. The JSON export contains all records and personal notes, regardless of current filters. The RDF export omits personal notes. There is no import workflow yet; exported notes can be reviewed as JSON and incorporated manually.

## Scientific status

- Two identifier records copied from the project mapping sheet, with exact row locations and WURCS; independent reconciliation against the live glycan registry is pending.
- Three **draft extractions** from two primary studies. Source passages were inspected during implementation; this is not domain review, a systematic review, or a risk-of-bias assessment.
- Two records come from Zabel et al. (2019), so they are not independent replication.
- The mouse study is the PDF already present at `Literature/msystems.00392-26.pdf`. Its mixture evidence must not be relabeled as isolated 2′-FL evidence.
- No infant clinical endpoint, recommendation, or complete causal path is asserted.
- Draft status is independent of personal curation notes; saving a note does not approve a scientific assertion.

## Extend the data

Edit `data/pilot.json`, not the rendered HTML. Add a source, then a record with a stable local ID, glycan references, exposure type, experimental system, strain, comparator, endpoint, source location, limitation, and review status. Untranscribed values must remain explicitly missing, rather than guessed. Keep mixture membership separate from evidence of an individual molecule's effect.

```sh
npm test
npm run build:rdf
```

These commands use Node.js 18+ and require no package installation. Commit the JSON and regenerated Turtle together. `model.mjs` contains filtering, integrity checks, and RDF generation; `app.mjs` renders the interface; `styles.css` controls presentation.

The RDF uses a clearly provisional `https://example.org/mommis/pilot/` namespace. Its `GlycanRecord` is an information record, not an OWL molecular class, and `StudyAssertion` contains statement text plus context. It does not establish BFO/RO compliance or import an approved MOMMIS ontology. `mentionsGlycan` is an indexing link, not proof of causality.

The supplied SPARQL example works on the exported graph when loaded into a triple store. The browser itself uses JavaScript filters and has no SPARQL service or reasoner.

## Next small contribution

Review E001 against Figure 2 of Zabel et al., transcribe the substrate concentration with its source location, and have a domain reviewer check the wording. Then agree the first formal relation mapping with Alex and Matthew before expanding the ontology.
