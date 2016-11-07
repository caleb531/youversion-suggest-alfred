# tests.test_add_language.test_get_language_name
# coding=utf-8

from __future__ import unicode_literals
from mock import patch, Mock, NonCallableMock

import nose.tools as nose

import tests.test_add_language as tests
import utilities.add_language as add_lang

with open('tests/html/languages.html') as html_file:
    patch_urlopen = patch(
        'urllib2.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_file.read())))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
def test_get_language_name():
    """should fetch language name for the given language ID"""
    language_name = add_lang.get_language_name('spa_es')
    nose.assert_equal(language_name, 'Español (España) - Spanish (Spain)')


@nose.with_setup(set_up, tear_down)
def test_get_language_name_charref():
    """should resolve HTML entities in language name"""
    language_name = add_lang.get_language_name('nhd')
    nose.assert_equal(language_name, 'Avañe\'ẽ - Chiripá')


@nose.with_setup(set_up, tear_down)
def test_get_language_name_cache():
    """should cache languages HTML after initial fetch"""
    add_lang.get_language_name('spa')
    with patch('urllib2.Request') as request:
        language_name = add_lang.get_language_name('fra')
        request.assert_not_called()
        nose.assert_equal(language_name, 'Français - French')
