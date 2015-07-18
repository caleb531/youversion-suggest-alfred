# tests.test_search_ref

import yvs.search_ref as yvs
from mock import patch
from tests.decorators import use_prefs


@patch('webbrowser.open')
def test_url_open_chapter(wb_open):
    """should open chapter search URL"""
    yvs.main('59/jhn.3')
    wb_open.assert_called_once_with(
        'https://www.google.com/search?q=John+3+%28ESV%29')


@patch('webbrowser.open')
def test_url_open_verse(wb_open):
    """should open verse search URL"""
    yvs.main('59/jhn.3.17')
    wb_open.assert_called_once_with(
        'https://www.google.com/search?q=John+3%3A17+%28ESV%29')


@patch('webbrowser.open')
def test_url_open_verse_range(wb_open):
    """should open verse range search URL"""
    yvs.main('59/jhn.3.16-17')
    wb_open.assert_called_once_with(
        'https://www.google.com/search?q=John+3%3A16-17+%28ESV%29')


@use_prefs({'language': 'es'})
@patch('webbrowser.open')
def test_unicode_search(wb_open):
    """should open search URL for reference containing Unicode"""
    yvs.main('128/exo.4')
    wb_open.assert_called_once_with(
        'https://www.google.com/search?q=%C3%89xodo+4+%28NVI%29')
