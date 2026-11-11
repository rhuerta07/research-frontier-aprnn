# Class-resolved behavior under two APRNN repair objectives
## A reproducibility case study in a fog-induced prediction-collapse regime

**Manuscript v2, revision 5 — 10 November 2026.** Author: Roberto Huerta, with AI assistance disclosed in the project README. This working manuscript is for focused external reassessment; it does not constitute journal acceptance or publication-readiness certification. This separately versioned draft preserves v1 and fixed public commit 37d81655fca7857032360e8df831c284c51dfe93 unchanged.

**Status:** language copyedit accepted following scientific review at bounded-preprint scope. The chronology of the original selected-only calibration and the later retrospective scalar sweep is explicit. No new numerical analysis, fitting, search, inference or repair accompanied this revision. Earlier manuscript revisions and the fixed public release remain preserved.

### Abstract

We re-examine a two-cohort APRNN objective comparison on one pretrained network using archived numerical evidence. The original network predicts digit 8 on 86.427% of 8,900 held-out MNIST-C fog images. The recorded repairs reach 53.21–59.29% fog accuracy from 19.90%, while reducing clean accuracy. J0/J1 disagree on 30.978% and 34.393% of fog predictions, including 1,215 and 1,453 disagreements between distinct non-8 classes. The mixed objective's infinity term is necessarily output dominated on these cohorts, qualifying the interpretation of its larger maximum parameter edits. A selected-cohort-calibrated scalar class-8 offset reaches 40.71–40.73% fog accuracy. A separately frozen ten-offset rule, fitted by selected-only mean cross-entropy plus (0.01/2) times squared offset norm, reaches 49.96% and 48.27%, with clean accuracy 92.44% and 92.84%. Both fixed rules fall below the corresponding repairs on fog accuracy; the ten-offset rule also falls below them on clean accuracy. The true-8/non-8 deficit varies across all four comparisons. Each selected cohort contains only four true 8s. Direct evaluation of the reviewer-supplied retrospective bias vector confirms 4,747/8,900 fog correct (53.34%) and 8,185/8,900 clean correct (91.97%). A complete threshold-based scalar sweep reaches 3,626/8,900 fog correct (40.74%). Both checks use held-out labels and are retrospective capability assessments; the ten-bias vector is neither a generalization result nor a certified bias-only ceiling. These observations support a bounded technical case study of class-structured behavior and fog/clean tradeoffs, not a causal decomposition, representation-improvement claim or general repair guarantee.

### 1. Revised question and evidence boundary

The question is how two explicitly specified output calibration rules fitted to the selected cohorts—a downward class-8 scalar and a regularized ten-offset vector—compare with the recorded repairs on fog accuracy, clean accuracy and class-specific changes. Failure of either fitted rule does not exclude other bias vectors or identify the repairs’ mechanism. Neither calibration is required to satisfy the selected-point repair constraints. Prediction collapse is an observation; “class-prior correction” is a possible explanation and does not imply that the data's label priors changed.

The completed J0/J1 experiment remains a valid measurement of different numerical solutions under matched captured common setups. Its interpretation changes: neither parameter-norm minimality versus functional preservation nor the general existence of repair regressions is new. Our earlier integrated note omitted a consequential class-level structure.

Primary clean/fog indices are 1100–9999, N=8,900; full clean 0–9999 is secondary. Cohorts P001/P002 each contain 100 frozen selected fog examples from 100–1099. One pretrained network and reused evaluation examples limit every conclusion here. The reanalysis and diagnostic design follow observed outcomes and are retrospective.

### 2. Prior work and the optimization intervention

APRNN's pointwise specification, drawdown and generalization distinctions provide the immediate setting [1]. PRDNN explicitly uses parameter-norm minimality [2]. REASSURE discusses weight-space change as a poor proxy for functional locality [3], and Majd et al. give a small-weight-change/new-error example [4]. These prior results establish that the maximum-edit comparison is not a new repair principle.

Zhang et al. study example prioritization and selection for constraint-based repair [7], while Ishimoto et al. study prediction of individual repairs and breaks [8]. AutoRIC uses constrained optimization and restrictive-constraint selection [9]. NSRepair explicitly treats correction and preservation as competing objectives [10]. These precedents limit broad novelty claims about selection, forecasting and repair side effects; differences in their tasks do not by themselves establish novelty for this case study.

The pinned APRNN script eval_1_aprnn.py uses the mixed objective, while experiments/mnist/repair.py already contains the parameter-only normalized-L1 plus infinity objective family with unit default weights [5]. We do not claim that our exact execution is identical to that helper's edit/encoding interfaces.

