# Research Frontier: APRNN reproducibility and objective sensitivity

An exploratory reproducibility, objective-sensitivity, and negative-results case study by Roberto Huerta, with AI assistance disclosed below. This is a bounded research artifact for external scientific criticism, not a peer-reviewed publication or an official APRNN extension. There is no claimed collaboration with UC Davis or endorsement by APRNN's authors.

## What can be reproduced here

| Reproduction level | Availability |
|---|---|
| Recalculate reported RP001 tables from archived per-image predictions and selected-point logits; recalculate pilot LOOCV from saved cohort summaries/features | **Available** with the included standard-library analysis |
| Independently rerun repaired models from checkpoints | **Not available**: checkpoints and a complete public replay environment are not supplied |
| Independently establish solver correctness, optimality, or formal continuous-domain guarantees | **Not provided** |

This is saved-evidence table reproduction, not end-to-end reproduction of the APRNN experiments. The repository and PR branches are public; draft PR status does not restrict access.

## Research and principal findings

We investigated whether repair-cohort properties or objective choice help explain held-out benefit and collateral damage in architecture-preserving neural-network repair. The central comparison reuses two frozen cohorts (P001/P002), with four completed J0/J1 repair runs under matching captured common constraints. Every run passed the checked 100 selected points.

| Cohort | Objective | Fog correct / 8,900 | Clean correct / 8,900 | Observed maximum parameter edit |
|---|---|---:|---:|---:|
| P001 | J0 | 5,087 | 8,448 | 2.137234 |
| P001 | J1 | 5,277 | 8,421 | 0.095826 |
| P002 | J0 | 4,736 | 8,327 | 3.000000 |
| P002 | J1 | 5,024 | 8,348 | 0.090313 |

J1 minus J0 fog accuracy is +2.135 and +3.236 percentage points. Clean differences have opposite signs: −0.303 and +0.236 pp. All four repairs reduce clean accuracy relative to the original model (8,595/8,900). Smaller observed maximum edits therefore did not preserve baseline clean accuracy in these cases. Maximum displacement is a post-repair observation, not a proof of globally minimal infinity displacement or a general guarantee.

J0 combines 1,000 selected-logit changes and 10,110 parameter deltas in an infinity-plus-normalized-L1 surrogate. J1 includes only parameter deltas. This changes both the quantities included and the L1 normalization denominator (11,110 to 10,110); it does not isolate their individual effects.

## Other findings

The eight-cohort median-margin pilot has seven evaluable repairs. P005 remains operationally missing after `TELEMETRY_UNAVAILABLE`; it was neither replaced nor imputed. Conditional leave-one-cohort-out MAE ratios are 0.575 for fog (passes ≤0.80) and 1.461 for clean (fails ≤0.90). The prespecified joint screen is **NO-GO**. Fog performance is sensitive to P004. No validated general predictor was established.

A later normalized pairwise compatibility proxy was retired: all 360 inspected pairs shared competitor class 8, all cohort median excesses were zero, and same-true-class zeros were structurally implied in this edit scope. This package preserves the manuscript's account; it does not independently rebuild that proxy from model tensors.

## Scientific scope

One pretrained 3×100 MNIST network, MNIST-C fog and clean counterparts, frozen 100-example cohorts drawn from indices 100–1099, and 10,110 editable parameters (second linear weights/biases and final biases). Primary fog and clean evaluation use indices 1100–9999 (8,900 each). Full clean evaluation uses 0–9999 (10,000) as a secondary population. First-layer and final output weights remain frozen.

Finite-image checkpoint replay and numerical point checks are different from formal continuous-domain verification. This release processes archived predictions and logits; it does **not** rerun inference, establish solver optimality, or reprove APRNN's guarantees.

## Reproduce the central tables

Use Python 3.10 or later; validated on Python 3.12.14. There are **no third-party dependencies** to install, hence no dependency versions to resolve. No Gurobi, Sytorch, GPU, Deepnote login, or cloud credentials are required.

```sh
git clone https://github.com/rhuerta07/research-frontier-aprnn.git
cd research-frontier-aprnn
git checkout --detach e364c5810cfc783bfeb4a7e1313d9fea6582cb7b
python analysis/reproduce_tables.py
python -m unittest discover -s tests -v
```

The checkout pins the verified scientific snapshot by full commit SHA and does not depend on the preparation branch remaining available. Later documentation corrections do not change that snapshot's analysis or evidence. To cite a later reviewed revision, record its full commit SHA separately.

The analysis command reads immutable saved evidence and prints JSON tables. It verifies release byte hashes, canonical JSON hashes linked to archived replay records, cohort/selected-label identities, cross-run image indices/labels/reference predictions, denominators, selected-point logits/margins, correct counts, correction/break transitions and J1-minus-J0 differences. It recalculates the original frozen LOOCV specification from saved cohort outcomes/features and checks the negative joint decision. Missing, malformed, altered or inconsistent evidence causes a nonzero exit.

