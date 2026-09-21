# Limitations

Written before the manuscript's discussion section, so the discussion
cannot outrun what is actually true of the data.

1. **SP 800-53 corpus is a curated subset, not the full catalog.** NIST SP
   800-53 Rev 5 has roughly 1,000 controls and enhancements across 20
   families. This build uses 54 base controls (no enhancements) across 18
   families, chosen for relevance to OT/ICS and physical-security
   crosswalks. Every row in `statements_sp80053.csv` is flagged `VERIFY`
   because the full catalog JSON was too large to re-fetch and verify
   verbatim in this build session; statement text reproduces the standard,
   widely-published catalog wording but has not been re-diffed against the
   primary PDF line by line. **Action for the author before release:**
   spot-check at least 10 of the 54 controls against
   https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final.

2. **CSF 2.0 subcategory count needs confirmation.** The extraction
   returned 106 subcategories; published counts for CSF 2.0 vary slightly
   (~106–113) depending on whether withdrawn/renumbered items from errata
   are counted. Confirm the exact figure before citing it as a precise "n"
   in the manuscript — use a range or the source-cited figure if unsure.

3. **TSA "policy" corpus is the public Guidelines, not the enforceable
   Security Directives.** The TSA Security Directive Pipeline-2021-01/02
   series (the binding directives referenced in the project title) are
   largely posted as Sensitive-Security-Information-redacted PDFs; full
   directive text is not reliably public. This build uses the fully public,
   unclassified "Pipeline Security Guidelines" (2018/2021) as the TSA
   policy-language corpus. This is a defensible and commonly used public
   proxy, but it is *not* the same document as the enforceable Security
   Directives, and the manuscript must say so explicitly rather than imply
   directive-level authority.

4. **TF-IDF cosine similarity is a lexical method, not a semantic embedding.**
   It scores shared vocabulary (with bigrams), not paraphrase or conceptual
   equivalence. Two genuinely equivalent requirements phrased with no shared
   words will score near zero and land in "No Match." This is the single
   biggest driver of the ~66% rank-1 "No Match" rate reported in
   `qa_report.txt` — it is a real limitation of the scoring method, not
   evidence that two-thirds of TSA requirements truly lack any NIST/CPG
   counterpart. The manuscript should report this rate as a property of the
   *method*, and frame the adjudication log's role as partly compensating
   for it (a human reviewer can recognize a paraphrase the scorer misses)
   — future work (see NEXT_STEPS.md) should re-run scoring with a sentence-
   embedding model to quantify how much of the "No Match" rate is a lexical
   artifact.

5. **Similarity-bucket thresholds (Direct ≥0.30, Partial ≥0.18, Related
   ≥0.08) are heuristic**, calibrated against this corpus's empirical score
   distribution (see BUILD_SPEC.md), not against an external ground truth.
   They should be treated as a triage aid for the human adjudicator, not as
   a validated classifier. The adjudication log's `adjudicated_alignment_type`
   — the human's final call — is the number that should be cited as the
   project's actual crosswalk result, not `tentative_alignment_type`.

6. **No independent inter-rater reliability statistic in this release.**
   The adjudication log as shipped has one adjudicator field per row. If a
   second reviewer adjudicates a sample independently, a kappa/agreement
   statistic could be added in a future version (see NEXT_STEPS.md) and
   would meaningfully strengthen a "validation study" framing of this work.

7. **Top-3 candidates per pair may miss the correct match.** For a small
   number of TSA statements the true best NIST/CPG match may rank 4th or
   lower and never reach the adjudication log. The QA report's spot checks
   are a partial mitigation, not a guarantee.

8. **Single-author-team construction.** The crosswalk and initial scoring
   were built in one working session by the author with AI assistance
   (Claude, Anthropic) for code, data wrangling, and drafting mechanics, as
   disclosed in the manuscript. The author made the analytic decisions
   (thresholds, corpus scope, alignment-type taxonomy) and is responsible
   for verifying every adjudicated row before release, per
   `docs/VERIFY_CHECKLIST.md`.
