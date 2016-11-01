# utilities.update_language

# This language utility updates an existing Bible data file for the given
# language (using existing data, such as default version, to recreate the data
# file)

from __future__ import unicode_literals
import argparse
import yvs.shared as shared
from operator import itemgetter
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

    add_language(
        language_id,
        default_version,
        max_version_id)
    print('Support for {} has been successfully updated.'.format(
        language_id.replace('_', '-')))


def main():

    cli_args = parse_cli_args()
    update_language(cli_args.language_id)


if __name__ == '__main__':
    main()
