#!/usr/bin/env python
# -*- coding: utf-8 -*-


class WebbrowserMock(object):
    """mock the builtin webbrowser module"""

    def open(self, url):
        """mock the webbrowser.open() function"""
        self.url = url
