# utilities.add_language

# This language utility adds support for a language to YouVersion Suggest by
# gathering and parsing data from the YouVersion website to create all needed
# language files; this utility can also be used to update any Bible data for an
# already-supported language

from __future__ import unicode_literals

import argparse
import io
import itertools
import json
import os
from operator import itemgetter

import utilities.book_parser as book_parser
import utilities.language_parser as language_parser
import utilities.version_parser as version_parser
import yvs.shared as yvs

# Parameters for structuring JSON data
JSON_PARAMS = {
    'indent': 2,
    'separators': (',', ': '),
    'ensure_ascii': False,
    'sort_keys': True
}


# Retrieve the language name from the YouVersion website
def get_language_name(language_id):

    language_name = language_parser.get_language_name(language_id)
    if not language_name:
        raise RuntimeError('Cannot retrieve language data. Aborting.')
    return language_name


# Returns a copy of the given version list with duplicates removed
def get_unique_versions(versions):

    unique_versions = []
    for name, group in itertools.groupby(versions, key=itemgetter('name')):
        # When duplicates are encountered, favor the version with the lowest ID
        version = min(group, key=itemgetter('id'))
        unique_versions.append(version)

    return unique_versions


# Retrieves a list of dictionaries representing Bible versions
def get_versions(language_id, max_version_id=None):

    versions = version_parser.get_versions(language_id)

    # Exclude versions whose numerical ID exceeds a certain limit (if defined)
    if max_version_id:
        versions[:] = [version for version in versions
                       if version['id'] <= max_version_id]

    versions.sort(key=itemgetter('name'))
    unique_versions = get_unique_versions(versions)

    return unique_versions


# Retrieves a list of books available in this language
def get_books(default_version):

    books = []
    chapter_data = yvs.get_chapter_data()

    books = book_parser.get_books(default_version)
    if not books:
        raise RuntimeError('Cannot retrieve book data. Aborting.')

    # Ensure that returned books are recognized by the workflow (where the
    # workflow only recognizes books within the Biblical canon)
    books[:] = [book for book in books if book['id'] in chapter_data]

    return books


# Constructs object representing all Bible data for a particular version
# This data includes the list of books, list of versions, and default version
def get_bible_data(language_id, default_version, max_version_id):

    bible = {}
    bible['versions'] = get_versions(
        language_id,
        max_version_id)

    # If no explicit default version is given, use version with smallest ID
    if not default_version:
        default_version = min(bible['versions'], key=itemgetter('id'))['id']
    elif not any(version['id'] == default_version for version in
                 bible['versions']):
        raise RuntimeError(
            'Given default version does not exist in language. Aborting.')

    bible['default_version'] = default_version
    bible['books'] = get_books(default_version)
    return bible


# Writes the given JSON data to a file as Unicode
def write_json_unicode(json_object, json_file):

    json_str = json.dumps(json_object, **JSON_PARAMS)
    json_file.write(json_str)
    json_file.write('\n')


# Constructs the Bible data object and save it to a JSON file
def save_bible_data(language_id, bible):

    bible_path = os.path.join(
        yvs.PACKAGED_DATA_DIR_PATH, 'bible',
        'language-{}.json'.format(language_id))
    with io.open(bible_path, 'w', encoding='utf-8') as bible_file:
        write_json_unicode(bible, bible_file)


# Adds this language's details (name, code) to the list of supported languages
def update_language_list(language_id, language_name):

    langs_path = os.path.join(yvs.PACKAGED_DATA_DIR_PATH, 'languages.json')
    with io.open(langs_path, 'r+', encoding='utf-8') as langs_file:
        langs = json.load(langs_file)
        langs[:] = [lang for lang in langs if lang['id'] != language_id]
        langs.append({
            'id': language_id,
            'name': language_name
        })
        langs.sort(key=itemgetter('id'))
        langs_file.truncate(0)
        langs_file.seek(0)
        write_json_unicode(langs, langs_file)


# Adds to the worklow support for the language with the given parameters
def add_language(language_id, default_version, max_version_id):

    print('Fetching language data...')
    language_name = get_language_name(language_id)

    print('Adding Bible data...')
    bible = get_bible_data(
        language_id,
        default_version,
        max_version_id)
    save_bible_data(language_id, bible)

    print('Updating language list...')
    update_language_list(language_id, language_name)


# Parses all command-line arguments
def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'language_id',
        metavar='code',
        help='the ISO 639-1 code of the language')
    parser.add_argument(
        '--default-version',
        type=int,
        help='the default version to use for this language')
    parser.add_argument(
        '--max-version-id',
        type=int,
        help='the upper limit to which Bible version IDs are constrained')

    return parser.parse_args()


def main():

    cli_args = parse_cli_args()
    print('Adding language \'{}\' data...'.format(
        cli_args.language_id))
    add_language(
        cli_args.language_id.replace('-', '_'),
        cli_args.default_version,
        cli_args.max_version_id)
    print('Added language \'{}\' data!'.format(
        cli_args.language_id))

if __name__ == '__main__':
    main()
