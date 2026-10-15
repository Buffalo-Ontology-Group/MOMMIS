# Prototype handoff — 9 October 2026

## Implemented

- Dependency-free, responsive HMO evidence explorer with search, glycan/system filters, source inspection and personal curation notes.
- Two molecular records from `final_postWF` rows 682–683 of the project identifier mapping.
- Three draft extractions from two studies, including the mSystems PDF already in this repository.
- JSON export with local notes, contextual Turtle export, and a SPARQL example.
- A reproducible standalone HTML build for an offline demonstration.

## Verification

`npm test`: seven passing tests for provenance, filtering, source independence, the 3-FL evidence gap, mixture/comparator preservation, and RDF literal escaping. `npm run build:rdf`, `npm run build:standalone`, JavaScript syntax checks, and `git diff --check` passed.

Visual/browser interaction QA was not completed: the runtime lacked a browser executable and the browser download failed. Local storage, downloads, keyboard navigation and narrow-screen layout should be checked in a browser before using the prototype in a presentation. RDF strings are generated reproducibly, but were not checked with an external RDF parser/reasoner in this environment.

## Research provenance

The three design manuscripts list Emily Steliotes as an author. They informed the interface architecture; their draft biological propositions were not copied into the evidence graph as established facts. The shared mapping sheet's authorship was not independently established. The current pilot imports its two identifier rows with exact locations and labels registry reconciliation as pending.

Primary evidence comes from Zabel et al. (2019), DOI `10.1038/s41598-019-43780-9`, and Mulakala et al. (2026), DOI `10.1128/msystems.00392-26`. Source links, inspected locations, and interpretation limits are in the dataset. E001 and E002 are separate observations from one study. E003 describes a combined-intervention comparison in mice and does not isolate a 2′-FL effect.

## First review

Start with E001: check Figure 2, transcribe dose from Methods, and review the wording. Agree an ontology mapping for this one record with Alex and Matthew. The pilot uses local information-record terms; it is not yet a formal BFO/RO-aligned ontology.
