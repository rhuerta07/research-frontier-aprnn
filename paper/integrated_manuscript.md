# Constraint satisfaction, objective choice, and collateral changes in APRNN
## An integrated reproducibility and negative-results case study

Research Frontier — integrated manuscript v1, 10 November 2026. Draft for external scientific criticism; not submitted or peer-reviewed. RP001 experimental development remains closed.

### Abstract

We examine whether properties of repair cohorts or repair objectives explain the held-out effects of APRNN parameter edits. Our investigation uses one pretrained 3×100 MNIST network, MNIST-C fog and clean counterparts, and the pinned APRNN implementation. Re-evaluation and checkpoint replay establish an empirical baseline while revealing differences between paper descriptions and executable settings. A prospective eight-cohort pilot yielded seven evaluable repairs and one operationally missing outcome. A frozen original-model median-margin forecast reduced fog prediction error but increased clean prediction error; the joint criterion failed, and the fog result was sensitive to one case. A later normalized pairwise lower-bound proxy was reproducible but structurally confounded and was retired. Finally, four fresh matched objective runs on two reused cohorts all satisfied the checked selected-point constraints. A parameter-only objective produced much smaller maximum parameter edits and 2.135–3.236 percentage points more fog accuracy than the original mixed objective, while its clean difference changed sign across cohorts. Every repaired model reduced primary clean accuracy relative to baseline. These results support a bounded empirical account of objective sensitivity and negative forecasting results. They establish neither a new repair algorithm, a validated compatibility predictor, nor a general reliability claim.

### 1. Question and contribution

A neural-network repair can satisfy its finite specification while changing behavior elsewhere. That distinction is established in prior repair research [1–5]. Our question is narrower: in an inspected APRNN setting, what information about the selected cohort or the repair-selection objective helps describe the resulting benefit and damage?

We contribute an auditable case study with three linked findings: a failed joint cohort forecast, a mathematically interpretable but scientifically unhelpful pairwise proxy, and a matched objective comparison showing different held-out behavior despite selected-point success. The objective comparison is the principal empirical result; the earlier stages explain what failed to support prediction and why the investigation changed direction. We claim no priority for gradients, margins, constraint selection, norm bounds or benefit–damage tradeoffs. Engineering work is supporting provenance, not itself the scientific contribution.

### 2. Related work and the boundary of novelty

APRNN provides architecture-preserving provable repair for specified pointwise or V-polytope properties, with empirical evaluation of generalization and drawdown [1]. Its guarantee does not automatically preserve unspecified inputs. Our finite-image checks do not independently reproduce its continuous-domain proof.

Zhang et al. prioritize repair examples using output and final-layer geometry [2]. Their input-stability ranking is distinct from displacement in editable-parameter space. Ishimoto et al. predict individual repairs and breaks and use predictions for repair-method choice [3]; our pilot instead forecasts aggregate changes across repair cohorts. These are differences of experimental setting, not sufficient novelty arguments.

AutoRIC studies constrained repair and restrictive-constraint selection [4]. More recent NSRepair explicitly frames correction and preservation as competing optimization objectives [5]. Thus objective choice and collateral damage cannot be our broad discovery. The candidate contribution is the particular controlled APRNN contrast, paired outcome decomposition, and transparent negative results. A focused literature check found no verified prior reproduction of this exact package, but that is not an exhaustive priority claim. The original APRNN authors and other repair researchers should judge whether this specificity is useful.

### 3. Implementation and evidence

The source lineage is APRNN commit 5f676a574cf418e10e458ac36b34d9f2f6417504, with documented runtime overlays and per-run hashes. Editable parameters are the second linear layer's 100×100 weights and 100 biases, plus ten final biases: 10,110 coordinates. First-layer and final output weights remain frozen. Original activations determine the branch restrictions encoded for selected examples. This edit scope makes each selected class-gap equation affine within the encoded branches; it does not describe arbitrary multilayer edits.

Independent loading and forward replay were used where recorded, with shared model-format assumptions disclosed. Saved optimizer status is not an independent optimality certificate. Inputs, scopes, constraints and checkpoints have different verification histories across stages; “independent verification” does not denote a wholly independent implementation or outside replication.

Primary fog and clean evaluation in the pilot and objective study use indices 1100–9999, N=8,900 each. Repair cohorts come from indices 100–1099; primary clean excludes their clean counterparts. Full clean indices 0–9999, N=10,000, are secondary. All these benchmark data had been examined previously. No fresh blinded test set was introduced.

### 4. Reproducibility and cohort sensitivity

Re-evaluating the authors' saved repair gave original/repaired counts of 1,771/4,577 on 8,900 fog images and 9,654/9,526 on 10,000 clean images. A newly generated R001 checkpoint gave 4,566 fog and 9,527 clean correct. Separate checkpoint replay reproduced the recorded R001 predictions within its stated shared-parser scope.

