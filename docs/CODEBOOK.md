# Codebook

## `data/processed/statements_tsa.csv`
| Column | Definition | Source / transformation |
|---|---|---|
| id | Unique statement ID, `TSA-###` | assigned sequentially by 02_extract.py in document order |
| section | Section/table identifier from the source guideline (e.g. `4.2`, `T2` = Table 2, `AppB` = Appendix B) | as printed in the source PDF |
| text | Atomic requirement/recommendation statement, one bullet per row | verbatim/near-verbatim extraction, see PROVENANCE.txt |

## `data/processed/statements_csf.csv`
| Column | Definition | Source / transformation |
|---|---|---|
| id | Unique statement ID, `CSF-###` | assigned sequentially |
| subcat_id | Official CSF 2.0 subcategory ID, e.g. `GV.OC-01` | NIST CSWP.29 |
| category | CSF 2.0 category name | NIST CSWP.29 |
| function | CSF 2.0 function (GOVERN/IDENTIFY/PROTECT/DETECT/RESPOND/RECOVER) | NIST CSWP.29 |
| text | Subcategory outcome text | NIST CSWP.29, verbatim |

## `data/processed/statements_sp80053.csv`
| Column | Definition | Source / transformation |
|---|---|---|
| id | Unique statement ID, `SP-###` | assigned sequentially |
| control_id | Official control ID, e.g. `AC-2` (base controls only, no enhancements) | NIST SP 800-53 Rev 5.2.0 OSCAL catalog |
| family | Control family name | NIST SP 800-53 Rev 5.2.0 |
| title | Control title | NIST SP 800-53 Rev 5.2.0 |
| text | Control statement (curated subset — **[VERIFY]** every row against the source before external release) | see LIMITATIONS.md §1 |
| verify_flag | Always `VERIFY` in this release | flags every SP 800-53 row for the author's verbatim check |

## `data/processed/statements_cpg.csv`
| Column | Definition | Source / transformation |
|---|---|---|
| id | Unique statement ID, `CPG-###` | assigned sequentially |
| cpg_id | Official CPG ID, e.g. `2.K` | CISA CPG v1.0.1 |
| title | CPG short title | CISA CPG v1.0.1 |
| text | CPG outcome/description | CISA CPG v1.0.1 |

## `data/processed/candidate_crosswalk.csv`
| Column | Definition | Source / transformation |
|---|---|---|
| candidate_id | Unique row ID, `CAND-#####` | assigned sequentially |
| tsa_id / tsa_section / tsa_text | The TSA statement being matched | copied from statements_tsa.csv |
| target_corpus | Which target corpus this candidate is from: `CSF2.0`, `SP800-53`, `CPG1.0.1` | 03_align.py |
| target_id / target_text | The candidate match's ID and text in the target corpus | copied from the relevant statements_*.csv |
| rank | 1 = best match, 2 = second-best, 3 = third-best (top-3 kept per TSA statement per corpus) | 03_align.py |
| cosine_similarity | TF-IDF (unigram+bigram, English stopwords removed) cosine similarity, range [0,1] | scikit-learn `TfidfVectorizer` + `cosine_similarity` |
| tentative_alignment_type | DRAFT rule-based bucket from cosine_similarity: Direct (≥0.30) / Partial (≥0.18) / Related (≥0.08) / No Match | 03_align.py; thresholds documented and challengeable, see BUILD_SPEC.md |

## `data/processed/adjudication_log.csv`
| Column | Definition | Source / transformation |
|---|---|---|
| adjudication_id | Unique row ID, `ADJ-####` | assigned sequentially |
| review_priority | `high` (Direct/Partial — confirm every one), `medium` (Related, score ≥0.10), `low` (Related <0.10, or a random 15-row spot-check sample of confident No Match rows) | 04_adjudication.py |
| tsa_id / tsa_section / tsa_text | The TSA statement under review | copied from candidate_crosswalk.csv (rank 1 only) |
| target_corpus / target_id / target_text | The rank-1 candidate match | copied from candidate_crosswalk.csv |
| cosine_similarity / tentative_alignment_type | The machine's score and DRAFT bucket | copied from candidate_crosswalk.csv |
| shared_terms_hint | Up to 4 non-stopword terms (>3 chars) shared between the two statements — a reading aid for the reviewer, not a decision | 04_adjudication.py |
| adjudicated_alignment_type | **[VERIFY]** — the human adjudicator's final call: Direct / Partial / Related / No Match / Reject | filled in by the author during Step 5 verification |
| adjudicator | **[VERIFY]** — name of the person who made the call | filled in by the author |
| adjudication_rationale | **[VERIFY]** — one to two sentences on why | filled in by the author |
| adjudication_date | **[VERIFY]** — ISO date of the decision | filled in by the author |
