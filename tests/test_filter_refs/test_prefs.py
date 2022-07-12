#!/usr/bin/env python3
# coding=utf-8

import os.path
import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down
from tests.decorators import use_user_prefs


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'eng', 'version': 59, 'copybydefault': False})
def test_version_persistence():
    """should remember version preferences"""
    results = yvs.get_result_list('mat 4')
    case.assertEqual(results[0]['title'], 'Matthew 4 (ESV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'spa', 'version': 128, 'copybydefault': False})
def test_language_persistence():
    """should remember language preferences"""
    results = yvs.get_result_list('gá 4')
    case.assertEqual(results[0]['title'], 'Gálatas 4 (NVI)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_missing_prefs():
    """should supply missing preferences with defaults"""
    yvs.core.set_user_prefs({})
    results = yvs.get_result_list('mat 5.3')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'eng', 'version': 999, 'copybydefault': False})
def test_invalid_user_version():
    """should raise exception when invalid version is set"""
    with case.assertRaises(Exception):
        yvs.get_result_list('ph 4')


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'eng', 'version': 111, 'copybydefault': False})
def test_copy_by_default_false():
    """should export correct data when "Copy By Default?" setting is false"""
    results = yvs.get_result_list('mat 5.3')
    case.assertEqual(results[0]['variables']['copybydefault'], 'False')
    case.assertEqual(results[0]['subtitle'], 'View on YouVersion')
    case.assertEqual(
        results[0]['mods']['cmd']['subtitle'], 'Copy content to clipboard')


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'eng', 'version': 111, 'copybydefault': True})
def test_copy_by_default_true():
    """should export correct data when "Copy By Default?" setting is true"""
    results = yvs.get_result_list('mat 5.3')
    case.assertEqual(results[0]['variables']['copybydefault'], 'True')
    case.assertEqual(results[0]['subtitle'], 'Copy content to clipboard')
    case.assertEqual(
        results[0]['mods']['cmd']['subtitle'], 'View on YouVersion')


@with_setup(set_up)
@with_teardown(tear_down)
def test_create_local_data_dir_silent_fail():
    """should silently fail if local data directory already exists"""
    yvs.core.create_local_data_dir()
    yvs.core.create_local_data_dir()
    case.assertTrue(
        os.path.exists(yvs.core.LOCAL_DATA_DIR_PATH),
        'local data directory does not exist')


@with_setup(set_up)
@with_teardown(tear_down)
def test_prettified_prefs_json():
    yvs.core.set_user_prefs({
        'language': 'spa',
        'version': 128,
        'refformat': '{name}\n{content}'
    })
    with open(yvs.core.get_user_prefs_path(), 'r') as user_prefs_file:
        user_prefs_json = user_prefs_file.read()
        case.assertIn('\n  ', user_prefs_json,
                      'User prefs JSON is not prettified')
