# MOMMIS collaboration rules

For a major redesign, scope reduction, or new release, follow `docs/VERSIONS.md`: create a new numbered branch and separate draft PR from the selected prior version. Preserve previous PRs/branches and identify the parent commit. Do not merge, close, delete, or force-push a prior version unless Emily explicitly requests it. Routine fixes may remain within their current version.

Keep molecular identity, experimental exposure, study-specific evidence and health interpretation separate. Preserve source, comparator, species/strain and review status. Retain Alex Diehl's prebiotic-disposition modeling decision unless a later explicit decision changes it. Do not promote a candidate mapping to a validated causal assertion.

The active ontology is `ontology/mommis-aligned.owl`. The active evidence shortlist is `explorer/data/mvp.json`. Rebuild with `scripts/build-mvp.py`. Historical migration scripts and original ontology sources are provenance, not commands to rerun over new edits.
