# tests.test_filter_refs_prefs
# coding=utf-8

from __future__ import unicode_literals
import os
import nose.tools as nose
import yvs.filter_refs as yvs
from tests.decorators import use_prefs


@use_prefs({'language': 'en', 'version': 59})
def test_version_persistence():
    """should remember version preferences"""
    results = yvs.get_result_list('mat 4')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Matthew 4 (ESV)')


@use_prefs({'language': 'es'})
def test_language_persistence():
    """should remember language preferences"""
    results = yvs.get_result_list('gá 4')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Gálatas 4 (NVI)')
