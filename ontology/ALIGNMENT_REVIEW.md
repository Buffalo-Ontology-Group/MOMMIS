> **Updated decision, 2026-10-14:** prebiotic **disposition** is agreed (not role). See [the disposition pattern](PREBIOTIC_PATTERN.md). The canonical aligned ontology now has 25 local classes. Earlier review notes below describe the pre-alignment state where explicitly noted.

# MOMMIS aligned draft — review with Alex

**Open `mommis-aligned.owl` in Protégé.** `mommis-aligned.ttl` encodes the same graph. This combined review draft supersedes the four-class file as the meeting entry point; the original four-class pattern and the two supplied source files remain available.

## Kept from each version

- **New milk-core:** four explicit component definitions; composition uses `part of`, not `is a milk`; generic 2′-FL is not constrained to occur in milk.
- **Original Turtle:** MOMMIS namespace and readable local identifiers; process/material separation; useful descriptions and provenance intentions.
- **High-level RDF:** all 14 named concepts, including immune processes, GALT, intestinal epithelial cells, peptides, MFGM, microbiota balance and immune health. Original descriptions are kept as `legacyDefinition` annotations, not silently endorsed definitions.
- **Both legacy files:** all detected conceptual property assertions and example axiom annotations are preserved as 19 annotation-only records in `legacy-links-for-review.ttl`. These are not imported into the ontology as validated effects.

There are 18 local classes in the aligned file. External classes are declarations, not complete imports. Candidate GO mappings are annotations only. Four component equivalences remain proposals pending review.

## Corrections and deliberate deferrals

| Original issue | Aligned decision |
|---|---|
| HMO parent CHEBI:75771 labeled oligosaccharide | Replaced with CHEBI:50699 (oligosaccharide). ChEBI:75771 is mouse metabolite. |
| Bioactive peptide modeled as something having a peptide part; peptide/HMO under anatomical entity in RDF | Peptide is a subclass of CHEBI:16670; HMO is a subclass of CHEBI:50699. No universal bioactivity restriction added. |
| Noncanonical `bfo#Process`, `bfo#MaterialEntity`, `bfo#Disposition` terms | Use declared numeric OBO identifiers for accepted broad categories; uncertain categories remain unresolved. |
| ImmuneHealth and GutMicrobiotaBalance placed under function/disposition | Preserve both concepts, remove disputed upper-category assertions, flag definitions for Alex. |
| Direct participant/role assertions on class IRIs and class/individual punning | Preserve original links in a separate annotation-only review ledger. No blind conversion to existential restrictions. |
| Broad affects/regulates links with no study context | Preserve as review records, not universal biological effects. |
| Placeholder PMIDs and “Your Name”/example GitHub metadata | Placeholder citations excluded from accepted evidence; real repository reference and Emily Steliotes creator metadata used. Originals remain archived. |
| Multiple namespaces and unnamed ontology | Reuse the old `http://purl.obolibrary.org/obo/mommis#` namespace provisionally. Record legacy IRIs in annotations and TSV; no claim of PURL registration. |
| Definition prose in rdfs:isDefinedBy | Preserve as legacyDefinition annotation; do not use prose as an ontology source IRI. |
| Large and mixed-version imports | No automatic network imports in the meeting draft. This is a usability/review boundary, not an import-complete release. Select pinned import subsets with Alex. |

## Not yet resolved

- HMO membership: chemical structural family versus molecules currently occurring in human milk; no equivalence to the new milk-associated component classes is asserted yet.
- Disposition choice is resolved. Measured microbial proliferation versus observed culture growth and demonstrated host benefit still requires careful evidence mapping.
- Temporal scope of `part of milk`, especially extracted or ingested material.
- Detailed GO/CL/UBERON mappings and the operational definitions of immune health and microbiota balance.
- The existing 2′-FL GlyTouCan discrepancy: project G49708ZB versus ChEBI's G10422IZ cross-reference. No exact mapping is asserted.
- Interface integration: the ontology tab now reads the OWL backend; evidence records remain separately curated and no full DL reasoning is performed by the server.

## Validation

Both source files parsed successfully. The aligned OWL RDF/XML and Turtle serialize the same graph (265 triples). Automated checks verify 18 local classes, the HMO and peptide category corrections, retention of four component definitions, and no class/named-individual punning in the aligned module.

An OWL RL test with explicitly labeled synthetic fixtures confirms that a chemical/carbohydrate/2′-FL instance related by part-of to a milk sample is classified as MilkAssociated2FL, while a comparable instance with no milk-context assertion is not inferred into that class. This is a limited entailment test, not proof of absence under open-world semantics, biological validation, a full DL consistency check, or validation against upstream imports. Fixtures are not saved in the ontology.

Rebuild and check with the Python package versions pinned in `requirements-validation.txt`.

```sh
python3 scripts/align-ontology.py
python3 tests/check_aligned_ontology.py
```

## Provenance and licensing

`legacy/mommis-2025.ttl` and `legacy/mommis-high-level.rdf` are byte-preserved copies of the supplied attachments. `legacy-iri-crosswalk.tsv` maps retained local classes and properties; `legacy-links-for-review.ttl` preserves the conceptual links. Review entries do not establish equivalence between old and new term meanings.

The original Turtle declares CC BY 4.0. That declaration is preserved on this derivative; these ontology artifacts should not be assumed to inherit the repository's blanket CC0 license. Attribution: Emily Steliotes / MOMMIS Project Team, original supplied MOMMIS drafts. The high-level RDF contains no explicit license declaration; confirm the intended unified release license before publication.

Term checks, 2026-10-14: https://www.ebi.ac.uk/chebi/CHEBI:75771 ; https://www.ebi.ac.uk/chebi/CHEBI:50699 ; https://www.ebi.ac.uk/chebi/CHEBI:16670 . Other finer mappings remain candidates.
