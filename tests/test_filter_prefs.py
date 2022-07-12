#!/usr/bin/env python3
# coding=utf-8

import glob
import json
import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_prefs as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout, use_user_prefs


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_show_languages():
    """should show all languages if no value is given"""
    results = yvs.get_result_list('language')
    case.assertEqual(
        len(results), len(glob.glob('yvs/data/bible/bible-*.json')))


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_languages():
    """should filter available languages if value is given"""
    results = yvs.get_result_list('language esp')
    case.assertEqual(results[0]['uid'], 'yvs-language-spa')
    case.assertEqual(
        results[0]['title'], 'Español (América Latina)')
    case.assertEqual(results[0].get('valid', True), True)
    case.assertEqual(len(results), 2)
    case.assertEqual(results[0]['variables'], {
        'pref_id': 'language',
        'pref_name': 'language',
        'value_id': '"spa"',
        'value_name': 'Español (América Latina)'
    })


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_languages_non_latin():
    """should filter non-latin language names"""
    results = yvs.get_result_list('language 繁')
    case.assertEqual(len(results), 1)
    case.assertEqual(results[0]['uid'], 'yvs-language-zho_tw')
    case.assertEqual(results[0]['title'], '繁體中文')
    case.assertEqual(results[0].get('valid', True), True)
    case.assertEqual(results[0]['variables'], {
        'pref_id': 'language',
        'pref_name': 'language',
        'value_id': '"zho_tw"',
        'value_name': '繁體中文'
    })


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {'language': 'spa', 'version': 128, 'refformat': '{name}\n{content}'})
def test_show_versions():
    """should show all versions if no value is given"""
    results = yvs.get_result_list('version')
    case.assertGreater(len(results), 10)


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_versions():
    """should filter available versions if value is given"""
    results = yvs.get_result_list('version ni')
    case.assertEqual(len(results), 3)
    case.assertEqual(results[0]['uid'], 'yvs-version-110')
    case.assertEqual(results[0]['title'],
                     'New International Reader’s Version (NIRV)')
    case.assertEqual(results[0].get('valid', True), True)
    case.assertEqual(results[0]['variables'], {
        'pref_id': 'version',
        'pref_name': 'version',
        'value_id': '110',
        'value_name': 'New International Reader’s Version (NIRV)'
    })


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {'language': 'spa', 'version': 128, 'refformat': '{name}\n{content}'})
def test_show_refformats():
    """should show all refformats if no value is given"""
    results = yvs.get_result_list('refformat')
    case.assertGreater(len(results), 3)


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_refformats():
    """should filter available refformats if value is given"""
    results = yvs.get_result_list('refformat http')
    result_title = '"Jesus wept." ¬ John 11:35 NIV ¬ {url}'.format(
        url=yvs.core.get_ref_url('111/jhn.11.35'))
    result_format_id = '"{content}"\n{name} {version}\n{url}'
    case.assertEqual(len(results), 1)
    case.assertEqual(results[0]['uid'],
                     'yvs-refformat-{id}'.format(id=result_format_id))
    case.assertEqual(results[0]['title'], result_title)
    case.assertEqual(results[0].get('valid', True), True)
    case.assertEqual(results[0]['variables'], {
        'pref_id': 'refformat',
        'pref_name': 'reference format',
        'value_id': json.dumps(result_format_id),
        'value_name': result_title
    })


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'eng', 'version': 59, 'refformat': 'Z {content}'})
def test_show_current_refformat():
    """should show current refformat as an available value"""
    results = yvs.get_result_list('refformat Z')
    case.assertEqual(len(results), 1)
    case.assertEqual(results[0]['uid'], 'yvs-refformat-Z {content}')
    case.assertEqual(results[0]['title'], 'Z Jesus wept.')
    case.assertEqual(results[0]['valid'], False)
    case.assertEqual(results[0]['variables'], {
        'pref_id': 'refformat',
        'pref_name': 'reference format',
        'value_id': '"Z {content}"',
        'value_name': 'Z Jesus wept.'
    })


@with_setup(set_up)
@with_teardown(tear_down)
def test_nonexistent_pref():
    """should not match nonexistent preference"""
    results = yvs.get_result_list('xyz')
    case.assertEqual(len(results), 0)


@with_setup(set_up)
@with_teardown(tear_down)
def test_nonexistent_value():
    """should return null result for nonexistent value"""
    results = yvs.get_result_list('language xyz')
    case.assertRegexpMatches(results[0]['title'], 'No Results')
    case.assertEqual(results[0]['valid'], False)
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_current_value():
    """should not make preference's current value actionable"""
    results = yvs.get_result_list('language english')
    case.assertEqual(results[0]['title'], 'English')
    case.assertEqual(results[0]['valid'], False)
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_invalid_query():
    """should show all available preferences for invalid preference name"""
    results = yvs.get_result_list('!@#')
    case.assertNotEqual(len(results), 0)