Let p denote the 10,110 editable parameter changes and o the 1,000 selected-logit changes. Define φ_m(v)=||v||∞+||v||₁/m. J0 applies the implemented upper-bound construction to φ_11110([o;p]); J1 applies it to φ_10110(p). Both the objective membership and L1 normalization change. The intervention does not isolate those two effects.

Barrier optimization with Method=2 and Crossover=0 is part of the experiment. Gurobi documents that crossover-off returns the interior solution computed by barrier [6]. We do not establish a unique numerical optimum, a canonical interior point of a particular optimal face, or invariance to algorithmic settings.

### 3. Why the maximum-edit contrast is expected

For selected example i, let original margin m_i=z_y-max_{j≠y}z_j and deficit d_i=(0.001-m_i)_+. Satisfying the specified class gap requires Δz_y-Δz_j≥d_i for the original strongest competitor, hence ||o||∞≥max_i d_i/2.

| Cohort | Worst original margin | Lower bound on output infinity displacement |
|---|---:|---:|
| P001 | -6.841700161 | 3.421350080 |
| P002 | -7.140667204 | 3.570833602 |

Both lower bounds exceed the ±3 editable box. J0's infinity term is therefore dominated by the output throughout the feasible set; parameter changes still contribute through normalized L1. J1 explicitly penalizes the maximum parameter edit. This explains the different incentives, not the exact observed displacement ratios or held-out effects.

The observed maximum parameter edits for J0/J1 are 2.137234/0.095826 for P001 and 3.000000/0.090313 for P002. P002/J0 is within about 2e-8 of its box bound, but no dual/sensitivity analysis establishes the effect of relaxing that bound. Actual L1/L2/support summaries have not been independently reconstructed from checkpoints for this draft. Objective values alone do not establish edit density without verification that the auxiliary bounds are tight.

### 4. Class-resolved observations from the frozen predictions

The original model predicts 8 on 7,692/8,900 cases. True-8 accuracy is 875/876; accuracy on all other classes is 896/8,024 (11.167%).

| Cohort/objective | Fog predicted 8 | Correct true-8 /876 | Correct non-8 /8,024 | True-8 breaks /all breaks |
|---|---:|---:|---:|---:|
| P001/J0 | 2,298 | 698 | 4,389 | 177/222 |
| P001/J1 | 1,518 | 637 | 4,640 | 238/272 |
| P002/J0 | 2,093 | 671 | 4,065 | 204/245 |
| P002/J1 | 1,211 | 463 | 4,561 | 412/448 |

All fog corrections concern true non-8 images; 79.7–92.0% of fog breaks concern true 8s. These directions are consistent with suppression of dominant class-8 predictions, but consistency is not causal identification. Class 1 fog accuracy decreases under J1: 334→175/995 in P001 and 411→244/995 in P002. “Broader recognition improvement” is not a uniform per-class result.

J0 and J1 disagree on 2,757/8,900 (30.978%) and 3,061/8,900 (34.393%) fog predictions. Of these, 1,215 and 1,453 involve two distinct non-8 predictions. A scalar class-8 bias change leaves the ordering among non-8 logits unchanged and cannot produce those transitions. Relative to the original classifier, each repair also changes 234–283 originally non-8 predictions. Exact scalar equivalence is ruled out. Section 6 measures a selected-calibrated scalar diagnostic: it yields substantial gains but falls short of each repair.

### 5. Clean behavior and uncertainty

| Cohort/objective | Correct true-8 /876 | Correct non-8 /8,024 | Total /8,900 |
|---|---:|---:|---:|
| Original | 820 | 7,775 | 8,595 |
| P001/J0 | 782 | 7,666 | 8,448 |
| P001/J1 | 727 | 7,694 | 8,421 |
| P002/J0 | 773 | 7,554 | 8,327 |
| P002/J1 | 745 | 7,603 | 8,348 |

In both cohorts, J1 has fewer correct true-8 predictions and more correct non-8 predictions than J0. The aggregate differences (-27, +21) describe different balances of this tradeoff; “sign reversal” is not a useful headline.

The exact paired McNemar p-values are 0.104655/0.247380. Approximate paired 95% image-sampling intervals are [-0.656,+0.050]/[-0.145,+0.617] percentage points. They do not quantify cohort or solver variability, prove equivalence, or erase observed finite-set differences. Corresponding fog differences remain +2.135/+3.236 pp; image-level p-values are not evidence of general repair reliability.

### 6. Scalar class-8 calibration diagnostic

