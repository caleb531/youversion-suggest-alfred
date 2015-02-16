#!/usr/bin/env python

import nose.tools as nose
import pep8
import glob


def test_source_compliance():
    """source files should comply with pep8"""
    style_guide = pep8.StyleGuide(quiet=True)
    files = glob.iglob('*/*.py')
    for file in files:
        result = style_guide.check_files((file,))
        msg = '{file} is not pep8-compliant'.format(file=file)
        yield nose.assert_equal, result.total_errors, 0, msg
