# yvs.shared
# coding=utf-8

from __future__ import unicode_literals

import hashlib
import json
import os
import os.path
import re
import shutil
import unicodedata
import urllib2
from gzip import GzipFile
from htmlentitydefs import name2codepoint
from StringIO import StringIO

# Unique identifier for the workflow
WORKFLOW_UID = 'com.calebevans.youversionsuggest'

# Path to the user's home directory
HOME_DIR_PATH = os.path.expanduser('~')
# Path to the directory where this workflow stores non-volatile local data
LOCAL_DATA_DIR_PATH = os.path.join(
    HOME_DIR_PATH, 'Library', 'Application Support', 'Alfred 3',
    'Workflow Data', WORKFLOW_UID)
# Path to the directory where this workflow stores volatile local data
LOCAL_CACHE_DIR_PATH = os.path.join(
    HOME_DIR_PATH, 'Library', 'Caches',
    'com.runningwithcrayons.Alfred-3', 'Workflow Data', WORKFLOW_UID)
# Path to the directory containing data files apart of the packaged workflow
PACKAGED_DATA_DIR_PATH = os.path.join(os.getcwd(), 'yvs', 'data')

# The maximum number of cache entries to store
MAX_NUM_CACHE_ENTRIES = 100

# The template used to build the URL for a Bible reference
REF_URL_TEMPLATE = 'https://www.bible.com/bible/{ref}'

# The user agent used for HTTP requests sent to the YouVersion website
USER_AGENT = 'YouVersion Suggest'
# The number of seconds to wait before timing out an HTTP request connection
REQUEST_CONNECTION_TIMEOUT = 3


# Creates the directory (and any nonexistent parent directories) where this
# workflow stores non-volatile local data
def create_local_data_dir():

    try:
        os.makedirs(LOCAL_DATA_DIR_PATH)
    except OSError:
        pass


# Creates the directory (and any nonexistent parent directories) where this
# workflow stores volatile local data (i.e. cache data)
def create_local_cache_dirs():

    try:
        os.makedirs(get_cache_entry_dir_path())
    except OSError:
        pass


# Retrieves bible data object (books, versions, etc.) for the given language
def get_bible_data(language_id):

    bible_data_path = os.path.join(
        PACKAGED_DATA_DIR_PATH, 'bible',
        'language-{}.json'.format(language_id))
    with open(bible_data_path, 'r') as bible_data_file:
        return json.load(bible_data_file)


# Retrieves map of chapter counts for every book of the Bible
def get_chapter_data():

    chapter_data_path = os.path.join(
        PACKAGED_DATA_DIR_PATH, 'bible', 'chapters.json')
    with open(chapter_data_path, 'r') as chapter_data_file:
        return json.load(chapter_data_file)


# Retrieves name of first book whose id matches the given id
def get_book(books, book_id):

    for book in books:  # pragma: no branch
        if book['id'] == book_id:
            return book['name']


# Retrieves first version object whose id matches the given id
def get_version(versions, version_id):

    for version in versions:
        if version['id'] == version_id:
            return version


# Retrieves a list of all supported versions for the given language
def get_versions(language_id):

    bible = get_bible_data(language_id)
    return bible['versions']


# Retrieves a list of all supported languages
def get_languages():

    languages_path = os.path.join(
        PACKAGED_DATA_DIR_PATH, 'bible', 'languages.json')
    with open(languages_path, 'r') as languages_file:
        return json.load(languages_file)


# Build the object for a single result list feedback item
def get_result_list_feedback_item(result):

    item = {}
    if 'arg' in result:
        item['arg'] = result['arg']
        item['quicklookurl'] = get_ref_url(item['arg'])
    item['valid'] = result.get('valid', 'yes')

    if 'uid' in result:
        item['uid'] = result['uid']
    if 'autocomplete' in result:
        item['autocomplete'] = result['autocomplete']

    # Result title
    item['title'] = result['title']
    # Subtitle text shown under result title
    item['subtitle'] = result['subtitle']
    # Associated text to use when action is invoked
    item['text'] = {
        # Text copied to clipboard when cmd-c is invoked for this result
        'copy': result.get('copy', result['title']),
        # Text shown when invoking Large Type for this result
        'largetype': result.get('largetype', result['title'])
    }
    # Use different args when different modifiers are pressed
    item['mods'] = {
        'ctrl': {
            'arg': result['title']
        }
    }
    # Icon shown next to result text
    item['icon'] = {
        'path': 'icon.png'
    }
    return item


