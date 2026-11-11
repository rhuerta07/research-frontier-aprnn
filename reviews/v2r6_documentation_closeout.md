# v2r6 documentation closeout — 11 November 2026

Current manuscript: [v2r6](../paper/integrated_manuscript_v2r6.md). Historical [v2r5](../paper/integrated_manuscript_v2r5.md) and v1 remain unchanged. This closes the Investigation Lead's QUALIFIED GO documentation requirements; sponsor merge approval remains pending. PR #2 stays unmerged.

The abstract, scalar discussion, T4–T5, discussion and bibliographic statement now distinguish public saved-record checks, internal private-NPZ calibration verification, and unrecovered historical retrospective companions. Reported retrospective numbers are retained with attribution. They are not represented as independently reproduced in this release. Archive descriptions link to the [manifest](../results/v2/manifest.json), accurately identifying the withheld NPZ and missing reviewer source/vectors, verification companions and other historical files. README and citation metadata designate v2r6 as current; an appended revision entry preserves the earlier log verbatim.

Validation of this documentation-only revision:

- Compared every pre-existing scientific numeric token in the manuscript body, all Markdown table rows, displayed equation, reference entries and historical revision log with v2r5: unchanged. The version/date and appended note are new metadata. Core conclusions are retained; availability and verification assertions are qualified.
- `python -S analysis/reproduce_tables.py` and `python -S analysis/reproduce_v2.py`: public saved-evidence reproduction passes.
- `python -m unittest discover -s tests -v`: all 25 existing tests pass.
- Changed manuscript links resolve; refreshed manifest hashes match supplied files. Git diff is limited to documentation, citation metadata and the release manifest. Analysis, tests and frozen evidence are unchanged.
- No NPZ, reviewer-owned material, model or dataset was added. No private-logit replay, inference, solver, optimization, calibration fit, experiment or infrastructure execution was needed for closeout.

Remaining limitations are unchanged: original reviewer vectors/source, retrospective verification and bibliography-check companions are unrecovered; original logits remain private pending rights clearance. These limit particular retrospective claims and full public numerical replay, as stated in the current manuscript. They do not require another research cycle before sponsor review of this bounded archive.
