> MVP v2 note: the active module now retains 18 local classes. Historical notes below describe PR #2. Use the root README and docs/MVP_SCOPE.md for the current launch instructions, scope and branch.

> **Updated decision, 2026-10-14:** prebiotic **disposition** is agreed (not role). See [the disposition pattern](PREBIOTIC_PATTERN.md). The canonical aligned ontology now has 25 local classes. Earlier review notes below describe the pre-alignment state where explicitly noted.

> **Canonical edit source:** `mommis-aligned.owl`. The [backend](../server/README.md) can read this file directly from GitHub. The aligned Turtle and interface snapshots are derived exports.

> **For the combined version incorporating the older MOMMIS models, open `mommis-aligned.owl` or `mommis-aligned.ttl`. See [Alignment review](ALIGNMENT_REVIEW.md). This page documents the earlier four-class pattern.**

# MOMMIS milk core — proposed pattern for review

Open `mommis-milk-core.owl` in Protégé using File → Open. The file uses OWL in RDF/XML syntax. Select the Classes tab, then the local milk component classes; inspect **Equivalent To** and **SubClass Of**. No network imports are needed to inspect this draft.

This is an initial four-class pattern, not a completed MOMMIS ontology or an implementation of the entire workbook. The namespace `https://example.org/mommis/draft/milk-core/` is temporary and is not an approved MOMMIS identifier policy.

## Proposed definitions (Manchester-style notation)

| Local class | Equivalent to |
|---|---|
| MilkChemicalComponent | CHEBI:24431 and (BFO:0000050 some UBERON:0001913) |
| MilkCarbohydrate | CHEBI:16646 and MilkChemicalComponent |
| MilkGlycoprotein | CHEBI:17089 and MilkChemicalComponent |
| MilkAssociated2FL | CHEBI:147155 and MilkCarbohydrate |

The local component classes are not subclasses of milk. The generic ChEBI 2′-FL class is not restricted to milk and does not receive a prebiotic disposition or benefit assertion. No experimental dose, microbial process, or patient outcome is asserted by this module.

## Sources and import status

Modeling source: the attached snapshot of `milk_ontology_parent_decisions.xlsm`, reviewed 2026-10-14: **Term parent decisions** rows 11, 13, 16; **Glycoprotein import** row 9; **2FL example** row 5 and the class-versus-instance comment in **Immune actors** A6.

External classes and the part-of property reuse OBO IRIs but are **declarations only**. Their full definitions, hierarchies, domains, ranges, and disjointness axioms are not imported. Do not interpret this as a ROBOT-extracted module, complete BFO alignment, or validation against the upstream import closure. Agree pinned upstream versions and an extraction strategy with Alex before expanding the module.

ChEBI pages checked on 2026-10-14:
- https://www.ebi.ac.uk/chebi/CHEBI:147155 — 2′-fucosyllactose
- https://www.ebi.ac.uk/chebi/CHEBI:16646 — carbohydrate
- https://www.ebi.ac.uk/chebi/CHEBI:17089 — glycoprotein
- Relation reference: https://oborel.github.io/obo-relations/ro-and-bfo/

### Identifier reconciliation needed

The explorer's project mapping uses GlyTouCan **G49708ZB** for 2′-FL. The ChEBI:147155 page currently cross-references **G10422IZ**, and its WURCS string differs from the project mapping. The difference has not been resolved; it is not by itself proof that either identifier is wrong. Compare reducing-end representation and structural specificity before asserting a mapping. No `owl:sameAs` or class equivalence between a GlyTouCan record and a ChEBI class has been added; the existing explorer mapping is unchanged.

## Decisions for Alex

1. Are these equivalence definitions appropriate, or should we initially use necessary conditions only?
2. Is `part of some milk` an acceptable context restriction? How should we represent extracted components, synthetic 2′-FL, and molecules after ingestion? This file does not resolve temporal membership.
3. Which external ontology versions and import extraction approach should be used? Which local namespace/ID policy should replace the temporary namespace?
4. How should a particular experimental material and microbial process connect to the existing provenance-aware study assertions?
5. Prebiotic activity uses a disposition. How should measured microbial proliferation be separated from demonstrated host benefit?

## Validation and next step

Run `python3 tests/check_owl_module.py` from the repository root. This checks XML structure, the four intended equivalence patterns, and that the draft does not constrain generic 2′-FL to milk or equate GlyTouCan and ChEBI entities. It is **not OWL reasoning or a consistency check**. Protégé opening and DL reasoner validation remain to be done, followed by validation with the agreed imports.

The explorer currently still reads its JSON dataset; it does not load this OWL file. The next increment is to agree this pattern, load a reviewed import subset, add one experimental example separately, and connect a query result to the interface.
