"""Semantic alignment: score every TSA statement against every candidate
statement in each target corpus (CSF, SP 800-53, CPG) with TF-IDF cosine
similarity, then keep the top-k candidates per (TSA statement, target
corpus) pair as the DRAFT crosswalk.

This is the "AI-assisted" half of the framework: a transparent, reproducible
scoring pass. It is not the adjudication itself — 04_adjudication.py turns
the scores into a review queue for the human adjudicator.
"""
import csv
import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

TOP_K = 3

# Rule-based bucketing thresholds for the tentative alignment type.
# These are DRAFT heuristics the human adjudicator can override; they are
# documented here (not hidden in a black box) precisely so they can be
# challenged during verification. Calibrated empirically against this
# corpus's TF-IDF cosine score distribution (see qa_report.txt): short,
# differently-worded regulatory statements rarely exceed ~0.35-0.40 cosine
# similarity even for genuinely equivalent requirements, so thresholds are
# set relative to the observed distribution rather than to an arbitrary
# absolute value. [VERIFY] the author should sanity-check these cut points
# against the labeled spot-check sample in the QA report.
THRESH_DIRECT = 0.30
THRESH_PARTIAL = 0.18
THRESH_RELATED = 0.08


def bucket(score):
    if score >= THRESH_DIRECT:
        return "Direct"
    if score >= THRESH_PARTIAL:
        return "Partial"
    if score >= THRESH_RELATED:
        return "Related"
    return "No Match"


def align_corpus(tsa_df, target_df, target_name, target_id_col, target_text_col):
    corpus_texts = list(tsa_df["text"]) + list(target_df[target_text_col])
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    tfidf = vec.fit_transform(corpus_texts)
    n_tsa = len(tsa_df)
    tsa_vecs = tfidf[:n_tsa]
    target_vecs = tfidf[n_tsa:]
    sims = cosine_similarity(tsa_vecs, target_vecs)

    rows = []
    for i, tsa_row in tsa_df.reset_index(drop=True).iterrows():
        row_scores = sims[i]
        top_idx = row_scores.argsort()[::-1][:TOP_K]
        for rank, j in enumerate(top_idx, start=1):
            score = float(row_scores[j])
            target_row = target_df.iloc[j]
            rows.append(
                {
                    "tsa_id": tsa_row["id"],
                    "tsa_section": tsa_row["section"],
                    "tsa_text": tsa_row["text"],
                    "target_corpus": target_name,
                    "target_id": target_row[target_id_col],
                    "target_text": target_row[target_text_col],
                    "rank": rank,
                    "cosine_similarity": round(score, 4),
                    "tentative_alignment_type": bucket(score),
                }
            )
    return pd.DataFrame(rows)


def main():
    tsa = pd.read_csv(os.path.join(OUT, "statements_tsa.csv"))
    csf = pd.read_csv(os.path.join(OUT, "statements_csf.csv"))
    sp = pd.read_csv(os.path.join(OUT, "statements_sp80053.csv"))
    cpg = pd.read_csv(os.path.join(OUT, "statements_cpg.csv"))

    parts = [
        align_corpus(tsa, csf, "CSF2.0", "subcat_id", "text"),
        align_corpus(tsa, sp, "SP800-53", "control_id", "text"),
        align_corpus(tsa, cpg, "CPG1.0.1", "cpg_id", "text"),
    ]
    candidate = pd.concat(parts, ignore_index=True)
    candidate.insert(0, "candidate_id", [f"CAND-{i+1:05d}" for i in range(len(candidate))])
    candidate.to_csv(os.path.join(OUT, "candidate_crosswalk.csv"), index=False)
    print(f"wrote candidate_crosswalk.csv ({len(candidate)} rows)")

    # quick score distribution summary, useful for QA/stats later
    summary = candidate.groupby(["target_corpus", "tentative_alignment_type"]).size().unstack(fill_value=0)
    print(summary)


if __name__ == "__main__":
    main()
