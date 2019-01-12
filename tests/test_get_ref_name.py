# tests.test_get_ref_name
# coding=utf-8

from __future__ import unicode_literals

import nose.tools as nose

import yvs.get_ref_name as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_get_ref_name(out):
    """should get name from reference UID"""
    yvs.main('111/psa.23')
    output = out.getvalue()
    nose.assert_equal(output, 'Psalm 23 (NIV)')
