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
def test_partial():
    """should match books by partial name"""
    results = yvs.get_result_list('luk')
    case.assertEqual(results[0]['title'], 'Luke 1 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_case():
    """should match books irrespective of case"""
    query_str = 'Matthew'
    results = yvs.get_result_list(query_str)
    results_lower = yvs.get_result_list(query_str.lower())
    results_upper = yvs.get_result_list(query_str.upper())
    case.assertListEqual(results_lower, results)
    case.assertListEqual(results_upper, results)
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_partial_ambiguous():
    """should match books by ambiguous partial name"""
    results = yvs.get_result_list('r')
    case.assertEqual(results[0]['title'], 'Ruth 1 (NIV)')
    case.assertEqual(results[1]['title'], 'Romans 1 (NIV)')
    case.assertEqual(results[2]['title'], 'Revelation 1 (NIV)')
    case.assertEqual(len(results), 3)


@with_setup(set_up)
@with_teardown(tear_down)
def test_numbered_partial():
    """should match numbered books by partial numbered name"""
    results = yvs.get_result_list('1 cor')
    case.assertEqual(results[0]['title'], '1 Corinthians 1 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_number_only():
    """should match single number query"""
    results = yvs.get_result_list('2')
    case.assertEqual(len(results), 8)


@with_setup(set_up)
@with_teardown(tear_down)
def test_numbered_nonnumbered_partial():
    """should match numbered and non-numbered books by partial name"""
    results = yvs.get_result_list('c')
    case.assertEqual(results[0]['title'], 'Colossians 1 (NIV)')
    case.assertEqual(results[1]['title'], '1 Chronicles 1 (NIV)')
    case.assertEqual(results[2]['title'], '2 Chronicles 1 (NIV)')
    case.assertEqual(results[3]['title'], '1 Corinthians 1 (NIV)')
    case.assertEqual(results[4]['title'], '2 Corinthians 1 (NIV)')
    case.assertEqual(len(results), 5)


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'fin', 'version': 330, 'copybydefault': False})
def test_non_first_word():
    """should match word other than first word in book name"""
    results = yvs.get_result_list('la')
    case.assertEqual(results[0]['title'], 'Laulujen laulu 1 (FB92)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_id():
    """should use correct ID for books"""
    results = yvs.get_result_list('philippians')
    case.assertEqual(results[0]['uid'], 'yvs-111/php.1')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_nonexistent():
    """should not match nonexistent books"""
    results = yvs.get_result_list('xyz')
    case.assertEqual(len(results), 0)