This is executable-artifact reproducibility, not an exact reconstruction of the historical 2023 optimization. The paper describes 9,000 fog generalization cases, whereas pinned code uses 8,900. Paper k=1 versus recorded implementation module index k=2 remains a convention/settings caveat. Matching rounded results cannot resolve either issue. The upstream repository itself warns of environmental and numerical variation [6].

R002 repeated R001's cohort and produced a matching checkpoint. It is repeatability evidence, not a fourth distinct cohort. R003 and R004 produced 5,128 and 4,462 fog-correct cases respectively, a difference of 666/8,900 or 7.483 percentage points. Both passed selected-point checks. Their clean correct counts were 9,470 and 9,409. Cohort composition and selection pools differed; this is descriptive sensitivity, not an identified cohort mechanism.

### 5. Prospective median-margin pilot: joint failure

Eight 100-image cohorts and their features were frozen before optimization. The only predictor was the original network's median true-class logit minus strongest competing logit on selected examples. The prospective status applies to feature/cohort freezing relative to these repairs, not to an outcome-naive research program.

Seven repairs satisfied all 100 selected examples. P005 failed operationally during initialization and has no evaluable checkpoint or imputed outcome. All seven evaluable repairs improved fog accuracy and reduced primary clean accuracy.

Conditional leave-one-cohort-out analysis used training-fold standardization, a ridge slope penalty of one, an unpenalized intercept, and a training-fold mean comparator; no outcome-driven hyperparameter search was performed.

| Target | Baseline MAE, pp | Margin MAE, pp | Ratio | Prespecified screen |
|---|---:|---:|---:|---|
| Fog accuracy change | 3.648 | 2.098 | 0.575 | Pass, threshold ≤0.80 |
| Clean accuracy change | 0.517 | 0.755 | 1.461 | Fail, threshold ≤0.90 |

The joint screen failed. Excluding P004 in an explicitly exploratory sensitivity analysis increased the fog ratio to about 0.880; that six-case analysis does not replace the seven-case primary analysis. The folds overlap and cohorts share examples and evaluation data. These ratios are exploratory performance screens, not significance tests or seven independent validation studies.

### 6. Repair pressure and a rejected compatibility proxy

Let editable displacement be δ, and let a selected branch-affine requirement be aᵀδ ≥ b. For nonzero a and unrestricted displacement, its single-row minimum infinity displacement is b₊/||a||₁. Bounds, gate constraints, other class competitors and anchors can raise the required displacement or make the full problem infeasible. If a=0 and b>0 the row is infeasible; if b≤0, δ=0 satisfies that single row. This is elementary norm duality, not a novel repair theorem.

For normalized rows uᵢ=aᵢ/||aᵢ||₁ and thresholds tᵢ=bᵢ/||aᵢ||₁, a feasible displacement must satisfy (uᵢ+uⱼ)ᵀδ ≥ tᵢ+tⱼ. The resulting lower bound is (tᵢ+tⱼ)₊/||uᵢ+uⱼ||₁ when the denominator is positive. A zero sum with positive combined threshold is infeasible; otherwise the combined row adds no positive displacement bound. Positive excess above the two standalone bounds strengthens a necessary bound, not a certificate of actual pairwise repair cost or full-set incompatibility.

The finalized screen selected the ten highest original deficits per cohort and one original strongest competitor per example: 45 pairs per cohort, 360 pairs including pre-repair-only P005 data. It yielded 95 positive excesses above 1e-10; every cohort median was zero. A separate team calculation reconstructed all normalized scores from model tensors with maximum discrepancy approximately 1.04e-17, sharing parser/data/runtime assumptions. An earlier unnormalized screen produced 87 positives and was superseded because equivalent row scaling changed its score; these counts are different constructions, not conflicting replications.

All 360 finalized pairs shared competitor class 8. None of 123 same-true-class pairs had positive excess. In this edit scope, the same true/competitor class pair fixes coordinate signs of the normals because hidden ReLU activations and gate masks are nonnegative. The L1 norm of the summed normalized normals is therefore exactly two in exact arithmetic, so the combined-row bound is at most the larger standalone bound. The zero excess is structurally implied; it is not empirical confirmation of compatibility.

We retired the proxy. The analysis neither proves every simpler feature explains it nor disproves the general compatibility hypothesis. No predictor was fitted to the known seven outcomes.

### 7. Matched objective comparison

We reused P001/P002 to investigate objective sensitivity after earlier outcomes were known. Four fresh completed solves ran sequentially in the pinned Python 3.12.16/PyTorch 2.10.0+cpu/NumPy 1.26.4/Gurobi 13.0.3 runtime. They are not four new cohorts or an independent prospective replication of the pilot.

