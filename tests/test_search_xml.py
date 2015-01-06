#!/usr/bin/env python
import unittest
import yv_suggest as yvs
from xml.etree import ElementTree as ET

class SearchXmlTestCase(unittest.TestCase):
    '''test the integrity of the result list XML'''

    def test_search_xml_validity(self):
        '''should be valid XML'''
        results = yvs.get_result_list('john 3:16')
        xml = yvs.get_result_list_xml(results)
        try:
            self.assertIsInstance(ET.fromstring(xml), ET.Element)
        except ET.ParseError:
            self.fail('result list XML is not valid')

    def test_search_xml_attrs(self):
        '''should match the attributes of each result in the result list'''
        results = yvs.get_result_list('matthew 6:34')
        result = results[0]
        xml = yvs.get_result_list_xml(results)
        root = ET.fromstring(xml)
        item = root.find('item')
        title = item.find('title')
        subtitle = item.find('subtitle')
        self.assertEqual(item.get('uid'), result.uid)
        self.assertEqual(item.get('arg'), result.arg)
        self.assertEqual(title.text, result.title)
        self.assertEqual(subtitle.text, result.subtitle)

if __name__ == '__main__':
    unittest.main()