# Constructs an Alfred JSON string from the given result list
def get_result_list_feedback_str(results):

    feedback = {
        'items': []
    }

    for result in results:

        feedback['items'].append(get_result_list_feedback_item(result))

    return json.dumps(feedback)


# Functions for accessing/manipulating mutable preferences


# Retrieves the path to the workflow's default user preferences file
def get_default_user_prefs_path():

    return os.path.join(
        PACKAGED_DATA_DIR_PATH, 'preferences', 'defaults.json')


# Retrieves the default values for all workflow preferences
def get_default_user_prefs():

    with open(get_default_user_prefs_path(), 'r') as defaults_file:
        return json.load(defaults_file)


# Retrieves the path to the workflow's user preferences file
def get_user_prefs_path():

    return os.path.join(LOCAL_DATA_DIR_PATH, 'preferences.json')


# Overrwrites (or creates) user preferences using the given preferences object
def set_user_prefs(user_prefs):

    # Always ensure that the data directory (where prefrences reside) exists
    create_local_data_dir()
    with open(get_user_prefs_path(), 'w') as prefs_file:
        json.dump(user_prefs, prefs_file)


# Extends user preferences with any missing keys
def extend_user_prefs(user_prefs, default_user_prefs):

    # If any keys in the preference defaults have been added or removed
    if set(user_prefs.keys()) != set(default_user_prefs.keys()):
        # Supply defaults for missing keys and remove non-standard keys
        new_user_prefs = {}
        for pref_key in default_user_prefs:
            new_user_prefs[pref_key] = user_prefs.get(
                pref_key, default_user_prefs[pref_key])
        return new_user_prefs
    else:
        return user_prefs


# Retrieves map of user preferences
def get_user_prefs():

    default_user_prefs = get_default_user_prefs()
    try:
        with open(get_user_prefs_path(), 'r') as prefs_file:
            return extend_user_prefs(
                json.load(prefs_file), default_user_prefs)
    except IOError:
        # If user preferences don't exist, create them
        set_user_prefs(default_user_prefs)
        return default_user_prefs


# Functions for accessing/manipulating cache data


# Calculates the unique SHA1 checksum used as the filename for a cache entry
def get_cache_entry_checksum(entry_key):

    return hashlib.sha1(entry_key.encode('utf-8')).hexdigest()


# Retrieves the local filepath for a cache entry
def get_cache_entry_path(entry_key):

    entry_checksum = get_cache_entry_checksum(entry_key)
    return os.path.join(get_cache_entry_dir_path(), entry_checksum)


# Retrieves the path to the directory where all cache entries are stored
def get_cache_entry_dir_path():

    return os.path.join(LOCAL_CACHE_DIR_PATH, 'entries')


# Retrieves the path to the manifest file listing all cache entries
def get_cache_manifest_path():

    return os.path.join(LOCAL_CACHE_DIR_PATH, 'manifest.txt')


# Purge all expired entries in the cache
def purge_expired_cache_entries(manifest_file):
    # Read checksums from manifest; splitlines(True) preserves newlines
    entry_checksums = manifest_file.read().splitlines(True)
    # Purge the oldest entry if the cache is too large
    if len(entry_checksums) > MAX_NUM_CACHE_ENTRIES:
        old_entry_checksum = entry_checksums[0].rstrip()
        manifest_file.truncate(0)
        manifest_file.seek(0)
        manifest_file.writelines(entry_checksums[1:])
        os.remove(os.path.join(
            get_cache_entry_dir_path(), old_entry_checksum))


# Adds to the cache a new entry with the given content
def add_cache_entry(entry_key, entry_content):

    create_local_cache_dirs()

    # Write entry content to entry file
    entry_path = get_cache_entry_path(entry_key)
    with open(entry_path, 'w') as entry_file:
        entry_file.write(entry_content.encode('utf-8'))

    entry_checksum = os.path.basename(entry_path)
    cache_manifest_path = get_cache_manifest_path()
    with open(cache_manifest_path, 'a+') as manifest_file:
        # Write the new entry checksum to manifest file
        manifest_file.write(entry_checksum)
        manifest_file.write('\n')
        manifest_file.seek(0)
        purge_expired_cache_entries(manifest_file)


# Retrieves the unmodified content of a cache entry
def get_cache_entry_content(entry_key):

    create_local_cache_dirs()
    entry_path = get_cache_entry_path(entry_key)
    try:
        with open(entry_path, 'r') as entry_file:
            return entry_file.read().decode('utf-8')
    except IOError:
        return None


