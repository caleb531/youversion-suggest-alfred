#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os
import os.path
import json
import re
import unicodedata
from xml.etree import ElementTree as ET

alfred_data_dir = os.path.join(os.path.expanduser('~'),
                               'Library', 'Application Support',
                               'Alfred 2', 'Workflow Data',
                               'com.calebevans.youversionsuggest')

prefs_path = os.path.join(alfred_data_dir, 'preferences.json')
recent_refs_path = os.path.join(alfred_data_dir, 'recent.json')

max_recent_refs = 10


def get_package_path():

    if '__file__' in globals():
        package_path = os.path.dirname(os.path.realpath(__file__))
    else:
        package_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    return package_path


def create_alfred_data_dir():

    try:
        os.makedirs(alfred_data_dir, 0o755)
    except OSError:
        pass


def get_bible_data(language):

    bible_data_path = os.path.join(get_package_path(), 'data', 'bible',
                                   'language-{}.json'.format(language))
    with open(bible_data_path, 'r') as bible_data_file:
        bible_data = json.load(bible_data_file)

    return bible_data


def get_chapter_data():

    chapter_data_path = os.path.join(get_package_path(), 'data', 'bible',
                                     'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        chapter_data = json.load(chapter_data_file)

    return chapter_data


def create_recent_refs():

    create_alfred_data_dir()
    recent_refs = []
    with open(recent_refs_path, 'w') as recent_refs_file:
        json.dump(recent_refs, recent_refs_file)

    return recent_refs


def get_recent_refs():

    try:
        with open(recent_refs_path, 'r') as recent_refs_file:
            recent_refs = json.load(recent_refs_file)
    except IOError:  # pragma: no cover
        recent_refs = create_recent_refs()

    return recent_refs


def update_recent_refs(recent_refs):
    with open(recent_refs_path, 'w') as recent_refs_file:
        json.dump(recent_refs, recent_refs_file)


def push_recent_ref(ref_uid, save=True):

    recent_refs = get_recent_refs()
    if ref_uid in recent_refs:
        recent_refs.remove(ref_uid)
    recent_refs.insert(0, ref_uid)
    if len(recent_refs) > max_recent_refs:
        recent_refs.pop()
    update_recent_refs(recent_refs)


def delete_recent_refs():

    try:
        os.remove(recent_refs_path)
    except OSError:
        pass


def get_book(books, book_id):

    for book in books:  # pragma: no cover
        if book['id'] == book_id:
            return book['name']


def query_matches_book(query_book, book_name):
    return (book_name.startswith(query_book) or
            (book_name[0].isnumeric() and
             book_name[2:].startswith(query_book)))


def get_version(versions, version_id):

    for version in versions:  # pragma: no cover
        if version['id'] == version_id:
            return version


def get_versions(language):

    bible = get_bible_data(language)
    return bible['versions']


def get_languages():

    languages_path = os.path.join(get_package_path(),
                                  'data', 'languages.json')
    with open(languages_path, 'r') as languages_file:
        languages = json.load(languages_file)

    return languages


def get_defaults():

    defaults_path = os.path.join(get_package_path(), 'data',
                                 'defaults.json')
    with open(defaults_path, 'r') as defaults_file:
        defaults = json.load(defaults_file)

    return defaults


def create_prefs():

    create_alfred_data_dir()
    defaults = get_defaults()
    with open(prefs_path, 'w') as prefs_file:
        json.dump(defaults, prefs_file)

    return defaults


def get_prefs(prefs=None):

    if prefs is not None:
        if 'language' not in prefs:
            prefs = get_defaults()
    else:
        try:
            with open(prefs_path, 'r') as prefs_file:
                prefs = json.load(prefs_file)
        except IOError:  # pragma: no cover
            prefs = create_prefs()

    return prefs


def update_prefs(prefs):

    with open(prefs_path, 'w') as prefs_file:
        json.dump(prefs, prefs_file)


def delete_prefs():

    try:
        os.remove(prefs_path)
    except OSError:
        pass


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


# Parses query string into components of a Bible reference
def get_ref_matches(query_str):

    # Pattern for parsing any bible reference
    patt = '^{book}(?:{chapter}(?:{verse}{endverse})?{version})?$'.format(
        book='(\d?(?:[^\W\d_]|\s)+|\d)\s?',
        chapter='(\d+)\s?',
        verse='(\d+)\s?',
        endverse='(\d+)?\s?',
        version='([a-z]+\d*)?.*?')
    return re.search(patt, query_str, flags=re.UNICODE)


# Builds the query object from the given query string
def get_query_object(query_str):

    # Match section of the bible based on query
    ref_matches = get_ref_matches(query_str)

    if not ref_matches:
        return None

    # Create query object for storing query data
    query = {}

    book_match = ref_matches.group(1)
    query['book'] = book_match.rstrip()

    chapter_match = ref_matches.group(2)
    if chapter_match:
        query['chapter'] = int(chapter_match)

        verse_match = ref_matches.group(3)
        if verse_match:
            query['verse'] = int(verse_match)

            verse_range_match = ref_matches.group(4)
            if verse_range_match:
                query['endverse'] = int(verse_range_match)

        version_match = ref_matches.group(5)
        if version_match:
            query['version'] = version_match.lstrip().upper()

    return query


# Parse the given reference UID into a dictionary
def get_ref_object(ref_uid, prefs=None):

    patt = '{version}/{book_id}\.{chapter}(?:\.{verse}{endverse})?'.format(
        version='(\d+)',
        book_id='(\d?[a-z]+)',
        chapter='(\d+)',
        verse='(\d+)',
        endverse='(?:-(\d+))?')

    ref_uid_matches = re.match(patt, ref_uid)
    ref = {}

    book_id = ref_uid_matches.group(2)
    prefs = get_prefs(prefs)
    bible = get_bible_data(prefs['language'])
    book_name = get_book(bible['books'], book_id)
    ref['book'] = book_name

    chapter = ref_uid_matches.group(3)
    ref['chapter'] = chapter

    verse_match = ref_uid_matches.group(4)
    if verse_match:
        ref['verse'] = int(verse_match)

    endverse_match = ref_uid_matches.group(5)
    if endverse_match:
        ref['endverse'] = int(endverse_match)

    version_id = int(ref_uid_matches.group(1))
    version_name = get_version(bible['versions'],
                               version_id)['name']
    ref['version'] = version_name

    return ref


# Retrieve the full reference identifier from the shorthand reference UID
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
