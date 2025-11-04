#!/usr/bin/env python3
# coding=utf-8

import json

import yvs.core as core
import yvs.filter_refs as filter_refs
from tests.decorators import redirect_stdout


def test_output():
    """should output ref result list JSON"""

    query_str = "genesis 50:20"

    with redirect_stdout() as out:
        filter_refs.main(query_str)

    output = out.getvalue().rstrip()
    results = filter_refs.get_result_list(query_str)
    feedback = core.get_result_list_feedback_str(results).rstrip()

    assert output == feedback


def test_null_result():
    """should output "No Results" JSON item for empty ref result list"""

    query_str = "xyz"

    with redirect_stdout() as out:
        filter_refs.main(query_str)

    feedback_str = out.getvalue()
    feedback = json.loads(feedback_str)

    assert len(feedback["items"]) == 1, "result item is missing"
    item = feedback["items"][0]
    assert item["title"] == "No Results"
    assert item["valid"] is False
