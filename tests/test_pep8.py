#!/usr/bin/env python

import unittest
import pep8
import glob
import os


class TestPep8(unittest.TestCase):
    """test all python source files for pep8 compliance"""

    def test_source_pep8_compliant(self):
        """source files should comply with pep8"""
        style_guide = pep8.StyleGuide(quiet=True)
        result = style_guide.check_files(glob.iglob('yv_suggest/*.py'))
        self.assertEqual(result.total_errors, 0,
                         'Source files are not pep8-compliant')

    def test_test_pep8_compliant(self):
        """unit tests should comply with pep8"""
        style_guide = pep8.StyleGuide(quiet=True)
        result = style_guide.check_files(glob.iglob('tests/*.py'))
        self.assertEqual(result.total_errors, 0,
                         'Unit tests are not pep8-compliant')

if __name__ == '__main__':
    unittest.main()
