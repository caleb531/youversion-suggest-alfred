# tests.test_copy_ref

from __future__ import unicode_literals
import yvs.copy_ref as yvs
from mock import Mock, NonCallableMock, patch
from nose.tools import assert_regexp_matches, assert_not_regexp_matches
from tests.decorators import redirect_stdout, use_prefs


with open('tests/files/psa.23.html') as html_file:
    patch_urlopen = patch(
        'urllib2.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_file.read())))


def setup():
    patch_urlopen.start()


def teardown():
    patch_urlopen.stop()


@redirect_stdout
def test_copy_chapter(out):
    '''should copy reference content for chapter'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    assert_regexp_matches(ref_content, 'Lorem')
    assert_regexp_matches(ref_content, 'nunc nulla')
    assert_regexp_matches(ref_content, 'fermentum')


@redirect_stdout
def test_copy_verse(out):
    '''should copy reference content for verse'''
    yvs.main('111/psa.23.2')
    ref_content = out.getvalue()
    assert_not_regexp_matches(ref_content, 'Lorem')
    assert_regexp_matches(ref_content, 'nunc nulla')
    assert_not_regexp_matches(ref_content, 'fermentum')


@redirect_stdout
def test_copy_verse_range(out):
    '''should copy reference content for verse range'''
    yvs.main('111/psa.23.1-2')
    ref_content = out.getvalue()
    assert_regexp_matches(ref_content, 'Lorem')
    assert_regexp_matches(ref_content, 'nunc nulla')
    assert_not_regexp_matches(ref_content, 'fermentum')


@redirect_stdout
def test_header(out):
    '''should prepend reference header to copied string'''
    yvs.main('59/psa.23')
    ref_content = out.getvalue()
    assert_regexp_matches(ref_content, r'^Psalm 23 \(ESV\)')


@redirect_stdout
@use_prefs({'language': 'es'})
def test_header_language(out):
    '''reference header should reflect chosen language'''
    yvs.main('128/psa.23')
    ref_content = out.getvalue()
    assert_regexp_matches(ref_content, r'^Salmos 23 \(NVI\)')


@redirect_stdout
def test_charref_dec(out):
    '''should evaluate decimal character references'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue().decode('utf-8')
    assert_regexp_matches(ref_content, r'\u201cLorem ipsum\u201d')


@redirect_stdout
def test_charref_hex(out):
    '''should evaluate hexadecimal character references'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue().decode('utf-8')
    assert_regexp_matches(ref_content, r'\u203a Nunc sem leo')


@redirect_stdout
def test_whitespace_words(out):
    '''should handle spaces appropriately'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    assert_regexp_matches(ref_content, 'adipiscing elit.',
                          'should respect content consisting of spaces')
    assert_regexp_matches(ref_content, 'consectetur adipiscing',
                          'should collapse consecutive spaces')


@redirect_stdout
def test_whitespace_lines(out):
    '''should add line breaks where appropriate'''
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    assert_regexp_matches(ref_content, r'Psalm 23 \(NIV\)\n\n\S',
                          'should add two line breaks after header')
    assert_regexp_matches(ref_content, r'amet,\nconsectetur',
                          'should add newline before each p block')
    assert_regexp_matches(ref_content, r'erat.\n\n\S',
                          'should add newline after each p block')
    assert_regexp_matches(ref_content, r'nec\nfermentum',
                          'should add newline between each q block')
    assert_regexp_matches(ref_content, r'elit.\n\nUt',
                          'should add newlines around each li1 block')
    assert_regexp_matches(ref_content, r'leo,\n\nhendrerit',
                          'should add two newlines for each b block')


@patch('urllib2.Request')
def test_url_always_chapter(Request):
    '''should always fetch HTML from chapter URL'''
    yvs.main('59/psa.23.2')
    Request.assert_called_once_with(
        'https://www.bible.com/bible/59/psa.23',
        headers={'User-Agent': 'YouVersion Suggest'})
