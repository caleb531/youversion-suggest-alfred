#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs
import os
import context_managers as ctx


def test_version_persistence():
    """should remember version preferences"""
    prefs = {
        'language': 'en',
        'version': 59
    }
    with ctx.use_prefs(prefs):
        results = yvs.get_result_list('mat 4')
        nose.assert_equal(len(results), 1)
        nose.assert_equal(results[0]['title'], 'Matthew 4 (ESV)')


def test_language_persistence():
    """should remember language preferences"""
    prefs = {
        'language': 'es'
    }
    with ctx.use_prefs(prefs):
        results = yvs.get_result_list('gá 4')
        nose.assert_equal(len(results), 1)
        nose.assert_true(results[0]['title'].startswith('Gálatas 4 '))


def test_creation():
    """should create preferences if nonexistent"""
    with ctx.use_default_prefs():
        yvs.shared.delete_prefs()
        nose.assert_false(os.path.exists(yvs.shared.prefs_path))
        defaults = yvs.shared.get_defaults()
        prefs = yvs.shared.get_prefs()
        nose.assert_true(os.path.exists(yvs.shared.prefs_path))
        nose.assert_equal(prefs, defaults)


def test_delete_nonexistent():
    """should attempt to delete nonexistent preferences without error"""
    with ctx.use_default_prefs():
        try:
            yvs.shared.delete_prefs()
            yvs.shared.delete_prefs()
        except Exception as error:
            nose.assert_true(False, error)
