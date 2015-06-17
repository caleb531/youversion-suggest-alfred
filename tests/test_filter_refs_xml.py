#!/usr/bin/env python

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs
from xml.etree import ElementTree as ET


def test_validity():
    """should return syntactically-valid XML"""
    results = yvs.get_result_list('john 3:16')
    xml = yvs.shared.get_result_list_xml(results)
    nose.assert_is_instance(ET.fromstring(xml), ET.Element)


def test_structure():
    """XML should match result list"""
    results = yvs.get_result_list('matthew 6:34')
    result = results[0]
    xml = yvs.shared.get_result_list_xml(results)
    root = ET.fromstring(xml)
    nose.assert_equal(root.tag, 'items',
                      'root element must be named <items>')
    item = root.find('item')
    nose.assert_is_not_none(item, '<item> element is missing')
    nose.assert_equal(item.get('uid'), result['uid'])
    nose.assert_equal(item.get('arg'), result['arg'])
    nose.assert_equal(item.get('valid'), 'yes')
    title = item.find('title')
    nose.assert_is_not_none(title, '<title> element is missing')
    nose.assert_equal(title.text, result['title'])
    subtitle = item.find('subtitle')
    nose.assert_is_not_none(subtitle, '<subtitle> element is missing')
    nose.assert_equal(subtitle.text, result['subtitle'])
    icon = item.find('icon')
    nose.assert_is_not_none(icon, '<icon> element is missing')
    nose.assert_equal(icon.text, 'icon.png')
