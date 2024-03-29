#!/usr/bin/env python3
# coding=utf-8

import json

import yvs.filter_refs as yvs
from tests import YVSTestCase
from tests.decorators import redirect_stdout


class TestMain(YVSTestCase):

    @redirect_stdout
    def test_output(self, out):
        """should output ref result list JSON"""
        query_str = "genesis 50:20"
        yvs.main(query_str)
        output = out.getvalue().rstrip()
        results = yvs.get_result_list(query_str)
        feedback = yvs.core.get_result_list_feedback_str(results).rstrip()
        self.assertEqual(output, feedback)

    @redirect_stdout
    def test_null_result(self, out):
        """should output "No Results" JSON item for empty ref result list"""
        query_str = "xyz"
        yvs.main(query_str)
        feedback_str = out.getvalue()
        feedback = json.loads(feedback_str)
        self.assertEqual(len(feedback["items"]), 1, "result item is missing")
        item = feedback["items"][0]
        self.assertEqual(item["title"], "No Results")
        self.assertEqual(item["valid"], False)
