#!/usr/bin/env python3
# coding=utf-8

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down
from tests.decorators import use_user_prefs


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'spa', 'version': 128, 'copybydefault': False})
def test_numbered():
    """should match versions ending in number by partial name"""
    results = yvs.get_result_list('lucas 4:8 rvr1')
    case.assertEqual(results[0]['title'], 'Lucas 4:8 (RVR1960)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'zho_tw', 'version': 46, 'copybydefault': False})
def test_non_ascii():
    """should match versions containing non-ASCII characters"""
    results = yvs.get_result_list('路加 4:8 cunp-上')
    case.assertEqual(results[0]['title'], '路加福音 4:8 (CUNP-上帝)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_case():
    """should match versions irrespective of case"""
    query = 'e 4:8 esv'
    results = yvs.get_result_list(query)
    results_lower = yvs.get_result_list(query.lower())
    results_upper = yvs.get_result_list(query.upper())
    case.assertListEqual(results_lower, results)
    case.assertListEqual(results_upper, results)
    case.assertEqual(len(results), 6)


@with_setup(set_up)
@with_teardown(tear_down)
def test_whitespace():
    """should match versions irrespective of surrounding whitespace"""
    results = yvs.get_result_list('1 peter 5:7    esv')
    case.assertEqual(results[0]['title'], '1 Peter 5:7 (ESV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_partial():
    """should match versions by partial name"""
    results = yvs.get_result_list('luke 4:8 es')
    case.assertEqual(results[0]['title'], 'Luke 4:8 (ESV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_partial_ambiguous():
    """should match versions by ambiguous partial name"""
    results = yvs.get_result_list('luke 4:8 c')
    case.assertEqual(results[0]['title'], 'Luke 4:8 (CEB)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_closest_match():
    """should try to find closest match for nonexistent versions"""
    results = yvs.get_result_list('hosea 6:3 nlab')
    case.assertEqual(results[0]['title'], 'Hosea 6:3 (NLT)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_exact():
    """should match versions by exact name"""
    results = yvs.get_result_list('hosea 6:3 amp')
    # Should NOT match AMPC
    case.assertEqual(results[0]['title'], 'Hosea 6:3 (AMP)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_nonexistent():
    """should use default version for nonexistent versions with no matches"""
    results = yvs.get_result_list('hosea 6:3 xyz')
    case.assertEqual(results[0]['title'], 'Hosea 6:3 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_id():
    """should use correct ID for versions"""
    results = yvs.get_result_list('malachi 3:2 esv')
    case.assertEqual(results[0]['uid'], 'yvs-59/mal.3.2')
    case.assertEqual(len(results), 1)
