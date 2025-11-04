#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs


def test_basic():
    """should match chapters"""

    results = filter_refs.get_result_list("matthew 5")

    assert results[0]["title"] == "Matthew 5 (NIV)"
    assert len(results) == 1


def test_ambiguous():
    """should match chapters by ambiguous book name"""

    results = filter_refs.get_result_list("a 3")

    assert results[0]["title"] == "Amos 3 (NIV)"
    assert results[1]["title"] == "Acts 3 (NIV)"
    assert len(results) == 2


def test_id():
    """should use correct ID for chapters"""

    results = filter_refs.get_result_list("luke 4")

    assert results[0]["uid"] == "yvs-111/luk.4"
    assert len(results) == 1


def test_zero_chapter():
    """should interpret chapter zero as chapter one"""

    results = filter_refs.get_result_list("ps 0")

    assert results[0]["title"] == "Psalms 1 (NIV)"
    assert len(results) == 1
