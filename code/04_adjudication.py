"""Build the human-adjudication log: the rank-1 candidate match for every
TSA statement against each target corpus, prioritized for review, with
empty fields for the author's final decision.

This is the artifact the skill's verification gate cares about: nothing
here is a finished crosswalow decision until a human fills in
`adjudicated_alignment_type`, `adjudicator`, and `adjudication_date`.
"""
import os
import re

import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

STOPWORDS = set(
    "a an the and or of to for in on with by is are be as at from into "
    "that this these those their its it not no shall should must may".split()
)


def shared_terms(a, b, k=4):
    wa = {w.lower().strip(".,;:()") for w in a.split() if w.lower() not in STOPWORDS and len(w) > 3}
    wb = {w.lower().strip(".,;:()") for w in b.split() if w.lower() not in STOPWORDS and len(w) > 3}
    shared = sorted(wa & wb)
    return ", ".join(shared[:k]) if shared else ""


def review_priority(row):
    t = row["tentative_alignment_type"]
    s = row["cosine_similarity"]
    if t == "Direct":
        return "high"  # rare — confirm every one
    if t == "Partial":
        return "high"  # the boundary cases that most need a human call
    if t == "Related" and s >= 0.10:
        return "medium"
    if t == "Related":
        return "low"
    return "low"  # confident No Match — spot-check only


def main():
    cand = pd.read_csv(os.path.join(OUT, "candidate_crosswalk.csv"))
    rank1 = cand[cand["rank"] == 1].copy()

    rank1["shared_terms_hint"] = rank1.apply(
        lambda r: shared_terms(str(r["tsa_text"]), str(r["target_text"])), axis=1
    )
    rank1["review_priority"] = rank1.apply(review_priority, axis=1)

    # Reviewable queue = everything except confident No Match, plus a random
    # spot-check sample of No Match rows for the QA report.
    reviewable = rank1[rank1["tentative_alignment_type"] != "No Match"].copy()
    no_match_sample = rank1[rank1["tentative_alignment_type"] == "No Match"].sample(
        n=min(15, (rank1["tentative_alignment_type"] == "No Match").sum()), random_state=42
    )
    queue = pd.concat([reviewable, no_match_sample], ignore_index=True)
    queue = queue.sort_values(
        ["review_priority", "cosine_similarity"], ascending=[True, False]
    ).reset_index(drop=True)

    priority_rank = {"high": 0, "medium": 1, "low": 2}
    queue = queue.sort_values(
        by="review_priority", key=lambda s: s.map(priority_rank)
    ).reset_index(drop=True)

    queue.insert(0, "adjudication_id", [f"ADJ-{i+1:04d}" for i in range(len(queue))])

    # Human-adjudication fields — explicitly marked PENDING_REVIEW until the
    # author (subject-matter expert) reviews. The publish gate will refuse
    # to proceed while these remain unresolved for high-priority rows.
    queue["adjudicated_alignment_type"] = "PENDING_REVIEW"
    queue["adjudicator"] = "PENDING_REVIEW"
    queue["adjudication_rationale"] = "PENDING_REVIEW"
    queue["adjudication_date"] = "PENDING_REVIEW"

    cols = [
        "adjudication_id",
        "review_priority",
        "tsa_id",
        "tsa_section",
        "tsa_text",
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
    queue = queue[cols]
    queue.to_csv(os.path.join(OUT, "adjudication_log.csv"), index=False)

    n_high = (queue["review_priority"] == "high").sum()
    n_med = (queue["review_priority"] == "medium").sum()
    n_low = (queue["review_priority"] == "low").sum()
    print(f"wrote adjudication_log.csv ({len(queue)} rows: high={n_high} medium={n_med} low={n_low})")


if __name__ == "__main__":
    main()
