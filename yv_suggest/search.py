#!/usr/bin/env python
# Search bible references matching the given query

import re
from xml.etree import ElementTree as ET
import shared


# Pattern for parsing any bible reference
ref_patt = '^{book}(?:{ch}(?:{v}{v_end}?)?{version}?)?$'.format(
    # Book name (including preceding number, if amu)
    book='\s?((?:\d)?[a-z ]+)\s?',
    # Chapter number
    ch='\s?(\d+)\s?',
    # Verse number
    v='\s?(\d+)\s?',
    #  End verse for a verse range
    v_end='(?:\s?(\d+))',
    # Version (translation) used to view reference
    version='(?:\s?([a-z]+\d*)\s?)')


# Guesses a version based on the given partial version
def guess_version(versions, version_query):

    version_query = version_query.upper()

    if version_query in versions:
        version_guess = version_query
    else:
        # Attempt to guess the version used
        version_guess = None
        for version in versions:
            if version.startswith(version_query):  # pragma: no cover
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

    query_str = query_str.lower()
    # Remove all non-alphanumeric characters
    query_str = re.sub('[^a-z0-9]', ' ', query_str)
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub('\s+', ' ', query_str)
    # Parse shorthand book name and chapter/verse notation
    query_str = re.sub('(\d)(?=[a-z])', '\\1 ', query_str)

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
    book_match = ref_matches.group(1)
    query['book'] = book_match.rstrip()

    # Parse chapter if given
    chapter_match = ref_matches.group(2)
    if chapter_match:
        query['chapter'] = int(chapter_match)

        # Parse verse if given
        verse_match = ref_matches.group(3)
        if verse_match:
            query['verse'] = int(verse_match)

            # Parse verse range if given
            verse_range_match = ref_matches.group(4)
            if verse_range_match:
                query['verse_end'] = int(verse_range_match)

        # Parse version if given
        version_match = ref_matches.group(5)
        if version_match:
            query['version'] = version_match.lstrip()

    return query


# Retrieves list of books matching the given query
def get_matching_books(books, query):

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

    bible = shared.get_bible_data()
    # Filter book list to match query
    matching_books = get_matching_books(bible['books'], query)
    chosen_version = None

    if 'version' in query:
        # Guess version if possible
        chosen_version = guess_version(bible['versions'], query['version'])

    if not chosen_version:
        # Use last version if version could not be guessed
        chosen_version = bible['default_version']

    # Build results list from books that matched the query
    for book in matching_books:

        # Result information
        result = {}

        if 'chapter' in query:

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

                    if 'verse_end' in query:

                        if query['verse_end'] > query['verse']:

                            result['uid'] += '-{verse}'.format(
                                verse=query['verse_end'])
                            result['title'] += '-{verse}'.format(
                                verse=query['verse_end'])

        else:
            # Find book if no chapter or verse is given

            result['uid'] = '{book}.1'.format(book=book['id'])
            result['title'] = '{book} 1'.format(book=book['name'])

        # Create result data using the given information
        if 'uid' in result:

            result['uid'] = '{version}/{uid}'.format(
                version=chosen_version.lower(),
                uid=result['uid'])
            result['arg'] = result['uid']
            result['title'] += ' ({version})'.format(version=chosen_version)
            result['subtitle'] = "View on YouVersion"
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
