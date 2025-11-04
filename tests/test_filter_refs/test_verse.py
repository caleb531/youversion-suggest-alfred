#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs


def test_basic():
    """should match verses"""

    results = filter_refs.get_result_list("luke 4:8")

    assert results[0]["title"] == "Luke 4:8 (NIV)"
    assert len(results) == 1


def test_ambiguous():
    """should match verses by ambiguous book reference"""

    results = filter_refs.get_result_list("a 3:2")

    assert results[0]["title"] == "Amos 3:2 (NIV)"
    assert results[1]["title"] == "Acts 3:2 (NIV)"
    assert len(results) == 2


def test_dot_separator():
    """should match verses preceded by dot"""

    results = filter_refs.get_result_list("luke 4.8")

    assert results[0]["title"] == "Luke 4:8 (NIV)"
    assert len(results) == 1


def test_space_separator():
    """should match verses preceded by space"""

    results = filter_refs.get_result_list("luke 4 8")

    assert results[0]["title"] == "Luke 4:8 (NIV)"
    assert len(results) == 1


def test_id():
    """should use correct ID for verses"""

    results = filter_refs.get_result_list("luke 4:8")

    assert results[0]["uid"] == "yvs-111/luk.4.8"
    assert len(results) == 1


def test_range():
    """should match verse ranges"""

    results = filter_refs.get_result_list("1 cor 13.4-7")

    assert results[0]["title"] == "1 Corinthians 13:4-7 (NIV)"
    assert len(results) == 1


def test_range_id():
    """should use correct ID for verse ranges"""

    results = filter_refs.get_result_list("1 cor 13.4-7")

    assert results[0]["uid"] == "yvs-111/1co.13.4-7"
    assert len(results) == 1


def test_range_invalid():
    """should not match nonexistent ranges"""

    results = filter_refs.get_result_list("1 cor 13.4-3")

    assert results[0]["title"] == "1 Corinthians 13:4 (NIV)"
    assert len(results) == 1


def test_zero_verse():
    """should interpret verse zero as verse one"""

    results = filter_refs.get_result_list("ps 23:0")

    assert results[0]["title"] == "Psalms 23:1 (NIV)"
    assert len(results) == 1
