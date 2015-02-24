#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from xml.etree import ElementTree as ET
import shared
import unicodedata


# Parse query string into components of a Bible reference
def get_ref_matches(query_str):
    # Pattern for parsing any bible reference
    patt = '^{book}(?:{chapter}(?:{verse}{endverse})?{version})?$'.format(
        # Book name (including preceding number, if any)
        book='(\d?(?:[^\W\d_]|\s)+)\s?',
        # Chapter number
        chapter='(\d+)\s?',
        # Verse number
        verse='(\d+)\s?',
        #  End verse for a verse range
        endverse='(\d+)?\s?',
        # Version (translation) used to view reference
        version='([^\W\d_]+\d*)?')
    return re.search(patt, query_str, flags=re.UNICODE)


# Find a version which best matches the given version query
def guess_version(versions, version_query):

    version_query = version_query.upper()

    # Chop off character from version query until matching version can be
    # found (if a matching version even exists)
    for i in xrange(len(version_query), 0, -1):
        for version in versions:
            if version['name'].startswith(version_query[:i]):
                return version

    return None


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

    query_str = query_str.lower()
    # Normalize all Unicode characters
    query_str = unicodedata.normalize('NFC', query_str)
    # Remove all non-alphanumeric characters
    query_str = re.sub('[\W_]', ' ', query_str, flags=re.UNICODE)
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub('\s+', ' ', query_str)
    # Parse shorthand reference notation
    query_str = re.sub('(\d)(?=[a-z])', '\\1 ', query_str)

    return query_str


# Builds the query object from the given query string
def get_query_object(query_str):

    # Match section of the bible based on query
    ref_matches = get_ref_matches(query_str)

    if not ref_matches:
        return None

    # Create query object for storing query data
    query = {}

    book_match = ref_matches.group(1)
    query['book'] = book_match.rstrip()

    chapter_match = ref_matches.group(2)
    if chapter_match:
        query['chapter'] = int(chapter_match)

        verse_match = ref_matches.group(3)
        if verse_match:
            query['verse'] = int(verse_match)

            verse_range_match = ref_matches.group(4)
            if verse_range_match:
                query['endverse'] = int(verse_range_match)

        version_match = ref_matches.group(5)
        if version_match:
            query['version'] = version_match.lstrip()

    return query


# Retrieves list of books matching the given query
def get_matching_books(books, query):

    matching_books = []

    for i in xrange(len(query['book']), 0, -1):
        if not matching_books:
            for book in books:
                book_name = book['name'].lower()
                # Check if book name begins with the typed book name
                if (book_name.startswith(query['book'][:i]) or
                    (book_name[0].isnumeric() and
                        book_name[2:].startswith(query['book'][:i]))):
                    matching_books.append(book)
        else:
            break

    return matching_books


# Retrieves search resylts matching the given query
def get_result_list(query_str):

    query_str = format_query_str(query_str)
    query = get_query_object(query_str)
    results = []

    if not query:
        return results

    bible = shared.get_bible_data()
    matching_books = get_matching_books(bible['books'], query)
    chosen_version = None

    if 'version' in query:
        chosen_version = guess_version(bible['versions'], query['version'])

    if not chosen_version:
        chosen_version = shared.get_version(bible['versions'],
                                            bible['default_version'])

    if 'chapter' not in query:
        query['chapter'] = 1

    # Build results list from books that matched the query
    for book in matching_books:

        # Result information
        result = {}

        # If chapter exists within the book
        if query['chapter'] >= 1 and query['chapter'] <= book['chapters']:

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
                result['title'] += ':{verse}'.format(
                    verse=query['verse'])

                if 'endverse' in query and query['endverse'] > query['verse']:

                    result['uid'] += '-{verse}'.format(
                        verse=query['endverse'])
                    result['title'] += '-{verse}'.format(
                        verse=query['endverse'])

        # Create result data using the given information
        if 'uid' in result:

            result['uid'] = '{version}/{uid}'.format(
                version=chosen_version['id'],
                uid=result['uid'])
            result['arg'] = result['uid']
            result['title'] += ' ({version})'.format(
                version=chosen_version['name'])
            result['subtitle'] = "View on YouVersion"
            results.append(result)

    return results


# Outputs an Alfred XML string from the given query string
def main(query_str='{query}'):

    results = get_result_list(query_str)

    if not results:

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
