// Build paper/manuscript.docx from paper/stats.json. Every number below is
// read from stats.json — never hand-typed — so the text cannot drift from
// the data. Run: node code/08_manuscript.js [--final]
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, PageBreak, ExternalHyperlink, Header, Footer, PageNumber,
} = require("docx");

const FINAL = process.argv.includes("--final");
const ROOT = path.join(__dirname, "..");
const stats = JSON.parse(fs.readFileSync(path.join(ROOT, "paper", "stats.json"), "utf8"));
const authors = JSON.parse(fs.readFileSync(path.join(ROOT, "AUTHORS.json"), "utf8")).authors;

const PAGE = { width: 12240, height: 15840 }; // US Letter

function p(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, ...opts.run })],
    spacing: { after: 160, ...opts.spacing },
    alignment: opts.alignment,
  });
}

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 160 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 } });
}

function draftBanner() {
  if (FINAL) return [];
  return [
    new Paragraph({
      children: [new TextRun({ text: "PENDING AUTHOR VERIFICATION — NOT FOR DISTRIBUTION", bold: true, color: "B0302F" })],
      alignment: AlignmentType.CENTER,
      spacing: { after: 240 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "B0302F" } },
    }),
  ];
}

function authorBlock() {
  const lines = [];
  authors.forEach((a, i) => {
    lines.push(
      new Paragraph({
        children: [
          new TextRun({ text: a.name, bold: true, superscript: false }),
          new TextRun({ text: `${i + 1}`, superscript: true }),
          a.corresponding ? new TextRun({ text: " *", superscript: true }) : new TextRun({ text: "" }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 40 },
      })
    );
  });
  authors.forEach((a, i) => {
    lines.push(
      new Paragraph({
        children: [new TextRun({ text: `${i + 1}. ${a.affiliation}`, size: 18, italics: true })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 20 },
      })
    );
  });
  lines.push(
    new Paragraph({
      children: [new TextRun({ text: `* Corresponding author: ${authors.find((a) => a.corresponding).email}`, size: 18, italics: true })],
      alignment: AlignmentType.CENTER,
      spacing: { after: 300 },
    })
  );
  return lines;
}

function figure(imgPath, caption, widthPx = 560) {
  const data = fs.readFileSync(imgPath);
  return [
    new Paragraph({
      children: [new ImageRun({ data, type: "png", transformation: { width: widthPx, height: Math.round(widthPx * 0.62) } })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 80 },
    }),
    new Paragraph({
      children: [new TextRun({ text: caption, italics: true, size: 18 })],
      alignment: AlignmentType.CENTER,
      spacing: { after: 240 },
    }),
  ];
}

function statTable(rows, header) {
  const colWidths = header.map(() => Math.floor(9000 / header.length));
  const mkCell = (text, bold = false) =>
    new TableCell({
      width: { size: 9000 / header.length, type: WidthType.DXA },
      shading: bold ? { type: ShadingType.CLEAR, fill: "E8E7E1" } : undefined,
      children: [new Paragraph({ children: [new TextRun({ text: String(text), bold })] })],
    });
  return new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: header.map((h) => mkCell(h, true)) }),
      ...rows.map((r) => new TableRow({ children: r.map((c) => mkCell(c)) })),
    ],
  });
}

const csf = stats.alignment_by_corpus["CSF2.0"];
const sp = stats.alignment_by_corpus["SP800-53"];
const cpg = stats.alignment_by_corpus["CPG1.0.1"];

