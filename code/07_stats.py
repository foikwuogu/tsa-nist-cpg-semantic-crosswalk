"""Write paper/stats.json — every number the manuscript quotes is
interpolated from this file, never typed by hand into prose."""
import json
import os

import pandas as pd

PROC = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
PAPER = os.path.join(os.path.dirname(__file__), "..", "paper")
os.makedirs(PAPER, exist_ok=True)


def main():
    tsa = pd.read_csv(os.path.join(PROC, "statements_tsa.csv"))
    csf = pd.read_csv(os.path.join(PROC, "statements_csf.csv"))
    sp = pd.read_csv(os.path.join(PROC, "statements_sp80053.csv"))
    cpg = pd.read_csv(os.path.join(PROC, "statements_cpg.csv"))
    cand = pd.read_csv(os.path.join(PROC, "candidate_crosswalk.csv"))
    adj = pd.read_csv(os.path.join(PROC, "adjudication_log.csv"))

    rank1 = cand[cand["rank"] == 1]
    by_corpus = {}
    for corpus in ["CSF2.0", "SP800-53", "CPG1.0.1"]:
        sub = rank1[rank1["target_corpus"] == corpus]
        counts = sub["tentative_alignment_type"].value_counts().to_dict()
        by_corpus[corpus] = {
            "n_tsa_statements": int(len(sub)),
            "direct": int(counts.get("Direct", 0)),
            "partial": int(counts.get("Partial", 0)),
            "related": int(counts.get("Related", 0)),
            "no_match": int(counts.get("No Match", 0)),
            "mean_cosine_similarity": round(float(sub["cosine_similarity"].mean()), 4),
            "max_cosine_similarity": round(float(sub["cosine_similarity"].max()), 4),
        }

    stats = {
        "generated_by": "code/07_stats.py",
        "n_tsa_statements": int(len(tsa)),
        "n_csf_subcategories": int(len(csf)),
        "n_sp80053_base_controls": int(len(sp)),
        "n_cpg_subgoals": int(len(cpg)),
        "n_candidate_crosswalk_rows": int(len(cand)),
        "top_k_candidates_per_pair": int(cand["rank"].max()),
        "n_adjudication_queue_rows": int(len(adj)),
        "adjudication_queue_by_priority": adj["review_priority"].value_counts().to_dict(),
        "alignment_by_corpus": by_corpus,
        "thresholds": {"direct": 0.30, "partial": 0.18, "related": 0.08},
        "overall_rank1_no_match_rate": round(
            float((rank1["tentative_alignment_type"] == "No Match").mean()), 4
        ),
        "overall_rank1_any_candidate_rate": round(
            float((rank1["tentative_alignment_type"] != "No Match").mean()), 4
        ),
    }

    with open(os.path.join(PAPER, "stats.json"), "w") as f:
        json.dump(stats, f, indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
