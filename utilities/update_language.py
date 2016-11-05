# utilities.update_language

# This language utility updates an existing Bible data file for the given
# language (using existing data, such as default version, to recreate the data
# file)

from __future__ import unicode_literals

import argparse
from operator import itemgetter

import yvs.shared as shared
from add_language import add_language


# Parses all command-line arguments
def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'language_id',
        metavar='code',
        help='the ISO 639-1 code of the language')

    return parser.parse_args()


# Updates the Bible data file for the language with the given ID
def update_language(language_id):

    bible = shared.get_bible_data(language_id)
    default_version = bible['default_version']
    max_version_id = max(bible['versions'], key=itemgetter('id'))['id']

    print('Updating language \'{}\' data...'.format(
        language_id))
    add_language(
        language_id,
        default_version,
        max_version_id)
    print('Updated language \'{}\' data!'.format(
        language_id))


def main():

    cli_args = parse_cli_args()
    update_language(cli_args.language_id)


if __name__ == '__main__':
    main()
