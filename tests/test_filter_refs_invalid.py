# tests.test_filter_refs_invalid

from __future__ import unicode_literals
import nose.tools as nose
import yvs.filter_refs as yvs
from tests import set_up, tear_down


@nose.with_setup(set_up, tear_down)
def test_empty():
    """should not match empty input"""
    results = yvs.get_result_list('')
    nose.assert_equal(len(results), 0)


@nose.with_setup(set_up, tear_down)
def test_non_alphanumeric():
    """should not match entirely non-alphanumeric input"""
    results = yvs.get_result_list('!!!')
    nose.assert_equal(len(results), 0)
