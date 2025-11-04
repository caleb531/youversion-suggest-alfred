#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests.decorators import use_user_prefs


@use_user_prefs({"language": "spa", "version": 128, "copybydefault": False})
def test_numbered():
    """should match versions ending in number by partial name"""

    results = filter_refs.get_result_list("lucas 4:8 rvr1")

    assert results[0]["title"] == "Lucas 4:8 (RVR1960)"
    assert len(results) == 1


@use_user_prefs({"language": "zho_tw", "version": 46, "copybydefault": False})
def test_non_ascii():
    """should match versions containing non-ASCII characters"""

    results = filter_refs.get_result_list("路加 4:8 cunp-上")

    assert results[0]["title"] == "路加福音 4:8 (CUNP-上帝)"
    assert len(results) == 1


def test_case():
    """should match versions irrespective of case"""

    query = "e 4:8 esv"
    results = filter_refs.get_result_list(query)
    results_lower = filter_refs.get_result_list(query.lower())
    results_upper = filter_refs.get_result_list(query.upper())

    assert results_lower == results
    assert results_upper == results
    assert len(results) == 6


def test_whitespace():
    """should match versions irrespective of surrounding whitespace"""

    results = filter_refs.get_result_list("1 peter 5:7    esv")

    assert results[0]["title"] == "1 Peter 5:7 (ESV)"
    assert len(results) == 1


def test_partial():
    """should match versions by partial name"""

    results = filter_refs.get_result_list("luke 4:8 es")

    assert results[0]["title"] == "Luke 4:8 (ESV)"
    assert len(results) == 1


def test_partial_ambiguous():
    """should match versions by ambiguous partial name"""

    results = filter_refs.get_result_list("luke 4:8 c")

    assert results[0]["title"] == "Luke 4:8 (CEB)"
    assert len(results) == 1


def test_numbers():
    """should match versions containing numbers"""

    results = filter_refs.get_result_list("luke 4:8 nasb2020")

    assert results[0]["title"] == "Luke 4:8 (NASB2020)"
    assert len(results) == 1


def test_closest_match():
    """should try to find closest match for nonexistent versions"""

    results = filter_refs.get_result_list("hosea 6:3 nlab")

    assert results[0]["title"] == "Hosea 6:3 (NLT)"
    assert len(results) == 1


def test_exact():
    """should match versions by exact name"""

    results = filter_refs.get_result_list("hosea 6:3 amp")

    # Should NOT match AMPC
    assert results[0]["title"] == "Hosea 6:3 (AMP)"
    assert len(results) == 1


def test_nonexistent():
    """should use default version for nonexistent versions with no matches"""

    results = filter_refs.get_result_list("hosea 6:3 xyz")

    assert results[0]["title"] == "Hosea 6:3 (NIV)"
    assert len(results) == 1


def test_id():
    """should use correct ID for versions"""

    results = filter_refs.get_result_list("malachi 3:2 esv")

    assert results[0]["uid"] == "yvs-59/mal.3.2"
    assert len(results) == 1
