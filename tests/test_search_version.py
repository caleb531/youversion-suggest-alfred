#!/usr/bin/env python

import nose.tools as nose
import yv_suggest.search as yvs


def test_numbered():
    """should match versions ending in number by partial name"""
    results = yvs.get_result_list('luke 4:8 rv1')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['subtitle'], 'RV1885')


def test_case():
    """should match versions irrespective of case"""
    query = 'e 4:8 esv'
    results = yvs.get_result_list(query)
    results_lower = yvs.get_result_list(query.lower())
    results_upper = yvs.get_result_list(query.upper())
    nose.assert_equal(len(results), 6)
    nose.assert_list_equal(results_lower, results)
    nose.assert_list_equal(results_upper, results)


def test_whitespace():
    """should match versions irrespective of surrounding whitespace"""
    results = yvs.get_result_list('1 peter 5:7    esv')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['subtitle'], 'ESV')


def test_partial():
    """should match versions by partial name"""
    results = yvs.get_result_list('luke 4:8 e')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['subtitle'], 'ESV')


def test_partial_ambiguous():
    """should match versions by ambiguous partial name"""
    results = yvs.get_result_list('luke 4:8 a')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['subtitle'], 'AMP')


def test_id():
    """should use correct ID for versions"""
    results = yvs.get_result_list('malachi 3:2 esv')
    nose.assert_equal(results[0]['uid'], 'esv/mal.3.2')
