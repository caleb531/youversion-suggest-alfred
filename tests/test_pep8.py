#!/usr/bin/env python

import nose.tools as nose
import pep8
import glob


def test_source_compliance():
    """source files should comply with pep8"""
    files = glob.iglob('*/*.py')
    for file in files:
        style_guide = pep8.StyleGuide(quiet=True)
        total_errors = style_guide.input_file(file)
        msg = '{} is not pep8-compliant'.format(file)
        yield nose.assert_equal, total_errors, 0, msg
