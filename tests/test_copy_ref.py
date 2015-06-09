#!/usr/bin/env python

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.copy_ref as yvs
import context_managers as ctx
from mock import patch, mock_open, Mock


with open('tests/files/psa.23.html') as file:
    yvs.urllib2.urlopen = Mock()
    yvs.urllib2.urlopen.return_value.read = Mock(return_value=file.read())


def test_copy_chapter():
    '''should copy reference content for chapter'''
    with ctx.redirect_stdout() as out:
        yvs.main('111/psa.23')
        ref_text = out.getvalue()
        nose.assert_regexp_matches(ref_text, 'Lorem')
        nose.assert_regexp_matches(ref_text, 'nunc nulla')
        nose.assert_regexp_matches(ref_text, 'fermentum')


def test_copy_verse():
    '''should copy reference content for verse'''
    with ctx.redirect_stdout() as out:
        yvs.main('111/psa.23.2')
        ref_text = out.getvalue()
        nose.assert_not_regexp_matches(ref_text, 'Lorem')
        nose.assert_regexp_matches(ref_text, 'nunc nulla')
        nose.assert_not_regexp_matches(ref_text, 'fermentum')


def test_copy_verse_range():
    '''should copy reference content for verse range'''
    with ctx.redirect_stdout() as out:
        yvs.main('111/psa.23.1-2')
        ref_text = out.getvalue()
        nose.assert_regexp_matches(ref_text, 'Lorem')
        nose.assert_regexp_matches(ref_text, 'nunc nulla')
        nose.assert_not_regexp_matches(ref_text, 'fermentum')


def test_header():
    '''should prepend reference header to copied string'''
    with ctx.redirect_stdout() as out:
        yvs.main('59/psa.23')
        ref_text = out.getvalue()
        nose.assert_regexp_matches(ref_text, '^Psalm 23 \(ESV\)')


def test_header_language():
    '''reference header should reflect chosen language'''
    with ctx.redirect_stdout() as out:
        yvs.main('128/psa.23', prefs={
            'language': 'es'
        })
        ref_text = out.getvalue()
        nose.assert_regexp_matches(ref_text, '^Salmos 23 \(NVI\)')


def test_charref_dec():
    '''should evaluate decimal character references'''
    with ctx.redirect_stdout() as out:
        yvs.main('111/psa.23')
        ref_text = out.getvalue().decode('utf-8')
        nose.assert_regexp_matches(ref_text, '\u201cLorem ipsum\u201d')


def test_charref_hex():
    '''should evaluate hexadecimal character references'''
    with ctx.redirect_stdout() as out:
        yvs.main('111/psa.23')
        ref_text = out.getvalue().decode('utf-8')
        nose.assert_regexp_matches(ref_text, '\u203a Nunc sem leo')


def test_whitespace_words():
    '''should preserve whitespace between words'''
    with ctx.redirect_stdout() as out:
        yvs.main('111/psa.23')
        ref_text = out.getvalue()
        nose.assert_regexp_matches(ref_text, 'adipiscing elit.')


def test_whitespace_lines():
    '''should add line breaks where appropriate'''
    with ctx.redirect_stdout() as out:
        yvs.main('111/psa.23')
        ref_text = out.getvalue()
        nose.assert_regexp_matches(ref_text, 'Psalm 23 \(NIV\)\n\n\S')
        nose.assert_regexp_matches(ref_text, 'amet,\nconsectetur')
        nose.assert_regexp_matches(ref_text, 'elit.\n\nUt')
        nose.assert_regexp_matches(ref_text, 'erat.\n\n\S')
        nose.assert_regexp_matches(ref_text, 'nec\n\nfermentum')


def test_url_always_chapter():
    '''should always fetch HTML from chapter URL'''
    with ctx.redirect_stdout() as out:
        yvs.urllib2.urlopen.reset_mock()
        yvs.main('59/psa.23.2')
        ref_text = out.getvalue()
        yvs.urllib2.urlopen.assert_called_once_with(
            'https://www.bible.com/bible/59/psa.23')
