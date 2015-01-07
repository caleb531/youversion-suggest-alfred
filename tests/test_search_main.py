#!/usr/bin/env python
import unittest
import yv_suggest.search as yvs
from xml.etree import ElementTree as ET
from StringIO import StringIO
import sys

class SearchMainTestCase(unittest.TestCase):
    '''test the main search function called by the workflow'''

    def capture_output(self, callback, *args):
        '''returns stdout output from callback'''
        original_stdout = sys.stdout
        output = ''
        try:
            out = StringIO()
            sys.stdout = out
            callback(*args)
            output = out.getvalue()
        finally:
            sys.stdout = original_stdout
            return output


    def test_output(self):
        '''should output result list XML'''
        query_str = 'genesis 50:20'
        output = self.capture_output(yvs.main, query_str).strip()
        results = yvs.get_result_list(query_str)
        xml = yvs.get_result_list_xml(results).strip()
        self.assertEqual(output, xml)

    def test_null_result(self):
        '''should output "No Results" XML item for empty result lists'''
        query_str = 'nothing'
        xml = self.capture_output(yvs.main, query_str).strip()
        root = ET.fromstring(xml)
        item = root.find('item')
        self.assertIsNotNone(item, '<item> element is missing')
        self.assertEqual(item.get('valid'), 'no')
        title = item.find('title')
        self.assertEqual(title.text, 'No Results')

if __name__ == '__main__':
    unittest.main()
