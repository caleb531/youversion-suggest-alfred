# tests.test_filter_refs_prefs
# coding=utf-8

from __future__ import unicode_literals
import os.path
import nose.tools as nose
import yvs.filter_refs as yvs
from tests import set_up, tear_down
from tests.decorators import use_user_prefs


@nose.with_setup(set_up, tear_down)
@use_user_prefs({'language': 'eng', 'version': 59})
def test_version_persistence():
    """should remember version preferences"""
    results = yvs.get_result_list('mat 4')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Matthew 4 (ESV)')


@nose.with_setup(set_up, tear_down)
@use_user_prefs({'language': 'spa', 'version': 128})
def test_language_persistence():
    """should remember language preferences"""
    results = yvs.get_result_list('gá 4')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Gálatas 4 (NVI)')


@nose.with_setup(set_up, tear_down)
def test_missing_prefs():
    """should supply missing preferences with defaults"""
    yvs.shared.set_user_prefs({})
    results = yvs.get_result_list('mat 5.3')
    nose.assert_equal(len(results), 1)


@nose.with_setup(set_up, tear_down)
@use_user_prefs({'language': 'eng', 'version': 999})
def test_invalid_user_version():
    """should raise exception when invalid version is set"""
    with nose.assert_raises(Exception):
        yvs.get_result_list('ph 4')


@nose.with_setup(set_up, tear_down)
def test_create_local_data_dir_silent_fail():
    """should silently fail if local data directory already exists"""
    yvs.shared.create_local_data_dir()
    yvs.shared.create_local_data_dir()
    nose.assert_true(
        os.path.exists(yvs.shared.LOCAL_DATA_DIR_PATH),
        'local data directory does not exist')
