# TSA Pipeline Policy-to-Control Crosswalk & Human-Adjudicated Semantic Alignment Framework

**Status: DRAFT — pending author verification (see `docs/VERIFY_CHECKLIST.md`). Not yet released.**
Version: 0.1.0-draft · Last updated: 2026-09-20

## What this is

A reproducible framework — and a worked, real dataset — for mapping TSA
pipeline security requirements onto NIST CSF 2.0, NIST SP 800-53 Rev 5, and
CISA's Cross-Sector Cybersecurity Performance Goals (CPGs), using a
transparent semantic-similarity scoring pass followed by a structured,
loggable human adjudication step. The crosswalk is real (built from the
actual public texts, not synthetic data); the adjudication log ships as a
review queue with the machine's tentative call and empty fields for the
human adjudicator's final decision and rationale — that queue, filled in,
*is* the adjudication log this project's evidence claim rests on.

## Why

Compliance analysts, auditors, and researchers routinely need to know how
one regulator's requirement maps onto another framework's controls. That
mapping is usually done ad hoc, by one person, with no record of the
reasoning. This project makes the process itself the artifact: every
candidate match is scored, every human decision is logged with a rationale,
and the whole thing reruns from the committed scripts.

## Dashboard

`site/dashboard.html` is a self-contained, browser-viewable dashboard (no
server needed — open the file directly) with the score charts and a
filterable/sortable view of the full adjudication review queue. Rebuild it
after re-running the pipeline with:

```bash
python3 - <<'PY'
import json
tpl = open("site/template.html").read()
stats = open("paper/stats.json").read()
import csv, io
with open("data/processed/adjudication_log.csv") as f:
    rows = list(csv.DictReader(f))
    for r in rows:
        r["cosine_similarity"] = float(r["cosine_similarity"])
adj = json.dumps(rows)
open("site/dashboard.html", "w").write(tpl.replace("__STATS_JSON__", stats).replace("__ADJUDICATION_JSON__", adj))
PY
```

## Installable package

The TF-IDF alignment scorer and adjudication-queue builder are also
packaged as a standalone, installable library — `pkg/` (PyPI name
`regulatory-crosswalk`) — for anyone who wants to run this same method on
their own two corpora, not just reproduce this TSA/NIST/CPG dataset:

```bash
pip install regulatory-crosswalk   # once published — see docs/PUBLISH_GUIDE.md
regcrosswalk align mine.csv theirs.csv --target-name TheirFramework -o candidates.csv
regcrosswalk adjudicate candidates.csv -o adjudication_log.csv
```

See `pkg/README.md` for the Python API and `pkg/tests/` for its test suite
(11 tests, all passing, no network required).

## Repository layout

```
BUILD_SPEC.md              the one-page spec this build follows
AUTHORS.json               canonical author list (drives README/CITATION/paper)
pkg/                        installable `regulatory-crosswalk` package (PyPI), CLI + tests
code/
  02_extract.py             raw source text -> atomic statement tables
  03_align.py               TF-IDF cosine similarity -> candidate crosswalk
  04_adjudication.py        candidate crosswalk -> human review queue
  05_qa.py                  QA report
  06_figures.py             manuscript figures (--final removes DRAFT stamp)
  07_stats.py               paper/stats.json (every number the paper quotes)
  provenance.py             fetch-record logger
data/
  raw/                      source captures + PROVENANCE.txt
  processed/                statement tables, candidate_crosswalk.csv,
                             adjudication_log.csv, qa_report.txt
docs/
  CODEBOOK.md  LIMITATIONS.md  VERIFY_CHECKLIST.md  NEXT_STEPS.md
paper/
  stats.json  figures/  manuscript.docx
```

## How to run it

```bash
pip install pandas scikit-learn matplotlib
python3 code/02_extract.py
python3 code/03_align.py
python3 code/04_adjudication.py
python3 code/05_qa.py
python3 code/06_figures.py        # add --final once verified, to drop the DRAFT stamp
python3 code/07_stats.py
```

Each script is idempotent and can be rerun on its own; run them in order the
first time. `data/processed/qa_report.txt` is written last-updated and
should be read before trusting anything downstream of it.

## Sources (see `data/raw/PROVENANCE.txt` for hashes and access dates)

| Source | Version | URL |
|---|---|---|
| TSA Pipeline Security Guidelines | Mar 2018, Change 1 Apr 2021 | tsa.gov/sites/default/files/pipeline_security_guidelines.pdf |
| NIST Cybersecurity Framework (CSF) 2.0 | CSWP.29, Feb 2024 | doi.org/10.6028/NIST.CSWP.29 |
| NIST SP 800-53 Rev 5 control catalog | Rev 5.2.0, base-control subset | github.com/usnistgov/oscal-content |
| CISA Cross-Sector Cybersecurity Performance Goals | v1.0.1, Mar 2023 | cisa.gov/sites/default/files/2023-03/CISA_CPG_REPORT_v1.0.1_FINAL.pdf |

All four are U.S. Government works in the public domain.

## Limitations

See `docs/LIMITATIONS.md`. Headline items: the SP 800-53 corpus is a curated
base-control subset (not the full ~1,000-control catalog) and every one of
its statement strings is flagged `[VERIFY]`; alignment scoring uses TF-IDF
lexical similarity, not a semantic embedding model, and this measurably
under-detects true matches that are phrased differently (see the paper's
discussion of the "No Match" rate).

## License

Code: MIT. Data, docs, and manuscript: CC BY 4.0. See `LICENSE`.

## Citation

See `CITATION.cff`. DOI pending Zenodo deposit.

## Maintainer

Friday Ogochukwu Ikwuogu (Friday.ikwuogu@gmail.com) — see `AUTHORS.json` for
the full author list and CRediT roles.
