#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import json
from xml.etree import ElementTree as ET

alfred_data_dir = os.path.join(os.path.expanduser('~'),
                               'Library', 'Application Support',
                               'Alfred 2', 'Workflow Data',
                               'com.calebevans.youversionsuggest')

prefs_path = os.path.join(alfred_data_dir, 'preferences.json')


def get_package_path():

    if '__file__' in globals():
        package_path = os.path.dirname(os.path.realpath(__file__))
    else:
        package_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    return package_path


def get_bible_data(language):

    bible_data_path = os.path.join(get_package_path(), 'data', 'bible',
                                   '{}.json'.format(language))
    with open(bible_data_path, 'r') as bible_data_file:
        bible_data = json.load(bible_data_file)

    return bible_data


def get_book(books, book_id):
    for book in books:
        if book['id'] == book_id:  # pragma: no cover
            return book['name']
    return None


def get_version(versions, version_id):
    for version in versions:
        if version['id'] == version_id:  # pragma: no cover
            return version
    return None


# Constructs an Alfred XML string from the given results list
def get_result_list_xml(results):

    root = ET.Element('items')

    for result in results:
        # Create <item> element for result with appropriate attributes
        item = ET.SubElement(root, 'item', {
            'uid': result['uid'],
            'arg': result.get('arg', ''),
            'valid': result.get('valid', 'yes')
        })
        # Create appropriate child elements of <item> element
        title = ET.SubElement(item, 'title')
        title.text = result['title']
        subtitle = ET.SubElement(item, 'subtitle')
        subtitle.text = result['subtitle']
        icon = ET.SubElement(item, 'icon')
        icon.text = 'icon.png'

    return ET.tostring(root)


def create_prefs():

    os.makedirs(alfred_data_dir, 0o755)
    defaults_path = os.path.join(get_package_path(), 'data',
                                 'defaults.json')

    with open(defaults_path, 'r') as defaults_file:
        defaults_text = defaults_file.read()
        with open(prefs_path, 'w') as prefs_file:
            prefs_file.write(defaults_text)

    return json.loads(defaults_text)


def get_prefs():

    try:
        # Create preferences file if it doesn't exist
        prefs = create_prefs()
    except OSError:
        # Otherwise, update existing preferences file
        with open(prefs_path, 'r') as prefs_file:
            prefs = json.load(prefs_file)

    return prefs


def update_prefs(prefs):

    with open(prefs_path, 'w') as prefs_file:
        json.dump(prefs, prefs_file)
