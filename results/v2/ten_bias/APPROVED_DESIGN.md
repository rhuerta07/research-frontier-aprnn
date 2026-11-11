# Proposed ten-bias logit calibration diagnostic — RP001 publication reassessment
Date: 10 November 2026
Status: DESIGN FOR SPONSOR APPROVAL. No calibration fit has been run. This authorizes nothing by itself.

## Question and scientific boundary

Can a single simple, regularized class-offset rule, fitted separately to each frozen 100-example P001/P002 cohort, reach the held-out fog accuracy of its recorded J0/J1 repairs? What clean and class-specific costs accompany that performance?

This is a diagnostic of attainable behavior with fixed representations. It is not a same-constraint APRNN repair, an exhaustive search over bias rules, or causal attribution of the repairs' mechanism. The design is outcome-informed, although the fitting rule will be frozen before either new fit.

## Inputs; no new inference

- Existing ORIGINAL_LOGITS.npz from experiments/publication_assessment/class8_scalar_diagnostic_2026_11_10/.
- Expected file size 2,084,250 bytes and SHA-256 ef356769710266f255539755b3a035975ac37814d49a4e46ad5fe46c30659e6b (copied from saved provenance; verify bytes before fitting).
- Frozen cohort and feature files under experiments/aprnn_r002_r004/prospective_pilot_2026_11_08/. Cohort SHA-256 3192c9f24785b16dea74bbc86d05e40c08926a007af2ec8d2bfb770a8a4a3fb6. Use original example IDs, not row-position assumptions.
- Existing J0/J1 saved predictions and the frozen scalar rule/results.
- Primary clean and fog: indices 1100–9999, N=8,900. Secondary full clean: 0–9999, N=10,000. Selected fog inputs: the frozen 100 IDs for the cohort, drawn from 100–1099.
- Check NPZ keys, shapes, labels, finite float64 logits, IDs and baseline argmax agreement. Load with allow_pickle=False. Verify each selected ID occurs exactly once, labels agree, and primary populations do not intersect selection.
- Reconstruct the already reported four scalar counterfactuals from the stored offsets as a consistency check. A mismatch stops this work; do not replace the logits, reselect offsets or regenerate inference.

## One fitting rule, used twice

For selected cohort C of n=100 examples with stored logits z_i and labels y_i, fit b in R^10 with sum_k b_k=0 by minimizing

L_C(b) = (1/n) sum_i [log(sum_k exp(z_ik+b_k)) - z_i,y_i - b_y_i] + (lambda/2) sum_k b_k^2,

where lambda = 1/n = 0.01.

There are nine identifiable offset degrees of freedom. All original weights and logits are fixed. No box constraint, class reweighting, temperature, feature term, clean anchor or additional calibration data is used. At evaluation, predict argmax_k(z_k+b_k), with lowest-index tie breaking.

Rationale for the fixed penalty: summed cross-entropy plus one-half squared offset norm gives a zero-centered, unit-scale Gaussian penalty in the original logit units. It discourages fitting extreme offsets to 100 examples. The scale is a design choice, not validated knowledge or an invariant property of logits. Do not select or revise it using these outcomes. No hyperparameter sweep, early-stopping selection, cross-validation or alternate baseline is authorized.

Fit P001 and P002 separately. Neither fit may access primary/full-clean labels, held-out fog labels, repaired logits/predictions, or the other cohort's fitted result. Input validation can check labels/IDs; the fit function receives only its own selected logits/labels. Save b, rule hash and convergence evidence for both fits before evaluating held-out outcomes.

## Exact numerical procedure

Use NumPy float64 and stable log-sum-exp, on CPU. Start b=0; deterministic full-batch projected gradient descent.

p_ik = softmax_k(z_i+b)
g_k = mean_i[p_ik - 1(y_i=k)] + lambda*b_k
g_projected = g - mean(g)
b_next = b - eta*g_projected; then subtract mean(b_next)

Fixed eta = 1/(0.5+lambda) = 100/51. The softmax covariance Hessian has spectral norm at most 0.5; the ridge makes the problem strictly convex. The objective has a unique minimizer on the zero-sum subspace in exact arithmetic. This controls fitting ambiguity, not generalization.

