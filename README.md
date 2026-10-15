# MOMMIS
Multi-ontology framework of Maternal Milk for Immune Systems

Developers:  Emily Steliotes, Matthew Lange, Alexander Diehl

## MOMMIS Evidence Explorer

The first research prototype lives in [`explorer/`](explorer/README.md). It connects two MilkOligoDB-derived glycan identifiers to three draft, source-linked study records and provides filtering, source inspection, local curation notes, and JSON/RDF exports.

```sh
python3 -m http.server 8000
```

Open **http://localhost:8000/explorer/**. Read the [pilot documentation](explorer/README.md) for scientific scope, data editing, and validation. This is an evidence-curation prototype, not a completed formal ontology or clinical decision tool.


## OWL-backed explorer

For the ontology-connected interface, follow [backend setup](server/README.md). The backend can track the OWL file in GitHub, while a portable HTML download uses a labeled snapshot. The source of truth is `ontology/mommis-aligned.owl`; `.ttl` and JSON/HTML snapshots are derived artifacts.
