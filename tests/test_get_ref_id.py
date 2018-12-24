# tests.test_get_ref_id
# coding=utf-8

from __future__ import print_function, unicode_literals

import nose.tools as nose

import yvs.get_ref_id as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_get_ref_id(out):
    """should get ID for copied reference"""
    yvs.main('Psalm 23 (NIV)\nLorem ipsum dolor sit amet')
    output = out.getvalue().strip()
    nose.assert_equal(output, 'Psalm 23 (NIV)')
