# MVP v3 scope and evidence selection

Emily asked to use the original evidence explorer before searching elsewhere. This revision replaces all nine v2 additions with seven explicitly selected original corpus records. It retains the original three contextual pilot records, both molecular identifier mappings, the focused ontology and the interface structure. No new web or literature search was performed.

The selection contains **10 evidence records, 14 core interface entities and eight cited source documents**. Source documents include reviews and must not be counted as independent experiments. All records need expert validation. The underlying OWL is unchanged from v2: 18 local and 13 external named class declarations.

## Source boundary

All evidence comes from PR #2 at commit `55097946fe0c3e63f81f8854167e3f1f45382ac6`:

- `explorer/data/pilot.json`: original E001–E003 and both identifier mappings.
- `explorer/knowledge-graph/source/original.html`: original edge IDs 724, 1002, 1816, 5321, 4121, 5109 and 5653.

`explorer/data/original-selection.json` stores exact copies of the selected source records and SHA-256 digests of both source files. The version's tests compare those copies against the pinned Git objects. `docs/mvp-selection.json` records selection reasons, omitted candidates and retired v2 IDs. No full corpus is loaded into the new interface.

## Selected records

| ID | Why retain it | Boundary to keep visible |
|---|---|---|
| E001 | Existing contextual Bi-26 growth extraction | Strain and culture context; no infant clinical inference |
| E002 | Existing fermentation-product extraction | Same paper as E001; does not establish host effects |
| E003 | Existing mouse immune-endpoint extraction | Three-HMO mixture plus microbe; not isolated 2′-FL |
| C0724 | Milk occurrence in secretor context | Background occurrence statement, not a universal milk composition axiom |
| C1002 | Reported B. infantis growth under oxidative stress | Exact strain, comparator and dose absent from selected excerpt |
| C1816 | Epithelial pathogen adhesion | Source-derived review statement; primary assay unresolved |
| C5321 | Human formula/cytokine connection | Resolve pronoun and full formula composition; retain GOS comparator |
| C4121 | NEC model differences | Preserve reported non-improvement in piglets alongside rat/mouse findings |
| C5109 | IgE endpoint relevant to the immune-development question | Selected excerpt omits species/age; do not infer oral tolerance |
| C5653 | Epithelial glycocalyx endpoint | Both 2′-FL and 3-FL mentioned; combined versus separate treatment unresolved |

The named sources in the corpus are PDF filenames. Links open the pinned original extraction, not those PDFs. No cited PDF was newly fetched or verified in this revision. Original `accepted` / `review` labels and numerical scores are preserved as imported metadata; the current status is always `Imported extraction — unverified` for corpus records.

## Alignment with the proposal

1. **Core ontology:** retain v2's focused OWL and Alex's prebiotic-disposition pattern. Avoid deriving new universal axioms from imported edges.
2. **Molecular identity:** reuse the existing MilkOligoDB–GlyTouCan / WURCS mappings for 2′-FL and 3-FL. C5653 explicitly mentions 3-FL; no other 2′-FL finding is transferred to it.
3. **Small evidence graph:** 10 traceable records, preserving context and uncertainty. This is a shortlist for curation, not completion of the human-validated assertion target.
4. **Competency questions:** four executable SPARQL queries, with original provenance also preserved in RDF. The browser displays saved results, not a SPARQL engine.
5. **AI benchmark:** worksheet includes original excerpts/statuses and empty human-adjudication fields. Source passages still need verification. Resolve primary-study overlap before evaluation splitting.

The evidence namespace `https://w3id.org/mommis/mvp/` remains provisional, with no claim of registered/resolving identifiers.

## Review with Alex

- Which existing source passage best distinguishes measured microbial growth from realization of the prebiotic disposition?
- Which endpoints need an observation/quality representation rather than a production/process mapping?
- Can the existing allergy/IgE sources support a specific oral-tolerance mechanism, or is this a documented literature gap?
- Which source passages should be adjudicated first for a small gold-standard extraction benchmark?

Check these existing cited sources first. Add outside literature only to fill a specific remaining gap.