A final-bias-only repair under the same ±3 per-coordinate box can improve a class gap by at most 6. Required selected improvements exceed 6 in both cohorts. Therefore no such repair can satisfy the same selected-point requirements; no solver run is needed to establish this.

A class-8-only decrease z_8←z_8-τ cannot satisfy all selected requirements even without the box. Necessary lower bounds on τ from original non-8 errors are 6.842700161/7.141667204; necessary upper bounds from selected true-8 points are 2.393007012/3.078081156. Both intervals are empty. This says nothing about usefulness as a partial, descriptive calibration baseline or about ten unconstrained biases.

#### D1. Provenance and fixed calibration rule

The historical prediction archives did not contain complete original logits. Research engineering therefore ran the original model once over each full 10,000-image clean/fog population, including selected points. The saved provenance reports matching model/data/cohort hashes and exact baseline labels and argmax predictions against all four archived repair baselines and both internal prediction archives. Selected IDs, labels and winners also matched the frozen cohort features. No repaired checkpoint was opened for this diagnostic.

The diagnostic used Python 3.13.18, NumPy 2.4.6 and Torch 2.12.0+cu130 on CPU, with two threads, uint8/255 preprocessing, ERAN float32 assignment followed by float64 evaluation, and lowest-index argmax ties. This differs from the historical repair runtime. Matching baseline predictions does not establish bitwise historical logit equivalence or guarantee identical near-threshold counterfactuals under another runtime. The original float64 logits, labels and indices are retained in ORIGINAL_LOGITS.npz.

For each selected cohort, the fixed rule minimizes selected classification errors, then chooses the smallest candidate τ. Only the 100 selected fog examples determine τ. The candidate endpoints, selected thresholds z₈−max_{j≠8}zⱼ and interval midpoints are enumerated; the unrestricted case adds a specified representative beyond the largest threshold. The primary range is 0≤τ≤3; the secondary range is τ≥0. Decimal/hexadecimal offsets and tied candidate counts are saved. These are finite float64 candidate calculations, not a proof of a minimum real-valued offset. The rule and selected choices were recorded before held-out counterfactual evaluation. No held-out oracle sweep was performed during this initial selected-only calibration diagnostic. The exhaustive held-out scalar sweep reported later in this section was a subsequent retrospective check; it did not select or revise the frozen selected-only offsets.

#### D2. Selected and held-out outcomes

| Cohort | Diagnostic | τ | Selected correct /100 | Fog correct /8,900 | Fog accuracy | Clean correct /8,900 | Clean accuracy |
|---|---|---:|---:|---:|---:|---:|---:|
| P001 | Bounded | 2.949567 | 40 | 3,623 | 40.71% | 8,501 | 95.52% |
| P002 | Bounded | 2.927490 | 38 | 3,625 | 40.73% | 8,502 | 95.53% |
| P001 | Unrestricted | 3.565289 | 43 | 3,529 | 39.65% | 8,458 | 95.03% |
| P002 | Unrestricted | 3.585779 | 41 | 3,522 | 39.57% | 8,457 | 95.02% |

Selected-set correctness measures calibration fit; it is not satisfaction of the APRNN gap/gate constraints. Each selected cohort contains only four true-8 examples (4/100), versus 876/8,900 in the primary fog set. This limits how well selected-only calibration represents the held-out cost to that class; it does not justify reweighting after observing outcomes. Original primary fog/clean correct counts are 1,771/8,595. Bounded calibration yields 2,151/2,145 fog corrections and 299/291 fog breaks, for net gains of 1,852/1,854. Its clean corrections/breaks are 10/104 and 10/103.

| Cohort/diagnostic | Fog true-8 correct /876 | Fog non-8 correct /8,024 | Clean true-8 correct /876 | Clean non-8 correct /8,024 |
|---|---:|---:|---:|---:|
| P001 bounded | 576 | 3,047 | 716 | 7,785 |
| P002 bounded | 584 | 3,041 | 717 | 7,785 |
| P001 unrestricted | 311 | 3,218 | 673 | 7,785 |
| P002 unrestricted | 298 | 3,224 | 672 | 7,785 |

All breaks under scalar calibration concern true 8s. No originally non-8 prediction changes, as required by the downward class-8 transformation. Larger unrestricted offsets improve selected correctness by three points but reduce held-out fog accuracy and true-8 accuracy. Complete ten-class tables, corrections/breaks, full-clean secondary outcomes and prediction agreements are retained in the diagnostic folder rather than compressed into a single aggregate score.

#### Class-group concentration and the retrospective global scalar check

The following descriptive grouping was identified after examining the class results.

