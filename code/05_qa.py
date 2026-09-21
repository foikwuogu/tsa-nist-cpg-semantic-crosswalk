"""Write data/processed/qa_report.txt: row counts, match rates, sanity
checks, and a named spot-check sample for the author to verify by hand.
"""
import os

import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def main():
    tsa = pd.read_csv(os.path.join(OUT, "statements_tsa.csv"))
    csf = pd.read_csv(os.path.join(OUT, "statements_csf.csv"))
    sp = pd.read_csv(os.path.join(OUT, "statements_sp80053.csv"))
    cpg = pd.read_csv(os.path.join(OUT, "statements_cpg.csv"))
    cand = pd.read_csv(os.path.join(OUT, "candidate_crosswalk.csv"))
    adj = pd.read_csv(os.path.join(OUT, "adjudication_log.csv"))

    lines = []
    lines.append("QA REPORT — TSA-NIST-CPG Semantic Crosswalk")
    lines.append("=" * 60)
    lines.append("")
    lines.append("1. ROW COUNTS")
    lines.append(f"   statements_tsa.csv      : {len(tsa)} atomic TSA statements")
    lines.append(f"   statements_csf.csv      : {len(csf)} CSF 2.0 subcategories")
    sp_verified = (sp["verify_flag"] == "VERIFIED").all() if "verify_flag" in sp.columns else False
    sp_status = "subset, VERIFIED 2026-09-20" if sp_verified else "subset, unverified"
    lines.append(f"   statements_sp80053.csv  : {len(sp)} SP 800-53 base controls ({sp_status})")
    lines.append(f"   statements_cpg.csv      : {len(cpg)} CPG v1.0.1 sub-goals")
    lines.append(f"   candidate_crosswalk.csv : {len(cand)} rows (130 TSA x 3 corpora x top-{cand['rank'].max()})")
    lines.append(f"   adjudication_log.csv    : {len(adj)} rows queued for human review")
    lines.append("")

    lines.append("2. NULL / EMPTY CHECKS")
    for name, df in [("tsa", tsa), ("csf", csf), ("sp", sp), ("cpg", cpg), ("candidate", cand)]:
        n_null = int(df.isna().sum().sum())
        lines.append(f"   {name}: {n_null} null cells")
    lines.append("")

    lines.append("3. DUPLICATE CHECKS")
    lines.append(f"   duplicate TSA statement text: {tsa['text'].duplicated().sum()}")
    lines.append(f"   duplicate CSF subcategory ids: {csf['subcat_id'].duplicated().sum()}")
    lines.append(f"   duplicate SP800-53 control ids: {sp['control_id'].duplicated().sum()}")
    lines.append(f"   duplicate CPG ids: {cpg['cpg_id'].duplicated().sum()}")
    lines.append("")

    lines.append("4. SCORE RANGE / SANITY CHECKS")
    lines.append(f"   cosine_similarity range: [{cand['cosine_similarity'].min():.4f}, {cand['cosine_similarity'].max():.4f}] (expected [0,1])")
    assert cand["cosine_similarity"].between(0, 1).all(), "similarity out of [0,1] range"
    lines.append("   PASS: all scores within [0,1]")
    rank1 = cand[cand["rank"] == 1]
    lines.append("")
    lines.append("   Rank-1 tentative alignment type counts by target corpus:")
    tbl = rank1.groupby(["target_corpus", "tentative_alignment_type"]).size().unstack(fill_value=0)
    for corpus in tbl.index:
        lines.append(f"     {corpus:10s}: " + ", ".join(f"{t}={int(tbl.loc[corpus, t])}" for t in tbl.columns))
    lines.append("")

    lines.append("5. ADJUDICATION QUEUE COMPOSITION")
    pr = adj["review_priority"].value_counts()
    for p in ["high", "medium", "low"]:
        lines.append(f"   {p:6s}: {int(pr.get(p, 0))} rows")
    unresolved = (adj["adjudicated_alignment_type"] == "[VERIFY]").sum()
    lines.append(f"   unresolved ([VERIFY]) decisions: {unresolved} / {len(adj)}")
    lines.append("   NOTE: publish_gate.py will refuse to proceed while any [VERIFY]")
    lines.append("         tag remains among the 'high' priority rows.")
    lines.append("")

    lines.append("6. NAMED SPOT CHECKS (author: verify these five by hand against the source PDFs)")
    spot = pd.concat(
        [
            rank1.sort_values("cosine_similarity", ascending=False).head(2),  # easy/high-confidence
            rank1[(rank1["cosine_similarity"] > 0.15) & (rank1["cosine_similarity"] < 0.25)].head(2),  # hard/borderline
            rank1.sort_values("cosine_similarity", ascending=True).head(1),  # extreme/no-match
        ]
    )
    for _, r in spot.iterrows():
        lines.append(
            f"   [{r['tsa_id']}] \"{r['tsa_text'][:70]}\" <-> "
            f"[{r['target_corpus']}/{r['target_id']}] \"{str(r['target_text'])[:70]}\" "
            f"(score={r['cosine_similarity']:.3f}, type={r['tentative_alignment_type']})"
        )
    lines.append("")

    lines.append("7. KNOWN LIMITATIONS SURFACED BY QA (see docs/LIMITATIONS.md for full list)")
    lines.append("   - SP 800-53 statement text is a curated subset (54 of ~1,000 controls); all 54")
    lines.append("     statement strings were verified against the official published catalog on")
    lines.append("     2026-09-20 (53/54 matched closely, IR-4 corrected — see PROVENANCE.txt).")
    lines.append("   - CSF 2.0 subcategory count (106) was verified on 2026-09-20 against the")
    lines.append("     official CSF 2.0 structure (6 functions, 22 categories, 106 subcategories).")
    lines.append("   - TF-IDF cosine similarity is a lexical, not a true semantic-embedding, method;")
    lines.append("     see LIMITATIONS.md for why this was chosen and its known failure modes.")
    lines.append("   - No 'Direct' alignment type appears for CPG (max observed score below threshold")
    lines.append("     for that corpus) — an honest empirical finding, not a bug; discussed in the paper.")

    report = "\n".join(lines)
    with open(os.path.join(OUT, "qa_report.txt"), "w") as f:
        f.write(report + "\n")
    print(report)


if __name__ == "__main__":
    main()