Let p be editable parameter displacement and o the 1,000 selected-logit changes. With φₘ(z)=||z||∞+(1/m)Σ|zₖ|, J0 minimizes the implemented upper-bound formulation of φ₁₁₁₁₀([o;p]); J1 uses φ₁₀₁₁₀(p). Aliases, absolute-value and maximum auxiliaries implement the source construction. Under free-real auxiliary and finite-expression assumptions, common feasible points can be extended to these auxiliaries. Our numeric gates check the common model; they do not independently certify exact-real projected equivalence of the complete problems.

The intervention changes both the included quantities and normalized-L1 weighting. It does not isolate output anchoring from normalization and does not minimize infinity displacement alone.

Before J1 optimization, each cohort's captured common setup had to equal J0's: semantic matrix hash, variables/bounds, rows and multiplicities, labels/indices, provenance, epsilon and selected solver settings. Both pairs passed. Epsilon was observed before/after common construction and classification equations checked; the earlier 900-getter trace was from a separate setup experiment.

Every resulting checkpoint passed separate plain-PyTorch replay: 100/100 selected points, gate restrictions, frozen parameters and editable bounds. The margin criterion was epsilon 0.001 with tolerance 1e-6. All minima lay near the active boundary; the fragility flag records proximity, not measured instability.

| Cohort | Objective | Primary fog correct | Primary clean correct | Maximum absolute editable displacement |
|---|---|---:|---:|---:|
| P001 | J0 | 5,087 | 8,448 | 2.137234 |
| P001 | J1 | 5,277 | 8,421 | 0.095826 |
| P002 | J0 | 4,736 | 8,327 | 3.000000 |
| P002 | J1 | 5,024 | 8,348 | 0.090313 |

Each primary denominator is 8,900; baseline counts are 1,771 fog and 8,595 clean. J1 minus J0 is +2.135 pp fog and −0.303 pp clean for P001, +3.236 pp fog and +0.236 pp clean for P002. Full-clean J0/J1 counts are 9,489/9,455 and 9,360/9,372, respectively, against baseline 9,654/10,000.

| Cohort/objective | Fog corrections | Fog breaks | Primary clean corrections | Primary clean breaks |
|---|---:|---:|---:|---:|
| P001/J0 | 3,538 | 222 | 49 | 196 |
| P001/J1 | 3,778 | 272 | 33 | 207 |
| P002/J0 | 3,210 | 245 | 32 | 300 |
| P002/J1 | 3,701 | 448 | 25 | 272 |

Both objectives improve fog while damaging clean behavior relative to baseline. J1 creates more fog corrections AND more fog breaks in both cohorts. Its smaller maximum edits do not preserve clean accuracy. The sign reversal in clean J1–J0 differences precludes a consistent clean advantage.

The new J0 outcome counts match historical P001/P002 counts, but matching counts do not establish matching checkpoints or independent new evidence. We do not add these repeated cases to the pilot sample size.

### 8. Threats to interpretation and review status

One network, one corruption, reused cohorts and test examples, and outcome-informed study development limit scope. Repeated benchmark inspection and overlapping cohorts prohibit a naive independent-image or independent-repair interpretation. Parameter displacement depends on units/parameterization and editable scope; the observed magnitude cannot establish a universal safety relation.

Different objectives select solutions differently, but exact numerical solutions can depend on solver tolerances, tie-breaking and multiple optima. No repeated-seed or second-model experiment estimates those effects. The work does not identify the unique cause of regressions or establish compatibility as their mechanism. No effect is claimed for LLMs.

Failures are retained. The historical pilot's P005 remains missing. Before the objective study, a launcher failed before admission on path canonicalization. A P001/J0 construction then failed before optimization on label shape; an explicitly authorized retry produced the four completed solves. This was not a failure-free four-construction history.

The final separate AI-assisted reviewer inspected all 400 selected-point records, solver/terminal evidence, common setups, objective diff and comparison/replay source, and checked summary arithmetic. That review returned QUALIFIED PASS. It did not reload checkpoints or reconstruct held-out counts from the large prediction arrays. Team-separated review is not outside scholarly peer review.

### 9. Conclusion

In these two cohorts, changing APRNN's objective specification materially changed the recorded repaired solutions and held-out behavior under matching captured common constraints. The parameter-only objective produced much smaller maximum parameter edits but did not preserve baseline clean accuracy. Earlier cohort forecasting and the selected compatibility proxy did not establish reliable prediction.

The defensible contribution is an empirical reproducibility and negative-results case study. RP001 development is closed. Its importance and suitability for publication require external criticism; no additional repair or infrastructure is commissioned by this manuscript.

### References

[1] Tao, Z., Nawas, S., Mitchell, J., and Thakur, A. V. (2023). Architecture-Preserving Provable Repair of Deep Neural Networks. PACMPL 7, PLDI, article 124. https://doi.org/10.1145/3591238 . Author full text: https://thakur.cs.ucdavis.edu/assets/pubs/PLDI2023.pdf .

