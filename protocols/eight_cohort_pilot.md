# Predicting benefit and damage from neural-network repair: an eight-cohort APRNN feasibility study

Research Frontier · 9 November 2026 · Research manuscript for review

## TL;DR

We asked whether a cheap measurement of repair examples could forecast what happens after a neural network is repaired. We froze eight random 100-image cohorts and their original-model median true-class logit margins before running APRNN. Seven repairs passed all selected examples; one attempt ended unresolved after a telemetry failure. On those seven evaluable cases, the prespecified margin model reduced fog-outcome prediction error by 42.5% relative to a training-mean baseline, but increased clean-outcome prediction error by 46.1%. The combined exploratory criterion failed. The fog signal was sensitive to one cohort. This is a mixed feasibility result, not a validated predictor or improved selection policy.

## What we did

APRNN changes network parameters while preserving architecture [1]. Earlier project repairs motivated a prospective question: can a cohort's pre-repair classification difficulty predict both benefit on corrupted images and deterioration on clean images? Historical R001–R004 results generated the hypothesis and were excluded from the prospective prediction analysis.

We used one fixed 3×100 MNIST network, MNIST-C fog, and the existing APRNN objective and editable parameter set. Eight distinct seeds, 2026111001–2026111008, produced independent sorted samples of 100 unique indices from 100–1099 using NumPy 2.3.5 PCG64. Across-cohort overlap was allowed. All eight cohorts and 800 pre-repair records were frozen before optimization. The sole predictor was the median, over selected examples, of the original network's true-class logit minus its largest competing logit. No predictor, direction, penalty or threshold was tuned using prospective outcomes.

The two primary responses were repaired-minus-original top-1 accuracy on fog and clean indices 1100–9999, each with 8,900 examples. Full 10,000-image clean accuracy was secondary. These are previously examined benchmark data, not a fresh blinded test set. Clean counterparts of the repair-selection pool are excluded from the primary clean response.

Execution used two stages of four slots, one attempt per slot, a 900-second solver limit, two solver threads, a 1,740-second monitored envelope and sampled 12 GiB process-group RSS guard. A cooperative six-hour study clock was retained across launches. These controls are not hard billing or memory guarantees. The first four slots met the recorded continuation criterion. Sponsor-authorized continuation followed, with the operational limitations described below.

## Results

Original primary correct counts were 1,771/8,900 for fog and 8,595/8,900 for clean. Changes below are percentage points (pp); internal analysis used fractions. Missing outcomes are not imputed.

| Slot | Median margin | Fog correct /8,900 | Fog change (pp) | Clean correct /8,900 | Clean change (pp) | Outcome |
|---|---:|---:|---:|---:|---:|---|
| P001 | -2.627437 | 5087 | +37.258 | 8448 | -1.652 | 100/100; reconciled |
| P002 | -2.618955 | 4736 | +33.315 | 8327 | -3.011 | 100/100; reconciled |
| P003 | -2.411724 | 4846 | +34.551 | 8487 | -1.213 | 100/100; reconciled |
| P004 | -1.634195 | 4201 | +27.303 | 8431 | -1.843 | 100/100; reconciled |
| P005 | -2.196436 | — | — | — | — | Unresolved telemetry failure; no retry |
| P006 | -2.029900 | 4424 | +29.809 | 8498 | -1.090 | 100/100; reconciled |
| P007 | -2.222135 | 4387 | +29.393 | 8470 | -1.404 | 100/100; reconciled |
| P008 | -2.286904 | 4953 | +35.753 | 8475 | -1.348 | 100/100; reconciled |

All seven evaluable repairs improved fog accuracy and reduced clean accuracy. Numerical pointwise success therefore coexisted with different held-out benefits and damage. This observation does not identify a causal mechanism.

For each leave-one-cohort-out fold, we standardized margins using only the six training cases' mean and population standard deviation. We fitted an unpenalized intercept and ridge-penalized slope, minimizing squared error plus slope squared (penalty 1). The comparator predicted the same training fold's outcome mean. No hyperparameters were selected. Analysis was conditional on the seven evaluable cases; all eight slots remained in the execution ledger.

| Primary target | Baseline MAE (pp) | Margin-model MAE (pp) | Error ratio | Frozen threshold | Result |
|---|---:|---:|---:|---:|---|
| Fog change | 3.648 | 2.098 | 0.575 | ≤0.80 | Pass |
| Clean change | 0.517 | 0.755 | 1.461 | ≤0.90 | Fail |