| Cohort | Fog class group | N | Bounded scalar correct | J0 correct | J1 correct |
|---|---|---:|---:|---:|---:|
| P001 | 0, 1, 6, 7 | 3,668 | 326 | 1,621 | 1,749 |
| P001 | 2, 3, 4, 5, 9 | 4,356 | 2,721 | 2,768 | 2,891 |
| P002 | 0, 1, 6, 7 | 3,668 | 326 | 1,224 | 1,512 |
| P002 | 2, 3, 4, 5, 9 | 4,356 | 2,715 | 2,841 | 3,049 |

Classes 0, 1, 6 and 7 account arithmetically for 80.8–88.5% of the bounded scalar-to-repair aggregate fog gap. This is not a causal attribution. Their correct count under scalar calibration rises from the original 276 to 326; “no improvement” would be inaccurate. Conversely, scalar calibration is close to P001/J0 on the other five classes (2,721 versus 2,768), but the difference is larger for some other comparisons.

Bounded scalar outcomes differ by two correct fog predictions between cohorts (0.0225 pp), versus 351 for J0 (3.9438 pp) and 253 for J1 (2.8427 pp). This similarity is observed in two cohorts; it does not establish cohort invariance.

For downward scalar offsets, correct non-8 predictions are nondecreasing in tau and correct true-8 predictions are nonincreasing. The reviewer's earlier 44.1% bound up to the P001 unrestricted offset is valid by a piecewise argument: up to its bounded offset, total correctness is at most 3,047+875=3,922; from that offset to its unrestricted offset it is at most 3,218+576=3,794. The preceding manuscript incorrectly rejected this bound because it overlooked that decomposition.

The exhaustive scalar check, now reproducible, gives a sharper bound. Predictions change only when tau crosses a nonnegative threshold z_8-max(non-8 logits). Evaluating zero, all distinct nonnegative thresholds, interval midpoints, and a value beyond the largest threshold covers the distinct scalar prediction regimes, including lowest-index argmax ties. We independently evaluated all 15,386 candidates on the stored float64 logits and reproduced the maximum of 3,626/8,900 (40.74%). The first candidate attaining the maximum is tau=2.928132603895912; five candidates attain the maximum. At that candidate, clean correctness is 8,502/8,900. When class 8 is never predicted on primary fog, fog correctness is 3,271/8,900. This establishes the global scalar maximum for this stored-logit, argmax diagnostic under the specified numerical convention, not a formal real-arithmetic certificate or a result about general bias vectors. The check uses held-out labels retrospectively and does not replace the frozen selected-only offsets. It remains 1,110 images (12.47 percentage points) below the weakest repair.

#### D3. Comparison with the recorded repairs

We report exact differences without a pass/fail comparability screen. The earlier exploratory ±1-point screen remains in the frozen diagnostic record but adds no interpretive value here. There are eight comparisons within cohorts: two cohorts × two scalar rules × two repair objectives. They share data and are not eight independent replications.

| Cohort | Scalar rule | Comparator | Scalar minus repair fog correct | Scalar minus repair clean correct | Scalar minus repair clean true-8 errors |
|---|---|---|---:|---:|---:|
| P001 | Bounded | J0 | −1,464 | +53 | +66 |
| P001 | Bounded | J1 | −1,654 | +80 | +11 |
| P001 | Unrestricted | J0 | −1,558 | +10 | +109 |
| P001 | Unrestricted | J1 | −1,748 | +37 | +54 |
| P002 | Bounded | J0 | −1,111 | +175 | +56 |
| P002 | Bounded | J1 | −1,399 | +154 | +28 |
| P002 | Unrestricted | J0 | −1,214 | +130 | +101 |
| P002 | Unrestricted | J1 | −1,502 | +109 | +73 |

Scalar fog shortfalls span 12.48–19.64 percentage points. Every scalar rule also incurs more clean true-8 errors. However, every scalar rule preserves more correct predictions in total on clean data. Fog true-8 comparisons are not uniformly favorable to repairs: P002 bounded calibration has 121 fewer true-8 fog errors than P002/J1. Neither aggregate clean superiority nor overall repair superiority follows without an explicit utility for these class/domain tradeoffs.

#### D4. Interpretation and verification boundary

**Negative for sufficiency of this fixed scalar rule; inconclusive for an overall clean/class tradeoff ranking.** Scalar calibration demonstrates that a substantial fog gain can be obtained without modifying representations, but does not reproduce the recorded repairs' fog accuracy. Comparing net gains does not identify a causal “fraction explained.” This does not prove representation improvement, exclude richer bias adjustments, or characterize the best ten-bias vector. The later retrospective scalar enumeration establishes a separate maximum for this one-dimensional family, not for richer bias corrections. The selected calibration rule, the original bounds and the two-cohort setting define the conclusion.

