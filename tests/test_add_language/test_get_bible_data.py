# tests.test_add_language.test_get_bible_data

from __future__ import unicode_literals

import nose.tools as nose
from mock import patch

# import yvs.shared as yvs
import utilities.add_language as add_lang
from tests.test_add_language import set_up, tear_down

VERSIONS = [
    {'id': 234, 'name': 'ABC'},
    {'id': 123, 'name': 'DEF'},
    {'id': 456, 'name': 'GHI'},
    {'id': 345, 'name': 'JKL'}
]
BOOKS = [
    {'id': 'gen', 'name': 'Genesis'},
    {'id': '1sa', 'name': '1 Samuel'},
    {'id': 'jhn', 'name': 'John'}
]


@nose.with_setup(set_up, tear_down)
@patch('utilities.add_language.get_books', return_value=BOOKS)
@patch('utilities.add_language.get_versions', return_value=VERSIONS)
def test_get_bible_data_default_version_explicit(get_versions, get_books):
    """should store explicitly-supplied default version into Bible data"""
    language_id = 'spa'
    default_version = 345
    bible = add_lang.get_bible_data(language_id, default_version)
    get_versions.assert_called_once_with(
        language_id=language_id, max_version_id=None)
    nose.assert_equal(bible['books'], BOOKS)
    nose.assert_equal(bible['default_version'], default_version)
    nose.assert_equal(bible['versions'], VERSIONS)


@nose.with_setup(set_up, tear_down)
@patch('utilities.add_language.get_books', return_value=BOOKS)
@patch('utilities.add_language.get_versions', return_value=VERSIONS)
def test_get_bible_data_default_version_implicit(get_versions, get_books):
    """should retrieve implicit default version if none is explicitly given"""
    bible = add_lang.get_bible_data(language_id='spa')
    nose.assert_equal(bible['books'], BOOKS)
    nose.assert_equal(bible['default_version'], 123)
    nose.assert_equal(bible['versions'], VERSIONS)


@nose.with_setup(set_up, tear_down)
@patch('utilities.add_language.get_books', return_value=BOOKS)
@patch('utilities.add_language.get_versions', return_value=VERSIONS)
def test_get_bible_data_default_version_nonexistent(get_versions, get_books):
    """should raise error if given default version does not exist in list"""
    language_id = 'spa'
    default_version = 999
    with nose.assert_raises(RuntimeError):
        add_lang.get_bible_data(language_id, default_version)


@nose.with_setup(set_up, tear_down)
@patch('utilities.add_language.get_books', return_value=BOOKS)
@patch('utilities.add_language.get_versions', return_value=VERSIONS)
def test_get_bible_data_max_version_id(get_versions, get_books):
    """should consider maximum version ID when building Bible data"""
    language_id = 'spa'
    bible = add_lang.get_bible_data(language_id, max_version_id=400)
    nose.assert_equal(bible['books'], BOOKS)
    nose.assert_equal(bible['default_version'], 123)
    get_versions.assert_called_once_with(
        language_id=language_id, max_version_id=400)
