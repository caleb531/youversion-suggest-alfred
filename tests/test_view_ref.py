#!/usr/bin/env python

import nose.tools as nose
from mock import patch
import yv_suggest.view_ref as yvs


@patch('webbrowser.open')
def test_url_open(open):
    """should attempt to open URL using webbrowser module"""
    yvs.main('59/jhn.3.17')
    open.assert_called_once_with(
        'https://www.bible.com/bible/59/jhn.3.17')
