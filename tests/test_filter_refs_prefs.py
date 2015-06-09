#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs
import os
from decorators import use_prefs, use_default_prefs


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
    nose.assert_true(results[0]['title'].startswith('Gálatas 4 '))


@use_default_prefs
def test_creation():
    """should create preferences if nonexistent"""
    yvs.shared.delete_prefs()
    nose.assert_false(os.path.exists(yvs.shared.prefs_path))
    defaults = yvs.shared.get_defaults()
    prefs = yvs.shared.get_prefs()
    nose.assert_true(os.path.exists(yvs.shared.prefs_path))
    nose.assert_equal(prefs, defaults)


@use_default_prefs
def test_delete_nonexistent():
    """should attempt to delete nonexistent preferences without error"""
    try:
        yvs.shared.delete_prefs()
        yvs.shared.delete_prefs()
    except Exception as error:
        nose.assert_true(False, error)
