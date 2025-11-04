#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs


def test_incomplete_verse():
    """should treat incomplete verse reference as chapter reference"""

    results = filter_refs.get_result_list("Psalms 19:")

    assert results[0]["title"] == "Psalms 19 (NIV)"
    assert len(results) == 1


def test_incomplete_dot_verse():
    """should treat incomplete .verse reference as chapter reference"""

    results = filter_refs.get_result_list("Psalms 19.")

    assert results[0]["title"] == "Psalms 19 (NIV)"
    assert len(results) == 1


def test_incomplete_verse_range():
    """should treat incomplete verse ranges as single-verse references"""

    results = filter_refs.get_result_list("Psalms 19.7-")

    assert results[0]["title"] == "Psalms 19:7 (NIV)"
    assert len(results) == 1
