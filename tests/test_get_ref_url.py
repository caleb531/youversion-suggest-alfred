#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import nose.tools as nose

import yvs.get_ref_url as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_get_ref_url(out):
    """should get URL for given reference ID"""
    yvs.main('59/jhn.3.17')
    output = out.getvalue().strip()
    nose.assert_equal(output, 'https://www.bible.com/bible/59/JHN.3.17')
