#!/usr/bin/env python3
# coding=utf-8

import json
import os
import os.path
import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.set_pref as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_set_language():
    """should set preferred language"""
    yvs.set_pref('language', 'spa')
    user_prefs = yvs.core.get_user_prefs()
    case.assertEqual(user_prefs['language'], 'spa')
    bible = yvs.core.get_bible(user_prefs['language'])
    case.assertEqual(user_prefs['version'], bible['default_version'])


@with_setup(set_up)
@with_teardown(tear_down)
def test_set_version():
    """should set preferred version"""
    yvs.set_pref('version', 59)
    user_prefs = yvs.core.get_user_prefs()
    case.assertEqual(user_prefs['version'], 59)


@with_setup(set_up)
@with_teardown(tear_down)
def test_set_nonexistent():
    """should discard nonexistent preferences"""
    yvs.set_pref('foo', 'bar')
    user_prefs = yvs.core.get_user_prefs()
    case.assertNotIn('foo', user_prefs)


@with_setup(set_up)
@with_teardown(tear_down)
def test_set_language_clear_cache():
    """should clear cache when setting language"""
    case.assertTrue(
        os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
        'local cache directory does not exist')
    yvs.cache.add_cache_entry('foo', 'blah blah')
    yvs.set_pref('language', 'spa')
    case.assertFalse(
        os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
        'local cache directory exists')


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_main(out):
    """should pass preference data to setter"""
    alfred_variables = {
        'pref_id': 'version',
        'pref_name': 'version',
        'value_id': '107',
        'value_name': 'New English Translation'
    }
    yvs.main(alfred_variables)
    alfred_json = json.loads(out.getvalue())
    case.assertEquals(
        alfred_json['alfredworkflow']['variables'], alfred_variables)
    user_prefs = yvs.core.get_user_prefs()
    case.assertEquals(user_prefs['version'], 107)
