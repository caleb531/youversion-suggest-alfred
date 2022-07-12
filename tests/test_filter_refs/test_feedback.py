#!/usr/bin/env python3
# coding=utf-8

import json
import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_validity():
    """should return syntactically-valid JSON"""
    results = yvs.get_result_list('john 3:16')
    feedback_str = yvs.core.get_result_list_feedback_str(results)
    case.assertIsInstance(json.loads(feedback_str), dict)


@with_setup(set_up)
@with_teardown(tear_down)
def test_structure():
    """JSON should match result list"""
    results = yvs.get_result_list('matthew 6:34')
    result = results[0]
    feedback_str = yvs.core.get_result_list_feedback_str(results)
    feedback = json.loads(feedback_str)
    case.assertIn('items', feedback, 'feedback object must have result items')
    item = feedback['items'][0]
    case.assertEqual(item['uid'], result['uid'])
    case.assertEqual(item['arg'], result['arg'])
    case.assertEqual(
        item['quicklookurl'], 'https://www.bible.com/bible/111/MAT.6.34')
    case.assertEqual(item['title'], 'Matthew 6:34 (NIV)')
    case.assertEqual(item['text']['copy'], result['title'])
    case.assertEqual(item['text']['largetype'], result['title'])
    case.assertEqual(item['subtitle'], result['subtitle'])
    case.assertEqual(item['icon']['path'], 'icon.png')
