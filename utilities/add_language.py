#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from pyquery import PyQuery as pq


json_params = {
    'indent': 2,
    'separators': (',', ': '),
    'ensure_ascii': False,
    'sort_keys': True
}


def get_url_content(url, **kw):

    return urllib2.urlopen(url).read().decode('utf-8')


def get_language_name(text):

    patt = '^\s*(.+?)(?:\s*\((\d+)\)\s*)$'
    matches = re.search(patt, text, flags=re.UNICODE)
    if matches:
        return matches.group(1)
    else:
        return None


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

    d = pq(url='https://www.bible.com/{}/versions'
           .format(params['language']['id'].replace('_', '-')),
           opener=get_url_content)

    category_elems = d('#main > article > ul > li')
    version_elems = None

    if category_elems:

        category_elem = category_elems[0]

        text = category_elem.text.strip()
        version_elems = d(category_elem).find('li')
        params['language']['name'] = get_language_name(text)

        if not params['language']['name']:
            raise RuntimeError('Language name cannot be determined. Aborting.')

    return version_elems


def get_item_name(item):

    return item['name']


def get_item_id(item):

    return item['id']


def get_versions(params):

    print('Retrieving version data...')

    versions = []
    unique_versions = []

    version_elems = get_version_elems(params)

    if not version_elems:
        raise RuntimeError('Cannot find the given language. Aborting.')

    for version_elem in version_elems:
        version = get_version(version_elem)
        if (not params['max_version_id'] or
           version['id'] <= params['max_version_id']):
            versions.append(version)

    sorted_versions = sorted(versions, key=get_item_name)
    for name, group in itertools.groupby(sorted_versions, get_item_name):
        version = min(group, key=get_item_id)
        unique_versions.append(version)

    return unique_versions


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

    if (params['default_version'] and
        not any(version['id'] == params['default_version'] for version in
                bible['versions'])):
        raise RuntimeError(
         'Given default version does not exist in given language. Aborting.')

    if not params['default_version']:
        params['default_version'] = min(bible['versions'],
                                        key=get_item_id)['id']

    bible['default_version'] = params['default_version']

    bible['books'] = get_books(params)

    return bible


def save_bible_data(params):

    language = params['language']
    bible = get_bible_data(params)
    bible_path = os.path.join('yv_suggest', 'data', 'bible',
                              'language-{}.json'
                              .format(language['id']))
    with open(bible_path, 'w') as bible_file:
        json.dump(bible, bible_file, **json_params)
        bible_file.write('\n')


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

    save_bible_data(params)
    update_language_list(params)


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('code')
    parser.add_argument(
        '--max-version-id',
        type=int)
    parser.add_argument(
        '--default-version',
        type=int)

    args = parser.parse_args()

    return args


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
