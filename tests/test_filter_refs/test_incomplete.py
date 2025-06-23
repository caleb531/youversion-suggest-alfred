#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests import YVSTestCase


class TestIncomplete(YVSTestCase):
    def test_incomplete_verse(self):
        """should treat incomplete verse reference as chapter reference"""
        results = filter_refs.get_result_list("Psalms 19:")
        self.assertEqual(results[0]["title"], "Psalms 19 (NIV)")
        self.assertEqual(len(results), 1)

    def test_incomplete_dot_verse(self):
        """should treat incomplete .verse reference as chapter reference"""
        results = filter_refs.get_result_list("Psalms 19.")
        self.assertEqual(results[0]["title"], "Psalms 19 (NIV)")
        self.assertEqual(len(results), 1)

    def test_incomplete_verse_range(self):
        """should treat incomplete verse ranges as single-verse references"""
        results = filter_refs.get_result_list("Psalms 19.7-")
        self.assertEqual(results[0]["title"], "Psalms 19:7 (NIV)")
        self.assertEqual(len(results), 1)
