#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import json


def get_language():
    return preferred_language

preferred_language = 'en'


def get_package_path():

    if '__file__' in globals():
        package_path = os.path.dirname(os.path.realpath(__file__))
    else:
        package_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    return package_path


def get_bible_data():

    path = os.path.join(get_package_path(), 'bible',
                        '{}.json'.format(get_language()))
    with open(path, 'r') as file:
        data = json.load(file)

    return data


def get_book(books, book_id):
    for book in books:
        if book['id'] == book_id:  # pragma: no cover
            return book['name']


def get_version(versions, version_id):
    for version in versions:
        if version['id'] == version_id:  # pragma: no cover
            return version
