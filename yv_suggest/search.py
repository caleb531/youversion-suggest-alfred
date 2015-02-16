#!/usr/bin/env python
# Search bible references matching the given query

import json
import re
import os.path
import sys
from xml.etree import ElementTree as ET


# Properly determines path to package
def get_package_path():

    if '__file__' in globals():
        package_path = os.path.dirname(os.path.realpath(__file__))
    else:
        package_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    return package_path


# Loads list of Bible books from file
def get_books():

    books_path = os.path.join(get_package_path(), 'bible', 'books.json')
    with open(books_path, 'r') as file:
        books = tuple(json.load(file))

    return books


# Loads list of Bible versions from file
def get_versions():

    versions_path = os.path.join(get_package_path(), 'bible', 'versions.json')
    with open(versions_path, 'r') as file:
        versions = tuple(json.load(file))

    return versions


# Default version (translation) for all results
default_version = 'NIV'

# Pattern for parsing any bible reference
ref_patt = '^{book}(?:{ch}(?:{sep}{v}{v_end}?)?{version}?)?$'.format(
    # Book name (including preceding number, if amu)
    book='((?:\d )?[a-z ]+)',
    # Chapter number
    ch='(\d+)',
    # Chapter-verse separator
    sep='(\:|\.)',
    # Verse number
    v='(\d+)',
    #  End verse for a verse range
    v_end='(?:-(\d+))',
    # Version (translation) used to view reference
    version='(?: ([a-z]+\d*))'
)


# Guesses a version based on the given partial version
def guess_version(partial_version):

    partial_version = partial_version.upper()
    versions = get_versions()

    if partial_version in versions:
        version_guess = partial_version
    else:
        # Use a predetermined version by default
        version_guess = default_version
        # Attempt to guess the version used
        for version in versions:
            if version.startswith(partial_version):  # pragma: no cover
                version_guess = version
                break

    return version_guess


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


# Simplifies the format of the query string
def format_query_str(query_str):

    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub('\s+', ' ', query_str)
    # Lowercase query for consistency
    query_str = query_str.lower()
    # Remove tokens at end of incomplete references
    query_str = re.sub('[\-\.\:]$', '', query_str)

    # Parse shorthand book name notation
    query_str = re.sub('^(\d)(?=[a-z])', '\\1 ', query_str)
    # Parse shorthand version notation
    query_str = re.sub('(?<=\d)([a-z]+\d*)$', ' \\1', query_str)

    return query_str


# Builds the query object from the given query string
def get_query_object(query_str):

    # Match section of the bible based on query
    ref_matches = re.search(ref_patt, query_str)

    if not ref_matches:
        return None

    # Create query object for storing query data
    query = {}

    # Parse partial book name if given
    query['book'] = ref_matches.group(1).rstrip()

    # Parse chapter if given
    if ref_matches.group(2):
        query['chapter'] = int(ref_matches.group(2))

        # Store separator used to separate chapter from verse number
        if ref_matches.group(3):
            query['separator'] = ref_matches.group(3)

        # Parse verse if given
        if ref_matches.group(4):
            query['verse'] = int(ref_matches.group(4))

            # Parse verse range if given
            if ref_matches.group(5):
                query['verse_end'] = int(ref_matches.group(5))

        # Parse version if given
        if ref_matches.group(6):
            query['version'] = ref_matches.group(6).lstrip()

    return query


# Retrieves list of books matching the given query
def get_matching_books(query):

    books = get_books()
    matching_books = []

    for book in books:
        book_name = book['name'].lower()
        # Check if book name begins with the typed book name
        if (book_name.startswith(query['book']) or
            (book_name[0].isnumeric() and
                book_name[2:].startswith(query['book']))):
            matching_books.append(book)

    return matching_books


# Retrieves search resylts matching the given query
def get_result_list(query_str):

    query_str = format_query_str(query_str)
    query = get_query_object(query_str)
    results = []

    if not query:
        return results

    # Filter book list to match query
    matching_books = get_matching_books(query)

    if 'version' in query:
        # Guess version if possible
        matched_version = guess_version(query['version'])
    else:
        # Otherwise, use default version
        matched_version = default_version

    # Build results list from books that matched the query
    for book in matching_books:

        # Result information
        result = {}

        if 'chapter' in query:

            # If chapter exists within the book
            if query['chapter'] <= book['chapters']:

                # Find chapter if given
                result['uid'] = '{book}.{chapter}'.format(
                    book=book['id'],
                    chapter=query['chapter'])
                result['title'] = '{book} {chapter}'.format(
                    book=book['name'],
                    chapter=query['chapter'])

                if 'verse' in query:

                    # Find verse if given
                    result['uid'] += '.{verse}'.format(
                        verse=query['verse'])
                    result['title'] += '{sep}{verse}'.format(
                        verse=query['verse'],
                        sep=query['separator'])

                    if 'verse_end' in query:

                        result['uid'] += '-{verse}'.format(
                            verse=query['verse_end'])
                        result['title'] += '-{verse}'.format(
                            verse=query['verse_end'])

        else:
            # Find book if no chapter or verse is given

            result['uid'] = '{book}.1'.format(book=book['id'])
            result['title'] = book['name']

        # Create result data using the given information
        if 'uid' in result:

            result['uid'] = '{version}/{uid}'.format(
                version=matched_version.lower(),
                uid=result['uid'])
            result['arg'] = result['uid']
            result['subtitle'] = matched_version
            results.append(result)

    return results


# Outputs an Alfred XML string from the given query string
def main(query_str='{query}'):

    results = get_result_list(query_str)

    if len(results) == 0:

        # If no matching results were found, indicate such
        results = [{
            'uid': 'yv-no-results',
            'valid': 'no',
            'title': 'No Results',
            'subtitle': 'No bible references matching \'{}\''.format(query_str)
        }]

    print(get_result_list_xml(results))

if __name__ == '__main__':
    main()
