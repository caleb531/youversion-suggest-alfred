#!/usr/bin/env python

from __future__ import unicode_literals
import sys
import nose.tools as nose
import yvs.filter_refs as yvs
from xml.etree import ElementTree as ET
from mock import patch
from tests.decorators import redirect_stdout


@redirect_stdout
def test_output(out):
    """should output ref result list XML"""
    query_str = 'genesis 50:20'
    yvs.main(query_str)
    output = out.getvalue().strip()
    results = yvs.get_result_list(query_str)
    xml = yvs.shared.get_result_list_xml(results).strip()
    nose.assert_equal(output, xml)


@redirect_stdout
def test_null_result(out):
    """should output "No Results" XML item for empty ref result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    xml = out.getvalue().strip()
    root = ET.fromstring(xml)
    item = root.find('item')
    nose.assert_is_not_none(item, '<item> element is missing')
    nose.assert_equal(item.get('valid'), 'no')
    title = item.find('title')
    nose.assert_equal(title.text, 'No Results')
