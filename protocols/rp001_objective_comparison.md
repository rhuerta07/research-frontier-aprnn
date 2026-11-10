# Objective choice and collateral changes in APRNN: a two-cohort case study

RP001 final research note — 2026-11-10

Status: development closed; descriptive note reviewed with a QUALIFIED PASS. This is an archived project research note, not a journal publication.

## Summary

In two frozen 100-example cohorts on one MNIST network, changing APRNN's optimization objective produced different repaired models under matching captured common constraints. A parameter-only objective yielded substantially smaller maximum parameter edits and greater fog accuracy than the original mixed objective in both cohorts. Nevertheless, both parameter-only repairs reduced clean accuracy relative to the original network. The clean difference between objectives changed sign across cohorts.

These observations show that, in the studied setting, acceptable point repairs can have materially different behavior and small parameter displacement does not ensure clean preservation. They do not establish a general repair method, estimate reliability across networks, or validate pre-repair prediction.

## Motivation and study boundary

RP001 began by asking whether the compatibility of the parameter changes demanded by selected examples helps explain generalization and collateral damage. An earlier eight-cohort margin pilot produced seven evaluable repairs; P005 had no evaluable checkpoint. Its prespecified joint predictive criterion failed. That result remains unchanged.

The present experiment asks a narrower question: does changing the objective used to select a repair affect the resulting behavior when the common constrained setup is matched? It does not directly test the earlier pairwise compatibility proxy.

## Methods

We used frozen P001 and P002 repair cohorts, each containing 100 selected fog examples, the same original 3×100 ReLU network, frozen datasets, editable parameter scope, bounds and solver settings. For each cohort we ran two objectives:

- J0: the original mixed objective, combining selected-logit changes with editable-parameter changes.
- J1: the same norm construction applied only to editable-parameter changes.

Both use an infinity term plus normalized L1. Removing the 1,000 logit-change entries changes the vector length from 11,110 to 10,110 and therefore changes the normalized-L1 weighting as well as removing the output term. The study tests this combined objective modification; it does not isolate output anchoring from normalization.

Before J1 optimization, the captured common setup had to match its cohort's J0 setup. Equation-based variable identities and row multisets were used to compare common numeric models; input identities, selected labels, parameter bounds, epsilon and captured solver settings were also checked. The comparison relies on shared APRNN/Sytorch assumptions and the existing numerical mapping procedure.

The pinned runtime used Python 3.12.16, PyTorch 2.10.0+cpu, NumPy 1.26.4 and Gurobi 13.0.3. Four completed repair runs were performed sequentially. One earlier P001/J0 construction failed before optimization because of label-shape handling; the failure was preserved, corrected, and retried once with explicit sponsor approval. Thus there were four completed repairs, not a failure-free four-construction history.

Each resulting checkpoint was separately loaded and evaluated with plain PyTorch. Verification checked the 100 selected examples, activation gates, frozen parameters and editable bounds. A selected margin passed at epsilon 0.001 with tolerance 1e-6. Solver status alone did not establish repair success. Primary clean and fog evaluations used indices 1100–9999, N=8,900 each. Full clean evaluation, N=10,000, was secondary.

## Results

All four completed repairs passed selected-point, activation-gate, scope and bound checks. Minimum selected margins were near 0.001; all checkpoints triggered the existing numerical-fragility flag. Both actual J0/J1 pairs passed the common-setup matching gate.

| Cohort | Objective | Fog correct / 8,900 | Clean correct / 8,900 | Maximum absolute parameter edit |
|---|---|---:|---:|---:|
| P001 | J0 | 5,087 | 8,448 | 2.137234 |
| P001 | J1 | 5,277 | 8,421 | 0.095826 |
| P002 | J0 | 4,736 | 8,327 | 3.000000 |
| P002 | J1 | 5,024 | 8,348 | 0.090313 |