These hashes pin the included evidence and connect it to saved internal records. They are **not external attestation** of its origin. The hash manifest itself is part of the reviewed commit; retain that commit when citing or checking the artifact.

## Evidence availability and verification levels

| Included material | What can be checked here |
|---|---|
| Four RP001 per-image prediction files, selected-point logits and common setups | Reconstruct primary/full-clean counts, transitions and selected-point success; check captured setup equality |
| Final RP001 saved summary | Cross-check reconstructed counts and report recorded parameter displacements and checkpoint hashes |
| Frozen eight-cohort indices/features and pilot reconciliation | Recalculate conditional LOOCV from saved cohort outcomes; P005 remains missing |
| Integrated manuscript, pilot/RP001 reports, final review and failure records | Inspect scientific methods, failed attempts, authorized retry and stated review limits |
| Evidence manifest | Source Deepnote paths, release byte hashes/sizes, format, purpose and verification boundaries |

The four prediction files total about 1.1 MB and are small enough to include directly; no external hosting is needed for core table reconstruction. Small text transfers may normalize a final newline; canonical JSON links are checked separately. Predictions were exported using a standard-library-only notebook with read-only project storage, without inference or optimization.

**Unavailable in this public package:** model checkpoints, dataset images, full solver matrices, upstream source/runtime overlays, and a verified public versioned binary archive. A private Deepnote link is not public artifact availability. Full checkpoint replay therefore remains an optional reproduction level requiring separately cleared weights/data/code and the archived runtime (Python 3.12.16, PyTorch 2.10.0+cpu, NumPy 1.26.4); no working public checkpoint replay is claimed. Historical reproduction tables and the retired proxy are documented, not independently reconstructed by this script. Pilot per-image outcomes are checked only at saved-summary level.

## Execution history and review limits

Retained records document P005's unresolved outcome, the earlier preoptimization P001/J0 construction failure, and the explicitly authorized retry that produced four completed solves. There was also a launcher failure before admission. Do not interpret the study as four failure-free construction attempts.

The saved separate AI-assisted review returned **QUALIFIED PASS** for a descriptive note. It is not outside scholarly peer review or external replication. Its own historical inability to read the large prediction arrays remains accurately described in that review; this release subsequently reconstructs those arrays' counts. See [review boundaries](reviews/review_scope_and_limitations.md).

## Limitations

Two reused cohorts, one small network and one corruption do not establish a new algorithm, causal mechanism or general reliability. Cohorts overlap and share repeatedly inspected evaluation sets; images are not independent repair replications. Objective normalization changes with objective membership. Numerical checks depend on tolerances (selected margin epsilon 0.001, tolerance 1e-6), shared model-format assumptions, solver tie-breaking and possible multiple optima. Near-boundary margins do not themselves demonstrate instability. External checkpoint replication, external attestation, historical billing and complete operational shutdown reconciliation remain incomplete.

## Prior work, attribution and licenses

Tao, Z., Nawas, S., Mitchell, J., and Thakur, A. V. (2023). *Architecture-Preserving Provable Repair of Deep Neural Networks*. PACMPL 7 (PLDI), article 124. https://doi.org/10.1145/3591238.

Upstream: https://github.com/95616ARG/APRNN, pinned commit `5f676a574cf418e10e458ac36b34d9f2f6417504`. Its applicable root license is **CC BY-NC-ND 4.0**. This release does not redistribute upstream code, modified upstream workers, model weights or dataset images, and does not relicense them. Rights clearance remains necessary before adding them. Other related work is cited in the [manuscript](paper/integrated_manuscript.md); the privately compiled literature review is not included as a primary paper.

Sponsor-approved licenses: **MIT** for original analysis/test code; **CC BY 4.0** for original manuscript/documentation. Saved research records are supplied for inspection; no grant of third-party rights is implied. See [LICENSE](LICENSE) and [third-party notice](THIRD_PARTY_NOTICES.md).

Author: **Roberto Huerta**. AI assistance: **ChatGPT research team**, credited as an assistance disclosure, not as a human author or independent scholarly reviewer. AI assistance supported analysis, engineering, writing and saved-evidence review; the author remains responsible for scholarly claims. No affiliations or credentials are asserted. Citation metadata is in [CITATION.cff](CITATION.cff).

The sponsor issued a Qualified PASS subject to the documentation corrections above and recommended merge followed by external scientific criticism. The sponsor inspected the code but did not independently rerun the tests; reported execution results remain the engineer's evidence. Formal artifact-evaluation certification has not been established.
