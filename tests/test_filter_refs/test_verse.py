#!/usr/bin/env python3
# coding=utf-8

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_basic():
    """should match verses"""
    results = yvs.get_result_list('luke 4:8')
    case.assertEqual(results[0]['title'], 'Luke 4:8 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_ambiguous():
    """should match verses by ambiguous book reference"""
    results = yvs.get_result_list('a 3:2')
    case.assertEqual(results[0]['title'], 'Amos 3:2 (NIV)')
    case.assertEqual(results[1]['title'], 'Acts 3:2 (NIV)')
    case.assertEqual(len(results), 2)


@with_setup(set_up)
@with_teardown(tear_down)
def test_dot_separator():
    """should match verses preceded by dot"""
    results = yvs.get_result_list('luke 4.8')
    case.assertEqual(results[0]['title'], 'Luke 4:8 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_space_separator():
    """should match verses preceded by space"""
    results = yvs.get_result_list('luke 4 8')
    case.assertEqual(results[0]['title'], 'Luke 4:8 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_id():
    """should use correct ID for verses"""
    results = yvs.get_result_list('luke 4:8')
    case.assertEqual(results[0]['uid'], 'yvs-111/luk.4.8')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_range():
    """should match verse ranges"""
    results = yvs.get_result_list('1 cor 13.4-7')
    case.assertEqual(results[0]['title'], '1 Corinthians 13:4-7 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_range_id():
    """should use correct ID for verse ranges"""
    results = yvs.get_result_list('1 cor 13.4-7')
    case.assertEqual(results[0]['uid'], 'yvs-111/1co.13.4-7')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_range_invalid():
    """should not match nonexistent ranges"""
    results = yvs.get_result_list('1 cor 13.4-3')
    case.assertEqual(results[0]['title'], '1 Corinthians 13:4 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_zero_verse():
    """should interpret verse zero as verse one"""
    results = yvs.get_result_list('ps 23:0')
    case.assertEqual(results[0]['title'], 'Psalms 23:1 (NIV)')
    case.assertEqual(len(results), 1)
