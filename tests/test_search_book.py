#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.search as yvs


def test_partial():
    """should match books by partial name"""
    results = yvs.get_result_list('luk')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Luke 1 (NIV)')


def test_case():
    """should match books irrespective of case"""
    query_str = 'Matthew'
    results = yvs.get_result_list(query_str)
    results_lower = yvs.get_result_list(query_str.lower())
    results_upper = yvs.get_result_list(query_str.upper())
    nose.assert_equal(len(results), 1)
    nose.assert_list_equal(results_lower, results)
    nose.assert_list_equal(results_upper, results)


def test_partial_ambiguous():
    """should match books by ambiguous partial name"""
    results = yvs.get_result_list('r')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'Ruth 1 (NIV)')
    nose.assert_equal(results[1]['title'], 'Romans 1 (NIV)')
    nose.assert_equal(results[2]['title'], 'Revelation 1 (NIV)')


def test_multiple_words():
    """should match books with names comprised of multiple words"""
    results = yvs.get_result_list('song of songs')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Song of Songs 1 (NIV)')


def test_numbered_partial():
    """should match numbered books by partial numbered name"""
    results = yvs.get_result_list('1 cor')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 1 (NIV)')


def test_numbered_whitespace():
    """should match numbered books irrespective of extra whitespace"""
    results = yvs.get_result_list('1    cor')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 1 (NIV)')


def test_nonnumbered_partial():
    """should match numbered books by partial non-numbered name"""
    results = yvs.get_result_list('john')
    nose.assert_equal(len(results), 4)
    nose.assert_equal(results[0]['title'], 'John 1 (NIV)')
    nose.assert_equal(results[1]['title'], '1 John 1 (NIV)')
    nose.assert_equal(results[2]['title'], '2 John 1 (NIV)')
    nose.assert_equal(results[3]['title'], '3 John 1 (NIV)')


def test_id():
    """should use correct ID for books"""
    results = yvs.get_result_list('philippians')
    nose.assert_equal(results[0]['uid'], '111/php.1')


def test_closest_match():
    """should try to find closest match for nonexistent books"""
    results = yvs.get_result_list('relevations')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Revelation 1 (NIV)')


def test_nonexistent():
    """should not match nonexistent books"""
    results = yvs.get_result_list('xyz')
    nose.assert_equal(len(results), 0)