[2] Zhang, L., Sun, S., Yan, J., Zhang, J., Wu, J., and Liu, J. (2025; online 2024). Accelerating constraint-based neural network repairs by example prioritization and selection. Frontiers of Computer Science 19(4), 194332. https://doi.org/10.1007/s11704-024-3902-x . Source: supplied full-text literature assessment and verified publisher record; no fresh primary PDF access claimed here.

[3] Ishimoto, Y., Kondo, M., Ma, L., Ubayashi, N., and Kamei, Y. (2025). Repairs and Breaks Prediction for Deep Neural Networks. TOSEM 34(4), article 94. https://doi.org/10.1145/3702983 . Source: existing supplied full-text assessment and author-institution record https://kyushu-u.elsevierpure.com/en/publications/repairs-and-breaks-prediction-for-deep-neural-networks/ ; ACM direct fetch was unavailable.

[4] Sun, X., Liu, W., Wang, S., Chen, T., Tao, Y., and Mao, X. AutoRIC: Automated Neural Network Repairing Based on Constrained Optimization. https://doi.org/10.1145/3690634 . Author manuscript https://shangwenwang.github.io/files/TOSEM-24B.pdf has provisional bibliographic fields; author's publication list labels 2024 and issue records use 2025. No new allegation about the published implementation is based on draft inconsistencies.

[5] Du, X., Zhang, Z., Wang, X., Liu, L., and Qian, J. (2026). Neural Network Repair With Shapley-Guided Search. CAAI Transactions on Intelligence Technology 11(3), 816–834. https://doi.org/10.1049/cit2.70147 . Publisher full text checked for multi-objective framing; no claim of reproducing its experiments or exhaustive comparison.

[6] APRNN author repository, https://github.com/95616ARG/APRNN . Our experiments use the pinned revision and recorded overlays, not an assumed unchanged latest repository.

### Appendix A. Evidence map

All relative paths below are in Deepnote project f6c5816d-e24f-4141-819e-a18f90ef4ef7.

| Manuscript claim | Principal saved source | Boundary |
|---|---|---|
| Artifact replay and R001–R004 | papers/APRNN_REPRODUCTION_WORKING_NOTE_R002_R004_ZHANG_2026-11-08.md; reviews/Independent_Checkpoint_Replay_APRNN_Repair_R001_2026-11-08.md | Historical layers contain superseded status statements; use dated result sections |
| Frozen pilot and failed joint screen | papers/APRNN_EIGHT_COHORT_PILOT_RESEARCH_REPORT_2026-11-09.md; experiments/aprnn_r002_r004/prospective_pilot_2026_11_08/POST_RUN_RECONCILIATION_AND_CONDITIONAL_LOOCV_v1.json | Conditional seven-case analysis, P005 missing |
| Rejected normalized proxy | papers/RP001_NORMALIZED_PAIR_FALSIFICATION_AUDIT_2026-11-09.md; papers/RP001_REPAIR_PRESSURE_WORKING_NOTE_2026-11-09.md | Shared-runtime reconstruction, retrospective development |
| Matched objective outcomes | papers/RP001_OPTION_B_FOUR_REPAIR_RESULTS_2026_11_10.md; experiments/aprnn_r002_r004/rp001_option_b_authorized_retry_v14_2026_11_10/RESULTS_VERIFIED.json | Two reused cohorts, four completed solves, one earlier failed construction |
| Checkpoints and predictions | experiments/aprnn_r002_r004/rp001_option_b_four_repair_2026_11_10/ | Internal stored artifacts, not yet an independently rebuilt public reproduction |
| Final review | reviews/Independent_Final_Scientific_Review_RP001_Option_B_2026-11-10.md | Separate AI-assisted saved-evidence review, not external peer review |
| Prior-work context | supplied Literature_Review_v2_Zhang_Verified.pdf; notes/LITERATURE_AND_APRNN_FEASIBILITY_2026-11-07.md | Some primary-source claims inherited from earlier documented reading |

### Appendix B. Release checklist and open scholarly questions

Before public submission, resolve author names/affiliations and contributor/AI-use disclosure, verify permission and licensing for shared code/data, and prepare a minimal access-tested evidence index using existing files. This writing/release work is not authorization for new infrastructure. An outside reviewer should check the central novelty claim and, if feasible, reconstruct primary outcome counts from the stored predictions; the current read-interface limitation is a known verification boundary, not a scientific reason to launch new repairs.

The single experimental gap with greatest value for a broader claim is transfer of the frozen matched-objective contrast to one independently pretrained network. It is proposed only in the accompanying assessment; no execution is authorized. No outside feedback or acceptance is fabricated.

