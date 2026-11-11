# Post-Peer-Review Scientific Decision Memo
10 November 2026 — Research Frontier publication assessment

**Decision: accept major revision of the interpretation; defer all new repairs. Recommend one separately approved, solver-free class-8 counterfactual diagnostic before deciding whether any further optimization is worth doing.** Freeze the existing manuscript and public commit 37d81655fca7857032360e8df831c284c51dfe93. A future manuscript must be v2. Our earlier GO was permission to seek criticism, not evidence of publication value; that criticism has exposed an important omission.

## 1. Review verdict: supported findings and overstatements

I read the supplied review in full and independently recalculated class-conditioned corrections, breaks, prediction frequencies, paired disagreements, selected margins and image-level paired statistics from the frozen public JSON. I inspected the pinned upstream objective/solver sources and primary prior-work/publisher records. No checkpoint inference, model construction, repair or solver was run.

**Verified class-collapse observations.** Original fog predicts 8 on 7,692/8,900 images (86.427%). True-8 accuracy is 875/876; other-class accuracy is 896/8,024 (11.167%). The labels themselves are not 86% class 8. This is a prediction collapse, not demonstrated label-prior shift.

| Repair | Fog predicted 8 | Fog correct true-8 /876 | Fog correct non-8 /8,024 | Fog breaks true-8 /all |
|---|---:|---:|---:|---:|
| P001/J0 | 2,298 | 698 | 4,389 | 177/222 |
| P001/J1 | 1,518 | 637 | 4,640 | 238/272 |
| P002/J0 | 2,093 | 671 | 4,065 | 204/245 |
| P002/J1 | 1,211 | 463 | 4,561 | 412/448 |

All fog corrections are true non-8s. Of fog breaks, 79.7–92.0% are true 8s. J1–J0 changes are +251 non-8/-61 true-8 correct in P001 and +496/-208 in P002. Class 1 worsens under J1: 334→175/995 and 411→244/995. Full ten-class correction/break tables are retained in CLASS_AUDIT_RESULTS.json.

**Verified disagreement, but not a causal explanation.** J0/J1 fog predictions disagree on 2,757/8,900 (30.978%) and 3,061/8,900 (34.393%). However, 1,215 and 1,453 disagreements have BOTH predictions non-8. A change only to class-8 bias cannot switch one winning non-8 class to a different non-8 class. Thus J1 cannot be exactly J0 plus an additional scalar class-8 shift. Relative to the original network, repairs change 234–283 originally non-8 fog predictions, correcting 139–220 and breaking 34–45 of them. This also rules out exact equivalence to a pure downward shift of the original class-8 bias.

Most corrections nevertheless occur among original-8 predictions. That is compatible with suppression explaining much of the gain, but winner-only predictions omit the competing logits and cannot quantify what a simple bias shift could achieve. The review's assertion that correction/break accounting “is one effect” is too strong. Matching a bias baseline's aggregate accuracy would demonstrate sufficiency of a simple alternative on this evaluation, not identify the actual APRNN mechanism or a causal fraction of its effect.

**Clean findings verified; “noise” needs care.** Original clean true-8/non-8 correct counts are 820/7,775. J0→J1 changes are 782→727 true-8 and 7,666→7,694 non-8 in P001; 773→745 and 7,554→7,603 in P002. Aggregate differences -27 and +21 are real finite-set counts, but not a stable direction across repairs.

Independent exact McNemar p-values are 0.104655 and 0.247380. Approximate paired 95% intervals are [-0.656,+0.050] and [-0.145,+0.617] percentage points. They assume image sampling and do not describe cohort/solver variation. Replace the rhetorical “sign reversal” with the class-resolved tradeoff and lack of established general direction; nonsignificance does not prove equal clean behavior. Fog paired statistics also reproduce (p≈4.02e-6 and 7.15e-11), but do not create independent repair replications.

## 2. Optimization reassessment

Let m_i=z_y-max_{j≠y}z_j and d_i=(0.001-m_i)_+. For the original strongest competitor, any successful selected-point repair requires Δz_y-Δz_j≥d_i, hence ||Δz||∞≥d_i/2.

Worst original margins independently read from frozen features give:
- P001: -6.841700161; J0 mixed infinity term ≥3.421350080.
- P002: -7.140667204; mixed infinity term ≥3.570833602.

Both exceed the editable box radius 3. Therefore throughout the feasible problem the mixed infinity term is output-dominated, not parameter-dominated. J0 still penalizes absolute parameter changes through normalized L1; it is not literally indifferent to increasing an individual edit. J1 separately penalizes maximum parameter displacement. The contrast in incentives is mathematical, and the maximum-edit observation should be demoted from the headline. **The exact observed 22–33-fold gaps are not forced by this derivation.**

P002/J0's observed max edit 2.999999980 is within about 2e-8 of its box. This shows near-bound activity; it does not establish the optimal value or held-out outcome would change if the box were relaxed. That requires sensitivity evidence not provided. No bound-variation solve is recommended.

