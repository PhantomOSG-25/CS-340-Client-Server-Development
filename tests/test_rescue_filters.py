"""Unit tests for rescue-category classification and queries."""

import unittest

from rescue_filters import build_rescue_query, classify_rescue_type


class RescueFilterTests(unittest.TestCase):
    def test_classifies_supported_breeds(self) -> None:
        self.assertEqual(
            "Water Rescue",
            classify_rescue_type("Labrador Retriever Mix"),
        )
        self.assertEqual(
            "Mountain Rescue",
            classify_rescue_type("German Shepherd"),
        )
        self.assertEqual("Other", classify_rescue_type("Beagle"))

    def test_builds_water_rescue_query(self) -> None:
        query = build_rescue_query("Water")

        self.assertEqual("Intact Female", query["sex_upon_outcome"])
        self.assertEqual(26, query["age_upon_outcome_in_weeks"]["$gte"])
        self.assertIn("Newfoundland", query["breed"]["$in"])

    def test_unknown_selection_returns_unfiltered_query(self) -> None:
        self.assertEqual({}, build_rescue_query(None))
        self.assertEqual({}, build_rescue_query("Unknown"))


if __name__ == "__main__":
    unittest.main()