The lead inspected the saved analysis source, rule, provenance, report and shutdown record, and independently recalculated accounting identities, ten-class totals and scalar-minus-repair arithmetic across 156 class/group rows and 48 comparison rows. This is a saved-table consistency check against previously verified repair counts, not an independent rerun of original-model inference or reconstruction of the binary logits. Research engineering reports a 171.5-second supervised analysis, zero solver initialization/optimization, and confirmed machine shutdown. These operational reports are retained separately from scientific validation.

### 7. Fixed ten-bias calibration and external reconstruction

#### T1. Exact objective and frozen numerical rule

For each cohort separately, with 100 selected original fog logits z_i and labels y_i, we fit additive offsets b in R^10 subject to sum_k b_k=0:

$$J(b)=\frac{1}{100}\sum_{i=1}^{100}\left[\log\sum_{k=0}^{9}\exp(z_{ik}+b_k)-(z_{i y_i}+b_{y_i})\right]+\frac{\lambda}{2}\sum_{k=0}^{9}b_k^2,\qquad \lambda=0.01.$$

The factor 1/2 is part of the rule. Using lambda times the squared norm would double the penalty and constitute a different diagnostic. Offsets are unbounded; the earlier ±3 repair infeasibility argument does not apply to this calibration. No temperature, class weighting, clean fitting data or held-out-label tuning is used. Fitting this convex surrogate is not maximizing held-out classification accuracy or testing every possible bias vector.

The approved procedure uses deterministic float64 projected gradient descent from zero, step 100/51, projected-gradient infinity tolerance 1e-8, and caps of 10,000 updates and 60 seconds per fit. P001/P002 converged in 110/133 updates, at projected gradients 9.19e-9/9.51e-9. Fitted vectors were saved before held-out evaluation. No new inference, checkpoint access or licensed solver was used. Numerical convergence is not formal certification.

#### T2. Primary outcomes and all four class-gap comparisons

Both primary populations contain 8,900 images, including 876 true 8s and 8,024 non-8s. Counts are exact; percentages are rounded. Selected-set correctness is 51/100 and 53/100 for P001/P002 calibration, versus 100/100 for each recorded repair; calibration correctness is not satisfaction of the repair gap/gate constraints.

| Cohort/method | Fog correct | Fog accuracy | Fog true-8 correct | Fog non-8 correct | Clean correct | Clean accuracy |
|---|---:|---:|---:|---:|---:|---:|
| P001 ten-bias | 4,446 | 49.96% | 321 | 4,125 | 8,227 | 92.44% |
| P001/J0 | 5,087 | 57.16% | 698 | 4,389 | 8,448 | 94.92% |
| P001/J1 | 5,277 | 59.29% | 637 | 4,640 | 8,421 | 94.62% |
| P002 ten-bias | 4,296 | 48.27% | 248 | 4,048 | 8,263 | 92.84% |
| P002/J0 | 4,736 | 53.21% | 671 | 4,065 | 8,327 | 93.56% |
| P002/J1 | 5,024 | 56.45% | 463 | 4,561 | 8,348 | 93.80% |

| Calibration cohort / comparator | Repair minus calibration fog correct | True-8 component | Non-8 component | Repair minus calibration clean correct |
|---|---:|---:|---:|---:|
| P001/J0 | 641 | 377 | 264 | 221 |
| P001/J1 | 831 | 316 | 515 | 194 |
| P002/J0 | 440 | 423 | 17 | 64 |
| P002/J1 | 728 | 215 | 513 | 85 |

The near-match on non-8 correctness for P002/J0 is exceptional: 423 of that 440-image gap concern true 8s, whereas the other comparisons include 264–515 non-8 deficits. These are differences in totals of correct predictions, not counts of paired disagreements or causal shares. All four must be considered together.

Ten-bias calibration increases fog correctness over bounded scalar calibration by 823/671 images, while losing 274/239 clean correct predictions. On fog classes 0, 1, 6 and 7 it reaches 1,431/1,217 correct, versus 326 under either bounded scalar rule; class 1 reaches 316/379 correct out of 995, versus six under the scalar. It predicts 8 on 696/452 primary fog images, compared with 1,211–2,298 for the repairs. Clean true-8 correct counts are 616/599. Aggregate accuracy cannot substitute for these class tradeoffs.

#### T3. Selected-class imbalance and interpretation

