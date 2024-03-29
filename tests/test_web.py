#!/usr/bin/env python3
# coding=utf-8


from gzip import GzipFile
from io import BytesIO
from unittest.mock import Mock, NonCallableMock, patch

import yvs.web as web
from tests import YVSTestCase

with open("tests/html/psa.23.html") as html_file:
    html_content = html_file.read()
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_content)),
    )


class TestWeb(YVSTestCase):
    pass

    def setUp(self):
        patch_urlopen.start()
        super().setUp()

    def tearDown(self):
        patch_urlopen.stop()
        super().tearDown()

    @patch("urllib.request.Request")
    def test_get_url_content(self, request):
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

    @patch("urllib.request.urlopen")
    @patch("urllib.request.Request")
    def test_get_url_content_timeout(self, request, urlopen):
        """should timeout URL content request after 3 seconds"""
        web.get_url_content("https://www.bible.com/bible/59/psa.23")
        urlopen.assert_called_once_with(request.return_value, timeout=5)

    @patch("urllib.request.Request")
    def test_get_url_content_compressed(self, request):
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
            self.assertEqual(url_content, html_content)

    @patch("urllib.request.Request")
    def test_get_url_content_optimized(self, request):
        """should optimize returned HTML by stripping <script> tags, etc."""
        url = "https://www.bible.com/bible/59/psa.23"
        html = web.get_url_content(url)
        optimized_html = web.optimize_html(html)
        self.assertIn("<script", html)
        self.assertIn("Lorem ipsum", html)
        self.assertNotIn("<script", optimized_html)
        self.assertIn("Lorem ipsum", optimized_html)
