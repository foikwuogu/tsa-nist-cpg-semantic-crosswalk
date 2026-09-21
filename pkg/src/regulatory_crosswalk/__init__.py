"""regulatory-crosswalk: transparent semantic-similarity scoring plus a
human-adjudication review queue for mapping one regulatory/standards
corpus onto another.

Typical use:

    import pandas as pd
    from regulatory_crosswalk import align_corpora, build_review_queue

    source = pd.read_csv("my_source_requirements.csv")   # columns: id, text
    target = pd.read_csv("their_target_controls.csv")     # columns: id, text

    candidates = align_corpora(source, target, target_name="TargetFramework")
    queue = build_review_queue(candidates)
    queue.to_csv("adjudication_log.csv", index=False)

The two artifacts a project built with this package should publish are the
candidate table (`candidates`) and the human-filled-in review queue
(`queue`) — the queue, once adjudicated, is the citable crosswalk.
"""

from .align import align_corpora, DEFAULT_THRESHOLDS, bucket_alignment_type
from .adjudicate import build_review_queue

__all__ = [
    "align_corpora",
    "build_review_queue",
    "bucket_alignment_type",
    "DEFAULT_THRESHOLDS",
]

__version__ = "1.0.1"
