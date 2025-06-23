#!/usr/bin/env python3
# coding=utf-8

from __future__ import unicode_literals

import hashlib
import os
import os.path
from unittest.mock import patch

import yvs.cache as cache
from tests import YVSTestCase
from tests.decorators import redirect_stdout


class TestCache(YVSTestCase):
    @redirect_stdout
    def test_cache_purge_oldest(self, out):
        """should purge oldest entry when cache grows too large"""
        entry_key = "a"
        num_entries = cache.MAX_NUM_CACHE_ENTRIES + 2
        purged_entry_checksum = hashlib.sha1(("a" * 1).encode("utf-8")).hexdigest()
        last_entry_checksum = hashlib.sha1(
            ("a" * num_entries).encode("utf-8")
        ).hexdigest()
        self.assertFalse(
            os.path.exists(cache.get_cache_entry_dir_path()),
            "local cache entry directory exists",
        )
        for i in range(num_entries):
            cache.add_cache_entry(entry_key, "blah blah")
            entry_key += "a"
        entry_checksums = os.listdir(cache.get_cache_entry_dir_path())
        self.assertEqual(len(entry_checksums), cache.MAX_NUM_CACHE_ENTRIES)
        self.assertNotIn(purged_entry_checksum, entry_checksums)
        self.assertIn(last_entry_checksum, entry_checksums)
        with open(cache.get_cache_manifest_path(), "r") as manifest_file:
            entry_checksums = manifest_file.read().splitlines()
            self.assertEqual(len(entry_checksums), cache.MAX_NUM_CACHE_ENTRIES)
            self.assertNotIn(purged_entry_checksum, entry_checksums)
            self.assertIn(last_entry_checksum, entry_checksums)

    @redirect_stdout
    def test_cache_truncate(self, out):
        """
        should truncate cache if max entries count changes
        between workflow versions
        """
        entry_key = "a"
        new_max_count = cache.MAX_NUM_CACHE_ENTRIES // 2
        num_entries = cache.MAX_NUM_CACHE_ENTRIES + 2
        purged_entry_checksum = hashlib.sha1(("a" * 1).encode("utf-8")).hexdigest()
        last_entry_checksum = hashlib.sha1(
            ("a" * num_entries).encode("utf-8")
        ).hexdigest()
        self.assertFalse(
            os.path.exists(cache.get_cache_entry_dir_path()),
            "local cache entry directory exists",
        )
        for i in range(num_entries // 2):
            cache.add_cache_entry(entry_key, "blah blah")
            entry_key += "a"
        with patch("yvs.cache.MAX_NUM_CACHE_ENTRIES", new_max_count):
            for i in range(num_entries // 2):
                cache.add_cache_entry(entry_key, "blah blah")
                entry_key += "a"
        entry_checksums = os.listdir(cache.get_cache_entry_dir_path())
        self.assertEqual(len(entry_checksums), new_max_count)
        self.assertNotIn(purged_entry_checksum, entry_checksums)
        self.assertIn(last_entry_checksum, entry_checksums)
        with open(cache.get_cache_manifest_path(), "r") as manifest_file:
            entry_checksums = manifest_file.read().splitlines()
            self.assertEqual(len(entry_checksums), new_max_count)
            self.assertNotIn(purged_entry_checksum, entry_checksums)
            self.assertIn(last_entry_checksum, entry_checksums)