The overall numerical screen required both targets to pass, so it failed. These heuristic thresholds are exploratory decision rules, not significance tests. There is no GO for a margin-based selection-policy trial. P005's operational failure also prevents describing execution as free of material operational violations; seven evaluable cases alone do not satisfy all protocol conditions.

Fold-level predictions, in pp:

| Held-out slot | Fog observed | Fog model | Fog baseline | Clean observed | Clean model | Clean baseline |
|---|---:|---:|---:|---:|---:|---:|
| P001 | 37.258 | 34.469 | 31.687 | -1.652 | -1.926 | -1.652 |
| P002 | 33.315 | 36.062 | 32.345 | -3.011 | -1.343 | -1.425 |
| P003 | 34.551 | 33.426 | 32.139 | -1.213 | -1.833 | -1.725 |
| P004 | 27.303 | 27.316 | 33.346 | -1.843 | -0.311 | -1.620 |
| P006 | 29.809 | 30.958 | 32.929 | -1.090 | -1.648 | -1.745 |
| P007 | 29.393 | 32.659 | 32.998 | -1.404 | -1.670 | -1.693 |
| P008 | 35.753 | 32.157 | 31.938 | -1.348 | -1.717 | -1.702 |

Exact values, training memberships and absolute errors are preserved in the analysis JSON. Seven correlated cross-validation folds do not constitute seven independent validation studies.

## Exploratory influence diagnostic

As an explicitly post hoc sensitivity check, we excluded P004 and repeated the same fixed leave-one-cohort-out calculation on the remaining six evaluable cases, re-estimating each training fold's scaling and coefficients. Fog MAE became 2.647 pp versus 3.009 pp for the baseline, a ratio of 0.880. This exceeds the original 0.80 threshold. The six-case diagnostic is below the protocol's minimum of seven evaluable cases and cannot replace or pass the prespecified screen.

P001 and P002 had nearly equal median margins (-2.627437 and -2.618955), yet fog changes differed by 3.944 pp and primary clean changes by 1.360 pp. Median margin was therefore an incomplete descriptor of repair outcomes even within this setting. P004's influence and this near-matched pair motivate caution rather than retrospective feature selection.

## What the evidence establishes

The repair pipeline used a verifier subprocess and recorded selected-point predictions, parameter constraints, held-out predictions and R2 receipts. Post-run reconciliation checked saved checkpoint, solver, summary, selected-point, held-out and index-record hashes against the final records; matched cohort identities and labels; checked solver-reported settings and status; and recalculated aggregate predictions. The primary clean response was recovered by slicing saved clean predictions and hash-checked historical original-model predictions to indices 1100–9999.

These checks establish internal saved-file consistency within the tested scope. They are not a new independent replay of the seven checkpoints, external authentication of an independent evidence issuer, independent solver-optimality certification, or a new read-only R2 recovery. A receipt's existence does not establish all those properties. APRNN's theoretical guarantees concern specified properties [1]; our reported empirical point checks do not independently certify continuous input regions or clean-behavior preservation.

The sponsor supplied an independent design-review verdict of QUALIFIED PASS for numerical analysis and NO-GO for the joint criterion. Its standalone post-pilot review document was not located in the inspected Deepnote inventory during manuscript preparation. That supplied verdict is distinguished from the directly inspected analysis run and saved evidence. The exploratory P004 calculation was separately reproduced during manuscript preparation.

## Failure and execution limitations

P005's worker monitor reported TELEMETRY_UNAVAILABLE during initialization. Only the initialization phase was saved; no solver result or checkpoint was available. The monitor terminated the worker, the unresolved evidence was archived, and later slots stopped. P005 was not retried or replaced.

A source audit confirmed the monitor code. Synthetic tests demonstrated that it could fail while parsing malformed process information from an unrelated process. A versioned correction checks process-group membership before parsing RSS and retains failure on malformed target-process telemetry. P006–P008 ran under a new captured environment with that correction and additional telemetry-error diagnostics. This addresses a demonstrated defect but does not retrospectively establish the exact cause of P005's failure: the original record omitted the underlying exception.

