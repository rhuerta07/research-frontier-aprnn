# Ten-bias diagnostic — completed 10 November 2026

**Decision: this fixed regularized calibration rule falls short of every corresponding repair on both primary fog and clean accuracy. Stop fitting; return results for sponsor review.**

## Primary results

All primary populations contain 8,900 images. Accuracy percentages below are rounded from exact counts.

| Cohort | Method | Selected correct /100 | Fog correct | Fog accuracy | Clean correct | Clean accuracy |
|---|---|---:|---:|---:|---:|---:|
| P001 | Bounded scalar | 40 | 3,623 | 40.71% | 8,501 | 95.52% |
| P001 | Ten biases | 51 | 4,446 | 49.96% | 8,227 | 92.44% |
| P001 | J0 | 100 | 5,087 | 57.16% | 8,448 | 94.92% |
| P001 | J1 | 100 | 5,277 | 59.29% | 8,421 | 94.62% |
| P002 | Bounded scalar | 38 | 3,625 | 40.73% | 8,502 | 95.53% |
| P002 | Ten biases | 53 | 4,296 | 48.27% | 8,263 | 92.84% |
| P002 | J0 | 100 | 4,736 | 53.21% | 8,327 | 93.56% |
| P002 | J1 | 100 | 5,024 | 56.45% | 8,348 | 93.80% |

Original fog/clean accuracy is 1,771/8,900 (19.90%) and 8,595/8,900 (96.57%). The ten-bias rule adds 823/671 correct fog predictions over bounded scalar calibration, with 274/239 fewer correct clean predictions. Against same-cohort repairs, its fog shortfalls are 440–831 images (4.94–9.34 pp); its clean shortfalls are 64–221 images (0.72–2.48 pp).

Calibration selected correctness is training fit, not satisfaction of APRNN's gap/gate requirements. Repair selected correctness is reported from the existing records, not fresh checkpoint inference.

## Class-level findings

| Cohort | Method | Fog classes 0,1,6,7 correct /3,668 | Fog classes 2,3,4,5,9 correct /4,356 | Fog true-8 correct /876 | Clean true-8 correct /876 |
|---|---|---:|---:|---:|---:|
| P001 | Ten biases | 1,431 | 2,694 | 321 | 616 |
| P001 | J0 | 1,621 | 2,768 | 698 | 782 |
| P001 | J1 | 1,749 | 2,891 | 637 | 727 |
| P002 | Ten biases | 1,217 | 2,831 | 248 | 599 |
| P002 | J0 | 1,224 | 2,841 | 671 | 773 |
| P002 | J1 | 1,512 | 3,049 | 463 | 745 |

The richer calibration substantially improves the four classes that the scalar barely changes (bounded scalar: 326 correct combined). Class 1 reaches 316/995 and 379/995, versus 6/995 under the bounded scalar. Thus the reviewer's hypothesis that class-specific offsets could help these classes was useful.

P002 ten-bias calibration nearly matches J0 on both non-8 groups: its total non-8 correct count is 4,048 versus 4,065. Of its 440-image aggregate fog deficit to J0, 423 concern true 8s and 17 concern non-8 classes. P001's 641-image J0 deficit comprises 377 true-8 and 264 non-8 images. These are finite-set arithmetic decompositions, not causal shares. Similar aggregate non-8 counts do not establish the same predictions: full disagreements and correct-prediction overlaps are retained.

Ten biases yield 3,291/3,191 fog corrections and 616/666 breaks relative to the original. On clean they yield 31/25 corrections and 399/357 breaks. True-8 losses and changes among other classes prevent fog gains from being described as uniform recognition improvement.

## Fixed method and convergence

The approved rule fits sum-to-zero class offsets using selected-only mean cross-entropy plus 0.01/2 times squared offset norm. It uses deterministic float64 projected gradient descent, initial offsets zero, step 100/51, projected-gradient infinity tolerance 1e-8, and a 10,000-update/60-second cap per fit. No parameter sweep, temperature, class reweighting, box constraint or clean calibration data was used.

P001 converged in 110 updates, projected gradient 9.19e-9; P002 in 133 updates, 9.51e-9. Mean offsets are within 3.4e-17 of zero. Both fitted vectors and convergence records were saved before held-out evaluation. Selected cross-entropy fell from 2.943 to 1.525 and from 3.009 to 1.536, excluding the penalty. Full vectors, losses and histograms are saved.

The successful analysis body took 0.292 seconds locally (about 0.43 seconds for the Python process including startup). Runtime: Python 3.12.14 and NumPy 2.3.5, CPU, one process with BLAS/OpenMP thread limits of one. This was saved-logit arithmetic and two calibration fits: zero model inference, APRNN repairs or licensed solver initialization. No Deepnote machine was started.

## Verification and preserved preflight failure

The uploaded NPZ exactly matches the recorded SHA-256 ef356769710266f255539755b3a035975ac37814d49a4e46ad5fe46c30659e6b and size 2,084,250 bytes.

Preflight independently reconstructed all four fixed-offset scalar outcomes: all 156 saved class/group rows match for N, original correct, scalar correct, corrections and breaks, and selected correctness matches. This reconstructs outcomes at the recorded offsets, not every candidate-selection calculation. Baseline labels/predictions match all four archived repair records; selected IDs/labels/winners match frozen evidence.

The first preflight failed before any calibration fit because the public cohort JSON has one extra final newline. The original Deepnote bytes were retrieved; their hash matches the approved cohort hash and parsed contents equal the public copy. The source was corrected to use these authenticated original bytes, and only then were the two fits run. The failed source, logs and failure record are preserved in preflight_failure_01/. No scientific rule or cohort was changed; this was not a failed fit followed by retuning.

A finite-difference synthetic gradient check had maximum error 1.78e-11. Stable log-sum-exp and gauge invariance checks passed; four invalid-input checks reject shape, label, dtype and nonfinite errors before fitting. An additional 126 saved-table accounting checks passed. These are implementation checks by the executing lead, not a new independent peer review or formal certification.

## Interpretation and stopping decision

The result is intermediate between the reviewer's illustrative scenarios: richer bias calibration improves fog accuracy substantially beyond the scalar, but does not reach the recorded repair range and preserves less aggregate clean accuracy than every corresponding repair. Under the approved decision rule, the result is negative for sufficiency of this particular regularized selected-only calibration.

Do not turn this into “all bias correction fails,” “APRNN improves representations,” or a causal fraction of APRNN's gain explained by biases. The fixed penalty and fitting loss may matter; neither was tuned, and there is no authorized sweep. Nine free directions fitted on 100 examples with only four true 8s limit interpretation.

Recommended next action: share this result and reproducibility packet with the same peer reviewer for a focused interpretation check, then decide whether to incorporate it into a separately revised manuscript. No new repairs, alternative calibration, cohort expansion or automatic manuscript/public-release changes follow from this result.

## Reproduction package

The downloadable packet includes the original NPZ, unchanged fixed public research artifact, prior scalar evidence and approved design snapshot, the source, fitted vectors, predictions, complete tables, provenance, run records and preserved preflight failure. A final package hash manifest covers actual contents. ANALYSIS_OUTPUT_HASHES.json preserves the earlier execution-time inventory; it predates log completion and final report packaging and is not the final bundle integrity manifest.

From the extracted package root:
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python ten_bias_diagnostic/run_diagnostic.py`

Reproduction reruns only the two small numerical calibration fits and overwrites derived files in that extracted copy. Keep the distributed package untouched and extract a separate copy for reproduction. Historical datasets/checkpoints/solver matrices are not included; none are required for this saved-logit diagnostic. No manuscript or public GitHub files were edited during this execution.

