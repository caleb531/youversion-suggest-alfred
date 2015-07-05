# yvs.filter_refs
# coding=utf-8

from __future__ import unicode_literals
import re
import yvs.shared as shared


# Parses the given query string into components of a Bible reference
def get_ref_matches(query_str):

    # Pattern for parsing any bible reference
    patt = '^{book}(?:{chapter}(?:{verse}{endverse})?{version})?$'.format(
        book='(\d?(?:[^\W\d_]|\s)+|\d)\s?',
        chapter='(\d+)\s?',
        verse='(\d+)\s?',
        endverse='(\d+)?\s?',
        version='([a-z]+\d*)?.*?')
    return re.search(patt, query_str, flags=re.UNICODE)


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

            endverse_match = ref_matches.group(4)
            if endverse_match:
                query['endverse'] = int(endverse_match)

        version_match = ref_matches.group(5)
        if version_match:
            query['version'] = version_match.lstrip().upper()

    return query


# Find a version which best matches the given version query
def guess_version(versions, version_query):

    # Chop off character from version query until matching version can be
    # found (if a matching version even exists)
    for i in xrange(len(version_query), 0, -1):
        for version in versions:
            if version['name'].startswith(version_query[:i]):
                return version

    return None


# Determines if the given query string matches the given book name
def query_matches_book(query_book, book_name):
    return (book_name.startswith(query_book) or
            (book_name[0].isnumeric() and
             book_name[2:].startswith(query_book)))


# Retrieves list of books matching the given query
def get_matching_books(books, query):

    matching_books = []

    for i in xrange(len(query['book']), 0, -1):
        if matching_books:
            break
        for book in books:
            book_name = book['name'].lower()
            if query_matches_book(query['book'][:i], book_name):
                matching_books.append(book)

    return matching_books


# Choose most appropriate version based on current parameters
def choose_best_version(prefs, bible, query):

    chosen_version = None

    if 'version' in query:
        chosen_version = guess_version(bible['versions'], query['version'])

    if not chosen_version and 'version' in prefs:
        chosen_version = shared.get_version(bible['versions'],
                                            prefs['version'])

    if not chosen_version:
        chosen_version = shared.get_version(bible['versions'],
                                            bible['default_version'])

    return chosen_version


# Build a single result item
def get_result(book, query, chosen_version):

    result = {}

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

    result['arg'] = '{version}/{uid}'.format(
        version=chosen_version['id'],
        uid=result['uid'])
    result['uid'] = 'yvs-{}'.format(result['arg'])
    result['title'] += ' ({version})'.format(
        version=chosen_version['name'])
    result['subtitle'] = 'View on YouVersion'

    return result


# Retrieves search resylts matching the given query
def get_result_list(query_str):

    query_str = shared.format_query_str(query_str)
    query = get_query_object(query_str)
    results = []

    if not query:
        return results

    prefs = shared.get_prefs()
    bible = shared.get_bible_data(prefs['language'])
    chapters = shared.get_chapter_data()
    matching_books = get_matching_books(bible['books'], query)

    if 'chapter' not in query:
        query['chapter'] = 1

    chosen_version = choose_best_version(prefs, bible, query)

    # Build result list from books matching the query
    for book in matching_books:

        # Skip result if given chapter exceeds number of chapters in book
        if query['chapter'] > chapters[book['id']]:
            continue

        # Result information
        results.append(get_result(book, query, chosen_version))

    return results


def main(query_str):

    results = get_result_list(query_str)

    if not results:
        results = [{
            'uid': 'yvs-no-results',
            'title': 'No Results',
            'subtitle': 'No bible references matching \'{}\''
            .format(query_str),
            'valid': 'no'
        }]

    print(shared.get_result_list_xml(results))

if __name__ == '__main__':
    main('{query}')
