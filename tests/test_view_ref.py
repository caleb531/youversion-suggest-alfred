# tests.test_view_ref

import nose.tools as nose
from mock import patch

import yvs.view_ref as yvs
from tests import set_up, tear_down


@nose.with_setup(set_up, tear_down)
@patch('webbrowser.open')
def test_url_open(wb_open):
    """should attempt to open URL using webbrowser module"""
    yvs.main('59/jhn.3.17')
    wb_open.assert_called_once_with(
        'https://www.bible.com/bible/59/jhn.3.17')
