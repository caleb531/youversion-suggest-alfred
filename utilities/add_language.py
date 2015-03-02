#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is a handy (albeit imperfect) tool for automatically adding
# support for any language to YouVersion Suggest. Please see the example
# function calls below for details on using it.

from __future__ import unicode_literals
from pyquery import PyQuery as pq
import os
import re
import io
import json
import urllib2


json_params = {
    'indent': 2,
    'separators': (',', ': '),
    'ensure_ascii': False,
    'sort_keys': True
}


def get_url_content(url, **kw):
    return urllib2.urlopen(url).read().decode('utf-8')


def language_matches(text, language):
    patt = '^({language}) \((\d+)\)$'.format(
        language=language.lower())
    matches = re.search(patt, text.lower(), flags=re.UNICODE)
    return matches is not None


def get_version(version_elem):
    link_elem = version_elem.find('a')
    url = link_elem.get('href')
    patt = '(?<=/versions/)(\d+)-([a-z]+\d*)'
    matches = re.search(patt, url, flags=re.UNICODE)
    return {
        'name': matches.group(2).upper(),
        'id': int(matches.group(1))
    }


def get_version_elems(params):

    d = pq(url='https://www.bible.com/versions',
           opener=get_url_content)

    category_elems = d('#main > article > ul > li')
    version_elems = None

    for category_elem in category_elems:
        text = category_elem.text.strip()
        if language_matches(text, params['language']['name']):
            version_elems = d(category_elem).find('li')
            break

    return version_elems


def get_item_name(item):
    return item['name']


def get_item_id(item):
    return item['id']


def get_versions(params):

    print('Retrieving version data...')

    versions = []

    version_elems = get_version_elems(params)

    if not version_elems:
        raise RuntimeError('Cannot find the given language. Aborting.')

    for version_elem in version_elems:
        version = get_version(version_elem)
        if ('max_version_id' in params and
           (version['id'] <= params['max_version_id']) or
           ('max_version_id' not in params)):
            versions.append(version)

    versions.sort(key=get_item_name)

    return versions


def get_book(book_elem):
    return {
        'name': book_elem.text.strip().encode('utf-8'),
        'id': book_elem.get('data-book')
    }


def get_chapter_data():

    chapter_data_path = os.path.join('yv_suggest', 'data', 'bible',
                                     'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        chapter_data = json.load(chapter_data_file)

    return chapter_data


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
        if book['id'] in chapter_data:
            books.append(book)

    return books


def get_bible_data(params):

    bible = {}

    bible['versions'] = get_versions(params)

    if 'default_version' not in params:
        params['default_version'] = min(bible['versions'],
                                        key=get_item_id)['id']

    bible['default_version'] = params['default_version']

    bible['books'] = get_books(params)

    return bible


def save_bible_data(params):

    language = params['language']
    bible = get_bible_data(params)
    bible_path = os.path.join('yv_suggest', 'data', 'bible',
                              'language-{}.json'.format(language['id']))
    with open(bible_path, 'w') as bible_file:
        json.dump(bible, bible_file, **json_params)


def update_language_list(params):

    print('Updating language list...')

    langs_path = os.path.join('yv_suggest', 'data', 'languages.json')
    with io.open(langs_path, 'r+', encoding='utf-8') as langs_file:
        langs = json.load(langs_file)
        if not any(lang['id'] == params['language']['id'] for lang in langs):
            langs.append(params['language'])
            langs.sort(key=get_item_id)
            json_str = unicode(json.dumps(langs, **json_params))
            langs_file.truncate(0)
            langs_file.seek(0)
            langs_file.write(json_str)
            langs_file.write('\n')


def add_language(params):

    print('Adding support for {}...'
          .format(params['language']['name']))
    save_bible_data(params)
    update_language_list(params)
    print('Support for {} has been successfully added.'
          .format(params['language']['name']))


# Example usage
# add_language({
#     'language': {
#         # Name of language must be written in said language
#         'name': 'Español',
#         # ISO language code
#         'id': 'es'
#     },
#     # Versions with lower IDs tend to be more popular and less obscure
#     'max_version_id': 200,
#     # If you know the default version you want to use, specify its ID
#     'default_version': 128
# })
