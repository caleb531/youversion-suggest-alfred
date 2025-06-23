#!/usr/bin/env python3
# coding=utf-8

import json

import yvs.core as core
import yvs.filter_refs as filter_refs
from tests import YVSTestCase
from tests.decorators import redirect_stdout


class TestMain(YVSTestCase):
    @redirect_stdout
    def test_output(self, out):
        """should output ref result list JSON"""
        query_str = "genesis 50:20"
        filter_refs.main(query_str)
        output = out.getvalue().rstrip()
        results = filter_refs.get_result_list(query_str)
        feedback = core.get_result_list_feedback_str(results).rstrip()
        self.assertEqual(output, feedback)

    @redirect_stdout
    def test_null_result(self, out):
        """should output "No Results" JSON item for empty ref result list"""
        query_str = "xyz"
        filter_refs.main(query_str)
        feedback_str = out.getvalue()
        feedback = json.loads(feedback_str)
        self.assertEqual(len(feedback["items"]), 1, "result item is missing")
        item = feedback["items"][0]
        self.assertEqual(item["title"], "No Results")
        self.assertEqual(item["valid"], False)
