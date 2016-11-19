# tests.test_update_language
# coding=utf-8

from __future__ import unicode_literals

import nose.tools as nose
from mock import patch

import utilities.update_language as update_lang
from tests import set_up, tear_down
from tests.decorators import redirect_stdout_unicode


@nose.with_setup(set_up, tear_down)
@patch('sys.argv', [update_lang.__file__, 'swe'])
@patch('utilities.update_language.add_language')
@redirect_stdout_unicode
def test_update_language(out, add_language):
    """should perform all necessary steps to update a language"""
    language_id = 'spa'
    update_lang.update_language(language_id)
    add_language.assert_called_once_with(
        language_id=language_id,
        default_version=128)


@nose.with_setup(set_up, tear_down)
@patch('sys.argv', [update_lang.__file__, 'swe'])
@patch('utilities.update_language.update_language')
@redirect_stdout_unicode
def test_main(out, update_language):
    """main function should pass correct arguments to update_language"""
    update_lang.main()
    update_language.assert_called_once_with(language_id='swe')


@patch('utilities.update_language.update_language',
       side_effect=KeyboardInterrupt)
@patch('utilities.update_language.parse_cli_args')
@redirect_stdout_unicode
def test_main_keyboardinterrupt(out, parse_cli_args, update_language):
    """main function should quit gracefully when ^C is pressed"""
    nose.assert_is_none(update_lang.main())
