# MOMMIS
Multi-ontology framework of Maternal Milk for Immune Systems

Developers:  Emily Steliotes, Matthew Lange, Alexander Diehl

## HMO Evidence Explorer

The first research prototype lives in [`explorer/`](explorer/README.md). It connects two MilkOligoDB-derived glycan identifiers to three draft, source-linked study records and provides filtering, source inspection, local curation notes, and JSON/RDF exports.

```sh
python3 -m http.server 8000
```

Open **http://localhost:8000/explorer/**. Read the [pilot documentation](explorer/README.md) for scientific scope, data editing, and validation. This is an evidence-curation prototype, not a completed formal ontology or clinical decision tool.
