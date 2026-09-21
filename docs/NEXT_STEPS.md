# Next Steps (v1.1 and beyond)

This v1.0.1 release establishes the framework and a real, working crosswalk
between TSA pipeline guidance and three federal cybersecurity frameworks.
It is a first step, not a finished reference crosswalk. Planned follow-ups:

1. **Swap TF-IDF for a sentence-embedding model** (e.g., a
   sentence-transformers model) and re-run `code/03_align.py` to quantify
   how much of the current ~66% rank-1 "No Match" rate is a lexical-overlap
   artifact versus a genuine coverage gap. Report both scorers side by side.

2. **Full SP 800-53 catalog.** Extend `statements_sp80053.csv` from the
   current 54-control base subset to the full catalog (base controls +
   enhancements), retaining the verification flag until each row is checked.

3. **Second independent adjudicator + inter-rater agreement.** Have a
   second qualified reviewer adjudicate a random sample of the queue
   independently, then compute Cohen's kappa against the primary
   adjudicator. This would upgrade the project from "single-adjudicator
   framework demonstration" to a genuine inter-rater validation study
   (archetype 6), which is the stronger and more citable claim.

4. **Extend to the enforceable Security Directives.** If/when a complete,
   unredacted public version of SD Pipeline-2021-02 (or its successor) is
   available, re-run the pipeline against that text instead of (or
   alongside) the public Guidelines, and report both.

5. **Add TSA Information Circulars and CPG v2.0** (if released) as
   additional target/source corpora, and generalize the framework to other
   regulated sectors (e.g., water, electricity) as a demonstration of
   reusability beyond pipelines.

6. **Versioned Zenodo releases.** Each of the above should ship as a new
   Zenodo version under the same concept DOI, with a changelog entry here.
