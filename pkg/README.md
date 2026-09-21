# regulatory-crosswalk

[![PyPI](https://img.shields.io/pypi/v/regulatory-crosswalk.svg)](https://pypi.org/project/regulatory-crosswalk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Transparent semantic-similarity scoring, plus a human-adjudication review
queue, for mapping one regulatory or standards corpus onto another.

Built for compliance analysts, auditors, and researchers who need to
reconcile overlapping requirements across frameworks (e.g., a sector
regulator's rule vs. NIST CSF, SP 800-53, or a CIS/CPG-style baseline) and
want the reasoning behind every mapping decision to be logged, not just the
final table.

## Why TF-IDF, not an embedding model?

This package deliberately scores with TF-IDF cosine similarity rather than
a sentence-embedding model. Every score here is reproducible from the two
input CSVs alone — no model weights to pin, no GPU, no network call, and a
score you can hand-verify by eye (shared words are visible in the
`shared_terms_hint` column). This is a design trade-off, not a claim that
lexical similarity is the best possible scorer: it under-detects genuine
paraphrases (see Limitations below). Treat its output as a triage aid for a
human reviewer, not a finished classification — that's the point of the
adjudication-queue step.

## Install

```bash
pip install regulatory-crosswalk
```

## Usage

### Python API

```python
import pandas as pd
from regulatory_crosswalk import align_corpora, build_review_queue

source = pd.read_csv("my_requirements.csv")   # columns: id, text
target = pd.read_csv("their_controls.csv")     # columns: id, text

candidates = align_corpora(source, target, target_name="TargetFramework", top_k=3)
queue = build_review_queue(candidates)
queue.to_csv("adjudication_log.csv", index=False)
```

`queue` has empty `adjudicated_alignment_type`, `adjudicator`,
`adjudication_rationale`, and `adjudication_date` columns — a human
reviewer fills these in. The filled-in queue, not the raw `candidates`
table, is the citable crosswalk result.

### CLI

```bash
regcrosswalk align source.csv target.csv --target-name CSF2.0 -o candidates.csv
regcrosswalk adjudicate candidates.csv -o adjudication_log.csv
```

Run `regcrosswalk align --help` / `regcrosswalk adjudicate --help` for all
options (custom column names, thresholds, top-k, sample size).

## Worked example

This package was extracted from, and is used by, a real crosswalk between
the TSA Pipeline Security Guidelines and NIST CSF 2.0 / SP 800-53 / CISA
CPG v1.0.1 — see the parent repository's `code/` directory for the full,
real-data pipeline this library powers.

## Limitations

- TF-IDF cosine similarity is lexical, not semantic: two genuinely
  equivalent statements with no shared vocabulary will score near zero.
  Expect a non-trivial "No Match" rate driven by phrasing, not by a true
  absence of overlap — that's exactly the case for keeping a human
  adjudicator in the loop.
- The default thresholds (Direct ≥0.30, Partial ≥0.18, Related ≥0.08) are
  heuristic. Calibrate them against your own corpus's score distribution
  rather than assuming they transfer.
- `build_review_queue`'s default priority rule (every Direct/Partial match
  is "high," a sample of "No Match" rows is spot-checked) is a starting
  point; pass your own `priority_fn` for a different policy.

## License

MIT. See `LICENSE`.

## Citing

If you use this package in published work, please cite it — see
`CITATION.cff` in the repository root.