Both selected cohorts contain four true 8s (4%), versus 876/8,900 (9.84%) on primary fog. The cross-entropy fit is sensitive to this selected-set label distribution; class-8 offsets are -3.841924/-3.942015. This is consistent with a contribution from cohort composition to the observed true-8 loss, but no controlled reweighting or alternative-cohort analysis identifies its causal magnitude. For unpenalized bias cross-entropy, the stationarity equations match mean fitted class probabilities to empirical class frequencies. With our L2 penalty the equations instead give mean(p_k)-frequency_k+lambda*b_k=0 (under the zero-sum gauge); exact frequency matching must not be asserted. No balancing or penalty retuning is added after observing these outcomes.

The conclusion is negative for sufficiency of this fixed selected-only regularized rule. It is not evidence that all bias adjustment fails or that the repairs improve representations. Every corresponding repair has higher aggregate fog and clean accuracy than these two fitted vectors. This finite-set comparison is not a claim about the full achievable bias-only fog/clean frontier, nor about all class-specific utilities.

#### T4. External reviewer observations and verified retrospective scores

The external reviewer independently refitted the approved objective from the original logits and reported exact agreement in primary counts. We subsequently evaluated all 12 supplied full-precision vectors directly on the archived logits, confirmed that decimal and hexadecimal representations agree, and reproduced every supplied fog/clean class-group count and selected accuracy where applicable. This verifies the scores of those vectors; we inspected the fitting/search source but did not regenerate its fits or greedy trajectory. The approved objective remains the exact T1 rule. The supplied penalty variants yield approximately 47.5–50.5% fog accuracy, showing that the observed shortfall survives these particular variants, not that every fitting rule is insufficient.

The reviewer supplies a standalone NumPy procedure starting from unpenalized cross-entropy fitting on the 8,900 held-out fog labels (4,634 correct), followed by six greedy passes through coordinates 0–9, trying 61 shifts in [-1.5,1.5] per coordinate and accepting strict increases in fog correctness. Its final vector, recentered to sum zero, directly reproduces 4,747/8,900 fog correct (53.34%) and 8,185/8,900 clean correct (91.97%). The supplied full-precision values, not the displayed three-decimal approximation, define this check. The intermediate cross-entropy vector's 4,634 score is also directly verified. No greedy search was rerun by the authors for this revision.

This vector establishes an attainable fog score, hence a lower bound on bias-only capability, not a best-case upper bound. Its fog score exceeds P002/J0 by 11 images but falls below the other three repairs. All four repairs have higher clean accuracy than this particular vector. Using held-out labels prevents a generalization interpretation; the result is a retrospective capability check rather than a deployable-baseline comparison. The nonexhaustive search does not certify the bias-only optimum or a fog/clean Pareto frontier.

No bias vector the reviewer examined matched or exceeded any recorded repair in both fog and clean accuracy. We confirmed this statement for the 12 supplied vectors and the supplied scalar maximum and endpoint scores against all four repairs. It is a statement about the examined vectors, not all possible biases. Scalar calibration preserves more clean correctness than every repair, and one supplied penalty variant ties P002/J0 at 8,327 clean correct; thus a blanket claim that every examined bias vector has worse clean accuracy would be false. Section 6 now reports the independently reconstructed global scalar maximum of 40.74%, separately from the fixed selected-only scalar outcomes.

#### T5. Reproduction and verification boundary

The completed local diagnostic verified the original-logit SHA-256 ef356769710266f255539755b3a035975ac37814d49a4e46ad5fe46c30659e6b, reconstructed all four saved fixed-offset scalar outcomes, and checked labels and baseline predictions against the archived evidence. An initial preflight stopped before fitting because the public cohort JSON had an extra trailing newline. The original Deepnote bytes matched the approved hash and had identical parsed cohort content; the failed preflight and correction were preserved. No cohort or scientific fitting rule changed.

The reproduction archive includes ORIGINAL_LOGITS.npz, the fixed source, selected cohorts, frozen fit records, predictions, complete class/comparison tables, provenance and the preserved failure. These support saved-logit arithmetic and numerical refitting, not checkpoint replay, solver certification or continuous-domain verification. For this revision we inspected the supplied source, evaluated all supplied vectors directly and independently enumerated scalar candidates; we performed no new fit, greedy-search regeneration or model inference. The reviewer's independent refitting is distinguished from our direct score verification.

### 8. Retained negative evidence and execution history

The eight-cohort pilot still has seven evaluable repairs; P005 is missing. Conditional frozen LOOCV ratios are 0.575 fog and 1.461 clean; the joint criterion failed. Post hoc analyses do not replace it. The retired normalized pairwise proxy and its architecture-specific zero-excess explanation remain methodological negatives, not validated predictors.

