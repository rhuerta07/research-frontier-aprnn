# RP001 Option B — independent final scientific review

2026-11-10. **QUALIFIED PASS for a descriptive research note. Stop development; no additional repairs or infrastructure recommended.**

This was a separate skeptical review of saved records and code, not a blinded review or an external replication. No machine, solver, optimization, repair, or new numerical experiment was started.

## Evidence examined
I read the final working report and RESULTS_VERIFIED.json; all four solver.json, terminal.json and independent_repair_points.json files; all four common_setup.json records; actual J0/J1 worker sources; common capture and semantic mapping code; checkpoint replay and paired-population comparison code. I independently counted 100 correct selected points in each of the four saved point-record files and recomputed their minimum saved margins. I checked exact equality of each pair's saved common setup JSON and checked all reported correction/break/net arithmetic in the final summary. The saved J0/J1 worker texts differ only in their intended objective vector assignment. Solver records each report raw status 2, one solution and small recorded violations; worker and replay terminal records report zero exits and absent process groups.

I did not independently reload checkpoints, rehash binary inputs/checkpoints, reconstruct solver matrices from tensors, reproduce solver optimality or re-execute tests. The direct held-out prediction files exceed the connected read-file interface's 64 KiB limit and are single-line JSON. I therefore could not independently recompute held-out counts from their individual prediction arrays through this interface. I checked the saved summary arithmetic and inspected the actual population-slicing/correction/break implementation instead. The final note should not call this a complete independent numerical reproduction.

## Findings
The saved primary counts are internally consistent:

| Cohort | J1 minus J0 fog correct | J1 minus J0 clean correct | Maximum absolute edit J0 → J1 |
|---|---:|---:|---:|
| P001 | +190 / 8,900 (+2.135 pp) | -27 / 8,900 (-0.303 pp) | 2.137234 → 0.095826 |
| P002 | +288 / 8,900 (+3.236 pp) | +21 / 8,900 (+0.236 pp) | 3.000000 → 0.090313 |

Every model loses primary clean accuracy relative to the original: P001 J0 -147, J1 -174; P002 J0 -268, J1 -247 correct examples. J1 creates more fog corrections and more fog breaks in both cohorts. Reporting only the net fog gains would conceal consequential behavioral differences. Clean differences between objectives have opposite signs across cohorts. There is no support for a consistent clean advantage of either objective from these cases.

Both saved common setups match within cohort. The actual checks compare semantic common-matrix hashes, bounds/types, labels/indices, provenance, selected settings and boundary epsilon; they do not constitute a formal equivalence proof. Selected-point minima are approximately 0.001 and pass the declared 1e-6 tolerance. A flag marking proximity to the repair margin is not itself an empirical demonstration of sensitivity to perturbation; describe those points as near the active constraint boundary rather than claiming observed numerical instability.

## Interpretation limits essential to publication
1. J0 contains 1,000 selected-output changes plus 10,110 parameter deltas; J1 contains the 10,110 parameter deltas. This changes both the mixed infinity term and the normalized-L1 denominator (11,110 to 10,110). Attribute the observed contrast to the combined objective specification. Do not isolate output anchoring or normalization independently.
2. These are two selected cohorts on one small network and one corruption. Cohorts share the evaluation set (and some selected examples); image counts are not independent repair replications. No general reliability, causal mechanism, unique optimum, universal parameter norm guarantee or new repair method is established.
3. Smaller observed maximum displacement is not a verified globally minimal infinity displacement by itself: J1 minimizes the declared combined norm surrogate, and solver status is not an independent optimality certificate. Say 'parameter-only objective produced smaller maximum edits'.
4. The result is not a test of prospective repair-pressure prediction or of the normalized pairwise proxy. Retain the original pilot's negative combined primary result.
5. Preserve the full execution history: one earlier preoptimization P001/J0 construction failed, followed by an explicitly approved retry and four completed solves. Do not describe the history as exactly four construction attempts with no failures.
6. Replay checks are pointwise and tolerance based. Shared code/model-format assumptions, solver tie-breaking and multiple optima remain. Report them without reopening engineering work.

## Defensible conclusion
“In these two cohorts, changing how APRNN selected among repairs satisfying the checked constraints materially changed held-out behavior. The parameter-only objective produced much smaller maximum parameter edits but did not preserve baseline clean accuracy.”

This is a useful bounded counterexample to treating small edits as sufficient evidence of clean preservation. The proposed phrase 'does not reliably prevent unintended consequences' is acceptable only as a clearly marked motivation or implication; the experiment does not estimate reliability across repair problems. The narrower wording above should be the paper's empirical conclusion.

Recommendation: finalize and archive the qualified research note with these limitations. No additional experiments, predictor fitting, repairs or infrastructure are needed for this conclusion.

