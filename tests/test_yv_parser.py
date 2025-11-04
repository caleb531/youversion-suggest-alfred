#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import Mock, NonCallableMock, patch

import pytest

from yvs.web import YVParser

with open("tests/html/psa.23.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


@pytest.fixture(autouse=True)
def _patch_urlopen():
    with patch_urlopen:
        yield


@patch("yvs.web.YVParser.handle_data")
def test_charref_name(handle_data):
    """should evaluate named character references"""

    parser = YVParser()
    parser.feed("&deg;")

    handle_data.assert_called_once_with("°")


@patch("yvs.web.YVParser.handle_data")
def test_charref_dec(handle_data):
    """should evaluate decimal character references"""

    parser = YVParser()
    parser.feed("&#176;")

    handle_data.assert_called_once_with("°")


@patch("yvs.web.YVParser.handle_data")
def test_charref_hex(handle_data):
    """should evaluate hexadecimal character references"""

    parser = YVParser()
    parser.feed("&#x00b0;")

    handle_data.assert_called_once_with("°")
