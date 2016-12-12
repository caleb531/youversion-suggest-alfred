# tests.test_shared

from __future__ import unicode_literals

import hashlib
import os
import os.path
from gzip import GzipFile
from StringIO import StringIO

import nose.tools as nose
from mock import Mock, NonCallableMock, patch

import tests
import yvs.shared as yvs
from tests.decorators import redirect_stdout, use_user_prefs

with open('tests/html/psa.23.html') as html_file:
    html_content = html_file.read()
    patch_urlopen = patch(
        'urllib2.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_content)))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
@patch('urllib2.Request')
def test_get_url_content(request):
    """should fetch uncompressed URL content"""
    url = 'https://www.bible.com/bible/59/psa.23'
    yvs.get_url_content(url)
    request.assert_called_once_with(url, headers={
        'User-Agent': 'YouVersion Suggest',
        'Accept-Encoding': 'gzip, deflate'
    })


@nose.with_setup(set_up, tear_down)
@patch('urllib2.urlopen')
@patch('urllib2.Request')
def test_get_url_content_timeout(request, urlopen):
    """should timeout URL content request after 3 seconds"""
    yvs.get_url_content('https://www.bible.com/bible/59/psa.23')
    urlopen.assert_called_once_with(request.return_value, timeout=3)


@nose.with_setup(set_up, tear_down)
@patch('urllib2.Request')
def test_get_url_content_compressed(request):
    """should automatically decompress compressed URL content"""
    url = 'https://www.bible.com/bible/59/psa.23'
    gzip_buf = StringIO()
    with GzipFile(fileobj=gzip_buf, mode='wb') as gzip_file:
        gzip_file.write(html_content)
    gzipped_content = gzip_buf.getvalue()
    response_mock = NonCallableMock(
        read=Mock(return_value=gzipped_content),
        info=Mock(return_value=NonCallableMock(
            get=Mock(return_value='gzip'))))
    with patch('urllib2.urlopen', return_value=response_mock):
        url_content = yvs.get_url_content(url).encode('utf-8')
        nose.assert_equal(url_content, html_content)


@nose.with_setup(set_up, tear_down)
@use_user_prefs({'language': 'es', 'version': 197})
def test_upgrade_language_id():
    """should upgrade ISO 639-1 language ID to ISO 639-3 variant"""
    bible = yvs.get_bible_data('es')
    nose.assert_equal(bible['default_version'], 128)
    prefs = yvs.get_user_prefs()
    nose.assert_equal(prefs['language'], 'spa')
    nose.assert_equal(prefs['version'], 197)


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_cache_housekeeping(out):
    """should purge oldest entry when cache grows too large"""
    entry_key = 'a'
    num_entries = yvs.MAX_NUM_CACHE_ENTRIES + 2
    purged_entry_checksum = hashlib.sha1(('a' * 1).encode('utf-8')).hexdigest()
    last_entry_checksum = hashlib.sha1(
        ('a' * num_entries).encode('utf-8')).hexdigest()
    nose.assert_false(
        os.path.exists(yvs.get_cache_entry_dir_path()),
        'local cache entry directory exists')
    for i in range(num_entries):
        yvs.add_cache_entry(entry_key, 'blah blah')
        entry_key += 'a'
    entry_checksums = os.listdir(yvs.get_cache_entry_dir_path())
    nose.assert_equal(len(entry_checksums), yvs.MAX_NUM_CACHE_ENTRIES)
    nose.assert_not_in(purged_entry_checksum, entry_checksums)
    nose.assert_in(last_entry_checksum, entry_checksums)
    with open(yvs.get_cache_manifest_path(), 'r') as manifest_file:
        entry_checksums = manifest_file.read().splitlines()
        nose.assert_equal(
            len(entry_checksums), yvs.MAX_NUM_CACHE_ENTRIES)
        nose.assert_not_in(purged_entry_checksum, entry_checksums)
        nose.assert_in(last_entry_checksum, entry_checksums)