The original network correctly classified 1,771 primary fog examples and 8,595 primary clean examples. Compared with J0, J1 increased fog accuracy by 2.135 percentage points in P001 and 3.236 points in P002. Its primary clean difference was −0.303 points in P001 and +0.236 points in P002. Secondary full-clean counts were J0/J1 9,489/9,455 in P001 and 9,360/9,372 in P002, against original 9,654.

Aggregate accuracy concealed both corrections and regressions:

| Cohort | Objective | Fog corrected | Fog broken | Clean corrected | Clean broken |
|---|---|---:|---:|---:|---:|
| P001 | J0 | 3,538 | 222 | 49 | 196 |
| P001 | J1 | 3,778 | 272 | 33 | 207 |
| P002 | J0 | 3,210 | 245 | 32 | 300 |
| P002 | J1 | 3,701 | 448 | 25 | 272 |

“Corrected” denotes previously incorrect examples becoming correct; “broken” denotes previously correct examples becoming incorrect. J1 produced more fog corrections and more fog breaks in both cohorts, despite its much smaller maximum edits.

## Interpretation and limitations

The matched runs demonstrate sensitivity to the objective specification in this particular setting. Reducing maximum parameter displacement did not prevent clean regressions. They also show why aggregate improvement is insufficient: a model may correct many fog examples while breaking other fog and clean examples.

The evidence does not identify a unique causal mechanism. Objective normalization changed, solver tie-breaking and multiple optima may influence which numerical solution was selected, and there were no repeated solver runs. Two cohorts on one network and shared evaluation examples do not estimate population reliability. Cohorts were frozen before these repairs, but the study and objective ablation followed earlier observed outcomes; it is exploratory rather than a fresh confirmatory test.

Numeric common-model agreement and checkpoint replay are evidence under specified software, mappings and tolerances. They are not formal real-arithmetic equivalence, independent optimality certificates, continuous-domain guarantees or a fully independent implementation of APRNN. Runtime epsilon was observed before/after common construction and its classification equations were checked; the earlier 900-read trace belonged to the earlier setup comparison, not every completed repair.

Maximum parameter displacement is a post-repair diagnostic dependent on the chosen parameterization. No pre-repair predictor, general compatibility measure or new repair algorithm is validated here. Prior margin and compatibility analyses are not upgraded by this experiment.

## Independent review

A separate reviewer inspected all 400 saved selected-point records, the four solver/terminal records, both pairs' common-setup agreement, the objective source difference and relevant replay/comparison source. They checked the correction/break/net arithmetic and supported the narrow conclusion with a QUALIFIED PASS. They did not rerun checkpoints or independently reconstruct held-out counts from the large per-image prediction arrays. The review therefore corroborates the saved evidence and interpretation; it is not a fresh numerical replication. See reviews/Independent_Final_Scientific_Review_RP001_Option_B_2026-11-10.md.

## Conclusion and stopping decision

In these two cohorts, changing how APRNN selected among repairs satisfying the checked constraints materially changed held-out behavior. Parameter-only minimization produced much smaller maximum edits but did not preserve baseline clean accuracy.

Development of RP001 is stopped. No additional repairs or infrastructure are recommended. The contribution is a bounded empirical case study with preserved negative results and execution failures, rather than a general repair method or universal rule.

## Evidence

Deepnote project: f6c5816d-e24f-4141-819e-a18f90ef4ef7.

- Detailed results: papers/RP001_OPTION_B_FOUR_REPAIR_RESULTS_2026_11_10.md.
- Successful checkpoints, common captures, solver records, replay and paired predictions: experiments/aprnn_r002_r004/rp001_option_b_four_repair_2026_11_10/.
- Exact source, authorized retry record and RESULTS_VERIFIED.json: experiments/aprnn_r002_r004/rp001_option_b_authorized_retry_v14_2026_11_10/.
- Preserved failed construction: experiments/aprnn_r002_r004/rp001_option_b_four_repair_2026_11_10_failed_attempt1/.
- Execution run: e891e008-803d-4abf-ac2a-30ca90a53385; final aggregation: d596f46c-d8f1-476a-a095-e68a64c34b31.
- Machine was confirmed stopped after verification; account-wide WLS sessions were not audited.

