# Build Spec

```
PROJECT:        TSA Pipeline Policy-to-Control Crosswalk & Human-Adjudicated
                Semantic Alignment Framework (dataset + methods paper)
                Archetypes: (1) Open dataset, (6) Validation/proxy-style
                alignment study, (8) Analysis/methods paper — stacked.

QUESTION:       How do TSA pipeline cybersecurity/physical-security
                requirements map onto NIST CSF 2.0, NIST SP 800-53 Rev 5,
                and CISA's Cross-Sector Cybersecurity Performance Goals
                (CPGs) — and how reliable is a semantic-similarity-assisted,
                human-adjudicated process at producing that mapping?

SOURCES:
  - TSA Pipeline Security Guidelines (Rev., March 2018, Change 1 April 2021)
    https://www.tsa.gov/sites/default/files/pipeline_security_guidelines.pdf
    Public, unclassified. Accessed 2026-09-20.
  - CISA Cross-Sector Cybersecurity Performance Goals (CPG) v1.0.1 (Mar 2023)
    https://www.cisa.gov/sites/default/files/2023-03/CISA_CPG_REPORT_v1.0.1_FINAL.pdf
    Public domain (US Government work). Accessed 2026-09-20.
  - NIST Cybersecurity Framework (CSF) 2.0 Core, NIST CSWP.29 (Feb 2024)
    https://doi.org/10.6028/NIST.CSWP.29
    Public domain (US Government work). Accessed 2026-09-20.
  - NIST SP 800-53 Rev 5.2.0 control catalog (OSCAL electronic edition)
    https://github.com/usnistgov/oscal-content (nist.gov/SP800-53/rev5)
    Public domain (US Government work). Accessed 2026-09-20.
    NOTE: base-control subset only (see LIMITATIONS) — all 54 statement
    strings were checked verbatim against the official catalog on
    2026-09-20 by the author (see data/raw/PROVENANCE.txt for the
    one correction made, to IR-4).

UNIT:           One atomic requirement/outcome statement from any one of
                the four corpora (a TSA guideline bullet, a CPG sub-goal,
                a CSF 2.0 subcategory, or an SP 800-53 base control).

MEASURES:
  - cosine_similarity: TF-IDF cosine similarity between a TSA statement and
    every candidate statement in each target corpus (CSF, SP 800-53, CPG).
  - tentative_alignment_type: rule-based bucket from the similarity score
    (Direct / Partial / Related / No Match) — a machine-generated proposal,
    superseded by the human adjudication below.
  - adjudicated_alignment_type & rationale: the human-reviewed, final
    decision recorded in the adjudication log — completed and signed off
    by the author on 2026-09-20 for all 149 rows.

OUTPUTS:
  data/processed/statements_tsa.csv, statements_csf.csv,
    statements_sp80053.csv, statements_cpg.csv
  data/processed/candidate_crosswalk.csv       (top-k candidate matches)
  data/processed/adjudication_log.csv          (review queue + decisions)
  data/processed/qa_report.txt
  paper/stats.json, paper/figures/*.png
  paper/manuscript.docx                        (methods paper)
  docs/README.md, CODEBOOK.md, LIMITATIONS.md, VERIFY_CHECKLIST.md,
    NEXT_STEPS.md

VENUES:         GitHub repository -> Zenodo deposit (DOI) for the dataset
                and code release; preprint submission kit (TechRxiv /
                arXiv cs.CR, author's choice) prepared for personal
                submission of the methods paper.

VERIFY POINTS (all closed as of 2026-09-20 — see docs/VERIFY_CHECKLIST.md):
  1. All 149 adjudication_log.csv rows (31 high, 66 medium, 52 low
     review_priority) — confirmed or overridden by the author; 91/149
     differ from the machine's tentative alignment type, each with a
     rationale.
  2. SP 800-53 control statement text — all 54 checked verbatim against
     the source catalog; 53/54 matched, IR-4 corrected.
  3. NIST CSF 2.0 subcategory count — confirmed as 106 subcategories / 22
     categories / 6 functions against the official CSF 2.0 structure (the
     108 figure considered earlier was CSF 1.1's count, not 2.0's).
  4. Author block / co-author order for this specific project (confirmed
     with user: Ikwuogu, Mike-Ewewie, Ayozie) — matches across
     AUTHORS.json, CITATION.cff, and the manuscript header.

LICENSE:        Code: MIT. Data, docs, and manuscript: CC BY 4.0 (source
                texts are US Government public-domain works; the crosswalk
                and adjudication log are the authors' derived contribution).

ASSUMPTIONS:
  - "Human adjudication" in this build is delivered as a structured,
    reviewable log: Claude proposes tentative machine-scored alignments,
    and the author (a subject-matter expert) performs the actual
    adjudication via the VERIFY_CHECKLIST before publication — consistent
    with the skill's verification-gate design. No claim is made that
    independent human review has already occurred; that is explicitly the
    author's step 5 task.
  - TSA Security Directive text proper (SD Pipeline-2021-01/02 series) is
    largely security-sensitive/redacted in public postings; this build
    uses the fully public, unclassified "Pipeline Security Guidelines" as
    the TSA policy corpus, which is the standard public proxy used in
    prior work product referenced in the author's profile.
```
