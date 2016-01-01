# tests.test_copy_ref

from __future__ import unicode_literals
import tests
import yvs.copy_ref as yvs
from mock import Mock, NonCallableMock, patch
import nose.tools as nose
from tests.decorators import redirect_stdout, use_user_prefs


with open('tests/files/psa.23.html') as html_file:
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
@redirect_stdout
def test_copy_chapter(out):
    """should copy reference content for chapter"""
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, 'Lorem')
    nose.assert_regexp_matches(ref_content, 'nunc nulla')
    nose.assert_regexp_matches(ref_content, 'fermentum')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_copy_verse(out):
    """should copy reference content for verse"""
    yvs.main('111/psa.23.2')
    ref_content = out.getvalue()
    nose.assert_not_regexp_matches(ref_content, 'Lorem')
    nose.assert_regexp_matches(ref_content, 'nunc nulla')
    nose.assert_not_regexp_matches(ref_content, 'fermentum')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_copy_verse_range(out):
    """should copy reference content for verse range"""
    yvs.main('111/psa.23.1-2')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, 'Lorem')
    nose.assert_regexp_matches(ref_content, 'nunc nulla')
    nose.assert_not_regexp_matches(ref_content, 'fermentum')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_header(out):
    """should prepend reference header to copied string"""
    yvs.main('59/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, r'^Psalm 23 \(ESV\)')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
@use_user_prefs({'language': 'es', 'version': 128})
def test_header_language(out):
    """reference header should reflect chosen language"""
    yvs.main('128/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, r'^Salmos 23 \(NVI\)')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_charref_dec(out):
    """should evaluate decimal character references"""
    yvs.main('111/psa.23')
    ref_content = out.getvalue().decode('utf-8')
    nose.assert_regexp_matches(ref_content, r'\u201cLorem ipsum\u201d')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_charref_hex(out):
    """should evaluate hexadecimal character references"""
    yvs.main('111/psa.23')
    ref_content = out.getvalue().decode('utf-8')
    nose.assert_regexp_matches(ref_content, r'\u203a Nunc sem leo')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_whitespace_words(out):
    """should handle spaces appropriately"""
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, 'adipiscing elit.',
                               'should respect content consisting of spaces')
    nose.assert_regexp_matches(ref_content, 'consectetur adipiscing',
                               'should collapse consecutive spaces')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_whitespace_lines(out):
    """should add line breaks where appropriate"""
    yvs.main('111/psa.23')
    ref_content = out.getvalue()
    nose.assert_regexp_matches(ref_content, r'Psalm 23 \(NIV\)\n\n\S',
                               'should add two line breaks after header')
    nose.assert_regexp_matches(ref_content, r'amet,\nconsectetur',
                               'should add newline before each p block')
    nose.assert_regexp_matches(ref_content, r'erat.\n\n\S',
                               'should add newline after each p block')
    nose.assert_regexp_matches(ref_content, r'nec\nfermentum',
                               'should add newline between each q block')
    nose.assert_regexp_matches(ref_content, r'elit.\n\nUt',
                               'should add newlines around each li1 block')
    nose.assert_regexp_matches(ref_content, r'leo,\n\nhendrerit',
                               'should add two newlines for each b block')


@nose.with_setup(set_up, tear_down)
@patch('urllib2.Request')
@redirect_stdout
def test_url_always_chapter(out, request):
    """should always fetch HTML from chapter URL"""
    yvs.main('59/psa.23.2')
    request.assert_called_once_with(
        'https://www.bible.com/bible/59/psa.23',
        headers={'User-Agent': 'YouVersion Suggest'})


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_cache_url_content(out):
    """should cache chapter URL content after first fetch"""
    query_str = '59/psa.23.2'
    yvs.main(query_str)
    fetched_content = out.getvalue()
    out.seek(0)
    out.truncate(0)
    with patch('urllib2.Request') as request:
        yvs.main(query_str)
        cached_content = out.getvalue()
        nose.assert_equal(cached_content, fetched_content)
        request.assert_not_called()
