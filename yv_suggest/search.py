#!/usr/bin/env python
# Search bible references corresponding to the typed query

# Import required modules
import json
import re
import os

# Base class for creating objects of attributes
class AttrObject:
    def __init__(self, attrs=None):
        if attrs:
            for key, value in attrs.items():
                setattr(self, key, value)

# Subclasses used for data storage
class Book(AttrObject): pass
class Query(AttrObject): pass
class Result(AttrObject): pass

# Load in books of the Bible
with open('yv_suggest/bible/books.json', 'r') as file:
    books = tuple(Book(book) for book in json.loads(file.read()))

# Load in Bible versions (translations)
with open('yv_suggest/bible/versions.json', 'r') as file:
    all_versions = tuple(json.loads(file.read()))

# Default translation for all results
default_version = 'NIV'

# Pattern for parsing any bible reference
bible_ref_patt = '^((\d+ )?[a-z ]+)( (\d+)((\:|\.)(\d+)?)?)?( [a-z]+\d*)?$'
# Pattern for parsing a chapter:verse reference (irrespective of book)
chapter_dot_verse_patt = '(\d+)\.(\d+)'

# Guess a translation based on the given partial version
def guess_version(partial_version):
    partial_version = partial_version.upper()

    if partial_version in all_versions:
        version_guess = partial_version
    else:
        # Use a predetermined version by default
        version_guess = default_version
        if partial_version != '':
            # Attempt to guess the version used
            for version in all_versions:
                if version.startswith(partial_version):
                    version_guess = version
                    break

    return version_guess

# Builds Aflred result item as XML
def get_result_xml(**params):
    return '''
    <item uid='{uid}' arg='{arg}' valid='{valid}'>
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>icon.png</icon>
    </item>\n'''.format(**params)

# Retrieves XML document for Alfred results
def get_result_list_xml(results):
    xml = '<?xml version="1.0"?>\n<items>\n'
    for result in results:

        if result.uid:
            xml += get_result_xml(
                uid=result.uid,
                arg=result.arg,
                title=result.title,
                subtitle=result.subtitle,
                valid='yes'
            )

    xml += '\n</items>'
    return xml

# Simplify the format of the query string
def format_query_str(query_str):
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub('\s+', ' ', query_str)
    # Lowercase query for consistency
    query_str = query_str.lower()
    return query_str

# Build the query object from the given query string
def get_query_object(query_str):

    # Match section of the bible based on query
    ref_matches = re.search(bible_ref_patt, query_str)

    if ref_matches:

        # Create query object for storing query data
        query = Query()

        # If reference is in form chapter.verse
        if re.search(chapter_dot_verse_patt, query_str):
            # Convert chapter.verse to chapter:verse
            query.separator = '.'
        else:
            query.separator = ':'

        # Parse partial book name if given
        if ref_matches.group(1):
            query.book = ref_matches.group(1).lower()
        else:
            query.book = None

        # Parse chapter if given
        if ref_matches.group(4):
            query.chapter = int(ref_matches.group(4))
        else:
            query.chapter = None

        # Parse verse if given
        if ref_matches.group(7):
            query.verse = int(ref_matches.group(7))
        else:
            query.verse = None

        # Parse version if given
        if ref_matches.group(8):
            query.version = ref_matches.group(8).lstrip().upper()
        else:
            query.version = None

    else:

        query = None

    return query

# Retrieve list of books matching the given query
def get_book_matches(query):
    book_matches = []
    for book in books:
        book_name = book.name.lower()
        # Check if book name begins with the typed book name
        if book_name.startswith(query.book) or (book_name[0].isnumeric() and book_name[2:].startswith(query.book)):
            book_matches.append(book)
    return book_matches

# Retrieve search resylts matching the given query
def get_result_list(query_str):

    query_str = format_query_str(query_str)
    query = get_query_object(query_str)
    results = []

    if not query: return results

    # Filter book list to match query
    book_matches = get_book_matches(query)

    # Build results list from books that matched the query
    for book in book_matches:

        # Result information
        result = Result()
        result.uid = None

        if query.version != None:
            # Guess version (translation) if possible
            query.version = guess_version(query.version)
        else:
            # Otherwise, use default translation
            query.version = default_version

        if query.chapter != None:

            # Find chapter or verse
            if query.chapter <= book.chapters:

                if query.verse != None:

                    # Find verse if given
                    result.uid = '{book}.{chapter}.{verse}'.format(
                        book=book.id,
                        chapter=query.chapter,
                        verse=query.verse
                    )
                    result.title = '{book} {chapter}{separator}{verse}'.format(
                        book=book.name,
                        chapter=query.chapter,
                        verse=query.verse,
                        separator=query.separator
                    )

                else:

                    # Find chapter if given
                    result.uid = '{book}.{chapter}'.format(
                        book=book.id,
                        chapter=query.chapter
                    )
                    result.title = '{book} {chapter}'.format(
                        book=book.name,
                        chapter=query.chapter
                    )

        else:
            # Find book if no chapter or verse is given

            result.uid = '{book}.1'.format(book=book.id)
            result.title = book.name

        # Create result data using the given information
        if result.uid:
            result.uid = '{version}/{uid}'.format(
                version=query.version.lower(),
                uid=result.uid
            )
            result.arg = result.uid
            result.subtitle = '{version}'.format(version=query.version.upper())
            results.append(result)

    return results

# Search the bible for the given book/chapter/verse reference
def main():

    query_str = "{query}".strip()
    results = get_result_list(query_str)

    if len(results) == 0:

        # If no matching results were found, indicate such
        results = [Result({
            'uid': 'yv-no-results',
            'arg': None,
            'valid': 'no',
            'title': 'No Results',
            'subtitle': 'No bible references matching \'{}\''.format(query_str)
        })]

    print(get_result_list_xml(results))

if __name__ == '__main__':
    main()
