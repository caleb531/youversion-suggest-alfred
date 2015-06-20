#!/usr/bin/env python

import nose.tools as nose
import yvs.view_ref as yvs
from mock import patch


@patch('webbrowser.open')
def test_url_open(open):
    """should attempt to open URL using webbrowser module"""
    yvs.main('59/jhn.3.17')
    open.assert_called_once_with(
        'https://www.bible.com/bible/59/jhn.3.17')
