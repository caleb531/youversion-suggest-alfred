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
        'name': matches.group(2).upper(),
        'id': int(matches.group(1))
    }


# Retrieve list of HTML elements, each corresponding to a Bible version
def get_version_elems(params):

    d = pq(url='https://www.bible.com/{}/versions'
           .format(params['language']['id'].replace('_', '-')),
           opener=get_url_content)

    category_elems = d('#main > article > ul > li')
    version_elems = None

    if category_elems:

        category_elem = category_elems[0]
        version_elems = d(category_elem).find('li')

        text = category_elem.text
        params['language']['name'] = get_language_name(text)

        if not params['language']['name']:
            raise RuntimeError('Language name cannot be determined. Aborting.')

    return version_elems


# Retrieve a list of dictionaries representing Bible versions
def get_versions(params):

    print('Retrieving version data...')

    versions = []
    unique_versions = []

    version_elems = get_version_elems(params)

    if not version_elems:
        raise RuntimeError('Cannot find the given language. Aborting.')

    for version_elem in version_elems:
        version = get_version(version_elem)
        # Only add version if ID does not exceed a certain limit (if defined)
        if (not params['max_version_id'] or
           version['id'] <= params['max_version_id']):
            versions.append(version)

    # Sort and remove duplicates from list of versions
    versions.sort(key=itemgetter('name'))
    for name, group in itertools.groupby(versions, key=itemgetter('name')):
        # When duplicates are encountered, favor the version with the lowest ID
        version = min(group, key=itemgetter('id'))
        unique_versions.append(version)

    return unique_versions


# Construct an object representing a book of the Bible
def get_book(book_elem):

    return {
        'name': book_elem.text.strip().encode('utf-8'),
        'id': book_elem.get('data-book')
    }


# Retrieve list of chapter counts for each book of the Bible
def get_chapter_data():

    chapter_data_path = os.path.join('yvs', 'data', 'bible',
                                     'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        chapter_data = json.load(chapter_data_file)

    return chapter_data


# Retrieve list of dictionaries, each representing a book of the Bible
def get_books(params):

    print('Retrieving book data...')

    books = []
    chapter_data = get_chapter_data()

    d = pq(url='https://www.bible.com/bible/{}/jhn.1'
           .format(params['default_version']),
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
def get_bible_data(params):

    bible = {}
    bible['versions'] = get_versions(params)

    # If no explicit default version is given, use version with lowest ID
    if not params['default_version']:
        params['default_version'] = min(bible['versions'],
                                        key=itemgetter('id'))['id']
    elif not any(version['id'] == params['default_version'] for version in
                 bible['versions']):
        raise RuntimeError(
         'Given default version does not exist in given language. Aborting.')

    bible['default_version'] = params['default_version']
    bible['books'] = get_books(params)
    return bible


# Construct the Bible data object and save it to a JSON file
def save_bible_data(params):

    language = params['language']
    bible = get_bible_data(params)
    bible_path = os.path.join('yvs', 'data', 'bible',
                              'language-{}.json'.format(language['id']))
    with open(bible_path, 'w') as bible_file:
        json.dump(bible, bible_file, **json_params)
        bible_file.write('\n')


# Add the given language parameters to the list of supported languages
def update_language_list(params):

    print('Updating language list...')

    langs_path = os.path.join('yvs', 'data', 'languages.json')
    with io.open(langs_path, 'r+', encoding='utf-8') as langs_file:
        langs = json.load(langs_file)
        # If language does not already exist in list of supported languages
        if not any(lang['id'] == params['language']['id'] for lang in langs):
            langs.append(params['language'])
            langs.sort(key=itemgetter('id'))
            json_str = unicode(json.dumps(langs, **json_params))
            langs_file.truncate(0)
            langs_file.seek(0)
            langs_file.write(json_str)
            langs_file.write('\n')


# Add support for the language with the given parameters to the workflow
def add_language(params):

    save_bible_data(params)
    update_language_list(params)


# Parse command-line arguments
def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'code',
        help='the language\'s ISO 639-1 code')
    parser.add_argument(
        '--max-version-id',
        type=int,
        help='the upper limit to which Bible version IDs are constrained')
    parser.add_argument(
        '--default-version',
        type=int)

    args = parser.parse_args()
    return args


# The params object is a more structured representation of the CLI arguments
def get_params(args):

    params = {
        'language': {
            'id': args.code.replace('-', '_'),
            'name': None
        },
        'max_version_id': args.max_version_id,
        'default_version': args.default_version
    }
    return params


def main():

    args = parse_args()
    params = get_params(args)
    print('Adding language support...')
    add_language(params)
    print('Support for {} has been successfully added.'
          .format(params['language']['name']))

if __name__ == '__main__':
    main()