The initial stage-two submission also failed a source-hash check before any prospective attempt. The local file used to calculate its pin contained one extra newline. The pin was corrected without changing the frozen cohorts or scientific analysis. Both failed engineering launches and P005's consumed attempt remain in the record.

The study proceeded under sponsor-authorized waivers of remaining readiness gates. Externally authenticated evidence, independent machine-stop enforcement and actual account charges remain unreconciled. Completed notebook runs do not prove detached-machine shutdown. The sponsor's reported 700 CPU hours are not billing evidence. This manuscript closes the numerical study; operational closure remains incomplete.

## Why this matters, and prior work

Repair success on the examples used to construct an intervention does not settle its effects elsewhere. In this pilot, forecasting corruption benefit and forecasting clean preservation gave different results. That distinction matters to evaluating targeted model changes, but the present small-network evidence does not support extrapolation to frontier models.

Tao, Nawas, Mitchell and Thakur's APRNN supplies the architecture-preserving repair method and its specification-level guarantee [1]. This study does not introduce a repair algorithm or extend its proof.

Zhang and colleagues prioritize and select repair examples with a score based on output differences normalized by final-layer weight differences, evaluating constraint-based repairs including PRDNN and RIPPLE [2]. Model-informed example selection is therefore established prior work. Our signed cohort-median logit margin, across-cohort response and APRNN forecast differ from their ranking-and-selection task; these differences alone do not establish methodological novelty.

Ishimoto and colleagues predict per-input repairs and breaks using original-model information [3]. This is close precedent for pre-repair outcome prediction. Our response is a cohort-level accuracy change after one repair attempt, rather than per-input repair/break labels. The tasks and reported performance are not directly interchangeable.

AutoRIC uses constrained optimization for quantitatively measured properties and selects restrictive classification constraints [4]. It motivates attention to the constraints imposed by a repair set. Our pilot neither tests AutoRIC nor demonstrates that constraint interaction explains our outcomes.

The contribution is a small, transparent prospective feasibility test of one frozen forecast, including its negative clean result, influential case and operational missingness. We make no priority claim for predicting repair outcomes, using margins, selecting examples, or studying benefit–damage tradeoffs. Our literature comparison draws on the supplied full-text assessment; AutoRIC's author-hosted manuscript has provisional bibliographic fields, so its published DOI identifies the work without treating that manuscript as the definitive version.

## What's next and open question

The next independent scientific question is: **does a prespecified measure of repair-constraint interaction or editable-parameter sensitivity add predictive information about clean deterioration beyond original-model margin?**

This is a research-pressure hypothesis, not a result of the pilot. Any future test should define its feature, baseline, outcome and compute budget prospectively and separate feature development from evaluation on newly drawn cohorts. The current seven outcomes should not become a tuning set followed by claims of independent validation. No new experiment is commissioned here.

With one network, one corruption, overlapping repair cohorts, previously examined evaluation data, one missing outcome and a monitor change, the defensible conclusion is limited: median margin showed a fragile fog-prediction signal and failed the joint forecast of benefit and damage. The negative result and execution limitations should accompany any public account.

## References

1. Tao, Z., Nawas, S., Mitchell, J., and Thakur, A. V. (2023). *Architecture-Preserving Provable Repair of Deep Neural Networks.* PACMPL 7 (PLDI), article 124. [DOI](https://doi.org/10.1145/3591238); [author full text](https://thakur.cs.ucdavis.edu/assets/pubs/PLDI2023.pdf).
2. Zhang, L., Sun, S., Yan, J., Zhang, J., Wu, J., and Liu, J. (2025). *Accelerating constraint-based neural network repairs by example prioritization and selection.* Frontiers of Computer Science 19(4), 194332. [DOI](https://doi.org/10.1007/s11704-024-3902-x).
3. Ishimoto, Y., Kondo, M., Ma, L., Ubayashi, N., and Kamei, Y. (2025). *Repairs and Breaks Prediction for Deep Neural Networks.* ACM TOSEM 34(4), article 94. [DOI](https://doi.org/10.1145/3702983).
4. Sun, X., Liu, W., Wang, S., Chen, T., Tao, Y., and Mao, X. (2025). *AutoRIC: Automated Neural Network Repairing Based on Constrained Optimization.* ACM TOSEM 34(2). [DOI](https://doi.org/10.1145/3690634); [author manuscript](https://shangwenwang.github.io/files/TOSEM-24B.pdf).

