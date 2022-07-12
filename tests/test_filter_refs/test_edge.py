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
def test_empty():
    """should not match empty input"""
    results = yvs.get_result_list('')
    case.assertEqual(len(results), 0)


@with_setup(set_up)
@with_teardown(tear_down)
def test_non_alphanumeric():
    """should not match entirely non-alphanumeric input"""
    results = yvs.get_result_list('!!!')
    case.assertEqual(len(results), 0)


@with_setup(set_up)
@with_teardown(tear_down)
def test_whitespace():
    """should ignore excessive whitespace"""
    results = yvs.get_result_list('  romans  8  28  nl  ')
    case.assertEqual(results[0]['title'], 'Romans 8:28 (NLT)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_littered():
    """should ignore non-alphanumeric characters"""
    results = yvs.get_result_list('!1@co#13$4^7&es*')
    case.assertEqual(results[0]['title'], '1 Corinthians 13:4-7 (ESV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_trailing_alphanumeric():
    """should ignore trailing non-matching alphanumeric characters"""
    results = yvs.get_result_list('2 co 3 x y z 1 2 3')
    case.assertEqual(results[0]['title'], '2 Corinthians 3 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'spa', 'version': 128, 'copybydefault': False})
def test_unicode_accented():
    """should recognize accented Unicode characters"""
    results = yvs.get_result_list('é 3')
    case.assertEqual(results[0]['title'], 'Éxodo 3 (NVI)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_unicode_normalization():
    """should normalize Unicode characters"""
    results = yvs.get_result_list('e\u0301')
    case.assertEqual(len(results), 0)


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'deu', 'version': 51, 'copybydefault': False})
def test_numbered_puncuation():
    """should match numbered books even if book name contains punctuation """
    results = yvs.get_result_list('1 ch')
    case.assertEqual(results[0]['title'], '1. Chronik 1 (DELUT)')
    case.assertEqual(len(results), 1)
