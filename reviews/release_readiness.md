# Sponsor review handoff

Status: prepared for sponsor inspection; not merged, tagged or externally distributed.

## Validation

- Standard-library-only analysis passed on Python 3.12.14.
- All 16 targeted unittest cases passed, including malformed/duplicate/nonfinite JSON, missing evidence/attempts, identity/label/index/denominator changes, transition accounting, evidence tampering and preservation of P005 missingness.
- Central integrated-manuscript count, correction/break and rounded displacement rows matched calculated results.
- Four prediction files were exported without inference/optimization using read-only Deepnote project storage. Raw byte hashes were checked on transfer; canonical JSON hashes match the final replay summaries.
- All four selected-point files recompute to 100/100 correct. Saved common setups match within each cohort.
- Pilot ratios recompute to fog 0.5750869342 and clean 1.4611892535; joint NO-GO.
- Security inspection covered proposed files and the two-commit publication history (placeholder initialization plus preparation). No credential patterns, private artifact URLs, environment captures, notebook outputs containing secrets, authorization tokens or upstream implementation files were found. This is a bounded automated-pattern and manual-content check, not a guarantee against all sensitive data.

## Scope and remaining limitations

RP001 held-out counts and transitions are reconstructed from saved predictions; selected margins from saved logits. Displacements remain recorded post-repair observations. Pilot outcomes remain saved-summary inputs, with independently recalculated frozen LOOCV arithmetic. Historical reproduction and proxy claims remain documented-only within this release.

No checkpoints/data images/full solver matrices or modified upstream source are redistributed. A verified public binary archive is absent, so external checkpoint replay is incomplete. Upstream CC BY-NC-ND 4.0 rights must be revisited before any such additions. Original analysis/tests use sponsor-approved MIT; original manuscript/documentation use sponsor-approved CC BY 4.0. Roberto Huerta is author; ChatGPT research team is disclosed as AI assistance without invented affiliations.

No new repairs, optimization, training, sampling or scientific-review cycle occurred. P005, the failed preoptimization construction and the authorized retry are retained. Historical runtime/billing/stop reconciliation limitations remain. The separate historical QUALIFIED PASS is not scholarly peer review.

Run from a fresh checkout:

```sh
python analysis/reproduce_tables.py
python -m unittest discover -s tests -v
```

The pull-request handoff supplies the exact commit SHA. Final sponsor approval is required before merge, tagging or distribution to external reviewers.
