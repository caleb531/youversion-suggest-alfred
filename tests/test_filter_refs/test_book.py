#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as yvs
from tests import YVSTestCase
from tests.decorators import use_user_prefs


class TestBook(YVSTestCase):

    def test_partial(self):
        """should match books by partial name"""
        results = yvs.get_result_list("luk")
        self.assertEqual(results[0]["title"], "Luke 1 (NIV)")
        self.assertEqual(len(results), 1)

    def test_case(self):
        """should match books irrespective of case"""
        query_str = "Matthew"
        results = yvs.get_result_list(query_str)
        results_lower = yvs.get_result_list(query_str.lower())
        results_upper = yvs.get_result_list(query_str.upper())
        self.assertListEqual(results_lower, results)
        self.assertListEqual(results_upper, results)
        self.assertEqual(len(results), 1)

    def test_partial_ambiguous(self):
        """should match books by ambiguous partial name"""
        results = yvs.get_result_list("r")
        self.assertEqual(results[0]["title"], "Ruth 1 (NIV)")
        self.assertEqual(results[1]["title"], "Romans 1 (NIV)")
        self.assertEqual(results[2]["title"], "Revelation 1 (NIV)")
        self.assertEqual(len(results), 3)

    def test_numbered_partial(self):
        """should match numbered books by partial numbered name"""
        results = yvs.get_result_list("1 cor")
        self.assertEqual(results[0]["title"], "1 Corinthians 1 (NIV)")
        self.assertEqual(len(results), 1)

    def test_number_only(self):
        """should match single number query"""
        results = yvs.get_result_list("2")
        self.assertEqual(len(results), 8)

    def test_numbered_nonnumbered_partial(self):
        """should match numbered and non-numbered books by partial name"""
        results = yvs.get_result_list("c")
        self.assertEqual(results[0]["title"], "Colossians 1 (NIV)")
        self.assertEqual(results[1]["title"], "1 Chronicles 1 (NIV)")
        self.assertEqual(results[2]["title"], "2 Chronicles 1 (NIV)")
        self.assertEqual(results[3]["title"], "1 Corinthians 1 (NIV)")
        self.assertEqual(results[4]["title"], "2 Corinthians 1 (NIV)")
        self.assertEqual(len(results), 5)

    @use_user_prefs({"language": "fin", "version": 330, "copybydefault": False})
    def test_non_first_word(self):
        """should match word other than first word in book name"""
        results = yvs.get_result_list("la")
        self.assertEqual(results[0]["title"], "Laulujen laulu 1 (FB92)")
        self.assertEqual(len(results), 1)

    def test_id(self):
        """should use correct ID for books"""
        results = yvs.get_result_list("philippians")
        self.assertEqual(results[0]["uid"], "yvs-111/php.1")
        self.assertEqual(len(results), 1)

    def test_nonexistent(self):
        """should not match nonexistent books"""
        results = yvs.get_result_list("xyz")
        self.assertEqual(len(results), 0)