# Removes all cache entries and the directory itself
def clear_cache():

    try:
        shutil.rmtree(LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass


# Query-related functions


# Normalizes the format of the query string
def normalize_query_str(query_str):

    query_str = query_str.lower()
    # Normalize all Unicode characters
    query_str = unicodedata.normalize('NFC', query_str)
    # Remove all non-alphanumeric characters
    query_str = re.sub(r'[\W_]', ' ', query_str, flags=re.UNICODE)
    # Remove extra whitespace
    query_str = query_str.strip()
    query_str = re.sub(r'\s+', ' ', query_str)
    # Parse shorthand reference notation
    query_str = re.sub(r'(\d)(?=[a-z])', '\\1 ', query_str)

    return query_str


# Parses the given reference UID into a dictionary representing that reference
def get_ref_object(ref_uid, user_prefs=None):

    patt = r'^{version}/{book_id}\.{chapter}(?:\.{verse}{endverse})?$'.format(
        version=r'(\d+)',
        book_id=r'(\d?[a-z]+)',
        chapter=r'(\d+)',
        verse=r'(\d+)',
        endverse=r'(?:-(\d+))?')

    ref_uid_matches = re.match(patt, ref_uid)
    ref = {
        'uid': ref_uid,
        'book_id': ref_uid_matches.group(2),
        'version_id': int(ref_uid_matches.group(1)),
        'chapter': int(ref_uid_matches.group(3))
    }

    # Include book name using book ID and currently-set language
    user_prefs = get_user_prefs()
    bible = get_bible_data(user_prefs['language'])
    book_name = get_book(bible['books'], ref['book_id'])
    ref['book'] = book_name

    # Include verse number if it exists
    verse_match = ref_uid_matches.group(4)
    if verse_match:
        ref['verse'] = int(verse_match)

    # Include end verse number if it exists
    endverse_match = ref_uid_matches.group(5)
    if endverse_match:
        ref['endverse'] = int(endverse_match)

    # Include full version name (acronym) if it exists
    version_name = get_version(bible['versions'], ref['version_id'])['name']
    ref['version'] = version_name

    return ref


# Retrieves the full reference identifier from the shorthand reference UID
def get_full_ref(ref):

    full_ref = '{book} {chapter}'.format(
        book=ref['book'],
        chapter=ref['chapter'])

    if 'verse' in ref:
        full_ref += ':{verse}'.format(verse=ref['verse'])

    if 'endverse' in ref:
        full_ref += '-{endverse}'.format(endverse=ref['endverse'])

    full_ref += ' ({version})'.format(version=ref['version'])

    return full_ref


# Builds the URL used to view the reference with the given UID
def get_ref_url(ref_uid):
    return REF_URL_TEMPLATE.format(ref=ref_uid.upper())


# Normalizes format of reference content by removing superfluous whitespace
def normalize_ref_content(ref_content):

    # Collapse consecutive spaces into a single space
    ref_content = re.sub(r' {2,}', ' ', ref_content)
    # Collapse sequences of three or more newlines into two
    ref_content = re.sub(r'\n{3,}', '\n\n', ref_content)
    # Strip leading/trailing whitespace for entire reference
    ref_content = re.sub(r'(^\s+)|(\s+$)', '', ref_content)
    # Strip leading/trailing whitespace for each paragraph
    ref_content = re.sub(r' ?\n ?', '\n', ref_content)
    return ref_content


# Retrieves HTML contents of the given URL as a Unicode string
def get_url_content(url):

    request = urllib2.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Accept-Encoding': 'gzip, deflate'
    })
    response = urllib2.urlopen(request, timeout=REQUEST_CONNECTION_TIMEOUT)
    url_content = response.read()

    # Decompress response body if gzipped
    if response.info().get('Content-Encoding') == 'gzip':
        str_buf = StringIO(url_content)
        with GzipFile(fileobj=str_buf, mode='rb') as gzip_file:
            url_content = gzip_file.read()

    return url_content.decode('utf-8')


# Evaluates HTML character reference to its respective Unicode character
def eval_html_charref(name):

    if name[0] == 'x':
        # Handle hexadecimal character references
        return unichr(int(name[1:], 16))
    elif name.isdigit():
        # Handle decimal character references
        return unichr(int(name))
    else:
        # Otherwise, assume character reference is a named reference
        return unichr(name2codepoint[name])
