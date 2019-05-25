#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import json
import os
import os.path

import nose.tools as nose
from mock import patch

import yvs.set_pref as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


@nose.with_setup(set_up, tear_down)
def test_set_language():
    """should set preferred language"""
    yvs.set_pref('language', 'spa')
    user_prefs = yvs.core.get_user_prefs()
    nose.assert_equal(user_prefs['language'], 'spa')
    bible = yvs.core.get_bible(user_prefs['language'])
    nose.assert_equal(user_prefs['version'], bible['default_version'])


@nose.with_setup(set_up, tear_down)
def test_set_version():
    """should set preferred version"""
    yvs.set_pref('version', 59)
    user_prefs = yvs.core.get_user_prefs()
    nose.assert_equal(user_prefs['version'], 59)


@nose.with_setup(set_up, tear_down)
def test_set_nonexistent():
    """should discard nonexistent preferences"""
    yvs.set_pref('foo', 'bar')
    user_prefs = yvs.core.get_user_prefs()
    nose.assert_not_in('foo', user_prefs)


@nose.with_setup(set_up, tear_down)
def test_set_language_clear_cache():
    """should clear cache when setting language"""
    nose.assert_true(
        os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
        'local cache directory does not exist')
    yvs.cache.add_cache_entry('foo', 'blah blah')
    yvs.set_pref('language', 'spa')
    nose.assert_false(
        os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
        'local cache directory exists')


@patch('yvs.set_pref.set_pref')
@redirect_stdout
def test_main(out, set_pref):
    """should pass preference data to setter"""
    yvs.main(json.dumps({
        'pref': {'id': 'language', 'name': 'language'},
        'value': {'id': 'spa', 'name': 'Español'}
    }))
    set_pref.assert_called_once_with('language', 'spa')
    pref_set_data = json.loads(out.getvalue())
    nose.assert_not_equals(pref_set_data['alfredworkflow']['arg'], '')
    nose.assert_equals(
        pref_set_data['alfredworkflow']['variables']['pref_name'], 'language')
    nose.assert_equals(
        pref_set_data['alfredworkflow']['variables']['pref_id'], 'language')
    nose.assert_equals(
        pref_set_data['alfredworkflow']['variables']['value_id'], 'spa')
    nose.assert_equals(
        pref_set_data['alfredworkflow']['variables']['value_name'], 'Español')
