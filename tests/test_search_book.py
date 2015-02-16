#!/usr/bin/env python

import nose.tools as nose
import yv_suggest.search as yvs


def test_partial():
    """should match books by partial name"""
    results = yvs.get_result_list('luk')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Luke')


def test_case():
    """should match books irrespective of case"""
    query_str = 'Matthew'
    results = yvs.get_result_list(query_str)
    results_lower = yvs.get_result_list(query_str.lower())
    results_upper = yvs.get_result_list(query_str.upper())
    nose.assert_equal(len(results), 1)
    nose.assert_list_equal(results_lower, results)
    nose.assert_list_equal(results_upper, results)


def test_whitespace():
    """should match books irrespective of surrounding whitespace"""
    results = yvs.get_result_list('    romans    ')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Romans')


def test_partial_ambiguous():
    """should match books by ambiguous partial name"""
    results = yvs.get_result_list('r')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'Ruth')
    nose.assert_equal(results[1]['title'], 'Romans')
    nose.assert_equal(results[2]['title'], 'Revelation')


def test_multiple_words():
    """should match books with names comprised of multiple words"""
    results = yvs.get_result_list('song of songs')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Song of Songs')


def test_numbered_partial():
    """should match numbered books by partial numbered name"""
    results = yvs.get_result_list('1 cor')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians')


def test_numbered_whitespace():
    """should match numbered books irrespective of extra whitespace"""
    results = yvs.get_result_list('1    cor')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians')


def test_nonnumbered_partial():
    """should match numbered books by partial non-numbered name"""
    results = yvs.get_result_list('john')
    nose.assert_equal(len(results), 4)
    nose.assert_equal(results[0]['title'], 'John')
    nose.assert_equal(results[1]['title'], '1 John')
    nose.assert_equal(results[2]['title'], '2 John')
    nose.assert_equal(results[3]['title'], '3 John')


def test_id():
    """should use correct ID for books"""
    results = yvs.get_result_list('philippians')
    nose.assert_equal(results[0]['uid'], 'niv/php.1')


def test_nonexistent():
    """should not match nonexistent books"""
    results = yvs.get_result_list('jesus')
    nose.assert_equal(len(results), 0)
