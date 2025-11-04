#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests.decorators import use_user_prefs


def test_empty():
    """should not match empty input"""

    results = filter_refs.get_result_list("")

    assert len(results) == 0


def test_non_alphanumeric():
    """should not match entirely non-alphanumeric input"""

    results = filter_refs.get_result_list("!!!")

    assert len(results) == 0


def test_whitespace():
    """should ignore excessive whitespace"""

    results = filter_refs.get_result_list("  romans  8  28  nl  ")

    assert results[0]["title"] == "Romans 8:28 (NLT)"
    assert len(results) == 1


def test_littered():
    """should ignore non-alphanumeric characters"""

    results = filter_refs.get_result_list("!1@co#13$4^7&es*")

    assert results[0]["title"] == "1 Corinthians 13:4-7 (ESV)"
    assert len(results) == 1


def test_trailing_alphanumeric():
    """should ignore trailing non-matching alphanumeric characters"""

    results = filter_refs.get_result_list("2 co 3 x y z 1 2 3")

    assert results[0]["title"] == "2 Corinthians 3 (NIV)"
    assert len(results) == 1


@use_user_prefs({"language": "spa", "version": 128, "copybydefault": False})
def test_unicode_accented():
    """should recognize accented Unicode characters"""

    results = filter_refs.get_result_list("é 3")

    assert results[0]["title"] == "Éxodo 3 (NVI)"
    assert len(results) == 1


def test_unicode_normalization():
    """should normalize Unicode characters"""

    results = filter_refs.get_result_list("e\u0301")

    assert len(results) == 0


@use_user_prefs({"language": "deu", "version": 51, "copybydefault": False})
def test_numbered_puncuation():
    """should match numbered books even if book name contains punctuation"""

    results = filter_refs.get_result_list("1 ch")

    assert results[0]["title"] == "1. Chronik 1 (DELUT)"
    assert len(results) == 1
