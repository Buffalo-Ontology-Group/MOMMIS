# MOMMIS milk-components corpus graph

Open `index.html` directly in a browser, or use the **full milk-components knowledge graph** link in the served MOMMIS Evidence Explorer. This generated viewer includes all data and uses no CDN, network library, or server for browsing. Source PDFs are not included.

## Views

- **Overview:** entity and predicate distributions, ontology coverage, review backlog, and potential alias groups.
- **Neighborhood graph:** directed one-hop view, up to 36 neighbors and 80 edges at a time. Click an entity to refocus, or an edge to inspect evidence. Keyboard users can Tab to graph elements and press Enter.
- **All entities:** paginated complete inventory, mapping identifiers, confidence, and source counts.
- **Evidence & relationships:** subject, predicate, object, evidence excerpt, imported status/quality score, source filenames and page references. All matches are available through pagination.
- **Type-to-type matrix:** counts by subject and object type; select a cell to inspect those relationships.
- **Sources:** source coverage with click-through filtering.

Search/type/mapping filters select matching entities and incident relationships, preserving cross-type context. Source, predicate, status, and matrix filters further restrict the relationships. JSON export includes all filtered relationships and their endpoints, not just the capped drawing. Scores of zero are preserved.

## Source and scientific interpretation

`source/original.html` is an unchanged copy of the supplied `milk_components_knowledge_graph.html`. The build script parses its JSON literals without executing its JavaScript. Source SHA-256 is embedded in the generated viewer. Entity IDs, edge directions, evidence excerpts, source labels, scores, and statuses are preserved; no automatic merging or scientific correction is performed.

Inventory: **5,663 entities, 6,032 relationships**, 12 entity types, 17 predicates, 112 distinct source filenames on relationships. **225** entity records are marked mapped (189 ChEBI, 36 GO); **5,438** are unmapped. There are **3,867 accepted** and **2,165 review** edge labels in the supplied file. These are imported statuses, not confirmation of expert review. Mapping confidences and quality scores have no documented calibration in the attachment.

There are 16 ontology IDs assigned to multiple entity records. These may represent aliases, mentions, or distinct contexts; they are surfaced for review rather than collapsed. Node labels include measurement statements as well as molecular and biological names.

A concrete direction-check example is `2′FL → contains_component → Infant formula`; the accompanying excerpt describes formula containing 2′-FL. The viewer retains this as supplied so reviewers can inspect and correct the extraction in its originating workflow.

**This corpus graph is not the canonical OWL ontology.** Corpus `is_a` edges, mapping IDs, and “accepted” statuses are not automatically promoted into OWL axioms. The existing `/api/ontology` remains sourced from `ontology/mommis-aligned.owl`. This graph is a broader evidence-curation surface, linked from the explorer, not a claim that its thousands of entities have been integrated into the 25-class MOMMIS module.

No explicit license declaration was found in the supplied HTML. Original source attribution and publication/reuse permissions should be retained when distributing the corpus; repository-level licensing does not settle rights in quoted source excerpts.

## Rebuild

```sh
python3 scripts/build-knowledge-graph.py
```

Edit `viewer.template.html` for UI changes. Replace `source/original.html` only with an authorized updated export, then rebuild. The script verifies unique IDs and complete endpoints. Browser visual verification was unavailable in the build environment; see PR validation details.

Interaction validation uses `tests/knowledge-graph.test.cjs` with jsdom (development-only). It checks dataset equality, full-table pagination, search, neighborhood selection, evidence inspection, matrix drilldown, 112 source rows, source filtering, and empty results. These DOM checks do not substitute for visual browser review.

## Duplicate cleanup

The reproducible build now merges 76 clear duplicate entity records (5,663 → 5,587). Unicode typography/case variants are matched within entity type; measurement unit case is preserved. A reviewed allowlist permits same-type singular/plural variants sharing ontology IDs. We do not merge broad classes with subtypes or conflicting classifications solely because they share an ID. Four remaining shared-ID groups are listed in `deduplication-report.json` for review.

All 6,032 assertions remain: repeated canonical endpoint pairs with different evidence, sources, pages, scores or statuses are distinct assertions. Exact duplicate assertions are collapsed if present. Original assertions, original IDs, aliases and merged node records are retained in the downloadable JSON; the supplied HTML archive is unchanged. Aliases are searchable and visible in entity details. This does not establish that every possible semantic synonym has been reconciled.