@with_setup(set_up)
@with_teardown(tear_down)
def test_show_all_preferences():
    """should show all available preferences if query is empty"""
    results = yvs.get_result_list('')
    case.assertNotEqual(len(results), 0)


@with_setup(set_up)
@with_teardown(tear_down)
def test_preferences_autocompletion():
    """autocompletion should be functioning for all preference results"""
    results = yvs.get_result_list('')
    for result in results:
        case.assertIn('autocomplete', result)
        case.assertIn('valid', result)
        case.assertEqual(result['valid'], False)


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_preferences_id():
    """should filter available preferences if partial pref ID is given"""
    results = yvs.get_result_list('reff')
    case.assertEqual(len(results), 1)
    case.assertEqual(results[0]['uid'], 'yvs-refformat')
    case.assertEqual(results[0]['title'], 'Reference Format')


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_preferences_name():
    """should filter available preferences if partial pref name is given"""
    results = yvs.get_result_list('refe')
    case.assertEqual(len(results), 1)
    case.assertEqual(results[0]['uid'], 'yvs-refformat')
    case.assertEqual(results[0]['title'], 'Reference Format')


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_preferences_name_partial():
    """should match partial pref name at word boundaries"""
    results = yvs.get_result_list('version en st')
    case.assertEqual(len(results), 2)
    case.assertEqual(results[1]['uid'], 'yvs-version-59')
    case.assertEqual(
        results[1]['title'], 'English Standard Version 2016 (ESV)')


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_preferences_show_current():
    """should show current values for all preferences"""
    results = yvs.get_result_list('')
    case.assertEqual(len(results), 5)
    case.assertIn('English', results[0]['subtitle'])
    case.assertIn('NIV', results[1]['subtitle'])


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({
    'language': 'eng', 'version': 999, 'refformat':
    '{name}\n\n{content}', 'versenumbers': False, 'copybydefault': False})
def test_filter_preferences_show_current_valid_only():
    """should not show invalid current preference values"""
    results = yvs.get_result_list('')
    case.assertEqual(len(results), 5)
    case.assertIn('currently', results[0]['subtitle'])
    case.assertNotIn('currently', results[1]['subtitle'])


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_preference_entire_query():
    """should match available preference values using entire query string"""
    results = yvs.get_result_list('language español (españa)')
    case.assertEqual(len(results), 1)
    case.assertEqual(results[0]['uid'], 'yvs-language-spa_es')
    case.assertEqual(results[0]['title'], 'Español (España)')
    case.assertEqual(results[0].get('valid', True), True)
    case.assertEqual(results[0]['variables'], {
        'pref_id': 'language',
        'pref_name': 'language',
        'value_id': '"spa_es"',
        'value_name': 'Español (España)'
    })


@with_setup(set_up)
@with_teardown(tear_down)
def test_filter_preference_ignore_special():
    """should ignore special characters when matching preference values"""
    results = yvs.get_result_list('language 繁體中文$$')
    case.assertEqual(len(results), 1)
    case.assertEqual(results[0]['uid'], 'yvs-language-zho_tw')
    case.assertEqual(results[0]['title'], '繁體中文')
    case.assertEqual(results[0].get('valid', True), True)
    case.assertEqual(results[0]['variables'], {
        'pref_id': 'language',
        'pref_name': 'language',
        'value_id': '"zho_tw"',
        'value_name': '繁體中文'
    })


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_main_output(out):
    """should output pref result list JSON"""
    query_str = 'language'
    yvs.main(query_str)
    output = out.getvalue().rstrip()
    results = yvs.get_result_list(query_str)
    feedback = yvs.core.get_result_list_feedback_str(results).rstrip()
    case.assertEqual(output, feedback)


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_null_result(out):
    """should output "No Results" JSON item for empty pref result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    feedback_str = out.getvalue()
    feedback = json.loads(feedback_str)
    case.assertEqual(len(feedback['items']), 1, 'result item is missing')
    item = feedback['items'][0]
    case.assertEqual(item['title'], 'No Results')
    case.assertEqual(item['valid'], False)


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_feedback_show_all(out):
    """should output JSON for all results if query is empty"""
    yvs.main('')
    output = out.getvalue().rstrip()
    results = yvs.get_result_list('')
    feedback = yvs.core.get_result_list_feedback_str(results).rstrip()
    case.assertEqual(output, feedback)
