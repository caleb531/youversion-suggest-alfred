# tests.test_filter_refs_invalid

from __future__ import unicode_literals
import nose.tools as nose
import yvs.filter_refs as yvs


def test_empty():
    """should not match empty input"""
    results = yvs.get_result_list('')
    nose.assert_equal(len(results), 0)


def test_non_alphanumeric():
    """should not match entirely non-alphanumeric input"""
    results = yvs.get_result_list('!!!')
    nose.assert_equal(len(results), 0)


def test_invalid_xml():
    """should not match input containing XML reserved characters"""
    results = yvs.get_result_list('<&>')
    nose.assert_equal(len(results), 0)
