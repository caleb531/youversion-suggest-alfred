#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import os
import os.path
import json
import re
import sys
import unicodedata
from xml.etree import ElementTree as ET

alfred_data_dir = os.path.join(
    os.path.expanduser('~'), 'Library', 'Application Support', 'Alfred 2',
    'Workflow Data', 'com.calebevans.youversionsuggest')

prefs_path = os.path.join(alfred_data_dir, 'preferences.json')
data_path = os.path.join(os.getcwd(), 'yvs', 'data')


def create_alfred_data_dir():

    try:
        os.makedirs(alfred_data_dir)
    except OSError:
        pass


def get_bible_data(language):

    bible_data_path = os.path.join(
        data_path, 'bible', 'language-{}.json'.format(language))
    with open(bible_data_path, 'r') as bible_data_file:
        return json.load(bible_data_file)


def get_chapter_data():

    chapter_data_path = os.path.join(data_path, 'bible', 'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        return json.load(chapter_data_file)


# Get name of first book whose id matches the given id
def get_book(books, book_id):

    return next(
        book['name'] for book in books if book['id'] == book_id)


# Get first version object whose id matches the given id
def get_version(versions, version_id):

    return next(
        version for version in versions if version['id'] == version_id)


def get_versions(language):

    bible = get_bible_data(language)
    return bible['versions']


def get_languages():

    languages_path = os.path.join(data_path, 'languages.json')
    with open(languages_path, 'r') as languages_file:
        return json.load(languages_file)


# Functions for accessing/manipulating mutable preferences


def get_defaults():

    defaults_path = os.path.join(data_path, 'defaults.json')
    with open(defaults_path, 'r') as defaults_file:
        return json.load(defaults_file)


def create_prefs():

    create_alfred_data_dir()
    defaults = get_defaults()
    with open(prefs_path, 'w') as prefs_file:
        json.dump(defaults, prefs_file)

    return defaults


def get_prefs():

    try:
        with open(prefs_path, 'r') as prefs_file:
            return json.load(prefs_file)
    except IOError:
        return create_prefs()


def update_prefs(prefs):

    with open(prefs_path, 'w') as prefs_file:
        json.dump(prefs, prefs_file)


# Constructs an Alfred XML string from the given results list
def get_result_list_xml(results):

    root = ET.Element('items')

    for result in results:
        # Create <item> element for result with appropriate attributes
        item = ET.SubElement(root, 'item', {
            'arg': result.get('arg', ''),
            'valid': result.get('valid', 'yes')
        })
        if 'uid' in result:
            item.set('uid', result['uid'])
        if 'autocomplete' in result:
            item.set('autocomplete', result['autocomplete'])
        # Create appropriate child elements of <item> element
        title = ET.SubElement(item, 'title')
        title.text = result['title']
        copy = ET.SubElement(item, 'text', {
            'type': 'copy'
        })
        copy.text = result['title']
        largetype = ET.SubElement(item, 'text', {
            'type': 'largetype'
        })
        largetype.text = result['title']
        subtitle = ET.SubElement(item, 'subtitle')
        subtitle.text = result['subtitle']
        icon = ET.SubElement(item, 'icon')
        icon.text = 'icon.png'

    return ET.tostring(root)


# Query-related functions


# Determines if the given query string matches the given book name
def query_matches_book(query_book, book_name):
    return (book_name.startswith(query_book) or
            (book_name[0].isnumeric() and
             book_name[2:].startswith(query_book)))


# Simplifies the format of the query string
def format_query_str(query_str):

    query_str = query_str.lower()
    # Normalize all Unicode characters
    query_str = unicodedata.normalize('NFC', query_str)
    # Remove all non-alphanumeric characters
    query_str = re.sub('[\W_]', ' ', query_str, flags=re.UNICODE)
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub('\s+', ' ', query_str)
    # Parse shorthand reference notation
    query_str = re.sub('(\d)(?=[a-z])', '\\1 ', query_str)

    return query_str


# Parses the given query string into components of a Bible reference
def get_ref_matches(query_str):

    # Pattern for parsing any bible reference
    patt = '^{book}(?:{chapter}(?:{verse}{endverse})?{version})?$'.format(
        book='(\d?(?:[^\W\d_]|\s)+|\d)\s?',
        chapter='(\d+)\s?',
        verse='(\d+)\s?',
        endverse='(\d+)?\s?',
        version='([a-z]+\d*)?.*?')
    return re.search(patt, query_str, flags=re.UNICODE)


# Parses the given reference UID into a dictionary representing that reference
def get_ref_object(ref_uid):

    patt = '{version}/{book_id}\.{chapter}(?:\.{verse}{endverse})?'.format(
        version='(\d+)',
        book_id='(\d?[a-z]+)',
        chapter='(\d+)',
        verse='(\d+)',
        endverse='(?:-(\d+))?')

    ref_uid_matches = re.match(patt, ref_uid)
    ref = {
        'uid': ref_uid
    }

    book_id = ref_uid_matches.group(2)
    prefs = get_prefs()
    bible = get_bible_data(prefs['language'])
    book_name = get_book(bible['books'], book_id)
    ref['book'] = book_name
    ref['book_id'] = book_id

    chapter = ref_uid_matches.group(3)
    ref['chapter'] = chapter

    verse_match = ref_uid_matches.group(4)
    if verse_match:
        ref['verse'] = int(verse_match)

    endverse_match = ref_uid_matches.group(5)
    if endverse_match:
        ref['endverse'] = int(endverse_match)

    version_id = int(ref_uid_matches.group(1))
    version_name = get_version(bible['versions'], version_id)['name']
    ref['version'] = version_name
    ref['version_id'] = version_id

    return ref


# Retrieves the full reference identifier from the shorthand reference UID
def get_full_ref(ref):

    full_ref = '{book} {chapter}'.format(
        book=ref['book'],
        chapter=ref['chapter'])

    if 'verse' in ref:
        full_ref += ':{verse}'.format(verse=ref['verse'])

    if 'endverse' in ref:
        full_ref += '-{endverse}'.format(endverse=ref['endverse'])

    full_ref += ' ({version})'.format(version=ref['version'])

    return full_ref
