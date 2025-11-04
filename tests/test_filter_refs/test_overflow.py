#!/usr/bin/env python3
# coding=utf-8

from __future__ import unicode_literals

import yvs.filter_refs as filter_refs


def test_chapter_overflow():
    """should constrain specified chapter to last chapter if too high"""

    results = filter_refs.get_result_list("a 25:2")

    assert results[0]["title"] == "Amos 9:2 (NIV)"
    assert results[1]["title"] == "Acts 25:2 (NIV)"
    assert len(results) == 2


def test_verse_overflow():
    """should constrain specified verse to last verse if too high"""

    results = filter_refs.get_result_list("a 2:50")

    assert results[0]["title"] == "Amos 2:16 (NIV)"
    assert results[1]["title"] == "Acts 2:47 (NIV)"
    assert len(results) == 2


def test_endverse_overflow():
    """should constrain specified endverse to last endverse if too high"""

    results = filter_refs.get_result_list("a 2:4-51")

    assert results[0]["title"] == "Amos 2:4-16 (NIV)"
    assert results[1]["title"] == "Acts 2:4-47 (NIV)"
    assert len(results) == 2


def test_verse_and_endverse_overflow():
    """should revert to single verse if verse and endverse are too high"""

    results = filter_refs.get_result_list("ps 23.7-9")

    assert results[0]["title"] == "Psalms 23:6 (NIV)"
    assert len(results) == 1
