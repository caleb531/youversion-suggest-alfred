# tests.test_set_pref
# coding=utf-8

from __future__ import unicode_literals

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
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['language'], 'spa')
    bible = yvs.shared.get_bible_data(user_prefs['language'])
    nose.assert_equal(user_prefs['version'], bible['default_version'])


@nose.with_setup(set_up, tear_down)
def test_set_version():
    """should set preferred version"""
    yvs.set_pref('version', 59)
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['version'], 59)


@nose.with_setup(set_up, tear_down)
def test_set_nonexistent():
    """should discard nonexistent preferences"""
    yvs.set_pref('foo', 'bar')
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_not_in('foo', user_prefs)


@nose.with_setup(set_up, tear_down)
def test_set_language_clear_cache():
    """should clear cache when setting language"""
    nose.assert_true(
        os.path.exists(yvs.shared.LOCAL_CACHE_DIR_PATH),
        'local cache directory does not exist')
    yvs.shared.add_cache_entry('foo', 'blah blah')
    yvs.set_pref('language', 'spa')
    nose.assert_false(
        os.path.exists(yvs.shared.LOCAL_CACHE_DIR_PATH),
        'local cache directory exists')


@patch('yvs.set_pref.set_pref')
@redirect_stdout
def test_main(out, set_pref):
    """should pass preference data to setter"""
    alfred_data = {
        'alfredworkflow': {
            'variables': {
                'pref_id': 'language',
                'pref_name': 'Language',
                'value_id': 'spa',
                'value_name': 'Español'
            }
        }
    }
    yvs.main(json.dumps(alfred_data))
    set_pref.assert_called_once_with('language', 'spa')
    nose.assert_equal(json.loads(out.getvalue()), alfred_data)