The review's refined J0 L1 upper bounds also check: since selected output L1≥Σd_i, parameter L1≤11110*(q0-max_i d_i/2)-Σd_i, giving approximately 450.435 and 380.921. From recorded J1 objectives and observed max edits, 10110*(q1-||p||∞) gives 142.023 and 136.510. These are upper bounds from epigraph feasibility; reading them as actual L1, and inferring a minimum support count from them, requires objective-auxiliary tightness/optimality assumptions. Do not publish them as independently measured norms. Larger or smaller density is currently unknown.

For an edited-parameter characterization, actual L1, L2, max norm, thresholded nonzero count and count within 1e-6 of ±3 would be useful read-only checkpoint summaries; literal nonzero count is unstable under floating-point/barrier outputs. They are not prerequisites for the narrower bias diagnostic, and do not justify another solve.

Pinned upstream and saved run settings confirm Method=2, Crossover=0. Gurobi documents that crossover-off returns the interior solution computed by barrier. State “objective under this barrier/presolve/tolerance configuration,” not a unique canonical minimum-edit repair. An exact relative-interior point of a particular optimal face is not independently proved by these saved records. Identical repeated aggregate counts do not prove classifier identity or solver determinism.

**New decisive feasibility result:** ten-output-bias-only repair with the SAME ±3 bounds is impossible for BOTH cohorts. Bias differences can improve any class gap by at most 6, but required improvements are 6.842700161 and 7.141667204. This remains infeasible with the 1e-6 checking tolerance. No licensed feasibility run is needed.

Even an UNBOUNDED class-8-only downward shift cannot meet all selected constraints: non-8 errors require τ≥6.842700161/7.141667204, while selected true-8 margins require τ≤2.393007012/3.078081156. These necessary intervals are empty. This does not prohibit useful descriptive calibration, nor settle unrestricted ten-bias feasibility.

## 3. Prior art and contribution

The reviewer is correct that REASSURE and PRDNN are material omissions. I read the relevant primary passages: REASSURE explicitly distinguishes weight-space changes from function-space locality; PRDNN defines parameter-norm minimality. Majd et al.'s Section II.B explicitly gives the small-weight-change/new-error example. Add these before submission; our broad principle is established, not new.

Pinned experiments/mnist/repair.py already includes unit-weight parameter-only normalized-L1 plus infinity objectives. J1's objective FAMILY therefore ships upstream. Its helper has different edit/encoding interfaces; do not claim our entire J1 execution is identical to that helper without a full comparison. eval_1_aprnn.py confirms the mixed objective, k=2, ±3. The defensible contribution is the measured, class-resolved contrast inside the inspected benchmark.

Citation checks:
- Springer and HEP publisher records for Zhang and Wiley's NSRepair article were reachable. No retraction notice was identified in their retrieved records/text. Crossref endpoints and the NSRepair mirror were unavailable. **Retraction is unconfirmed: do not label either paper retracted or remove it on that basis.** Absence from retrieved text is not proof no notice exists.
- AutoRIC's authors/title and constrained-repair content are supported by the primary author-hosted PDF/publication list. Its PDF has provisional citation fields; ACM direct access returned 403. Final publisher issue metadata remains unconfirmed here; do not adopt an aggregator's unrelated title mapping.
- The 8,900 arithmetic reproduces the authors' saved-artifact rounded 31.53%; it strengthens a paper/code discrepancy diagnosis, but cannot establish the exact historical 2023 evaluation population from rounding alone.
- The reviewer's new permutation p-values and mechanical explanation of the pilot were not independently reproduced here and are not incorporated as findings. They cannot replace the frozen failed joint criterion.

A focused primary-source search did not locate a published quantitative class-8-offset explanation of this exact APRNN setup. This is not proof of novelty. PRDNN already discusses low fog accuracy on a related network. The stronger candidate question is **how well a simple logit calibration reproduces the observed class-resolved gains and costs in this benchmark**, not whether APRNN generally “only corrects priors.”

## 4. Prioritized next test: one solver-free diagnostic

**Proposal only, for sponsor approval:** use original-model logits to evaluate z_8(x)←z_8(x)-τ, all other logits fixed. This is a descriptive calibration baseline, not an APRNN repair satisfying the selected constraints; we have already proved it cannot satisfy those constraints.

First inspect existing internal NPZ/logit records. The public JSON has original winners and selected margins, not complete original held-out logits; internal NPZ contents have not been inspected. If absent, one forward evaluation of the frozen original network on the existing selected examples and clean/fog populations can supply them. No repaired model, fitting of weights, gradients or solver is needed.

Before inspecting any counterfactual held-out labels, fix the policy: for each frozen cohort choose τ≥0 minimizing selected-cohort classification errors, tie-break by the smallest τ with a fixed argmax/tie convention. Evaluate only the finite breakpoints and interval representatives induced by the selected logits. Report box-limited τ∈[0,3] as primary and an explicitly unconstrained calibration diagnostic as secondary; neither is a constraint-satisfying repair. Same chosen τ applies to both clean and fog held-out sets. Any full held-out sweep is descriptive/oracle-labelled and cannot select the headline τ.

Prespecify all ten true-class accuracies, corrections/breaks, true-8 retention, predicted-8 frequency, disagreement with J0/J1 and changes among original-non-8 predictions. Primary interpretation is the full tradeoff, not a single fog count.

