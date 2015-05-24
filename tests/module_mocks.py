#!/usr/bin/env python


class WebbrowserMock(object):
    """mock the builtin webbrowser module"""

    def open(self, url):
        self.url = url
