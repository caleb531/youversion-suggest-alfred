#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests import YVSTestCase
from tests.decorators import use_user_prefs


class TestVersion(YVSTestCase):
    @use_user_prefs({"language": "spa", "version": 128, "copybydefault": False})
    def test_numbered(self):
        """should match versions ending in number by partial name"""
        results = filter_refs.get_result_list("lucas 4:8 rvr1")
        self.assertEqual(results[0]["title"], "Lucas 4:8 (RVR1960)")
        self.assertEqual(len(results), 1)

    @use_user_prefs({"language": "zho_tw", "version": 46, "copybydefault": False})
    def test_non_ascii(self):
        """should match versions containing non-ASCII characters"""
        results = filter_refs.get_result_list("路加 4:8 cunp-上")
        self.assertEqual(results[0]["title"], "路加福音 4:8 (CUNP-上帝)")
        self.assertEqual(len(results), 1)

    def test_case(self):
        """should match versions irrespective of case"""
        query = "e 4:8 esv"
        results = filter_refs.get_result_list(query)
        results_lower = filter_refs.get_result_list(query.lower())
        results_upper = filter_refs.get_result_list(query.upper())
        self.assertListEqual(results_lower, results)
        self.assertListEqual(results_upper, results)
        self.assertEqual(len(results), 6)

    def test_whitespace(self):
        """should match versions irrespective of surrounding whitespace"""
        results = filter_refs.get_result_list("1 peter 5:7    esv")
        self.assertEqual(results[0]["title"], "1 Peter 5:7 (ESV)")
        self.assertEqual(len(results), 1)

    def test_partial(self):
        """should match versions by partial name"""
        results = filter_refs.get_result_list("luke 4:8 es")
        self.assertEqual(results[0]["title"], "Luke 4:8 (ESV)")
        self.assertEqual(len(results), 1)

    def test_partial_ambiguous(self):
        """should match versions by ambiguous partial name"""
        results = filter_refs.get_result_list("luke 4:8 c")
        self.assertEqual(results[0]["title"], "Luke 4:8 (CEB)")
        self.assertEqual(len(results), 1)

    def test_numbers(self):
        """should match versions containing numbers"""
        results = filter_refs.get_result_list("luke 4:8 nasb2020")
        self.assertEqual(results[0]["title"], "Luke 4:8 (NASB2020)")
        self.assertEqual(len(results), 1)

    def test_closest_match(self):
        """should try to find closest match for nonexistent versions"""
        results = filter_refs.get_result_list("hosea 6:3 nlab")
        self.assertEqual(results[0]["title"], "Hosea 6:3 (NLT)")
        self.assertEqual(len(results), 1)

    def test_exact(self):
        """should match versions by exact name"""
        results = filter_refs.get_result_list("hosea 6:3 amp")
        # Should NOT match AMPC
        self.assertEqual(results[0]["title"], "Hosea 6:3 (AMP)")
        self.assertEqual(len(results), 1)

    def test_nonexistent(self):
        """should use default version for nonexistent versions with no matches"""
        results = filter_refs.get_result_list("hosea 6:3 xyz")
        self.assertEqual(results[0]["title"], "Hosea 6:3 (NIV)")
        self.assertEqual(len(results), 1)

    def test_id(self):
        """should use correct ID for versions"""
        results = filter_refs.get_result_list("malachi 3:2 esv")
        self.assertEqual(results[0]["uid"], "yvs-59/mal.3.2")
        self.assertEqual(len(results), 1)
