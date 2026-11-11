# v2 rights and provenance assessment

## Release boundary

The user authorizes publication of the cleared manuscript, derived summaries, original analysis/tests and provenance records. `ORIGINAL_LOGITS.npz` and reviewer-owned scripts/vectors are excluded. No dataset images, model weights, upstream implementations, modified APRNN workers, credentials or private notebook links are added. Historical filesystem paths in provenance identify sources; readers do not need Deepnote access for public saved-record checks.

## Withheld original logits

- SHA256: `ef356769710266f255539755b3a035975ac37814d49a4e46ad5fe46c30659e6b`.
- Bytes: 2,084,250.
- Source: Deepnote `experiments/publication_assessment/class8_scalar_diagnostic_2026_11_10/ORIGINAL_LOGITS.npz`.
- Contents: 10,000 original float64 ten-class logits per fog/identity domain, labels, indices, original predictions, and two selected index arrays. No image pixels, model weights or object/pickle arrays. See the included baseline provenance for recorded model/data hashes and preprocessing; this release did not rerun that preprocessing or infer from the model.
- Private verification authenticates these bytes and checks predictions/labels against public records. It does not independently attest the initial forward evaluation or reacquire/hash the original image and weight files.

## Applicable notices and conclusion

The repository's existing MIT grant covers original `analysis/` and `tests/` code; original documentation/manuscript use CC BY 4.0. The two archived source files under `results/v2/sources/` are original Research Frontier diagnostic code, also under MIT (see LICENSE); they are not upstream APRNN implementations. Existing evidence licenses do not grant underlying third-party rights.

APRNN upstream commit `5f676a574cf418e10e458ac36b34d9f2f6417504` has a CC BY-NC-ND 4.0 root license, which does not authorize sharing adapted material. That alone does not establish that numerical outputs are adapted material, nor does it clear output redistribution. The inspected google-research/mnist-c repository root has an Apache 2.0 notice, but that alone does not establish the rights for every downloaded MNIST/MNIST-C asset or pretrained weight. No model-specific permission or explicit generated-logit redistribution clearance was established from the available records. Reviewer-source permission is separately unresolved.

**Conclusion: the NPZ cannot presently be marked cleared for public release under the existing arrangements.** The specific remaining task is to identify the licenses/terms attached to the actual model weights and dataset assets referenced by the recorded hashes, and obtain or document permission applicable to distribution of their generated logits/labels. Recover and authorize reviewer-owned material separately. This blocks full public numerical replay, not the focused draft PR. No legal conclusion that output distribution is prohibited is asserted.
