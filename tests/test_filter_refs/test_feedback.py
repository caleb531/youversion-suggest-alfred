#!/usr/bin/env python3
# coding=utf-8

import json

import yvs.core as core
import yvs.filter_refs as filter_refs


def test_validity():
    """should return syntactically-valid JSON"""

    results = filter_refs.get_result_list("john 3:16")
    feedback_str = core.get_result_list_feedback_str(results)

    assert isinstance(json.loads(feedback_str), dict)


def test_structure():
    """JSON should match result list"""

    results = filter_refs.get_result_list("matthew 6:34")
    result = results[0]
    feedback_str = core.get_result_list_feedback_str(results)
    feedback = json.loads(feedback_str)

    assert "items" in feedback, "feedback object must have result items"
    item = feedback["items"][0]
    assert item["uid"] == result["uid"]
    assert item["arg"] == result["arg"]
    assert item["title"] == "Matthew 6:34 (NIV)"
    assert item["text"]["copy"] == result["title"]
    assert item["text"]["largetype"] == result["title"]
    assert item["subtitle"] == result["subtitle"]
    assert item["icon"]["path"] == "icon.png"