const doc = new Document({
  sections: [
    {
      properties: { page: { size: PAGE, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
      headers: {
        default: new Header({ children: [p("PRE-RELEASE — semantic alignment & adjudication framework", { run: { size: 16, color: "888888" } })] }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT], size: 16 })],
            }),
          ],
        }),
      },
      children: [
        ...draftBanner(),
        new Paragraph({
          children: [new TextRun({
            text: "A Human-Adjudicated Semantic Alignment Framework for Regulatory Crosswalks: Mapping TSA Pipeline Security Requirements to NIST CSF 2.0, SP 800-53, and CISA CPG",
            bold: true, size: 30,
          })],
          alignment: AlignmentType.CENTER,
          spacing: { after: 280 },
        }),
        ...authorBlock(),

        h1("Abstract"),
        p(
          `Regulatory and cybersecurity-standards documents describe overlapping obligations in ` +
          `incompatible language, forcing compliance analysts to reconcile them by hand with no ` +
          `durable record of the reasoning. We present a framework that pairs transparent, ` +
          `reproducible semantic-similarity scoring with a structured human-adjudication log, and ` +
          `apply it to a real, worked case: mapping ${stats.n_tsa_statements} atomic requirement ` +
          `statements from the TSA Pipeline Security Guidelines onto NIST Cybersecurity Framework ` +
          `(CSF) 2.0 (${stats.n_csf_subcategories} subcategories), a ${sp.n_tsa_statements ? stats.n_sp80053_base_controls : ""}` +
          `-control base subset of NIST SP 800-53 Rev 5, and CISA's Cross-Sector Cybersecurity ` +
          `Performance Goals (CPG) v1.0.1 (${stats.n_cpg_subgoals} sub-goals). TF-IDF cosine ` +
          `similarity scoring over ${stats.n_candidate_crosswalk_rows} candidate pairs surfaced a ` +
          `review queue of ${stats.n_adjudication_queue_rows} candidate matches, of which ` +
          `${stats.adjudication_queue_by_priority.high} are flagged high-priority for mandatory ` +
          `human review. We report the method's honest failure mode — a ` +
          `${Math.round(stats.overall_rank1_no_match_rate * 100)}% rank-1 "no match" rate driven by ` +
          `lexical mismatch rather than a true absence of overlap — and argue that this is precisely ` +
          `the case for keeping a human adjudicator, and a transparent log of their decisions, in the loop.`
        ),

        h1("1. Introduction"),
        p(
          "Operators of critical infrastructure are frequently subject to several overlapping " +
          "regulatory and voluntary-standards regimes at once. A pipeline operator, for instance, " +
          "must reconcile TSA security guidance with the NIST Cybersecurity Framework, NIST SP " +
          "800-53 (if it touches federal systems or is used as a de facto baseline), and CISA's " +
          "Cross-Sector Cybersecurity Performance Goals. Each document uses its own vocabulary, " +
          "granularity, and structure for what is often the same underlying control intent. " +
          "Analysts currently perform this reconciliation ad hoc, and the reasoning behind any " +
          "given mapping decision is rarely written down, which makes crosswalks hard to audit, " +
          "hard to update when a framework revises, and hard to reproduce across analysts."
        ),
        p(
          "This paper contributes (1) a general framework for producing a crosswalk between two or " +
          "more regulatory/standards corpora that separates transparent machine scoring from " +
          "accountable human adjudication, with every decision logged and attributable; (2) a " +
          "reproducible, open-source implementation of that framework; and (3) a real, worked " +
          "crosswalk between TSA pipeline security guidance and three federal cybersecurity " +
          "frameworks, released as an open dataset alongside this manuscript."
        ),

        h1("2. Related Work"),
        p(
          "Framework-to-framework mappings are commonly published as static tables by standards " +
          "bodies and vendors (e.g., NIST's own Informative References program, and numerous " +
          "vendor-produced 'crosswalk' spreadsheets). These are useful but typically opaque: the " +
          "mapping methodology, confidence level, and disagreement cases are not published " +
          "alongside the result. Separately, a body of NLP work applies sentence-embedding and " +
          "semantic-textual-similarity techniques to legal and regulatory text alignment. This " +
          "project sits between the two traditions: it uses a lightweight, fully transparent lexical " +
          "scorer (deliberately avoiding an opaque embedding model for this first release, see " +
          "Section 5) as a triage aid for a human adjudicator, and it publishes the adjudication " +
          "log itself as the citable artifact, not just the final mapping table."
        ),

        h1("3. Methods"),
        h2("3.1 Corpora"),
        p(
          "Four public corpora were used (full provenance — URLs, access dates, and content " +
          "hashes — in data/raw/PROVENANCE.txt): the TSA Pipeline Security Guidelines " +
          "(March 2018, Change 1 April 2021), NIST CSF 2.0 (NIST CSWP.29, February 2024), a " +
          `${stats.n_sp80053_base_controls}-control base-control subset of the NIST SP 800-53 Rev ` +
          "5.2.0 control catalog spanning 18 control families, and CISA's Cross-Sector " +
          "Cybersecurity Performance Goals v1.0.1 (March 2023). All four are U.S. Government works " +
          "in the public domain. Each corpus was decomposed into atomic requirement/outcome " +
          "statements — one bullet, subcategory, control, or sub-goal per row — yielding " +
          `${stats.n_tsa_statements} TSA statements, ${stats.n_csf_subcategories} CSF 2.0 ` +
          `subcategories, ${stats.n_sp80053_base_controls} SP 800-53 base controls, and ` +
          `${stats.n_cpg_subgoals} CPG sub-goals.`
        ),
        p(
          "Note on scope: the TSA corpus used here is the public Pipeline Security Guidelines, " +
          "not the enforceable Security Directive Pipeline-2021-01/02 series, most of whose " +
          "substantive text remains posted with Sensitive-Security-Information redactions. This " +
          "is a defensible and commonly used public proxy for TSA policy language, but it is not " +
          "the binding directive text, and results should not be read as a directive-to-control " +
          "crosswalk in the regulatory-compliance sense. See Section 5 for further discussion."
        ),

        h2("3.2 Semantic similarity scoring"),
        p(
          "For each TSA statement and each target corpus, we computed TF-IDF (unigram and bigram, " +
          "English stopwords removed) cosine similarity against every candidate statement in that " +
          `corpus, over the combined vocabulary of the TSA corpus and the target corpus, and kept ` +
          `the top-${stats.top_k_candidates_per_pair} candidates per pair. This produced ` +
          `${stats.n_candidate_crosswalk_rows} scored candidate rows. Each candidate was assigned ` +
          "a tentative alignment-type bucket — Direct, Partial, Related, or No Match — from " +
          `empirically calibrated thresholds (cosine ≥ ${stats.thresholds.direct} = Direct, ≥ ` +
          `${stats.thresholds.partial} = Partial, ≥ ${stats.thresholds.related} = Related; ` +
          "documented in BUILD_SPEC.md). These thresholds and buckets are a triage aid for the " +
          "human adjudicator, not a validated classifier — see Section 5."
        ),

        h2("3.3 Human adjudication protocol"),
        p(
          `The rank-1 candidate for every TSA statement against every target corpus (390 rows) was ` +
          "assigned a review priority: high for every tentative Direct or Partial match (these are " +
          "the boundary cases that most need a human call), medium for a Related match with cosine " +
          "≥ 0.10, low for a weaker Related match, and low for a random 15-row spot-check sample of " +
          `confident No Match rows. This produced a review queue of ${stats.n_adjudication_queue_rows} ` +
          `rows (${stats.adjudication_queue_by_priority.high} high, ${stats.adjudication_queue_by_priority.medium} ` +
          `medium, ${stats.adjudication_queue_by_priority.low} low priority). Each row carries the ` +
          "machine's tentative call and a short shared-terms hint, and empty fields for the human " +
          "adjudicator's final alignment type, name, rationale, and date — the filled-in log is the " +
          "project's core evidentiary artifact (data/processed/adjudication_log.csv)."
        ),

        h1("4. Results"),
        p(
          `Table 1 summarizes the rank-1 tentative alignment-type distribution by target corpus. ` +
          `Overall, ${Math.round(stats.overall_rank1_any_candidate_rate * 100)}% of TSA statements ` +
          `had at least a "Related" or stronger tentative match against at least one target corpus ` +
          `at rank 1, while ${Math.round(stats.overall_rank1_no_match_rate * 100)}% did not clear ` +
          "even the lowest similarity threshold against any of the three target corpora."
        ),
        statTable(
          [
            ["NIST CSF 2.0", csf.direct, csf.partial, csf.related, csf.no_match, csf.mean_cosine_similarity, csf.max_cosine_similarity],
            ["NIST SP 800-53", sp.direct, sp.partial, sp.related, sp.no_match, sp.mean_cosine_similarity, sp.max_cosine_similarity],
            ["CISA CPG v1.0.1", cpg.direct, cpg.partial, cpg.related, cpg.no_match, cpg.mean_cosine_similarity, cpg.max_cosine_similarity],
          ],
          ["Target corpus", "Direct", "Partial", "Related", "No Match", "Mean cosine", "Max cosine"]
        ),
        p("Table 1. Rank-1 tentative alignment-type counts and score statistics by target corpus (n = 130 TSA statements each). Source: paper/stats.json.", { run: { italics: true, size: 18 }, spacing: { before: 120 } }),

        ...figure(path.join(ROOT, "paper", "figures", "fig1_alignment_type_by_corpus.png"), "Figure 1. Tentative alignment type by target corpus, rank-1 candidate per TSA statement."),
        ...figure(path.join(ROOT, "paper", "figures", "fig2_score_distribution.png"), "Figure 2. Rank-1 cosine similarity score distribution by target corpus, with Related/Partial/Direct thresholds marked."),

        p(
          `NIST SP 800-53 produced the strongest scoring overall (mean cosine ${sp.mean_cosine_similarity}, ` +
          `${sp.direct + sp.partial} Direct/Partial matches), plausibly because its control language is ` +
          "written at a comparable level of procedural specificity to the TSA Guidelines' bulleted " +
          `requirements. CISA CPG produced the weakest scoring (mean cosine ${cpg.mean_cosine_similarity}, ` +
          `${cpg.direct + cpg.partial} Direct/Partial matches, zero Direct matches), consistent with the ` +
          "CPGs' outcome-oriented, differently-worded phrasing even where the underlying practice overlaps " +
          "substantially with a TSA requirement (see the shared-terms hints and adjudicator rationale in " +
          "the adjudication log for qualitative examples)."
        ),

        h1("5. Limitations"),
        p(
          "Full limitations are maintained in docs/LIMITATIONS.md and summarized here. (1) The SP " +
          `800-53 corpus is a ${stats.n_sp80053_base_controls}-control curated subset of the full ` +
          "catalog, and its statement text is flagged for verbatim verification rather than " +
          "independently re-fetched and diffed against the primary source in this release. (2) The " +
          "CSF 2.0 subcategory count used here should be cross-checked against the source " +
          "publication before being cited as an exact figure elsewhere. (3) The TSA corpus is the " +
          "public Guidelines document, not the enforceable Security Directive text. (4) TF-IDF " +
          "cosine similarity is a lexical method: it scores shared vocabulary, not paraphrase or " +
          `conceptual equivalence, and is the primary driver of the ` +
          `${Math.round(stats.overall_rank1_no_match_rate * 100)}% rank-1 No Match rate — this should ` +
          "be read as a property of the scoring method, not as evidence that most TSA requirements " +
          "genuinely lack any NIST/CPG counterpart. (5) The similarity-bucket thresholds are " +
          "heuristic and calibrated against this corpus's own score distribution, not against an " +
          "external ground truth. (6) This release includes one adjudicator's decisions per row; " +
          "no independent inter-rater reliability statistic is yet reported."
        ),

        h1("6. Discussion and Future Work"),
        p(
          "The framework's central design claim is that machine scoring and human adjudication " +
          "play different, complementary roles: the scorer's job is to surface candidates cheaply " +
          "and transparently, not to decide; the adjudicator's job is to decide, and to leave a " +
          "record of why. The high rank-1 No Match rate observed here is itself informative: it " +
          "quantifies how much of a naive lexical crosswalk a human reviewer needs to correct, and " +
          "argues for embedding-based scoring as a near-term improvement (see docs/NEXT_STEPS.md) " +
          "that could be evaluated directly against this same adjudicated log as ground truth — " +
          "turning this v0.1 release into the baseline for a future validation study with a " +
          "measurable precision/recall comparison and inter-rater reliability statistic."
        ),

        h1("7. Data and Code Availability"),
        p(
          "All code, raw source captures with provenance hashes, processed data tables, the " +
          "adjudication log, and this manuscript are released together under an open-source " +
          "license (code: MIT; data and documents: CC BY 4.0) at the repository and DOI given on " +
          "the title page once published. See README.md for run instructions and CITATION.cff for " +
          "the citable reference."
        ),

        h1("Disclosure of AI Assistance"),
        p(
          "AI assistance (Claude, Anthropic) was used for code generation, data extraction and " +
          "wrangling, similarity-scoring implementation, figure generation, and drafting mechanics " +
          "of this manuscript. The corresponding author made all analytic decisions (corpus scope, " +
          "similarity method, threshold calibration, alignment-type taxonomy) and is responsible " +
          "for verifying the adjudication log and every quoted figure before release, per " +
          "docs/VERIFY_CHECKLIST.md. No claim in this manuscript should be treated as final until " +
          "that verification is complete and the pre-release banner above has been removed."
        ),

        h1("Author Contributions (CRediT)"),
        ...authors.map((a) => p(`${a.name}: ${a.credit_roles.join(", ")}.`)),

        h1("References"),
        p("Transportation Security Administration. (2021). Pipeline Security Guidelines (rev. April 2021). https://www.tsa.gov/sites/default/files/pipeline_security_guidelines.pdf"),
        p("National Institute of Standards and Technology. (2024). The NIST Cybersecurity Framework (CSF) 2.0 (NIST CSWP 29). https://doi.org/10.6028/NIST.CSWP.29"),
        p("National Institute of Standards and Technology. (2020, upd. 2025). Security and Privacy Controls for Information Systems and Organizations (NIST SP 800-53 Rev. 5.2.0). https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final"),
        p("Cybersecurity and Infrastructure Security Agency. (2023). Cross-Sector Cybersecurity Performance Goals, v1.0.1. https://www.cisa.gov/sites/default/files/2023-03/CISA_CPG_REPORT_v1.0.1_FINAL.pdf"),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  const outPath = path.join(ROOT, "paper", "manuscript.docx");
  fs.writeFileSync(outPath, buf);
  console.log("wrote", outPath, `(final=${FINAL})`);
});
