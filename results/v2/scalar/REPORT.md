# Class-8 scalar calibration diagnostic — 10 November 2026

**Assessment: negative for sufficiency of this prespecified scalar baseline.** It reproduces a useful portion of the recorded fog gain, but every selected-calibrated offset misses every J0/J1 repair on fog accuracy by more than one percentage point. All same-cohort comparisons fail the exploratory comparability heuristic. Aggregate clean accuracy is often higher for the scalar, while true-8 behavior can be worse: comparative clean/class desirability is therefore inconclusive, and these results do not establish overall APRNN superiority.

**Smallest justified next action:** give these verified tables to the research lead for pending D1–D4 sections. Keep further optimization and expansion deferred. A richer bias baseline would be a separate scientific decision, not an automatic follow-up.

## D1 — provenance and frozen choice

Both internal NPZ archives contain predictions/tie records, not complete logits. One original-model forward pass per domain covered 10,000 fog plus 10,000 clean examples; selected points are included in fog. The frozen model/data/cohort hashes passed. Original predictions and labels matched all four public-reference repair baselines and both internal NPZ archives; selected IDs/labels/winners matched the frozen feature record. No repaired checkpoint was opened. Public blobs were checked against commit `37d81655fca7857032360e8df831c284c51dfe93`; the only accepted byte normalization was an explicitly recorded extra final newline in the public file.

Preprocessing and model decoding reuse the inspected replay: uint8/255, reshape784, ERAN float32 assignment then float64, lowest-index argmax, two CPU threads. Runtime was the existing environment: {'numpy': '2.4.6', 'python': '3.13.18 (main, Oct 28 2026, 14:29:13) [GCC 12.2.0]', 'torch': '2.12.0+cu130'}. Full float64 logits, indices, labels and original winners are in `ORIGINAL_LOGITS.npz`.

`PRESPECIFIED_RULE.json` was saved before execution. `CALIBRATION_RULE.json` was saved before counterfactual outcomes; `CALIBRATION_SELECTION.json` and `D1_SELECTION.csv` were saved before held-out counterfactual evaluation. Candidates use only each cohort’s selected thresholds plus endpoints and interval midpoints; the unrestricted set adds one specified representative beyond its largest nonnegative threshold. Fewest selected errors wins, then the smallest candidate τ. Decimal and hexadecimal offsets, all candidate errors and tied-optimum candidate counts are retained. Subtraction and ties use float64 semantics, not an exact-real minimal-offset proof. No oracle or held-out offset sweep was run.

| Cohort | Diagnostic | τ | Selected correct /100 | Candidate count |
|---|---|---:|---:|---:|
| P001 | bounded | 2.94956672913698 | 40 | 149 |
| P001 | unrestricted | 3.56528881834417 | 43 | 178 |
| P002 | bounded | 2.92748996594984 | 38 | 139 |
| P002 | unrestricted | 3.58577934144704 | 41 | 182 |

Selected accuracy is calibration performance, not satisfaction of the selected repair constraints. The established scalar/bounded-bias infeasibility results were not retested by optimization.

## D2 — complete tradeoff

Original primary fog: 1,771/8,900 correct, predicted8=7,692, true8 errors=1. Original primary clean: 8,595/8,900 correct, predicted8=839, true8 errors=56.

| Cohort | Diagnostic | Population | Correct /8900 (%) | Corrections | Breaks | True8 correct /876 | Non8 correct /8024 | Predicted8 | True8 errors |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| P001 | bounded | fog_primary | 3623 (40.7079) | 2151 | 299 | 576 | 3047 | 1413 | 300 |
| P001 | bounded | clean_primary | 8501 (95.5169) | 10 | 104 | 716 | 7785 | 720 | 160 |
| P001 | unrestricted | fog_primary | 3529 (39.6517) | 2322 | 564 | 311 | 3218 | 564 | 565 |
| P001 | unrestricted | clean_primary | 8458 (95.0337) | 10 | 147 | 673 | 7785 | 676 | 203 |
| P002 | bounded | fog_primary | 3625 (40.7303) | 2145 | 291 | 584 | 3041 | 1452 | 292 |
| P002 | bounded | clean_primary | 8502 (95.5281) | 10 | 103 | 717 | 7785 | 721 | 159 |
| P002 | unrestricted | fog_primary | 3522 (39.5730) | 2328 | 577 | 298 | 3224 | 531 | 578 |
| P002 | unrestricted | clean_primary | 8457 (95.0225) | 10 | 148 | 672 | 7785 | 675 | 204 |

