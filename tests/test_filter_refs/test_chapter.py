#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests import YVSTestCase


class TestChapter(YVSTestCase):
    def test_basic(self):
        """should match chapters"""
        results = filter_refs.get_result_list("matthew 5")
        self.assertEqual(results[0]["title"], "Matthew 5 (NIV)")
        self.assertEqual(len(results), 1)

    def test_ambiguous(self):
        """should match chapters by ambiguous book name"""
        results = filter_refs.get_result_list("a 3")
        self.assertEqual(results[0]["title"], "Amos 3 (NIV)")
        self.assertEqual(results[1]["title"], "Acts 3 (NIV)")
        self.assertEqual(len(results), 2)

    def test_id(self):
        """should use correct ID for chapters"""
        results = filter_refs.get_result_list("luke 4")
        self.assertEqual(results[0]["uid"], "yvs-111/luk.4")
        self.assertEqual(len(results), 1)

    def test_zero_chapter(self):
        """should interpret chapter zero as chapter one"""
        results = filter_refs.get_result_list("ps 0")
        self.assertEqual(results[0]["title"], "Psalms 1 (NIV)")
        self.assertEqual(len(results), 1)
