# tests.test_filter_refs_edge
# coding=utf-8

from __future__ import unicode_literals
import nose.tools as nose
import yvs.filter_refs as yvs
from tests.decorators import use_prefs


def test_whitespace():
    """should ignore excessive whitespace"""
    results = yvs.get_result_list('  romans  8  28  a  ')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Romans 8:28 (AMP)')


def test_littered():
    """should ignore non-alphanumeric characters"""
    results = yvs.get_result_list('!1@co#13$4^7&e*')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13:4-7 (ESV)')


def test_trailing_alphanumeric():
    """should ignore trailing non-matching alphanumeric characters"""
    results = yvs.get_result_list('2 co 3 x y z 1 2 3')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '2 Corinthians 3 (NIV)')


@use_prefs({'language': 'es'})
def test_unicode_accented():
    """should recognize accented Unicode characters"""
    results = yvs.get_result_list('é 3')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Éxodo 3 (NVI)')


def test_unicode_normalization():
    """should normalize Unicode characters"""
    results = yvs.get_result_list('e\u0301')
    nose.assert_equal(len(results), 0)
