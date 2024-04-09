#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests import YVSTestCase
from tests.decorators import use_user_prefs


class TestEdge(YVSTestCase):

    def test_empty(self):
        """should not match empty input"""
        results = filter_refs.get_result_list("")
        self.assertEqual(len(results), 0)

    def test_non_alphanumeric(self):
        """should not match entirely non-alphanumeric input"""
        results = filter_refs.get_result_list("!!!")
        self.assertEqual(len(results), 0)

    def test_whitespace(self):
        """should ignore excessive whitespace"""
        results = filter_refs.get_result_list("  romans  8  28  nl  ")
        self.assertEqual(results[0]["title"], "Romans 8:28 (NLT)")
        self.assertEqual(len(results), 1)

    def test_littered(self):
        """should ignore non-alphanumeric characters"""
        results = filter_refs.get_result_list("!1@co#13$4^7&es*")
        self.assertEqual(results[0]["title"], "1 Corinthians 13:4-7 (ESV)")
        self.assertEqual(len(results), 1)

    def test_trailing_alphanumeric(self):
        """should ignore trailing non-matching alphanumeric characters"""
        results = filter_refs.get_result_list("2 co 3 x y z 1 2 3")
        self.assertEqual(results[0]["title"], "2 Corinthians 3 (NIV)")
        self.assertEqual(len(results), 1)

    @use_user_prefs({"language": "spa", "version": 128, "copybydefault": False})
    def test_unicode_accented(self):
        """should recognize accented Unicode characters"""
        results = filter_refs.get_result_list("é 3")
        self.assertEqual(results[0]["title"], "Éxodo 3 (NVI)")
        self.assertEqual(len(results), 1)

    def test_unicode_normalization(self):
        """should normalize Unicode characters"""
        results = filter_refs.get_result_list("e\u0301")
        self.assertEqual(len(results), 0)

    @use_user_prefs({"language": "deu", "version": 51, "copybydefault": False})
    def test_numbered_puncuation(self):
        """should match numbered books even if book name contains punctuation"""
        results = filter_refs.get_result_list("1 ch")
        self.assertEqual(results[0]["title"], "1. Chronik 1 (DELUT)")
        self.assertEqual(len(results), 1)
