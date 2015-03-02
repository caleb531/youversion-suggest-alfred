#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs


def test_basic():
    """should match verses"""
    results = yvs.get_result_list('luke 4:8', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Luke 4:8 (NIV)')


def test_ambiguous():
    """should match verses by ambiguous book reference"""
    results = yvs.get_result_list('a 3:2', prefs={})
    nose.assert_equal(len(results), 2)
    nose.assert_equal(results[0]['title'], 'Amos 3:2 (NIV)')
    nose.assert_equal(results[1]['title'], 'Acts 3:2 (NIV)')


def test_dot_separator():
    """should match verses preceded by dot"""
    results = yvs.get_result_list('luke 4.8', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Luke 4:8 (NIV)')


def test_space_separator():
    """should match verses preceded by space"""
    results = yvs.get_result_list('luke 4 8', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Luke 4:8 (NIV)')


def test_range():
    """should match verse ranges"""
    results = yvs.get_result_list('1 cor 13.4-7', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13:4-7 (NIV)')


def test_id():
    """should use correct ID for verses"""
    results = yvs.get_result_list('luke 4:8', prefs={})
    nose.assert_equal(results[0]['uid'], 'yvs-111/luk.4.8')


def test_range_id():
    """should use correct ID for verse ranges"""
    results = yvs.get_result_list('1 cor 13.4-7', prefs={})
    nose.assert_equal(results[0]['uid'], 'yvs-111/1co.13.4-7')


def test_range_invalid():
    """should not match nonexistent ranges"""
    results = yvs.get_result_list('1 cor 13.4-3', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13:4 (NIV)')
