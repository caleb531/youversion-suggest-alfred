#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests.decorators import use_user_prefs


def test_book():
    """should recognize shorthand book syntax"""

    results = filter_refs.get_result_list("1co")

    assert results[0]["title"] == "1 Corinthians 1 (NIV)"
    assert len(results) == 1


def test_chapter():
    """should recognize shorthand chapter syntax"""

    results = filter_refs.get_result_list("1 co13")

    assert results[0]["title"] == "1 Corinthians 13 (NIV)"
    assert len(results) == 1


def test_version():
    """should recognize shorthand version syntax"""

    results = filter_refs.get_result_list("1 co 13esv")

    assert results[0]["title"] == "1 Corinthians 13 (ESV)"
    assert len(results) == 1


@use_user_prefs({"language": "zho_tw", "version": 46, "copybydefault": False})
def test_version_unicode():
    """should allow shorthand Unicode versions"""

    results = filter_refs.get_result_list("創世記1:3次經")

    assert results[0]["title"] == "創世記 1:3 (次經)"
    assert len(results) == 1
