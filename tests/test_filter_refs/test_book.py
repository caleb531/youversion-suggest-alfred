#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests.decorators import use_user_prefs


def test_partial():
    """should match books by partial name"""

    results = filter_refs.get_result_list("luk")

    assert results[0]["title"] == "Luke 1 (NIV)"
    assert len(results) == 1


def test_case():
    """should match books irrespective of case"""

    query_str = "Matthew"
    results = filter_refs.get_result_list(query_str)
    results_lower = filter_refs.get_result_list(query_str.lower())
    results_upper = filter_refs.get_result_list(query_str.upper())

    assert results_lower == results
    assert results_upper == results
    assert len(results) == 1


def test_partial_ambiguous():
    """should match books by ambiguous partial name"""

    results = filter_refs.get_result_list("r")

    assert results[0]["title"] == "Ruth 1 (NIV)"
    assert results[1]["title"] == "Romans 1 (NIV)"
    assert results[2]["title"] == "Revelation 1 (NIV)"
    assert len(results) == 3


def test_numbered_partial():
    """should match numbered books by partial numbered name"""

    results = filter_refs.get_result_list("1 cor")

    assert results[0]["title"] == "1 Corinthians 1 (NIV)"
    assert len(results) == 1


def test_number_only():
    """should match single number query"""

    results = filter_refs.get_result_list("2")

    assert len(results) == 8


def test_numbered_nonnumbered_partial():
    """should match numbered and non-numbered books by partial name"""

    results = filter_refs.get_result_list("c")

    assert results[0]["title"] == "Colossians 1 (NIV)"
    assert results[1]["title"] == "1 Chronicles 1 (NIV)"
    assert results[2]["title"] == "2 Chronicles 1 (NIV)"
    assert results[3]["title"] == "1 Corinthians 1 (NIV)"
    assert results[4]["title"] == "2 Corinthians 1 (NIV)"
    assert len(results) == 5


@use_user_prefs({"language": "fin", "version": 330, "copybydefault": False})
def test_non_first_word():
    """should match word other than first word in book name"""

    results = filter_refs.get_result_list("la")

    assert results[0]["title"] == "Laulujen laulu 1 (FB92)"
    assert len(results) == 1


def test_id():
    """should use correct ID for books"""

    results = filter_refs.get_result_list("philippians")

    assert results[0]["uid"] == "yvs-111/php.1"
    assert len(results) == 1


def test_nonexistent():
    """should not match nonexistent books"""

    results = filter_refs.get_result_list("xyz")

    assert len(results) == 0