- **Positive/simple-baseline-sufficient:** calibrated shift reaches comparable fog performance without worse clean/true-8 costs. That weakens the practical case for the complicated repair on these records; publish a benchmark/calibration caution. It does NOT prove APRNN operated solely through final bias changes.
- **Negative:** shifts fall short, or matching fog gains sacrifices substantially more clean/true-8 behavior. Reject scalar calibration as a sufficient explanation under this fixed rule, without claiming representation recovery or ruling out richer ten-bias/global adjustments.
- **Inconclusive:** good fog matches but conflicting class costs, unstable calibration across the two cohorts, ties, missing/inconsistent logits, or strong difference between selected-calibrated and held-out-oracle results. Report the tradeoff; do not expand automatically.

For “comparable,” predeclare an exploratory one-percentage-point margin on each aggregate accuracy and require no greater true-8 error count; this is a decision heuristic, not a significance/equivalence proof. Also report exact differences so the heuristic cannot hide an important miss. These rules are outcome-informed design choices for a retrospective diagnostic, not pristine preregistration.

## 5. Lean plan, exposure and hard stops

Assets: fixed original checkpoint/data, cohorts, public predictions, pinned model parser/runtime and existing replay code. Required change: one short read-only forward/logit-and-offset script or notebook plus class tables; no framework, solver adapter or new dependency. Preserve hashes, selected-label order and untouched checkpoint bytes.

Expected new solver runs: **zero**. Existing-logit processing should take seconds; if inference is needed, plan at most ten CPU minutes plus one minute cleanup in the existing environment, with a command timeout and machine-stop/readback using existing controls. This is a planning/processing bound, not a verified billing ceiling; no dollar estimate is claimed. If restore/transfer cannot fit the bounded task or needs new infrastructure, stop and return the obstacle.

Stop immediately on source/model/data mismatch, baseline argmax mismatch against archived predictions, incomplete logits, wrong selected-label order, or unexpected model writes/solver imports. No new repair/retry is authorized. Actual extra-norm extraction, if desired and already easy, can share the existing read-only checkpoint path; do not build a public checkpoint system.

**Do not commission five J1 runs now.** They cannot resolve the baseline mechanism question; frozen cohorts are not fresh independent settings. Historical J0 epsilon, source/runtime overlays, bounds, preprocessing and full common constraints must be reconciled first. Old outcome summaries are not matched-model certificates. If that cannot be established, the claimed five-run bargain may require five new J0 controls as well. Configured 900-second solver limits alone imply up to 75 solver minutes for five J1s; existing worker/replay envelopes permit 150 monitored minutes plus setup/cleanup, not “seconds” inferred from the old paper. Positive or negative scalar results do not automatically authorize expansion.

## 6. Publication decision and gate

**Revise the narrative now; propose the zero-solver diagnostic next; defer a peer-reviewed empirical submission and all additional repairs.** Preserve the original public release and RP001 records. A separately versioned v2 should lead with class-resolved churn, the output-dominated mixed objective and the limits of scalar calibration. Move proxy/engineering history to appendices, add REASSURE/PRDNN/Majd and upstream helper attribution, and demote “small edits did not preserve accuracy” from novelty to context. The clean counts remain, with correctly qualified sampling intervals.

The reviewer has identified a more useful question, not supplied its answer. Neither n=2 nor a positive diagnostic determines venue acceptance. Before any stronger statement about class-bias correction, verify the original logits and the prespecified counterfactual; before citing a retraction, obtain a real publisher notice; before claiming dense edits, inspect actual deltas; before using historical controls, establish comparability. Keep the joint pilot NO-GO unchanged.

**Sponsor decision requested:** approve only the bounded original-logit/offset diagnostic, or stop at a revised technical note. This memo authorizes no execution beyond the completed read-only saved-record analysis.

### Provenance and sources

Read-only audit: experiments/publication_assessment/post_peer_review_2026_11_10/read_only_class_audit.py and CLASS_AUDIT_RESULTS.json. All ten-class counts, paired statistics and mathematical numeric inputs are retained. Script uses Python standard library; its input/output paths record the local review workspace. Frozen GitHub release was not modified; no Deepnote machine was started. Review text was supplied as APRNN_independent_peer_review(1).md; its asserted external independence is sponsor-provided, not separately authenticated.

Primary references checked: REASSURE https://arxiv.org/pdf/2110.07682 (intro pp.1–2); PRDNN https://arxiv.org/pdf/2104.04413 (norm/minimality definitions); Majd et al. https://arxiv.org/pdf/2109.14041 (Section II.B); pinned APRNN https://github.com/95616ARG/APRNN/tree/5f676a574cf418e10e458ac36b34d9f2f6417504 ; Gurobi Crossover https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#parameter:Crossover ; Springer https://link.springer.com/article/10.1007/s11704-024-3902-x ; Wiley https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/cit2.70147 ; AutoRIC primary manuscript https://shangwenwang.github.io/files/TOSEM-24B.pdf and author publication list https://shangwenwang.github.io/publications/ .
