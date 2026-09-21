import os
import unittest

import pandas as pd

from regulatory_crosswalk import align_corpora, build_review_queue

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


class TestBuildReviewQueue(unittest.TestCase):
    def setUp(self):
        source = pd.read_csv(os.path.join(FIXTURES, "source.csv"))
        target = pd.read_csv(os.path.join(FIXTURES, "target.csv"))
        self.candidates = align_corpora(source, target, target_name="TESTCORPUS", top_k=3)

    def test_verify_fields_present_and_unfilled(self):
        queue = build_review_queue(self.candidates, no_match_sample_size=2)
        for col in ("adjudicated_alignment_type", "adjudicator", "adjudication_rationale", "adjudication_date"):
            self.assertIn(col, queue.columns)
            self.assertTrue((queue[col] == "PENDING_REVIEW").all())

    def test_no_match_rows_are_sampled_not_all_included(self):
        queue = build_review_queue(self.candidates, no_match_sample_size=1)
        no_match_in_queue = (queue["tentative_alignment_type"] == "No Match").sum()
        no_match_in_candidates = (
            (self.candidates["rank"] == 1) & (self.candidates["tentative_alignment_type"] == "No Match")
        ).sum()
        # sampled count should be <= 1 per target corpus, and strictly less
        # than the full population whenever more than 1 no-match row exists
        self.assertLessEqual(no_match_in_queue, 1)
        if no_match_in_candidates > 1:
            self.assertLess(no_match_in_queue, no_match_in_candidates)

    def test_high_priority_rows_are_direct_or_partial(self):
        queue = build_review_queue(self.candidates)
        high = queue[queue["review_priority"] == "high"]
        self.assertTrue(high["tentative_alignment_type"].isin(["Direct", "Partial"]).all())

    def test_adjudication_ids_are_unique(self):
        queue = build_review_queue(self.candidates)
        self.assertEqual(queue["adjudication_id"].nunique(), len(queue))


if __name__ == "__main__":
    unittest.main()