Four completed J0/J1 solves passed selected-point replay within declared tolerances. An earlier failed P001/J0 construction and explicit retry remain in the record; the public artifact is not a history of four failure-free constructions. The captured common-setup hashes match within each cohort, but the public package does not include matrices enabling an outside reconstruction. Saved-prediction table reproduction, checkpoint inference and formal certification are distinct evidence levels.

### 9. Discussion and publication boundary

The completed sequence shows that output offsets alone can recover substantial fog accuracy in this prediction-collapse regime. The fixed scalar rule reaches approximately 40.7%, and the richer fixed ten-offset rule reaches 48–50%, while recorded repairs reach 53–59%. The fixed-rule outcomes are not successive certified maxima; the separate exhaustive scalar check establishes 40.74% for that one-dimensional family. Direct evaluation of the reviewer-supplied held-out-fitted bias vector extends demonstrated bias-only capability to at least 53.34% fog accuracy, with 8,185 clean correct and greater clean damage than the recorded repairs. We therefore cannot interpret the remaining performance gap as evidence of representation improvement. The most defensible contribution is the documented class-structured fog/clean tradeoff across repair objectives and simple output calibration, including negative results and the limits of mechanistic interpretation.

One network and two selected cohorts support a preprint or technical note, not a general empirical law or a new repair principle. No further calibration search is needed to establish that scope. Formal venue readiness also requires ordinary editorial and citation checks; an external reviewer's favorable assessment is not journal acceptance.

No remaining-cohort J1 expansion, second network, new repair or solver experiment is commissioned by this draft. Historical J0 controls would require explicit comparability checks before a future paired expansion.

Bibliographic metadata were checked against publisher and DOI-registration records on 10 November 2026. The source-check record accompanies this manuscript; it documents the limits of the check separately from the scientific findings.

**Conclusion:** recorded APRNN repairs and fixed calibration rules produce distinct class-structured fog/clean outcomes. Both fixed calibration rules improve fog accuracy substantially but fail to reproduce the corresponding repairs’ fog accuracy; the ten-offset rule has worse aggregate fog and clean accuracy. This does not exclude more effective bias vectors or identify a representation-level mechanism. The evidence supports a bounded preprint or technical note; the experimental investigation is complete at that scope, with the frozen release preserved.

### References

[1] Zhe Tao, Stephanie Nawas, Jacqueline Mitchell, and Aditya V. Thakur. 2023. Architecture-Preserving Provable Repair of Deep Neural Networks. *Proceedings of the ACM on Programming Languages* 7, PLDI, Article 124, 25 pages. https://doi.org/10.1145/3591238.

[2] Matthew Sotoudeh and Aditya V. Thakur. 2021. Provable Repair of Deep Neural Networks. *Proceedings of the 42nd ACM SIGPLAN International Conference on Programming Language Design and Implementation*, 588–603. Author preprint: https://arxiv.org/abs/2104.04413.

[3] Feisi Fu and Wenchao Li. 2022. Sound and Complete Neural Network Repair with Minimality and Locality Guarantees. *International Conference on Learning Representations*. Author preprint, version 3: https://arxiv.org/abs/2110.07682v3.

[4] Keyvan Majd, Siyu Zhou, Heni Ben Amor, Georgios Fainekos, and Sriram Sankaranarayanan. 2021. Local Repair of Neural Networks Using Optimization. *arXiv preprint* arXiv:2109.14041. https://arxiv.org/abs/2109.14041.

[5] APRNN contributors. *APRNN source code*, commit 5f676a574cf418e10e458ac36b34d9f2f6417504. Files eval_1_aprnn.py and experiments/mnist/repair.py. https://github.com/95616ARG/APRNN/tree/5f676a574cf418e10e458ac36b34d9f2f6417504.

[6] Gurobi Optimization. *Gurobi Optimizer Reference Manual: Crossover parameter*. Online documentation, accessed 10 November 2026. https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#parameter:Crossover.

[7] Long Zhang, Shuo Sun, Jun Yan, Jian Zhang, Jiangzhao Wu, and Jian Liu. 2025. Accelerating constraint-based neural network repairs by example prioritization and selection. *Frontiers of Computer Science* 19(4), Article 194332. https://doi.org/10.1007/s11704-024-3902-x.

[8] Yuta Ishimoto, Masanari Kondo, Lei Ma, Naoyasu Ubayashi, and Yasutaka Kamei. 2025. Repairs and Breaks Prediction for Deep Neural Networks. *ACM Transactions on Software Engineering and Methodology* 34(4), 1–42. https://doi.org/10.1145/3702983.

