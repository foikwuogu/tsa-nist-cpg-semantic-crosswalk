"""Turn a scored candidate table into a human-adjudication review queue.

The queue is the package's core contribution: it separates the machine's
tentative call (transparent, reproducible, but lexical and imperfect) from
the human adjudicator's final, logged, attributable decision. Nothing in
this module ever fills in the adjudication fields itself — that would
defeat the point.
"""
from __future__ import annotations

import re
from typing import Optional

import pandas as pd

_STOPWORDS = set(
    "a an the and or of to for in on with by is are be as at from into "
    "that this these those their its it not no shall should must may".split()
)


def _shared_terms(a: str, b: str, k: int = 4) -> str:
    wa = {w.lower().strip(".,;:()") for w in str(a).split() if w.lower() not in _STOPWORDS and len(w) > 3}
    wb = {w.lower().strip(".,;:()") for w in str(b).split() if w.lower() not in _STOPWORDS and len(w) > 3}
    shared = sorted(wa & wb)
    return ", ".join(shared[:k]) if shared else ""


def _default_priority(row: pd.Series) -> str:
    t = row["tentative_alignment_type"]
    s = row["cosine_similarity"]
    if t == "Direct":
        return "high"
    if t == "Partial":
        return "high"
    if t == "Related" and s >= 0.10:
        return "medium"
    return "low"


def build_review_queue(
    candidates: pd.DataFrame,
    *,
    rank_filter: int = 1,
    no_match_sample_size: int = 15,
    random_state: int = 42,
    priority_fn=None,
) -> pd.DataFrame:
    """Build a prioritized human-adjudication review queue from a candidate
    table produced by :func:`regulatory_crosswalk.align.align_corpora`.

    Every non-"No Match" row at `rank_filter` (default: the best candidate
    per source statement) is included, plus a random sample of confident
    "No Match" rows for spot-checking. Each row gets empty
    `adjudicated_alignment_type`, `adjudicator`, `adjudication_rationale`,
    and `adjudication_date` fields for a human reviewer to fill in.

    Parameters
    ----------
    candidates : DataFrame
        Output of `align_corpora` (optionally concatenated across several
        target corpora).
    rank_filter : int
        Which rank to review (1 = the best candidate per source statement).
    no_match_sample_size : int
        How many confident "No Match" rows to sample per target corpus for
        spot-checking (0 to skip).
    priority_fn : callable, optional
        A function `(row) -> "high"|"medium"|"low"` to override the default
        priority assignment.

    Returns
    -------
    DataFrame with columns: adjudication_id, review_priority, source_id,
    source_text, target_corpus, target_id, target_text, cosine_similarity,
    tentative_alignment_type, shared_terms_hint, adjudicated_alignment_type,
    adjudicator, adjudication_rationale, adjudication_date.
    """
    priority_fn = priority_fn or _default_priority
    ranked = candidates[candidates["rank"] == rank_filter].copy()

    reviewable = ranked[ranked["tentative_alignment_type"] != "No Match"].copy()
    parts = [reviewable]
    if no_match_sample_size > 0:
        for corpus, group in ranked[ranked["tentative_alignment_type"] == "No Match"].groupby("target_corpus"):
            n = min(no_match_sample_size, len(group))
            if n > 0:
                parts.append(group.sample(n=n, random_state=random_state))
    queue = pd.concat(parts, ignore_index=True) if len(parts) > 1 else reviewable

    queue["shared_terms_hint"] = queue.apply(
        lambda r: _shared_terms(r["source_text"], r["target_text"]), axis=1
    )
    queue["review_priority"] = queue.apply(priority_fn, axis=1)

    priority_rank = {"high": 0, "medium": 1, "low": 2}
    queue = queue.sort_values(by="review_priority", key=lambda s: s.map(priority_rank)).reset_index(drop=True)
    queue.insert(0, "adjudication_id", [f"ADJ-{i + 1:04d}" for i in range(len(queue))])

    for col in ("adjudicated_alignment_type", "adjudicator", "adjudication_rationale", "adjudication_date"):
        queue[col] = "[VERIFY]"

    cols = [
        "adjudication_id",
        "review_priority",
        "source_id",
        "source_text",
        "target_corpus",
        "target_id",
        "target_text",
        "cosine_similarity",
        "tentative_alignment_type",
        "shared_terms_hint",
        "adjudicated_alignment_type",
        "adjudicator",
        "adjudication_rationale",
        "adjudication_date",
    ]
    return queue[cols]
