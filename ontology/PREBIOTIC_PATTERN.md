# Agreed prebiotic disposition pattern

Emily confirmed on 2026-10-14 that she and Alex prefer **disposition**, not role. The supplied screenshot says **prebiotic**, referring to the 2′-FL material; no probiotic role/disposition was introduced.

Implemented in the canonical `mommis-aligned.owl`:

- PrebioticDisposition is a BFO:0000016 disposition, inhering in some material entity.
- PrebioticMaterial is equivalent to material entity AND has disposition some PrebioticDisposition.
- CHEBI:147155 (2′-FL) has disposition some PrebioticDisposition, per the supplied model. This is an explicitly requested extension axiom, not a claim that ChEBI itself asserts it.
- BacterialCellPopulationProliferation is a proposed child of GO:0008283.
- RegulationOfBacterialCellPopulationProliferation is a child of GO:0042127 and regulates some bacterial cell population proliferation.
- PositiveRegulationOfBacterialCellPopulationProliferation has parents GO:0008284 and the local regulation class, and positively regulates some bacterial cell population proliferation.
- PositiveRegulationByPrebioticMaterial is the local positive-regulation process AND realizes some PrebioticDisposition.
- PositiveRegulationBy2FL is the local positive-regulation process AND realizes some (PrebioticDisposition AND inheres in some CHEBI:147155).

## One explicit translation correction

The slide draws regulation below proliferation. In GO, regulation is connected to its target with **regulates**, not an is-a assertion that regulation itself is proliferation. The implementation preserves both concepts and uses a restriction for the target rather than adding a false subclass axiom to GO. Likewise, local bacterial regulation regulates bacterial proliferation; it is not made a subclass of the proliferation being regulated.

Sources checked: https://amigo.geneontology.org/amigo/term/GO:0042127 and https://amigo.geneontology.org/amigo/term/GO:0008284 . New local classes remain proposed extensions; existing upstream coverage has not been exhaustively assessed.

No axiom says that a disposition must be realized in every context, that every exposure increases proliferation, or that a clinical benefit follows. Full imported-ontology consistency and detailed evidence-to-process mapping remain to be reviewed.

The earlier `mommis-milk-core.owl` is a historical four-class snapshot. Edit **mommis-aligned.owl** going forward. Do not rerun `scripts/align-ontology.py` on the working ontology: that one-time migration reproduces the earlier legacy alignment and will overwrite later edits.
