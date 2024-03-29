#!/usr/bin/env python3
# coding=utf-8

import unittest
from gzip import GzipFile
from io import BytesIO
from unittest.mock import Mock, NonCallableMock, patch

from nose2.tools.decorators import with_setup, with_teardown

import tests
import yvs.web as web

case = unittest.TestCase()

with open("tests/html/psa.23.html") as html_file:
    html_content = html_file.read()
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_content)),
    )


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@with_setup(set_up)
@with_teardown(tear_down)
@patch("urllib.request.Request")
def test_get_url_content(request):
    """should fetch uncompressed URL content"""
    url = "https://www.bible.com/bible/59/psa.23"
    web.get_url_content(url)
    request.assert_called_once_with(
        url,
        headers={
            "User-Agent": "YouVersion Suggest",
            "Accept-Encoding": "gzip, deflate",
        },
    )


@with_setup(set_up)
@with_teardown(tear_down)
@patch("urllib.request.urlopen")
@patch("urllib.request.Request")
def test_get_url_content_timeout(request, urlopen):
    """should timeout URL content request after 3 seconds"""
    web.get_url_content("https://www.bible.com/bible/59/psa.23")
    urlopen.assert_called_once_with(request.return_value, timeout=5)


@with_setup(set_up)
@with_teardown(tear_down)
@patch("urllib.request.Request")
def test_get_url_content_compressed(request):
    """should automatically decompress compressed URL content"""
    url = "https://www.bible.com/bible/59/psa.23"
    gzip_buf = BytesIO()
    with GzipFile(fileobj=gzip_buf, mode="wb") as gzip_file:
        gzip_file.write(html_content.encode("utf-8"))
    gzipped_content = gzip_buf.getvalue()
    response_mock = NonCallableMock(
        read=Mock(return_value=gzipped_content),
        info=Mock(return_value=NonCallableMock(get=Mock(return_value="gzip"))),
    )
    with patch("urllib.request.urlopen", return_value=response_mock):
        url_content = web.get_url_content(url)
        case.assertEqual(url_content, html_content)


@with_setup(set_up)
@with_teardown(tear_down)
@patch("urllib.request.Request")
def test_get_url_content_optimized(request):
    """should optimize returned HTML by stripping <script> tags, etc."""
    url = "https://www.bible.com/bible/59/psa.23"
    html = web.get_url_content(url)
    optimized_html = web.optimize_html(html)
    case.assertIn("<script", html)
    case.assertIn("Lorem ipsum", html)
    case.assertNotIn("<script", optimized_html)
    case.assertIn("Lorem ipsum", optimized_html)
