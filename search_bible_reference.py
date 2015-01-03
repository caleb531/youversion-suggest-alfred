#!/usr/bin/env python
# Search bible references corresponding to the typed query

# Import required modules
import cgi, json, re, time

# Base class for creating objects of attributes
class AttrObject:
    def __init__(self, attrs=None):
        if attrs:
            for key, value in attrs.items():
                setattr(self, key, value)

# Subclasses used for data storage
class Book(AttrObject): pass
class Query(AttrObject): pass
class Reference(AttrObject): pass

# Load in books of the Bible
with open('books.json', 'r') as file:
    books = tuple(Book(book) for book in json.loads(file.read()))

# Load in Bible versions (translations)
with open('versions.json', 'r') as file:
    all_versions = tuple(json.loads(file.read()))

# Load in XML <item> template
with open('item.xml', 'r') as file:
    item_xml = file.read()

# Default translation for all results
default_version = 'NIV'

# Base bible reference URL
base_url = 'https://www.bible.com/bible'

# Pattern for parsing any bible reference
bible_ref_patt = '^((\d+ )?[a-z ]+)( (\d+)((\:|\.)(\d+)?)?)?( [a-z\d]+)?$'
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
    return item_xml.format(**params)

# Retrieves XML document for Alfred results
def get_result_list_xml(results):
    xml = '<?xml version="1.0"?>\n<items>\n'
    for result in results:

        if result.id != None:
            xml += get_result_xml(
                id=result.id,
                url=result.url,
                title=result.title,
                subtitle=result.subtitle,
                valid='yes'
            )

    xml += '</items>'
    return xml

# Simplify the format of the query string
def format_query_str(query_str):
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub('\s+', ' ', query_str)
    # Lowercase query for consistency
    query_str = query_str.lower()
    return query_str

# Search the bible for the given book/chapter/verse/version
def search_bible(query_str):
    results = []

    # Create query object for storing query data
    query = Query()
    query_str = format_query_str(query_str)
    # If reference is in form chapter.verse
    if re.search(chapter_dot_verse_patt, query_str):
        # Convert chapter.verse to chapter:verse
        query.separator = '.'
    else:
        query.separator = ':'

    # Match section of the bible based on query
    book_matches = re.search(bible_ref_patt, query_str)

    if book_matches != None:

        # Parse partial book name if given
        if book_matches.group(1) != None and book_matches.group(1) != '':
            query.book = book_matches.group(1).lower()
        else:
            query.book = None

        # Parse chapter if given
        if book_matches.group(4) != None and book_matches.group(4) != '':
            query.chapter = int(book_matches.group(4))
        else:
            query.chapter = None

        # Parse verse if given
        if book_matches.group(7) != None and book_matches.group(7) != '':
            query.verse = int(book_matches.group(7))
        else:
            query.verse = None

        # Parse version if given
        if book_matches.group(8) != None:
            query.version = book_matches.group(8).lstrip().upper()
        else:
            query.version = None

        # Filter book list to match query
        book_matches = []
        for book in books:
            book_name = book.name.lower()
            # Check if book name begins with the typed book name
            if book_name.startswith(query.book) or (book_name[0].isnumeric() and book_name[2:].startswith(query.book)):
                book_matches.append(book)

        # Build results list from books that matched the query
        for book in book_matches:

            # Result information
            result = Reference()
            result.id = None

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
                        result.id = '{book}.{chapter}.{verse}'.format(
                            book=book.id,
                            chapter=query.chapter,
                            verse=query.verse
                        )
                        result.title = '{book} {chapter}{sep}{verse}'.format(
                            book=book.name,
                            chapter=query.chapter,
                            verse=query.verse,
                            sep=query.separator
                        )

                    else:

                        # Find chapter if given
                        result.id = '{book}.{chapter}'.format(
                            book=book.id,
                            chapter=query.chapter
                        )
                        result.title = '{book} {chapter}'.format(
                            book=book.name,
                            chapter=query.chapter
                        )

            else:
                # Find book if no chapter or verse is given

                result.id = '{book}.1'.format(book=book.id)

                result.title = book.name

            # Create result data using the given information
            if result.id != None:
                result.id += '.{version}'.format(version=query.version.lower())
                result.url = '{base}/{version}/{id}'.format(
                    base=base_url,
                    version=query.version.lower(),
                    id=result.id)
                result.version = query.version.upper()
                result.subtitle = '{version} translation'.format(version=result.version)
                results.append(result)

    return get_result_list_xml(results)

print search_bible("{query}")
