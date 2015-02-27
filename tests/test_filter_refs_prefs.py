#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs
import os


def test_version_remembrance():
    """should remember version preferences"""
    prefs = yvs.shared.get_prefs()
    original_version = prefs['version']
    prefs['version'] = 59
    yvs.shared.update_prefs(prefs)
    results = yvs.get_result_list('mat 4', use_prefs=True)
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Matthew 4 (ESV)')
    prefs['version'] = original_version
    yvs.shared.update_prefs(prefs)


def test_language_remembrance():
    """should remember language preferences"""
    prefs = yvs.shared.get_prefs()
    original_version = prefs['language']
    prefs['language'] = 'es'
    yvs.shared.update_prefs(prefs)
    results = yvs.get_result_list('gá 4', use_prefs=True)
    nose.assert_equal(len(results), 1)
    nose.assert_true(results[0]['title'].startswith('Gálatas 4 '))
    prefs['version'] = original_version
    yvs.shared.update_prefs(prefs)


def test_creation():
    """should create preferences if nonexistent"""
    yvs.shared.delete_prefs()
    nose.assert_false(os.path.exists(yvs.shared.prefs_path))
    defaults = yvs.shared.get_defaults()
    prefs = yvs.shared.get_prefs(use_prefs=True)
    nose.assert_true(os.path.exists(yvs.shared.prefs_path))
    nose.assert_equal(prefs, defaults)


def test_delete_nonexistent():
    """should attempt to delete nonexistent preferences without error"""
    yvs.shared.delete_prefs()
    yvs.shared.delete_prefs()