All ten true-class accuracies, corrections/breaks and true8/non8 totals for the scalar, original and each repair are in `D2_ALL_CLASS_COUNTS.csv` (accuracy fractions plus exact numerators/denominators). `RESULTS.json` additionally retains predicted8 false positives, true8 false negatives, original-non8 changes and prediction agreement/disagreement with **all four** existing repairs, for both primary domains and full clean. Scalar changes among original non8 predictions are exactly zero for every population; corresponding repair changes and differences are retained. Selected-point agreement with each same-cohort repair is also retained.

Full-clean secondary correct counts /10,000: P001/bounded=9544; P001/unrestricted=9497; P002/bounded=9545; P002/unrestricted=9496. Original full-clean count is 9,654. Full-clean class tables and repair comparisons remain in the same numerical files.

## D3 — exact same-cohort comparisons

All differences below are scalar minus repair. Δtrue8 errors is reported separately on each domain. “Comparable” requires |Δaccuracy|≤1 percentage point on each primary domain and no greater true8 error count on either. This is an exploratory retrospective heuristic, not an equivalence test.

| Cohort | Diagnostic | Repair | Δfog correct (pp) | Δclean correct (pp) | Δfog true8 errors | Δclean true8 errors | Fog agreement /8900 | Fog net-gain ratio | Comparable |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| P001 | bounded | J0 | -1464 (-16.4494) | +53 (+0.5955) | +122 | +66 | 4916 | 0.5585 | No |
| P001 | bounded | J1 | -1654 (-18.5843) | +80 (+0.8989) | +61 | +11 | 4607 | 0.5282 | No |
| P001 | unrestricted | J0 | -1558 (-17.5056) | +10 (+0.1124) | +387 | +109 | 4536 | 0.5302 | No |
| P001 | unrestricted | J1 | -1748 (-19.6404) | +37 (+0.4157) | +326 | +54 | 4482 | 0.5014 | No |
| P002 | bounded | J0 | -1111 (-12.4831) | +175 (+1.9663) | +87 | +56 | 5716 | 0.6253 | No |
| P002 | bounded | J1 | -1399 (-15.7191) | +154 (+1.7303) | -121 | +28 | 4820 | 0.5699 | No |
| P002 | unrestricted | J0 | -1214 (-13.6404) | +130 (+1.4607) | +373 | +101 | 5374 | 0.5906 | No |
| P002 | unrestricted | J1 | -1502 (-16.8764) | +109 (+1.2247) | +165 | +73 | 4861 | 0.5383 | No |

The fog net-gain ratio divides scalar-minus-original correct count by repair-minus-original correct count on this fixed population; it is descriptive arithmetic, **not a causal fraction explained**. `D3_COMPARISONS.csv` reports all four repair comparisons separately for each offset/population, with exact aggregate differences and flags. `D3_ALL_CLASS_DIFFERENCES.csv` supplies exact class/group differences. Agreement and class-specific tradeoffs prevent aggregate matching from being mistaken for classifier identity.

## D4 — interpretation and limitations

The primary shifts add 1,852/1,854 correct fog predictions, so scalar calibration has a substantial useful descriptive effect on these records. Nevertheless, their same-cohort fog shortfalls are 1,111–1,654 images (12.48–18.58 percentage points). Unrestricted selected calibration improves selected accuracy but reduces held-out fog accuracy and substantially increases true8 errors. The rule is insufficient to reproduce the repair outcomes under the frozen diagnostic; this does not prove representation improvement, identify APRNN’s mechanism, or rule out richer bias adjustments.

Cleaner aggregate accuracy does not uniformly mean better class behavior. In particular, the bounded scalar loses more true8 clean predictions than each same-cohort repair while avoiding all original-non8 prediction changes. Which clean/class tradeoff is preferable is inconclusive without a separately justified utility criterion. No manuscript text was edited. These retrospective two-cohort, one-network finite-set results do not establish population equivalence or independent repair replication.

## Execution and artifacts

Analysis run `d25375a5-dafd-44f1-98ec-5a3542b01b22`: completed successfully. Supervisor wall time 171.51486715395004 seconds, no timeout, child process group absent; CPU limit 570/600 seconds, wall limit600 seconds. Solver imports were blocked and none occurred; checkpoint/model writes were blocked. No optimization, repaired-model inference, new cohort or public change occurred. `stderr.log` is empty and no analysis failure was recorded. The first metadata-only run inspected NPZ keys.

`scalar_diagnostic.py` is the analysis source; `make_report.py` verifies output hashes and reproduces the frozen class audit from public-pinned records before emitting this report. `BASELINE_PROVENANCE.json`, `OUTPUT_HASHES.json`, `SUPERVISOR.json` and `FINAL_HASHES.json` retain inputs, source/output hashes and execution evidence. Shutdown readback is saved separately in `SHUTDOWN.json` after cleanup.
