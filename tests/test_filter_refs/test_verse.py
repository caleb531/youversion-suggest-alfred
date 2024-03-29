#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as yvs
from tests import YVSTestCase


class TestVerse(YVSTestCase):

    def test_basic(self):
        """should match verses"""
        results = yvs.get_result_list("luke 4:8")
        self.assertEqual(results[0]["title"], "Luke 4:8 (NIV)")
        self.assertEqual(len(results), 1)

    def test_ambiguous(self):
        """should match verses by ambiguous book reference"""
        results = yvs.get_result_list("a 3:2")
        self.assertEqual(results[0]["title"], "Amos 3:2 (NIV)")
        self.assertEqual(results[1]["title"], "Acts 3:2 (NIV)")
        self.assertEqual(len(results), 2)

    def test_dot_separator(self):
        """should match verses preceded by dot"""
        results = yvs.get_result_list("luke 4.8")
        self.assertEqual(results[0]["title"], "Luke 4:8 (NIV)")
        self.assertEqual(len(results), 1)

    def test_space_separator(self):
        """should match verses preceded by space"""
        results = yvs.get_result_list("luke 4 8")
        self.assertEqual(results[0]["title"], "Luke 4:8 (NIV)")
        self.assertEqual(len(results), 1)

    def test_id(self):
        """should use correct ID for verses"""
        results = yvs.get_result_list("luke 4:8")
        self.assertEqual(results[0]["uid"], "yvs-111/luk.4.8")
        self.assertEqual(len(results), 1)

    def test_range(self):
        """should match verse ranges"""
        results = yvs.get_result_list("1 cor 13.4-7")
        self.assertEqual(results[0]["title"], "1 Corinthians 13:4-7 (NIV)")
        self.assertEqual(len(results), 1)

    def test_range_id(self):
        """should use correct ID for verse ranges"""
        results = yvs.get_result_list("1 cor 13.4-7")
        self.assertEqual(results[0]["uid"], "yvs-111/1co.13.4-7")
        self.assertEqual(len(results), 1)

    def test_range_invalid(self):
        """should not match nonexistent ranges"""
        results = yvs.get_result_list("1 cor 13.4-3")
        self.assertEqual(results[0]["title"], "1 Corinthians 13:4 (NIV)")
        self.assertEqual(len(results), 1)

    def test_zero_verse(self):
        """should interpret verse zero as verse one"""
        results = yvs.get_result_list("ps 23:0")
        self.assertEqual(results[0]["title"], "Psalms 23:1 (NIV)")
        self.assertEqual(len(results), 1)
