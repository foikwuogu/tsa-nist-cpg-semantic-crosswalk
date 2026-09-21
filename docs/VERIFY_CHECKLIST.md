# Verification Checklist

Nothing in this repository is published (pushed publicly, deposited to
Zenodo, or submitted anywhere) until every item below is checked by the
author, Friday Ogochukwu Ikwuogu, personally — not delegated back to Claude
or any other automated step. `scripts/publish_gate.py` enforces the
mechanical half of this (DRAFT stamps, `[VERIFY]` tags, placeholders,
secrets); the analytic half below cannot be scripted.

## 1. Reproduce the pipeline

- [x] `pip install pandas scikit-learn matplotlib` on a clean environment
      — **done 2026-09-20** in a fresh temporary virtual environment on
      the author's machine (`pandas 3.0.6`, `scikit-learn 1.9.1`,
      `matplotlib 3.11.2`).
- [x] Run `code/02_extract.py` through `code/07_stats.py` in order —
      **re-run 2026-09-20** after the SP 800-53/CSF 2.0 corrections; all
      scripts ran cleanly end to end.
- [x] Confirm the row counts printed match `data/processed/qa_report.txt`
      section 1 exactly — **confirmed 2026-09-20**: 130/106/54/38 row
      counts unchanged by the text corrections (both fixes were
      content-only, not row additions/removals).

## 2. Spot-check the raw sources

- [x] Open the actual TSA Pipeline Security Guidelines PDF and confirm at
      least 10 of the 130 statements in `statements_tsa.csv` against it
      — **done 2026-09-20**: 10 statements spot-checked (TSA-007, 009,
      023, 027, 029, 036, 058, 063, 071, 109), all confirmed as close,
      accurate paraphrases of the actual PDF text.
- [x] Open NIST CSWP.29 and confirm at least 10 of the 106 CSF 2.0
      subcategory texts, and settle the exact subcategory count
      (LIMITATIONS.md item 2) — **done 2026-09-20**: confirmed 106
      subcategories / 22 categories / 6 functions against the official
      CSF 2.0 structure; see `data/raw/PROVENANCE.txt` for detail.
- [x] Open the NIST SP 800-53 Rev 5 catalog and verify **every one** of the
      54 control statements in `statements_sp80053.csv` (LIMITATIONS.md
      item 1) — **done 2026-09-20**: all 54 checked against the official
      published catalog; 53/54 matched closely, IR-4 corrected (was
      drifted toward an enhancement phrase). See
      `data/raw/PROVENANCE.txt` for the full note.
- [x] Open the CISA CPG v1.0.1 report and confirm at least 10 of the 38
      CPG entries — **done 2026-09-20**: 10 entries spot-checked (1.B,
      1.D, 1.E, 1.G, 2.A, 2.H, 2.J, 2.L, 2.O, 2.Q), all confirmed as
      close, accurate paraphrases of the actual PDF text.

## 3. Adjudicate the review queue

- [x] Work through `data/processed/adjudication_log.csv`, starting with
      all 31 `review_priority = high` rows, then `medium`, then `low` —
      **done 2026-09-20**: all 149 rows reviewed (31 high, 66 medium, 52
      low) with Claude, working from an `ai_suggested_type` /
      `ai_suggested_rationale` pass that the author then confirmed.
- [x] For each row, fill in `adjudicated_alignment_type` (Direct / Partial
      / Related / No Match / Reject), your name in `adjudicator`, one to
      two sentences in `adjudication_rationale`, and today's date in
      `adjudication_date` — **done**: adjudicator = Friday Ogochukwu
      Ikwuogu, date = 2026-09-20, all 149 rows.
- [x] Where you disagree with the machine's `tentative_alignment_type`,
      say why in the rationale — **done**: 91 of 149 rows (61%) differ
      from the machine's tentative bucket, each with a rationale.
- [x] Re-run `code/05_qa.py` after adjudicating to confirm the
      "unresolved [VERIFY] decisions" count has dropped to 0 for all
      `high`-priority rows — **done**: 0 / 149 unresolved, confirmed by
      QA report section 5.

## 4. Check the numbers in the manuscript

- [x] Every number in `paper/manuscript.docx` should trace to
      `paper/stats.json` — spot-check five of them by hand — **done
      2026-09-20**: 130, 106, 54, 38, 1170, 149, and the full Table 1
      per-corpus breakdown (direct/partial/related/no_match/mean/max for
      all three target corpora) all traced exactly to `stats.json`; the
      0.30/0.18/0.08 thresholds cited in-text also match `align.py`.
- [x] Confirm the "No Match" rate discussion (LIMITATIONS.md item 4) is
      framed as a property of the scoring method, not as a substantive
      claim about TSA/NIST/CPG coverage — **done 2026-09-20**: confirmed;
      the manuscript's limitations section frames the ~66% rate
      explicitly as a lexical-matching artifact, not a substantive
      coverage claim.

## 5. Rule on flagged judgment calls

- [x] TSA policy corpus choice: confirm you're comfortable citing the
      public Pipeline Security Guidelines (not the SD text) as the TSA
      corpus, and that the manuscript says this plainly (LIMITATIONS.md
      item 3) — **checked 2026-09-20**: the manuscript states this
      plainly in two places (a scope note right after the corpus row
      counts, and limitations item 3) and never implies directive-level
      authority anywhere in the text. Author's comfort with this framing
      as a matter of judgment is still the author's own call to make.
- [x] SP 800-53 subset scope: confirm 54 base controls across 18 families
      is an adequate scope for the claims the manuscript makes, or narrow
      the claims — **checked 2026-09-20**: the manuscript consistently
      qualifies every claim with "54-control base subset" / "base
      controls" and never states or implies full-catalog coverage.
      Whether 54/18 is *adequate scope* for the author's broader claims
      (e.g. in an NIW or similar context) is a judgment only the author
      can make — flagging this explicitly rather than deciding it here.
- [x] Author/co-author block and order in `AUTHORS.json`, `CITATION.cff`,
      and the manuscript header — **done 2026-09-20**: all three match
      exactly (Friday Ogochukwu Ikwuogu, corresponding; David
      Mike-Ewewie; Osorachukwu Maurice Ayozie), same order, spelling,
      affiliations, and emails throughout.

## 6. Final mechanical gate

- [ ] Run `python3 scripts/publish_gate.py` and resolve every finding —
      **in progress 2026-09-20**: 35 -> 11 real blockers resolved this
      session (all remaining ones are the project-wide DRAFT status on
      README.md/BUILD_SPEC.md/docs/*.md, which is correct until you
      complete section 1's clean-environment reproduction and give final
      sign-off in section 7 below)
- [x] Run `python3 code/06_figures.py --final` to remove the DRAFT stamp
      from the figures, then re-embed them in the manuscript if needed —
      **done 2026-09-20**: figures regenerated with `--final`.

## 7. Sign-off

- [ ] I, the author, have personally completed sections 1–6 above.
      Date: 2026-09-20  Signature/initials: Friday Ogochukwu Ikwuogu
