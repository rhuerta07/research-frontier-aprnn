> Historical v2r5 preparation handoff. The current manuscript is [v2r6](../paper/integrated_manuscript_v2r6.md); see the [documentation closeout](v2r6_documentation_closeout.md) for the required corrections and current merge-approval boundary. The evidence gaps below remain disclosed, rather than being presented as recovered.

# Preprint v2r5 release handoff — 11 November 2026 UTC

**Decision: ready for a focused draft PR; keep unmerged pending research-lead review.** This is a release of available evidence, with explicit gaps. It is not complete public numerical reproducibility or publication certification. The research lead owns manuscript interpretation and editing.

## Frozen scope and provenance

Base/v1 commit: `37d81655fca7857032360e8df831c284c51dfe93`. Existing v1 manuscript, evidence manifest, analysis and 16 tests are unchanged. Current manuscript is [v2r5](../paper/integrated_manuscript_v2r5.md), copied verbatim from Deepnote `papers/RESEARCH_FRONTIER_INTEGRATED_APRNN_MANUSCRIPT_v2r5_COPYEDITED_2026_11_10.md`:

- Bytes: 38,419.
- SHA256: `807d46d609c27208aef87d904898dc78eb4fd7d997d0e7eda40bdf68b5ccbb19`.
- [New manifest](../results/v2/manifest.json) records exported source paths, byte hashes and generated release files. Original source hash records remain archival; missing original files are not reconstructed.

Only saved-record analysis and the exact previously frozen two-cohort NumPy calibration refit were used. No inference, model loading, APRNN repair, Gurobi, new cohorts or retuning. One detached read-only Deepnote run exported four existing files as bytes to avoid connector text normalization; it completed successfully. Terminal readback: detached export run `2ab3078b-5d5a-4a8c-8bd3-b63039eac983` succeeded; main project machine `stopped` on 11 November UTC. Detached execution had no persistent interactive session.

## Verification performed

Python 3.12.14; optional NumPy 2.3.5 (already available). Commands from repository root:

```sh
python -S analysis/reproduce_v2.py
python -m unittest discover -s tests -v
python analysis/reproduce_v2.py --logits /PRIVATE/PATH/ORIGINAL_LOGITS.npz --refit-ten-bias
```

The private path above is a placeholder; no automatic download is provided. The first command proves the public path has no site-package requirement. The suite passes 25 tests: the unchanged 16 v1 tests plus 9 targeted v2 tests. Public checks reconstruct class/group outcomes, prediction-collapse transitions and J0/J1 disagreements from existing per-image predictions; validate 246 saved class rows and partitions; check frozen fits, gauge and penalty convention; verify release hashes. Archived confidence intervals, mathematical derivations and bibliographic assertions are not independently re-established by this script.

Private-logit verification first checks the NPZ byte hash, exact schema, finite float64 logits, all indices/labels, original argmax against all four archived baseline records, and selected cohort identities. It reproduces every selected scalar candidate error and D1 choice, all 246 class rows, all recorded scalar paired agreements/count differences and all ten-bias paired comparison integer fields. It does not evaluate unavailable reviewer vectors or recreate the later retrospective enumeration/search record.

| Frozen selected-only calibration | Selected correct / 100 | Fog correct / 8,900 | Clean correct / 8,900 |
|---|---:|---:|---:|
| P001 scalar bounded, τ=2.949566729136976 | 40 | 3,623 | 8,501 |
| P001 scalar unrestricted, τ=3.565288818344169 | 43 | 3,529 | 8,458 |
| P002 scalar bounded, τ=2.927489965949844 | 38 | 3,625 | 8,502 |
| P002 scalar unrestricted, τ=3.585779341447035 | 41 | 3,522 | 8,457 |
| P001 ten-bias, λ=0.01 | 51 | 4,446 | 8,227 |
| P002 ten-bias, λ=0.01 | 53 | 4,296 | 8,263 |

The optional refit imports only numerical functions from the archived original source (never its nonportable `run()` entrypoint). It uses the original zero start, sum-zero projection, step 100/51, λ/2 penalty, 1e-8 gradient threshold and update/time caps. Refits match saved offsets within declared `rtol=atol=1e-10`, selected counts and 110/133 updates. This checks repeatability of shared code, not implementation independence, mathematical optimality or the trajectory of a different reviewer search.

## Failures preserved and corrected

1. Initial wrapper assumed frozen fits were at the JSON root; actual schema nests them under `fits`. It raised `KeyError: 'P001'` before numerical replay. Corrected lookup; repeat passed.
2. Initial scalar agreement check incorrectly restricted `clean_full` to primary indices. It failed `paired scalar agreement`; corrected population selection to use 0–9999 for full clean. Repeat passed.
3. UTF-8 file transport normalized CRLF in two ten-bias CSVs. Detected original byte-hash disagreement, exported exact bytes, and verified against archived hashes before inclusion.
4. Original ten-bias preflight failure and provenance correction are preserved verbatim in the evidence directory. Its original failed source/log files and `PREDICTIONS.json` appear in the archival hash list but were not recovered; no replacement is labeled an original.

## Missing companion records — recovery manifest

The user confirmed these records cannot currently be identified as individual Deepnote files. Possible original container: `RP001_manuscript_v2r3_reviewer_packet_2026_11_10.zip` (availability unconfirmed). Exact original internal filenames and hashes are unknown; recover them from the original packet rather than inventing names.

| Required original material | Manuscript claims affected | Current verification status |
|---|---|---|
| Twelve full-precision reviewer bias vectors and supplied script/JSON, with source/permission | Later reviewer-vector scores and comparisons | Manuscript reports only; underlying vectors unavailable. No rounded-value reconstruction. |
| Original direct-score and scalar-sweep verification record, including enumeration/ties and input hashes | Later direct-score confirmations; 15,386-candidate retrospective scalar maximum (3,626 fog correct), endpoints/ties | Not independently verified in this release. Selected-only calibration is distinct and does not support these retrospective claims. |
| Original bibliographic source-check record | Reported source/metadata validation | No companion verification evidence available; citations retained verbatim. |

The manuscript's statements that these artifacts accompany the revision are not fulfilled by this PR. This discrepancy is explicitly disclosed without editing the authoritative manuscript. Recover artifacts and obtain appropriate redistribution permission before representing the public package as supporting these claims. Direct scoring, even if later recovered, would not reproduce a search trajectory.

## Rights and remaining limitations

[Rights assessment](v2_rights_and_provenance.md): NPZ remains private. Its inclusion is blocked on redistribution clearance, not on engineering. Derived tables, cleared manuscript, original analysis/tests and provenance are included. Draft PR branches are public; draft status is not privacy protection.

Two cohorts, shared code/model assumptions, solver tolerances and possible multiple optima remain limitations. Finite saved-image numerical agreement is not formal verification or end-to-end checkpoint replay. Calibrations do not satisfy all selected APRNN constraints. Neither scalar failure nor the larger repair outcomes establishes a representation-level mechanism or excludes richer bias adjustments.

Next action: research lead reviews this PR and the missing-evidence list; recover the original reviewer packet and settle binary/reviewer redistribution before any merge or public-release claim of full reproducibility. No new experiments are needed to resolve these release gaps.

## Release hygiene

All changed Markdown relative links resolve. Targeted credential/private-key patterns matched neither changed files nor historical Git blobs; these scans are not a guarantee against every secret format. No NPZ, weights, images or private notebook URLs are added. Manuscript hash and unchanged v1 files were rechecked. Original diagnostic output-hash lists retain historical filenames, including missing records; the fresh manifest lists only files actually supplied.
