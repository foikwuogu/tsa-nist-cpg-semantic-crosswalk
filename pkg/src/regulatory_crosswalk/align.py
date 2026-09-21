"""Transparent semantic-similarity scoring between two statement corpora.

Deliberately uses TF-IDF cosine similarity rather than an opaque embedding
model: every score is reproducible from the two input tables alone, with no
model weights, network call, or GPU required. This is a design choice, not
an oversight — see the README's "Why TF-IDF" section. A future release may
add an optional embedding-based scorer as an alternative, not a replacement.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Thresholds:
    """Cosine-similarity cut points for the tentative alignment-type bucket.

    These are a triage aid for a human adjudicator, not a validated
    classifier — calibrate them against your own corpus's score
    distribution (see the README) rather than assuming these defaults fit.
    """

    direct: float = 0.30
    partial: float = 0.18
    related: float = 0.08


DEFAULT_THRESHOLDS = Thresholds()


def bucket_alignment_type(score: float, thresholds: Thresholds = DEFAULT_THRESHOLDS) -> str:
    """Map a cosine similarity score to a tentative alignment-type label."""
    if score >= thresholds.direct:
        return "Direct"
    if score >= thresholds.partial:
        return "Partial"
    if score >= thresholds.related:
        return "Related"
    return "No Match"


def align_corpora(
    source: pd.DataFrame,
    target: pd.DataFrame,
    *,
    source_id_col: str = "id",
    source_text_col: str = "text",
    target_id_col: str = "id",
    target_text_col: str = "text",
    target_name: str = "target",
    top_k: int = 3,
    thresholds: Thresholds = DEFAULT_THRESHOLDS,
    ngram_range: tuple = (1, 2),
) -> pd.DataFrame:
    """Score every source statement against every target statement with
    TF-IDF cosine similarity, and return the top-k candidates per source
    statement, each tagged with a tentative alignment-type bucket.

    Parameters
    ----------
    source, target : DataFrame
        Two statement tables. Each row is one atomic requirement/control/
        outcome statement.
    source_id_col, source_text_col, target_id_col, target_text_col : str
        Column names to use from each table.
    target_name : str
        A label for the target corpus, carried into the output's
        `target_corpus` column (useful when aligning a source against
        several target corpora and concatenating the results).
    top_k : int
        Number of candidate matches to keep per source statement.
    thresholds : Thresholds
        Cut points for the tentative alignment-type bucket.
    ngram_range : tuple
        Passed to scikit-learn's TfidfVectorizer.

    Returns
    -------
    DataFrame with one row per (source statement, candidate) pair:
    source_id, source_text, target_corpus, target_id, target_text, rank,
    cosine_similarity, tentative_alignment_type.
    """
    if len(source) == 0 or len(target) == 0:
        raise ValueError("source and target must both be non-empty")

    source_texts = list(source[source_text_col].astype(str))
    target_texts = list(target[target_text_col].astype(str))
    combined = source_texts + target_texts

    vec = TfidfVectorizer(stop_words="english", ngram_range=ngram_range, min_df=1)
    tfidf = vec.fit_transform(combined)
    n_source = len(source_texts)
    source_vecs = tfidf[:n_source]
    target_vecs = tfidf[n_source:]
    sims = cosine_similarity(source_vecs, target_vecs)

    top_k = min(top_k, len(target))
    rows = []
    source_reset = source.reset_index(drop=True)
    target_reset = target.reset_index(drop=True)
    for i, src_row in source_reset.iterrows():
        row_scores = sims[i]
        top_idx = row_scores.argsort()[::-1][:top_k]
        for rank, j in enumerate(top_idx, start=1):
            score = float(row_scores[j])
            tgt_row = target_reset.iloc[j]
            rows.append(
                {
                    "source_id": src_row[source_id_col],
                    "source_text": src_row[source_text_col],
                    "target_corpus": target_name,
                    "target_id": tgt_row[target_id_col],
                    "target_text": tgt_row[target_text_col],
                    "rank": rank,
                    "cosine_similarity": round(score, 4),
                    "tentative_alignment_type": bucket_alignment_type(score, thresholds),
                }
            )
    return pd.DataFrame(rows)
