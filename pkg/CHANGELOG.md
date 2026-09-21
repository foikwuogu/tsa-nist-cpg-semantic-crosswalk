# Changelog

## 0.1.0 — 2026-09-20

Initial release.

- `align_corpora()`: TF-IDF cosine similarity scoring between two statement
  corpora, top-k candidates with tentative alignment-type buckets.
- `build_review_queue()`: prioritized human-adjudication review queue with
  empty verification fields.
- `regcrosswalk` CLI: `align` and `adjudicate` subcommands.
- 11 unit tests (fixtures-based, no network or external services required).
- Extracted from, and used by, the TSA/NIST CSF 2.0/SP 800-53/CISA CPG
  crosswalk in the parent repository.