At each iterate check the projected gradient. Stop successfully when its infinity norm is at most 1e-8 and abs(mean(b)) at most 1e-12. Maximum 10,000 updates per fit; at most 60 seconds per fit. Fail on nonfinite values or an objective increase exceeding 1e-10 relative to the previous iterate. Retain termination reason, final objective, initial/final selected cross-entropy, penalty, projected-gradient norm and offsets. Do not evaluate a nonconverged fit as a scientific result; no automatic algorithm/penalty replacement.

These are small numerical calibration fits, not APRNN optimization or licensed solver use.

## Outcomes fixed before fitting

Report counts as well as percentages, separately for each cohort:
1. Selected correctness and cross-entropy, explicitly training performance.
2. Primary fog and clean accuracy; corrections and breaks relative to the original.
3. Every true class's N, correct count, corrections and breaks; true-8/non-8 totals and predicted-class histogram.
4. The previously identified class groups {0,1,6,7} and {2,3,4,5,9}, described as outcome-informed groups, not independent discovery or new confirmatory endpoints.
5. Prediction disagreement with the original, both frozen scalar results and both same-cohort repairs, including changes among originally non-8 predictions and non-8/non-8 transitions.
6. Exact calibrated-minus-comparator counts/percentage-point differences, and correct-prediction overlap. Secondary full-clean outcomes remain separate.

No ±1-point pass/fail screen, pooled cohort significance claim, best-feature selection or causal fraction explained. The scalar records remain fixed.

## Interpretation specified in advance

- If both calibrated fog accuracies reach or exceed their respective lower same-cohort repair counts (P001: 5,087; P002: 4,736 of 8,900), conclude this regularized bias rule can attain at least the weaker recorded repair's aggregate fog accuracy on both cohorts. Class/clean costs and prediction overlap remain necessary to interpret similarity. This does not show that APRNN operates by bias correction.
- If both remain below those values, conclude this particular regularized rule falls short of the recorded repair range. Report exact gaps; do not say all bias-only adjustments fail or claim representation improvement.
- If one reaches that level and one does not, report cohort-dependent results.
- If fitting fails, provenance fails, or results depend on implementation choices beyond the fixed rule, report unresolved/inconclusive; do not tune until it looks decisive.
- Intermediate gains above the scalar are informative even when repairs are not reached. Clean versus class ranking remains utility-dependent; no universal winner is declared.

The comparison thresholds summarize observed repair levels, not statistical equivalence, independent replication or prospectively unbiased performance estimates.

## Lean execution and stopping rules

After separate sponsor approval: one small NumPy script using existing input/output conventions; two numerical fits; zero model inference, checkpoints, Gurobi initialization, APRNN repairs, new cohorts or network replication. Include only a few targeted numerical checks (stable probabilities/gradient, zero-sum invariance and rejection of input mismatches). Do not create a framework.

Prefer local CPU after transferring the roughly 2 MB NPZ and small text assets. No GPU, license or new Deepnote machine is needed. Expected fitting time is seconds; this is a planning estimate, not measured evidence. Hard limits: 60 seconds per fit, five minutes for the complete supervised analysis, one CPU process, no retries that change the scientific rule. Stop and preserve evidence on provenance/convergence failure. Any necessary machine startup would be a separate operational decision.

Save one new diagnostic folder containing protocol/source/input hashes, the two fixed offset vectors, convergence records, predictions, CSV tables and a short interpretation. Preserve existing scalar, repair, failed-run and manuscript-v1 records. Return the outcome for sponsor review; no automatic five-cohort expansion or manuscript/public release.

## Immediate sharing gap

The prior reviewer packet omitted ORIGINAL_LOGITS.npz, so the scalar result has not yet been independently reconstructed from that file. Supply the exact historical NPZ first; do not regenerate it. The recorded hash above identifies the expected bytes.

## Approval requested

Approve exactly two fixed-rule ten-bias calibration fits and the stated saved-logit evaluations, with no licensed solver use or new model inference. Until approved, this remains a proposal.
