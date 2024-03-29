#!/usr/bin/env python3
# coding=utf-8

from __future__ import unicode_literals

import yvs.filter_refs as yvs
from tests import YVSTestCase


class TestOverflow(YVSTestCase):

    def test_chapter_overflow(self):
        """should constrain specified chapter to last chapter if too high"""
        results = yvs.get_result_list("a 25:2")
        self.assertEqual(results[0]["title"], "Amos 9:2 (NIV)")
        self.assertEqual(results[1]["title"], "Acts 25:2 (NIV)")
        self.assertEqual(len(results), 2)

    def test_verse_overflow(self):
        """should constrain specified verse to last verse if too high"""
        results = yvs.get_result_list("a 2:50")
        self.assertEqual(results[0]["title"], "Amos 2:16 (NIV)")
        self.assertEqual(results[1]["title"], "Acts 2:47 (NIV)")
        self.assertEqual(len(results), 2)

    def test_endverse_overflow(self):
        """should constrain specified endverse to last endverse if too high"""
        results = yvs.get_result_list("a 2:4-51")
        self.assertEqual(results[0]["title"], "Amos 2:4-16 (NIV)")
        self.assertEqual(results[1]["title"], "Acts 2:4-47 (NIV)")
        self.assertEqual(len(results), 2)

    def test_verse_and_endverse_overflow(self):
        """should revert to single verse if verse and endverse are too high"""
        results = yvs.get_result_list("ps 23.7-9")
        self.assertEqual(results[0]["title"], "Psalms 23:6 (NIV)")
        self.assertEqual(len(results), 1)
