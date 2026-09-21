import os
import unittest

import pandas as pd

from regulatory_crosswalk import align_corpora, bucket_alignment_type, DEFAULT_THRESHOLDS
from regulatory_crosswalk.align import Thresholds

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


class TestBucketAlignmentType(unittest.TestCase):
    def test_thresholds(self):
        self.assertEqual(bucket_alignment_type(0.5), "Direct")
        self.assertEqual(bucket_alignment_type(0.30), "Direct")
        self.assertEqual(bucket_alignment_type(0.20), "Partial")
        self.assertEqual(bucket_alignment_type(0.10), "Related")
        self.assertEqual(bucket_alignment_type(0.01), "No Match")
        self.assertEqual(bucket_alignment_type(0.0), "No Match")

    def test_custom_thresholds(self):
        custom = Thresholds(direct=0.9, partial=0.5, related=0.1)
        self.assertEqual(bucket_alignment_type(0.6, custom), "Partial")


class TestAlignCorpora(unittest.TestCase):
    def setUp(self):
        self.source = pd.read_csv(os.path.join(FIXTURES, "source.csv"))
        self.target = pd.read_csv(os.path.join(FIXTURES, "target.csv"))

    def test_output_shape(self):
        result = align_corpora(self.source, self.target, target_name="TESTCORPUS", top_k=2)
        # 4 source rows x top_k=2 candidates each
        self.assertEqual(len(result), 8)
        expected_cols = {
            "source_id", "source_text", "target_corpus", "target_id", "target_text",
            "rank", "cosine_similarity", "tentative_alignment_type",
        }
        self.assertEqual(expected_cols, set(result.columns))
        self.assertTrue((result["target_corpus"] == "TESTCORPUS").all())

    def test_scores_in_unit_range(self):
        result = align_corpora(self.source, self.target, top_k=3)
        self.assertTrue(result["cosine_similarity"].between(0, 1).all())

    def test_known_easy_match_ranks_first(self):
        # S-2 ("Change all default passwords upon installation") should
        # rank T-2 ("Change all default manufacturer passwords before
        # deployment") above the unrelated T-4 (baseline configuration).
        result = align_corpora(self.source, self.target, top_k=4)
        s2 = result[result["source_id"] == "S-2"].sort_values("rank")
        self.assertEqual(s2.iloc[0]["target_id"], "T-2")

    def test_known_no_match_case(self):
        # S-4 shares no vocabulary with any target row; its best score
        # should not clear even the "Related" threshold.
        result = align_corpora(self.source, self.target, top_k=1)
        s4 = result[result["source_id"] == "S-4"].iloc[0]
        self.assertLess(s4["cosine_similarity"], DEFAULT_THRESHOLDS.related)
        self.assertEqual(s4["tentative_alignment_type"], "No Match")

    def test_rejects_empty_input(self):
        empty = self.source.iloc[0:0]
        with self.assertRaises(ValueError):
            align_corpora(empty, self.target)


if __name__ == "__main__":
    unittest.main()
