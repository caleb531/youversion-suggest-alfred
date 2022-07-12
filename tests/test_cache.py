#!/usr/bin/env python3
# coding=utf-8

from __future__ import unicode_literals

import hashlib
import os
import os.path
import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.cache as cache
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_cache_housekeeping(out):
    """should purge oldest entry when cache grows too large"""
    entry_key = 'a'
    num_entries = cache.MAX_NUM_CACHE_ENTRIES + 2
    purged_entry_checksum = hashlib.sha1(
        ('a' * 1).encode('utf-8')).hexdigest()
    last_entry_checksum = hashlib.sha1(
        ('a' * num_entries).encode('utf-8')).hexdigest()
    case.assertFalse(
        os.path.exists(cache.get_cache_entry_dir_path()),
        'local cache entry directory exists')
    for i in range(num_entries):
        cache.add_cache_entry(entry_key, 'blah blah')
        entry_key += 'a'
    entry_checksums = os.listdir(cache.get_cache_entry_dir_path())
    case.assertEqual(len(entry_checksums), cache.MAX_NUM_CACHE_ENTRIES)
    case.assertNotIn(purged_entry_checksum, entry_checksums)
    case.assertIn(last_entry_checksum, entry_checksums)
    with open(cache.get_cache_manifest_path(), 'r') as manifest_file:
        entry_checksums = manifest_file.read().splitlines()
        case.assertEqual(
            len(entry_checksums), cache.MAX_NUM_CACHE_ENTRIES)
        case.assertNotIn(purged_entry_checksum, entry_checksums)
        case.assertIn(last_entry_checksum, entry_checksums)
