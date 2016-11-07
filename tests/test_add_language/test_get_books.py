# tests.test_add_language.test_get_books
# coding=utf-8

from __future__ import unicode_literals
from mock import patch, Mock, NonCallableMock

import nose.tools as nose

import tests.test_add_language as tests
import utilities.add_language as add_lang

with open('tests/html/books.html') as html_file:
    html_content = html_file.read()
    patch_urlopen = patch(
        'urllib2.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_content)))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
def test_get_books():
    """should fetch book list in proper format"""
    books = add_lang.get_books(default_version=75)
    nose.assert_equal(len(books), 3)
    nose.assert_list_equal(books, [
        {
            'id': 'gen',
            'name': 'Genesis',
        },
        {
            'id': '1sa',
            'name': '1 Samuël',
        },
        {
            'id': 'jhn',
            'name': 'Johannes',
        }
    ])


@nose.with_setup(set_up, tear_down)
@patch('yvs.shared.get_url_content', return_value=html_content)
def test_get_books_url(get_url_content):
    """should fetch book list for the given default version"""
    default_version = 75
    add_lang.get_books(default_version)
    get_url_content.assert_called_once_with(
        'https://www.bible.com/bible/{}/jhn.1'.format(default_version))
