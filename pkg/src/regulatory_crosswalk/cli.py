"""Command-line interface: `regcrosswalk align` and `regcrosswalk adjudicate`."""
from __future__ import annotations

import argparse
import sys

import pandas as pd

from .align import align_corpora, Thresholds
from .adjudicate import build_review_queue


def _cmd_align(args: argparse.Namespace) -> int:
    source = pd.read_csv(args.source)
    target = pd.read_csv(args.target)
    thresholds = Thresholds(direct=args.direct, partial=args.partial, related=args.related)
    result = align_corpora(
        source,
        target,
        source_id_col=args.source_id_col,
        source_text_col=args.source_text_col,
        target_id_col=args.target_id_col,
        target_text_col=args.target_text_col,
        target_name=args.target_name,
        top_k=args.top_k,
        thresholds=thresholds,
    )
    result.to_csv(args.out, index=False)
    print(f"wrote {args.out} ({len(result)} candidate rows)", file=sys.stderr)
    return 0


def _cmd_adjudicate(args: argparse.Namespace) -> int:
    candidates = pd.read_csv(args.candidates)
    queue = build_review_queue(
        candidates,
        rank_filter=args.rank,
        no_match_sample_size=args.no_match_sample,
    )
    queue.to_csv(args.out, index=False)
    n_high = (queue["review_priority"] == "high").sum()
    print(f"wrote {args.out} ({len(queue)} rows, {n_high} high-priority)", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="regcrosswalk", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_align = sub.add_parser("align", help="score one corpus against another with TF-IDF cosine similarity")
    p_align.add_argument("source", help="CSV of source statements")
    p_align.add_argument("target", help="CSV of target statements")
    p_align.add_argument("--source-id-col", default="id")
    p_align.add_argument("--source-text-col", default="text")
    p_align.add_argument("--target-id-col", default="id")
    p_align.add_argument("--target-text-col", default="text")
    p_align.add_argument("--target-name", default="target", help="label for the target corpus in the output")
    p_align.add_argument("--top-k", type=int, default=3)
    p_align.add_argument("--direct", type=float, default=0.30, help="cosine threshold for 'Direct'")
    p_align.add_argument("--partial", type=float, default=0.18, help="cosine threshold for 'Partial'")
    p_align.add_argument("--related", type=float, default=0.08, help="cosine threshold for 'Related'")
    p_align.add_argument("-o", "--out", default="candidate_crosswalk.csv")
    p_align.set_defaults(func=_cmd_align)

    p_adj = sub.add_parser("adjudicate", help="build a prioritized human-adjudication review queue")
    p_adj.add_argument("candidates", help="CSV produced by 'regcrosswalk align'")
    p_adj.add_argument("--rank", type=int, default=1, help="which candidate rank to review (default: best)")
    p_adj.add_argument("--no-match-sample", type=int, default=15, help="spot-check sample size per corpus")
    p_adj.add_argument("-o", "--out", default="adjudication_log.csv")
    p_adj.set_defaults(func=_cmd_adjudicate)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
