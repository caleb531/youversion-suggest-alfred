#!/usr/bin/env python

# This script is a handy (albeit imperfect) tool for automatically adding
# support for any language to YouVersion Suggest.

from __future__ import unicode_literals
import argparse
import io
import itertools
import json
import os
import re
import urllib2
from operator import itemgetter
from pyquery import PyQuery as pq


# Parameters for structuring JSON data
json_params = {
    'indent': 2,
    'separators': (',', ': '),
    'ensure_ascii': False,
    'sort_keys': True
}


# Retrieve HTML contents of the given URL as a Unicode string
def get_url_content(url, **kw):

    return urllib2.urlopen(url).read().decode('utf-8')


# Parse the language name from the given category header string
def get_language_name(text):

    patt = '^\s*(.+?)(?:\s*\((\d+)\)\s*)$'
    matches = re.search(patt, text, flags=re.UNICODE)
    if matches:
        return matches.group(1)
    else:
        return None


# Construct an object representing a Bible version
def get_version(version_elem):

    link_elem = version_elem.find('a')
    url = link_elem.get('href')
    patt = '(?<=/versions/)(\d+)-([a-z]+\d*)'
    matches = re.search(patt, url, flags=re.UNICODE)
    return {
        'id': int(matches.group(1)),
        'name': matches.group(2).upper(),
    }


# Retrieve list of HTML elements, each corresponding to a Bible version
def get_version_elems(language_id):

    d = pq(url='https://www.bible.com/{}/versions'
           .format(language_id.replace('_', '-')),
           opener=get_url_content)

    category_elems = d('#main > article > ul > li')
    version_elems = None

    if category_elems:

        category_elem = category_elems[0]
        version_elems = d(category_elem).find('li')

        text = category_elem.text
        language_name = get_language_name(text)

        if not language_name:
            raise RuntimeError('Language name cannot be determined. Aborting.')

    return version_elems, language_name


# Retrieve a list of dictionaries representing Bible versions
def get_versions(language_id, max_version_id):

    print('Retrieving version data...')

    versions = []
    unique_versions = []

    version_elems, language_name = get_version_elems(language_id)

    if not version_elems:
        raise RuntimeError('Cannot find the given language. Aborting.')

    for version_elem in version_elems:
        version = get_version(version_elem)
        # Only add version if ID does not exceed a certain limit (if defined)
        if not max_version_id or version['id'] <= max_version_id:
            versions.append(version)

    # Sort and remove duplicates from list of versions
    versions.sort(key=itemgetter('name'))
    for name, group in itertools.groupby(versions, key=itemgetter('name')):
        # When duplicates are encountered, favor the version with the lowest ID
        version = min(group, key=itemgetter('id'))
        unique_versions.append(version)

    return unique_versions, language_name


# Construct an object representing a book of the Bible
def get_book(book_elem):

    return {
        'id': book_elem.get('data-book'),
        'name': book_elem.text.strip()
    }


# Retrieve list of chapter counts for each book of the Bible
def get_chapter_data():

    chapter_data_path = os.path.join('yvs', 'data', 'bible', 'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        chapter_data = json.load(chapter_data_file)

    return chapter_data


# Retrieve list of dictionaries, each representing a book of the Bible
def get_books(default_version):

    print('Retrieving book data...')

    books = []
    chapter_data = get_chapter_data()

    d = pq(url='https://www.bible.com/bible/{}/jhn.1'
           .format(default_version),
           opener=get_url_content)

    book_elems = d('#menu_book_chapter a[data-book]')

    if not book_elems:
        raise RuntimeError('Cannot retrieve book data. Aborting.')

    for book_elem in book_elems:
        book = get_book(book_elem)
        # Only add book to list if a chapter count exists for that book
        if book['id'] in chapter_data:
            books.append(book)

    return books


# Construct object representing all Bible data for a particular version
# This data includes the list of books, list of versions, and default version
def get_bible_data(language_id, default_version, max_version_id):

    bible = {}
    bible['versions'], language_name = get_versions(
        language_id,
        max_version_id)

    # If no explicit default version is given, use version with lowest ID
    if not default_version:
        default_version = min(bible['versions'], key=itemgetter('id'))['id']
    elif not any(version['id'] == default_version for version in
                 bible['versions']):
        raise RuntimeError(
         'Given default version does not exist in given language. Aborting.')

    bible['default_version'] = default_version
    bible['books'] = get_books(default_version)
    return bible, language_name


# Write JSON data to file as Unicode
def write_json_unicode(json_object, file):
    json_str = unicode(json.dumps(json_object, **json_params))
    file.write(json_str)
    file.write('\n')


# Construct the Bible data object and save it to a JSON file
def save_bible_data(language_id, bible):

    bible_path = os.path.join(
        'yvs', 'data', 'bible',
        'language-{}.json'.format(language_id))
    with io.open(bible_path, 'w', encoding='utf-8') as bible_file:
        write_json_unicode(bible, bible_file)


# Add the given language parameters to the list of supported languages
def update_language_list(language_id, language_name):

    print('Updating language list...')

    langs_path = os.path.join('yvs', 'data', 'languages.json')
    with io.open(langs_path, 'r+', encoding='utf-8') as langs_file:
        langs = json.load(langs_file)
        # If language does not already exist in list of supported languages
        if not any(lang['id'] == language_id for lang in langs):
            langs.append({
                'id': language_id,
                'name': language_name
            })
            langs.sort(key=itemgetter('id'))
            langs_file.truncate(0)
            langs_file.seek(0)
            write_json_unicode(langs, langs_file)


# Add support for the language with the given parameters to the workflow
def add_language(language_id, default_version, max_version_id):

    bible, language_name = get_bible_data(
        language_id,
        default_version,
        max_version_id)
    save_bible_data(language_id, bible)
    update_language_list(language_id, language_name)


# Parse command-line arguments
def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'code',
        help='the language\'s ISO 639-1 code')
    parser.add_argument(
        '--default-version',
        type=int,
        help='the default version to use for this language')
    parser.add_argument(
        '--max-version-id',
        type=int,
        help='the upper limit to which Bible version IDs are constrained')

    args = parser.parse_args()
    return args


def main():

    args = parse_cli_args()
    print('Adding language support...')
    add_language(
        args.code.replace('-', '_'),
        args.default_version,
        args.max_version_id)
    print('Support for {} has been successfully added.'
          .format(args.code.replace('_', '-')))

if __name__ == '__main__':
    main()
