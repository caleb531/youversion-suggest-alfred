#!/usr/bin/env python

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs
from xml.etree import ElementTree as ET
from decorators import redirect_stdout
import inspect
import sys


@redirect_stdout
def test_output(out):
    """should output ref result list XML"""
    query_str = 'genesis 50:20'
    yvs.main(query_str, prefs={})
    output = out.getvalue().strip()
    results = yvs.get_result_list(query_str, prefs={})
    xml = yvs.shared.get_result_list_xml(results).strip()
    nose.assert_equal(output, xml)


@redirect_stdout
def test_null_result(out):
    """should output "No Results" XML item for empty ref result list"""
    query_str = 'xyz'
    yvs.main(query_str, prefs={})
    xml = out.getvalue().strip()
    root = ET.fromstring(xml)
    item = root.find('item')
    nose.assert_is_not_none(item, '<item> element is missing')
    nose.assert_equal(item.get('valid'), 'no')
    title = item.find('title')
    nose.assert_equal(title.text, 'No Results')


def test_source_only():
    """should run script assuming script is not a file"""
    yvs.shared.sys.argv[0] = yvs.shared.__file__
    del yvs.shared.__file__
    results = yvs.get_result_list('e', prefs={})
    nose.assert_equal(len(results), 6)
    yvs.shared.__file__ = yvs.shared.sys.argv[0]
