#!/usr/bin/env python3
# coding=utf-8

import json
import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_output(out):
    """should output ref result list JSON"""
    query_str = 'genesis 50:20'
    yvs.main(query_str)
    output = out.getvalue().rstrip()
    results = yvs.get_result_list(query_str)
    feedback = yvs.core.get_result_list_feedback_str(results).rstrip()
    case.assertEqual(output, feedback)


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_null_result(out):
    """should output "No Results" JSON item for empty ref result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    feedback_str = out.getvalue()
    feedback = json.loads(feedback_str)
    case.assertEqual(len(feedback['items']), 1, 'result item is missing')
    item = feedback['items'][0]
    case.assertEqual(item['title'], 'No Results')
    case.assertEqual(item['valid'], False)
