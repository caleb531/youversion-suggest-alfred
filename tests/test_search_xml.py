#!/usr/bin/env python
import unittest
import yv_suggest.search as yvs
from xml.etree import ElementTree as ET


class SearchXmlTestCase(unittest.TestCase):
    """test the integrity of the result list XML"""

    def test_validity(self):
        """should be valid XML"""
        results = yvs.get_result_list('john 3:16')
        xml = yvs.get_result_list_xml(results)
        try:
            self.assertIsInstance(ET.fromstring(xml), ET.Element)
        except ET.ParseError:
            self.fail('result list XML is not valid')

    def test_structure(self):
        """should contain necessary elements/attributes/values"""
        results = yvs.get_result_list('matthew 6:34')
        result = results[0]
        xml = yvs.get_result_list_xml(results)
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, 'items', 'root element incorrectly named')
        item = root.find('item')
        self.assertIsNotNone(item, '<item> element is missing')
        self.assertEqual(item.get('uid'), result['uid'])
        self.assertEqual(item.get('arg'), result['arg'])
        self.assertEqual(item.get('valid'), 'yes')
        title = item.find('title')
        self.assertIsNotNone(title, '<title> element is missing')
        self.assertEqual(title.text, result['title'])
        subtitle = item.find('subtitle')
        self.assertIsNotNone(subtitle, '<subtitle> element is missing')
        self.assertEqual(subtitle.text, result['subtitle'])
        icon = item.find('icon')
        self.assertIsNotNone(icon, '<icon> element is missing')
        self.assertEqual(icon.text, 'icon.png')

if __name__ == '__main__':
    unittest.main()