[9] Xinyu Sun, Wanwei Liu, Shangwen Wang, Tingyu Chen, Ye Tao, and Xiaoguang Mao. 2025. AutoRIC: Automated Neural Network Repairing Based on Constrained Optimization. *ACM Transactions on Software Engineering and Methodology* 34(2), 1–29. https://doi.org/10.1145/3690634.

[10] Xiaofu Du, Zixiong Zhang, Xuesong Wang, Linqiang Liu, and Junyan Qian. 2026. Neural Network Repair With Shapley-Guided Search. *CAAI Transactions on Intelligence Technology* 11(3), 816–834. https://doi.org/10.1049/cit2.70147.

### Evidence and append-only update log

Frozen v1: papers/RESEARCH_FRONTIER_INTEGRATED_APRNN_MANUSCRIPT_v1_2026_11_10.md.
Decision: reviews/POST_PEER_REVIEW_SCIENTIFIC_DECISION_MEMO_2026_11_10.md.
Read-only reanalysis: experiments/publication_assessment/post_peer_review_2026_11_10/CLASS_AUDIT_RESULTS.json and read_only_class_audit.py.
Public baseline: https://github.com/rhuerta07/research-frontier-aprnn/tree/37d81655fca7857032360e8df831c284c51dfe93 .

10 November 2026: v2 started from independently recomputed saved-record class findings and source/math reassessment. No new inference or repair results added. D1–D4 remain empty pending research SWE evidence.

10 November 2026 — D1–D4 integrated from experiments/publication_assessment/class8_scalar_diagnostic_2026_11_10/. Sources: REPORT.md, CALIBRATION_RULE.json, D1_SELECTION.csv, D2_CLASS_TABLE.csv, D3_COMPARISONS.csv, BASELINE_PROVENANCE.json, scalar_diagnostic.py and SHUTDOWN.json. Independent saved-table arithmetic passed; original-model inference and binary-logit reconstruction were not rerun by the lead. V1 and the public GitHub artifact remain unchanged. No new research execution is commissioned.

10 November 2026 — focused external reassessment, v2 revision 1: narrowed the tested question and abstract to scalar calibration; retitled Section 6; added post hoc four-class concentration and observed cohort differences; verified four true-8 selected examples per cohort; removed the comparability screen from the current interpretation while preserving its frozen source record. Corrected the proposed ceiling to a conservative 46.06% for 0≤τ≤3.585779341447035 only. No ten-bias results, new inference, fitting or repairs were added. The previously distributed v2 packet remains an earlier snapshot.

10 November 2026 — v2 revision 2: integrated the approved ten-bias results, exact mean-cross-entropy plus lambda/2 objective, all four class-gap decompositions, selected-label imbalance and verification boundaries. Added the reviewer's independent reconstruction and clearly separated their unsupplied penalty variants and held-out-fitted bias vector from independently verified author results. No new fit, search, inference, repair or public GitHub mutation was performed. Earlier log entries describe their historical state.

10 November 2026 — v2 revision 3: corrected the overly broad clean-accuracy comparison; verified scores for all 12 reviewer-supplied vectors and the complete scalar candidate grid without regenerating fits or greedy search; confirmed 4,747 fog/8,185 clean and the scalar maximum 3,626. Replaced the range-limited discussion, acknowledged the valid piecewise 44.1% bound, added selected accuracies and removed editorial instructions. Verification artifacts and original supplied script/JSON accompany this revision. Earlier append-only log entries describe the information available at their time and are not current verification claims. No repairs, inference, new fitting or public GitHub edits.

10 November 2026 — v2 revision 4: scientific reviewer returned READY FOR BOUNDED PREPRINT after reading v2r3, explicitly without inspecting the verification record. Corrected the T4 heading and remaining imperatives; expanded reference entries and placed prior-work context in Section 2. Publisher/DOI bibliographic checks found no identified retraction notice for Zhang or NSRepair and confirmed AutoRIC's final metadata; detailed limitations are recorded separately. No new calculation, fitting, repair, model inference or public-release mutation accompanied this editorial revision. Earlier draft and reviewer-evidence snapshots remain preserved.

10 November 2026 — v2 revision 5: accepted the supplied restrained language copyedit after comparison with v2r4. Tables, displayed equation, numeric text, reference list and prior append-only log entries were unchanged by the copyeditor. Resolved the D1 author query: the no-oracle-sweep statement applies to the initial selected-only calibration diagnostic, before the later retrospective scalar enumeration; the latter did not select or revise frozen offsets. No numerical analysis or experiment was rerun.
