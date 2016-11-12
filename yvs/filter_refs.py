# yvs.filter_refs
# coding=utf-8

from __future__ import unicode_literals

import re
import sys

import yvs.shared as shared


# Parses the given query string into components of a Bible reference
def get_ref_matches(query_str):

    # Pattern for parsing any bible reference
    patt = '^{book}(?:{chapter}(?:{verse}{endverse})?{version})?$'.format(
        book=r'(\d?(?:[^\W\d_]|\s)+|\d)\s?',
        chapter=r'(\d+)\s?',
        verse=r'(\d+)\s?',
        endverse=r'(\d+)?\s?',
        version=r'([a-z]+\d*)?.*?')
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


# Finds a version which best matches the given version query
def guess_version(versions, version_query):

    # Chop off character from version query until matching version can be
    # found (if a matching version even exists)
    for i in xrange(len(version_query), 0, -1):
        for version in versions:
            if version['name'].startswith(version_query[:i]):
                return version

    return None


# Formats book name by removing non-alphanumeric characters
def normalize_book_name(book_name):

    book_name = book_name.lower()
    # Remove all non-alphanumeric characters
    book_name = re.sub(r'[\W_]', ' ', book_name, flags=re.UNICODE)
    # Remove extra whitespace
    book_name = book_name.strip()
    book_name = re.sub(r'\s+', ' ', book_name)

    return book_name


# Retrieves list of books matching the given query
def get_matching_books(books, query):

    matching_books = []

    for i in xrange(len(query['book']), 0, -1):
        book_query = query['book'][:i]
        for book in books:
            book_name = normalize_book_name(book['name'])
            if book_name.startswith(book_query):
                matching_books.append(book)
        # Stop if all possible matching books have been found
        # for the current query
        if matching_books:
            break

    return matching_books


# Chooses most appropriate version based on current parameters
def choose_best_version(user_prefs, bible, query):

    chosen_version = None

    if 'version' in query:
        chosen_version = guess_version(bible['versions'], query['version'])

    if not chosen_version and 'version' in user_prefs:
        chosen_version = shared.get_version(
            bible['versions'], user_prefs['version'])

    return chosen_version


# Builds a single result item
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

    query_str = shared.normalize_query_str(query_str)
    query = get_query_object(query_str)
    results = []

    if not query:
        return results

    user_prefs = shared.get_user_prefs()
    bible = shared.get_bible_data(user_prefs['language'])
    chapters = shared.get_chapter_data()
    matching_books = get_matching_books(bible['books'], query)

    if 'chapter' not in query:
        query['chapter'] = 1

    chosen_version = choose_best_version(user_prefs, bible, query)

    # Build result list from books matching the query
    for book in matching_books:

        # If given chapter does not exceed number of chapters in book
        if query['chapter'] <= chapters[book['id']]:

            results.append(get_result(book, query, chosen_version))

    return results


def main(query_str):

    results = get_result_list(query_str)
    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No references matching \'{}\''.format(query_str),
            'valid': 'no'
        })

    print(shared.get_result_list_feedback_str(results))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
