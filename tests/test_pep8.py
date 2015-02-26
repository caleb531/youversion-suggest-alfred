#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import pep8
import glob


def test_compliance():
    files = glob.iglob('*/*.py')
    for file in files:
        test_compliance.__doc__ = '{} should comply with pep8'.format(file)
        style_guide = pep8.StyleGuide(quiet=True)
        total_errors = style_guide.input_file(file)
        msg = '{} is not pep8-compliant'.format(file)
        yield nose.assert_equal, total_errors, 0, msg
