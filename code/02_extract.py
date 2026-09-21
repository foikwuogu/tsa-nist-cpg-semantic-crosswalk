"""Parse the four raw source captures into atomic, ID-tagged statement tables.

Outputs (data/processed/):
  statements_tsa.csv       id, section, text
  statements_cpg.csv       id, cpg_id, title, text
  statements_csf.csv       id, subcat_id, category, function, text
  statements_sp80053.csv   id, control_id, family, title, text, verify_flag
"""
import csv
import os
import re

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(OUT, exist_ok=True)


def read_table_rows(path, n_cols, skip_header_row=True):
    """Read a '|'-delimited table from a markdown file, skipping metadata
    lines above the header row (the header row is the first line whose
    first cell, lowercased, contains an expected keyword)."""
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    started = False
    for line in lines:
        if not line.strip():
            continue
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < n_cols:
            continue
        if not started:
            # this is the header row
            started = True
            continue
        rows.append(cells[:n_cols])
    return rows


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def extract_tsa():
    rows = read_table_rows(os.path.join(RAW, "tsa_pipeline_security_guidelines.md"), 2)
    out = []
    for i, (section, text) in enumerate(rows, start=1):
        out.append([f"TSA-{i:03d}", section, text])
    write_csv(os.path.join(OUT, "statements_tsa.csv"), ["id", "section", "text"], out)
    return out


def extract_cpg():
    rows = read_table_rows(os.path.join(RAW, "cisa_cpg_v1.0.1.md"), 3)
    out = []
    for i, (cpg_id, title, text) in enumerate(rows, start=1):
        out.append([f"CPG-{i:03d}", cpg_id, title, text])
    write_csv(os.path.join(OUT, "statements_cpg.csv"), ["id", "cpg_id", "title", "text"], out)
    return out


def extract_csf():
    rows = read_table_rows(os.path.join(RAW, "nist_csf2_core.md"), 4)
    out = []
    for i, (subcat_id, category, function, text) in enumerate(rows, start=1):
        out.append([f"CSF-{i:03d}", subcat_id, category, function, text])
    write_csv(
        os.path.join(OUT, "statements_csf.csv"),
        ["id", "subcat_id", "category", "function", "text"],
        out,
    )
    return out


def extract_sp80053():
    rows = read_table_rows(os.path.join(RAW, "nist_sp80053_rev5_subset.md"), 4)
    out = []
    for i, (control_id, family, title, text) in enumerate(rows, start=1):
        verify_flag = "VERIFY" if control_id.split("-")[-1] not in ("1",) else "VERIFY"
        out.append([f"SP-{i:03d}", control_id, family, title, text, verify_flag])
    write_csv(
        os.path.join(OUT, "statements_sp80053.csv"),
        ["id", "control_id", "family", "title", "text", "verify_flag"],
        out,
    )
    return out


if __name__ == "__main__":
    tsa = extract_tsa()
    cpg = extract_cpg()
    csf = extract_csf()
    sp = extract_sp80053()
    print(f"TOTAL statements: TSA={len(tsa)} CPG={len(cpg)} CSF={len(csf)} SP800-53={len(sp)}")
