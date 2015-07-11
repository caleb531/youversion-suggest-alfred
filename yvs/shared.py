# yvs.shared
# coding=utf-8

from __future__ import unicode_literals
import os
import os.path
import json
import re
import urllib2
import unicodedata
from xml.etree import ElementTree as ET

ALFRED_DATA_DIR = os.path.join(
    os.path.expanduser('~'), 'Library', 'Application Support', 'Alfred 2',
    'Workflow Data', 'com.calebevans.youversionsuggest')

PREFS_PATH = os.path.join(ALFRED_DATA_DIR, 'preferences.json')
DATA_PATH = os.path.join(os.getcwd(), 'yvs', 'data')

USER_AGENT = 'YouVersion Suggest'


def create_alfred_data_dir():

    try:
        os.makedirs(ALFRED_DATA_DIR)
    except OSError:
        pass


def get_bible_data(language):

    bible_data_path = os.path.join(
        DATA_PATH, 'bible', 'language-{}.json'.format(language))
    with open(bible_data_path, 'r') as bible_data_file:
        return json.load(bible_data_file)


def get_chapter_data():

    chapter_data_path = os.path.join(DATA_PATH, 'bible', 'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        return json.load(chapter_data_file)


# Get name of first book whose id matches the given id
def get_book(books, book_id):

    return next(book['name'] for book in books if book['id'] == book_id)


# Get first version object whose id matches the given id
def get_version(versions, version_id):

    return next(version for version in versions if version['id'] == version_id)


def get_versions(language):

    bible = get_bible_data(language)
    return bible['versions']


def get_languages():

    languages_path = os.path.join(DATA_PATH, 'languages.json')
    with open(languages_path, 'r') as languages_file:
        return json.load(languages_file)


# Functions for accessing/manipulating mutable preferences


def get_defaults():

    defaults_path = os.path.join(DATA_PATH, 'defaults.json')
    with open(defaults_path, 'r') as defaults_file:
        return json.load(defaults_file)


def create_prefs():

    create_alfred_data_dir()
    defaults = get_defaults()
    with open(PREFS_PATH, 'w') as prefs_file:
        json.dump(defaults, prefs_file)

    return defaults


def get_prefs():

    try:
        with open(PREFS_PATH, 'r') as prefs_file:
            return json.load(prefs_file)
    except IOError:
        return create_prefs()


def update_prefs(prefs):

    with open(PREFS_PATH, 'w') as prefs_file:
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
        copy.text = result.get('copy', result['title'])
        largetype = ET.SubElement(item, 'text', {
            'type': 'largetype'
        })
        largetype.text = result.get('largetype', result['title'])
        subtitle = ET.SubElement(item, 'subtitle')
        subtitle.text = result['subtitle']
        icon = ET.SubElement(item, 'icon')
        icon.text = 'icon.png'

    return ET.tostring(root)


# Query-related functions

# Simplifies the format of the query string
def format_query_str(query_str):

    query_str = query_str.lower()
    # Normalize all Unicode characters
    query_str = unicodedata.normalize('NFC', query_str)
    # Remove all non-alphanumeric characters
    query_str = re.sub(r'[\W_]', ' ', query_str, flags=re.UNICODE)
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub(r'\s+', ' ', query_str)
    # Parse shorthand reference notation
    query_str = re.sub(r'(\d)(?=[a-z])', '\\1 ', query_str)

    return query_str


# Parses the given reference UID into a dictionary representing that reference
def get_ref_object(ref_uid):

    patt = r'^{version}/{book_id}\.{chapter}(?:\.{verse}{endverse})?$'.format(
        version=r'(\d+)',
        book_id=r'(\d?[a-z]+)',
        chapter=r'(\d+)',
        verse=r'(\d+)',
        endverse=r'(?:-(\d+))?')

    ref_uid_matches = re.match(patt, ref_uid)
    ref = {
        'uid': ref_uid,
        'book_id': ref_uid_matches.group(2),
        'version_id': int(ref_uid_matches.group(1)),
        'chapter': int(ref_uid_matches.group(3))
    }

    # Include book name using book ID and currently-set language
    prefs = get_prefs()
    bible = get_bible_data(prefs['language'])
    book_name = get_book(bible['books'], ref['book_id'])
    ref['book'] = book_name

    # Include verse number if it exists
    verse_match = ref_uid_matches.group(4)
    if verse_match:
        ref['verse'] = int(verse_match)

    # Include end verse number if it exists
    endverse_match = ref_uid_matches.group(5)
    if endverse_match:
        ref['endverse'] = int(endverse_match)

    # Include full version name (acronym) if it exists
    version_name = get_version(bible['versions'], ref['version_id'])['name']
    ref['version'] = version_name

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


# Simplify format of reference content by removing unnecessary whitespace
def format_ref_content(ref_content):

    # Collapse consecutive spaces to single space
    ref_content = re.sub(r' {2,}', ' ', ref_content)
    # Collapse sequences of three or more newlines into two
    ref_content = re.sub(r'\n{3,}', '\n\n', ref_content)
    # Strip leading/trailing whitespace for entire reference
    ref_content = re.sub(r'(^\s+)|(\s+$)', '', ref_content)
    # Strip leading/trailing whitespace for each paragraph
    ref_content = re.sub(r' ?\n ?', '\n', ref_content)
    return ref_content


# Retrieve HTML contents of the given URL as a Unicode string
def get_url_content(url):

    request = urllib2.Request(url, headers={'User-Agent': USER_AGENT})
    connection = urllib2.urlopen(request)
    return connection.read().decode('utf-8')


# Evaluate character reference to its respective Unicode character
def eval_charref(name):

    if name[0] == 'x':
        # Handle hexadecimal character references
        return unichr(int(name[1:], 16))
    else:
        # Handle decimal character references
        return unichr(int(name))
