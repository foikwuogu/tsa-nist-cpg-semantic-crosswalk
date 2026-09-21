# Publish Guide

**`docs/VERIFY_CHECKLIST.md` is fully checked off and signed
(2026-09-20, Friday Ogochukwu Ikwuogu), and `python3 scripts/publish_gate.py .`
reports zero real blockers.** The SP 800-53 text has been verified, the
review queue has been adjudicated for all 149 rows, and the CSF 2.0
subcategory count has been confirmed. v0.1.0 is cleared to publish.

Suggested repository name: `tsa-nist-cpg-semantic-crosswalk`

## 1. GitHub

A GitHub token is available in this environment. Once the gate is clear:

1. Tell Claude "push to GitHub" and it will run `scripts/publish_github.py`,
   which creates the repository, commits with identity from `AUTHORS.json`,
   pushes, and tags a `v0.1.0` release — or do it yourself:
   ```bash
   cd /path/to/project
   git init -b main
   git add -A
   git commit -m "Initial release: TSA-NIST-CPG semantic crosswalk v0.1.0"
   gh repo create tsa-nist-cpg-semantic-crosswalk --public --source=. --remote=origin
   git push -u origin main
   git tag v0.1.0 -m "v0.1.0 — verified initial release"
   git push origin v0.1.0
   ```
2. On GitHub: Releases tab -> the `v0.1.0` tag -> "Create release from tag" ->
   paste this as the release notes:
   > First verified release of the TSA Pipeline Policy-to-Control Crosswalk
   > and human-adjudicated semantic alignment framework. 130 TSA statements
   > crosswalked against NIST CSF 2.0, NIST SP 800-53 (base-control subset),
   > and CISA CPG v1.0.1, with a fully adjudicated review log and methods
   > manuscript.

## 2. Zenodo (DOI)

Simplest path, since the repo is on GitHub:

1. Log in at zenodo.org with your ORCID (0009-0009-2222-1318).
2. Account -> GitHub -> flip the switch for
   `tsa-nist-cpg-semantic-crosswalk`.
3. On GitHub, publish the `v0.1.0` release (step 1 above) — Zenodo archives
   it automatically and mints a DOI within minutes.
4. Add the DOI badge Zenodo gives you to the top of `README.md`, and copy
   the DOI into `CITATION.cff` (replacing the `PENDING` placeholder) and
   into the manuscript's title-page footnote.
5. Metadata to double check on the Zenodo record before it's final:
   creators = the three names/ORCIDs/affiliations in `AUTHORS.json`; license
   = CC BY 4.0 for data/docs (note in the description that code is MIT);
   keywords from `CITATION.cff`; related identifier = the GitHub repo URL.

If you'd rather not link GitHub->Zenodo, the manual path is: New Upload on
zenodo.org, drag in a zip of the repository plus `paper/manuscript.docx`
(exported as PDF), fill in the same metadata by hand, Publish.

## 3. Preprint (arXiv cs.CR recommended)

The manuscript's subject matter (semantic alignment of regulatory text,
applied NLP methodology) fits **arXiv cs.CR** (Cryptography and Security) or
**cs.CL** (Computation and Language) as a secondary category.

1. If this is your first arXiv submission, you may need an endorsement:
   arxiv.org/auth/endorse. A short request note:
   > "I'm submitting my first paper to arXiv cs.CR: a methods paper on a
   > human-adjudicated semantic alignment framework for regulatory
   > crosswalks (TSA pipeline security vs. NIST/CISA frameworks). Could you
   > endorse me for cs.CR? [arXiv endorsement link goes here]"
2. Export `paper/manuscript.docx` to PDF (LibreOffice: `soffice --headless
   --convert-to pdf paper/manuscript.docx`) — run
   `node code/08_manuscript.js --final` first if you haven't already, to
   remove the pre-verification banner (the figures are already final).
3. Submit at arxiv.org/submit: upload the PDF, enter the title and author
   list exactly as in `AUTHORS.json`, paste the abstract from the
   manuscript, category cs.CR (primary), cs.CL (secondary, optional),
   license CC BY 4.0, comments field: "Code and data:
   [GitHub URL] (DOI: [Zenodo DOI])".
4. Moderation typically takes one to a few business days. Save the arXiv ID
   to the evidence log the day it appears.

## 4. PyPI (the `regulatory-crosswalk` package)

The alignment + adjudication-queue logic is also packaged as an installable
library in `pkg/` (name `regulatory-crosswalk`, confirmed available on
PyPI — no existing project uses it). It's built and its 11 tests verified
in this session's sandbox already; PyPI itself is not reachable from this
sandbox's network (only pypi.org's index API is allowlisted for `pip
install`, not the upload endpoint), so the actual `twine upload` step needs
to run from your own machine or CI.

1. `cd pkg && pip install -e ".[dev]"` then `python -m unittest discover -s
   tests -v` — confirm all 11 tests still pass on your machine.
2. Create a PyPI account and an API token scoped to this project (once the
   first release exists) at pypi.org/manage/account/token/.
3. Build fresh artifacts: `pip install build && python -m build` (from
   `pkg/`) — produces `dist/regulatory_crosswalk-0.1.0.tar.gz` and
   `dist/regulatory_crosswalk-0.1.0-py3-none-any.whl`. (Pre-built copies
   from this session are already in `pkg/dist/` if you'd rather reuse
   them — they were built and metadata-checked here, just not uploaded.)
4. `pip install twine && python -m twine upload dist/*` — username
   `__token__`, password = the API token.
5. Tag the same version (`v0.1.0`) on the GitHub repo and on the Zenodo
   record for consistency, and add the PyPI badge/link to `pkg/README.md`
   and the root `README.md`.
6. Optional but recommended given the test suite and docs already exist:
   also submit to **JOSS** (joss.theoj.org/papers/new) — it explicitly
   wants "substantial scholarly effort" + tests + docs, which this package
   now has, and this repo's manuscript in `paper/` can be adapted into
   JOSS's shorter `paper.md` format if you want a second citable artifact.

## 5. After every submission

Log it the same day: date, artifact, venue, URL/DOI/tracking number,
status. Update the README status line with the DOI once minted, and
`CITATION.cff`'s `identifiers` and `repository-code` fields.
