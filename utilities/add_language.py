#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pyquery import PyQuery as pq
import re
import io
import json
import urllib2


json_params = {
    'indent': 2,
    'ensure_ascii': False,
    'sort_keys': False
}


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
        'name': matches.group(2),
        'id': int(matches.group(1))
    }


def get_version_elems(d, params):

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

    versions = []

    d = pq(url='https://www.bible.com/versions')

    version_elems = get_version_elems(d, params)

    for version_elem in version_elems:
        version = get_version(version_elem)
        if (('max_version_id' in params and
            (version['id'] <= params['max_version_id']) or
             'max_versions' in params and len(versions) < params['']) or
            ('max_version_id' not in params and
             'max_versions' not in params)):
            versions.append(version)

    versions.sort(key=get_item_name)

    return versions


def get_book(book_elem):
    return {
        'name': book_elem.text.strip().encode('utf-8'),
        'id': book_elem.get('data-book')
    }


def get_url_content(url, **kw):
    return urllib2.urlopen(url).read().decode('utf-8')


def get_books(params):

    books = []

    d = pq(url='https://www.bible.com/bible/{}/jhn.1'
           .format(params['default_version']),
           opener=get_url_content)

    book_elems = d('#menu_book_chapter a[data-book]')

    for book_elem in book_elems:
        book = get_book(book_elem)
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

    bible = get_bible_data(params)
    bible_path = 'yv_suggest/data/bible/language-{}.json'.format(
        params['language']['id'])
    with open(bible_path, 'w') as bible_file:
        json.dump(bible, bible_file, **json_params)


def update_language_list(params):

    langs_path = 'yv_suggest/data/languages.json'
    with io.open(langs_path, 'r+', encoding='utf-8') as langs_file:
        langs = json.load(langs_file)
        if not any(lang['id'] == params['language']['id'] for lang in langs):
            langs.append(params['language'])
            langs.sort(key=get_item_id)
            langs_file.truncate(0)
            langs_file.seek(0)
            langs_file.write(unicode(json.dumps(langs, **json_params)))


def add_language(params):

    update_language_list(params)
    save_bible_data(params)


add_language({
    'language': {
        'name': 'Nederlands',
        'id': 'nl'
    }
})
