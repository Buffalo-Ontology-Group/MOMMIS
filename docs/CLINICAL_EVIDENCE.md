# Clinical outcomes review — 3 November 2026

This v4 branch preserves PR #4 and adds eight primary-study summaries. Default view shows only the eight; select All 18 records for the earlier ten. Download `preview/mommis-mvp-v4.html` and open in a browser. The standalone HTML is an offline snapshot. The served interface still uses the existing OWL backend. No new disease efficacy axioms were added to OWL.

## What was screened

All 6,032 edge records in the original PR #2 archive at commit `55097946fe0c3e63f81f8854167e3f1f45382ac6` were searched for NEC, milk allergy, β-lactoglobulin, EVC001 and related terms (271 broad candidates, including background and references). This is a targeted scan, not a full-text systematic review of every original PDF. The search audit lists candidate IDs and exact selected original records. Original snippets and extraction labels are preserved separately from the new interpretation.

Tobias 2022 is already present. Reviews supply leads for LNFP III/CMA, DSLNT/NEC and contrasting 2′-FL animal studies. Henrick 2021 is named in the archive, but some attributed content describes Bacteroides experiments, suggesting source misattribution. Those imported assertions were not validated or reused; CL005 was re-extracted from the primary abstract. The original archive remains intact.

Gaps motivating external searches: infant CMPA randomized formula outcomes, randomized B. infantis-containing combination evidence, and primary sources for review-level HMO disease claims. Primary journal/PubMed sources were checked for all eight summaries. Vandenplas and Seppo claims were checked in full text; other records conservatively retain Abstract checked status. Dose and timing are explicitly unverified when not available in checked passages. This is not expert adjudication or a complete risk-of-bias assessment.

## Shortlist and interpretation

| Record | Study | Appropriate interpretation |
|---|---|---|
| CL001 | Vandenplas 2022 | EHF + 2′-FL/LNnT supported growth in physician-diagnosed CMPA; does not prove HMO-induced tolerance or cure. |
| CL002 | Seppo 2017 | Milk LNFP III associated with challenge-confirmed CMA; not a 2′-FL intervention. |
| CL003 | Tobias 2022 | EVC001 associated with lower NEC in historical cohorts; confounding remains. |
| CL004 | Jacobs 2013 / ProPrems | Randomized three-species combination reduced NEC; cannot isolate B. infantis. Primary sepsis endpoint was null. |
| CL005 | Henrick 2021 | EVC001-associated infant cytokine changes; biomarkers, not clinical allergy/NEC outcomes. |
| CL006 | Autran 2018 | Milk DSLNT associated with NEC in a cohort with eight cases; no supplementation efficacy claim. |
| CL007 | Good 2016 | 2′-FL reduced experimental NEC in mice; eNOS/perfusion mechanism, not demonstrated B. infantis mediation. |
| CL008 | Cilieborg 2016 | No significant NEC benefit of 2′-FL in preterm pigs over five days; retained as counterevidence. |

Each source URL, comparator, population, endpoint, dose uncertainty, review depth and limitation is in `explorer/data/mvp.json` and the record inspector. Trial papers and mechanistic analyses are not interchangeable evidence units. The FDA preterm-probiotic safety communication is linked in the interface; this is a research tool, not a product recommendation.

## Questions for Alex / next curation session

1. Model disease occurrence, clinical severity, symptom scores and immune biomarkers as distinct measured endpoints. Which reused disease terms and outcome patterns fit MOMMIS best?
2. Keep EVC001, Bi-26, ATCC 15697 and the ProPrems combination distinct. Do not infer a continuous 2′-FL → any B. infantis → disease-prevention chain.
3. Adjudicate CL003 and CL005 first: verify full Methods, sample sizes, dose, timing, analysis populations, funding and conflicts; then curate one immune biomarker at a time.
4. Resolve original Henrick filename/content mismatch before accepting its corpus edges. Trace C5109 to the primary mouse allergy experiment; do not present that old excerpt as infant evidence.
5. Check interventions for adverse events and broader trial evidence before making clinical recommendations. Expand the clinical shortlist only after these eight are reviewed.

The evidence is reified in RDF: records report study-specific endpoints. The OWL mapping remains provisional and no universal prevention assertions are generated. Query 2 now includes clinical outcomes and study design/type. Original E001 dose correction is carried forward from the local v3 follow-up; PR #4 itself is unchanged.
