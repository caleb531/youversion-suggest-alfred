# tests.test_update_languagess
# coding=utf-8

from __future__ import unicode_literals

import glob

import nose.tools as nose
from mock import patch

import utilities.update_languages as update_langs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout_unicode


@nose.with_setup(set_up, tear_down)
@patch('utilities.update_languages.update_language')
@redirect_stdout_unicode
def test_update_languages(out, update_language):
    """should perform all necessary steps to update all languages"""
    update_langs.update_languages()
    nose.assert_equal(
        update_language.call_count,
        len(glob.glob('yvs/data/languages/language-*.json')))


@nose.with_setup(set_up, tear_down)
@patch('utilities.update_languages.update_languages')
@redirect_stdout_unicode
def test_main(out, update_languages):
    """main function should pass correct arguments to update_languages"""
    update_langs.main()
    update_languages.assert_called_once_with()


@patch('utilities.update_languages.update_languages',
       side_effect=KeyboardInterrupt)
@redirect_stdout_unicode
def test_main_keyboardinterrupt(out, update_languages):
    """main function should quit gracefully when ^C is pressed"""
    nose.assert_is_none(update_langs.main())
