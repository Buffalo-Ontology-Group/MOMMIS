# MVP v2 scope and rationale

## Sources reviewed

- Attached T15 proposal, “Formalizing MOMMIS: An Ontology and Evidence-Aware Knowledge Graph for Human Milk Bioactives and Infant Immune Development,” including its five specific aims and October 20 notes. The document sets a pilot target of approximately 10–15 assertions and three to four competency questions. The proposal itself is not copied into this public repository.
- Drive folder `1uZ7zykpvX_bW05yY7n17uyoJtef9Yv14`: listed all nine direct entries. Read the relevant parent-decision workbook and September 2026 modeling presentation. The literature subfolder contains a roughly 298 MB ZIP; it was inventoried, not unpacked or comprehensively reviewed. Unrelated planning documents/templates/publication lists were not used to select terms.
- `milk_ontology_parent_decisions.xlsm`: Term parent decisions rows 5–24; Immune actors rows 5–12; 2FL example rows 5–12; Modeling rules rows 5–10; existing ontology term list and key-paper notes. Candidate mappings and secondary summaries are not independent validation.
- PR #2's three contextual pilot records and two molecular mappings, preserved as selection sources. The large corpus was inspected to assess noise and ambiguity; no generic corpus edge was promoted to a verified mechanistic assertion.
- Luo et al. 2023, PMID 37641283, primary abstract read 27 October 2026. Four distinct PND21 endpoints were represented with shared study identity and incomplete comparator/dose fields. They do not count as four studies. Other workbook-selected sources need primary-passage review.

## Inclusion rules

An entity must anchor the selected glycan identities, experimental exposure, B. infantis partner, or a selected measured endpoint. An evidence record must have a traceable source and preserve its host, intervention and review status. Choose explicit records rather than automated degree ranking. Evidence count includes incomplete candidates; this is not completion of the proposal's 10–15 human-curated assertions target.

| Aim | MVP implementation | Remaining work |
|---|---|---|
| 1: core OWL/RDF | Retained 18 local classes and existing disposition / proliferation model. Removed seven out-of-scope local classes. | Alex reviews definitions, temporal milk context, parentage and imported ontology closure. |
| 2: glycan identifiers | Two existing GlyTouCan / WURCS mappings, 2′-FL and 3-FL. | Reconcile against registries; 3-FL remains identity-only. |
| 3: evidence graph | 12 contextual records from seven cited studies, preserving mixtures and species. | Verify the five workbook candidates, four abstract extractions and three earlier drafts against full text and expert review. |
| 4: competency questions | Four runnable SPARQL queries with saved results and RDF export. | Expand to class-level inference only after mappings and import closure are validated. |
| 5: AI benchmark | Exportable curation worksheet with source, candidate interpretation and blank gold-label / reviewer fields. | Select exact snippets, adjudicate labels, choose a study-held-out split, then run and evaluate one extraction approach. |

## Deliberate exclusions

Removed the full corpus from the new active interface and branch: broad nutritional categories, analytical methods, numerical measurement nodes, unrelated adult outcomes and dense gene/enzyme detail. Peptides, MFGM and generic glycoprotein classes are deferred in line with the proposal. B-cell activation, T-cell activation, adaptive immune response and phagocytosis are removed from the active OWL because this shortlist does not need their local placeholders. Their reference definitions remain in PR #2 and source history.

The active ontology retains 18 local classes and 13 external named class declarations. These 31 OWL classes are not the same count as the interface's 18 core entities. Historical source files are retained only as provenance; they are not loaded by the MVP.

## Modeling cautions carried forward

A milk component is not a subclass of milk. Material, disposition, process, measured endpoint and interpretation remain distinct. Prebiotic disposition is retained, following Alex's modeling decision. A concentration change is not automatically evidence of production; candidate links to IgA/cytokine-production classes are marked as interpretations. External GO candidates from the workbook remain annotations in the evidence model, not asserted equivalence axioms.

E003 is a mouse mixture intervention, not an isolated 2′-FL effect. E009–E012 share the Luo study; their abstract does not provide the detailed comparator or dose. E008's human formula comparison remains a candidate until the primary passage is checked. No complete 2′-FL → B. infantis → oral-tolerance causal chain is asserted.

## Questions for Alex

1. Which measured endpoint warrants mapping to a process class, and which should remain an observation / quality?
2. What single primary study and mechanism should establish the first oral-tolerance-specific assertion?
3. Which minimal evidence and exposure classes should be formally reused (for example OBI/ECO/SEPIO) before adding local terms?
4. Should the generic 2′-FL disposition restriction remain universal, or be constrained by material / experimental context?

The evidence namespace `https://w3id.org/mommis/mvp/` is provisional and is not a claim of a registered/resolving persistent identifier.
