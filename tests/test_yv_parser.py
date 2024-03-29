#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import Mock, NonCallableMock, patch

from tests import YVSTestCase
from yvs.web import YVParser

with open("tests/html/psa.23.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


class TestYVParser(YVSTestCase):

    def setUp(self):
        patch_urlopen.start()
        super().setUp()

    def tearDown(self):
        patch_urlopen.stop()
        super().tearDown()

    @patch("yvs.web.YVParser.handle_data")
    def test_charref_name(self, handle_data):
        """should evaluate named character references"""
        parser = YVParser()
        parser.feed("&deg;")
        handle_data.assert_called_once_with("°")

    @patch("yvs.web.YVParser.handle_data")
    def test_charref_dec(self, handle_data):
        """should evaluate decimal character references"""
        parser = YVParser()
        parser.feed("&#176;")
        handle_data.assert_called_once_with("°")

    @patch("yvs.web.YVParser.handle_data")
    def test_charref_hex(self, handle_data):
        """should evaluate hexadecimal character references"""
        parser = YVParser()
        parser.feed("&#x00b0;")
        handle_data.assert_called_once_with("°")
