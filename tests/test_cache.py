#!/usr/bin/env python3
# coding=utf-8

from __future__ import unicode_literals

import hashlib
import os
import os.path
from unittest.mock import patch

import yvs.cache as cache
from tests import YVSTestCase


class TestCache(YVSTestCase):
    def test_cache_purge_oldest(self):
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

    def test_cache_truncate(self):
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

    def test_cache_add_duplicate_keys(self):
        """
        should delete duplicate cache entries without error
        """
        num_entries = cache.MAX_NUM_CACHE_ENTRIES + 10
        first_entry_key = "first_foo"
        last_entry_key = "last_foo"
        # Add duplicate entries to verify that no FileNotFoundError is raised
        # when attempting to purge a cache entry that has already been purged
        cache.add_cache_entry(first_entry_key, f"{first_entry_key}_value")
        cache.add_cache_entry(first_entry_key, f"{first_entry_key}_value")
        # Fill up the cache to force the first entry to be purged
        for i in range(num_entries):
            # Since the new MRU-based implementation moves new entries to the
            # top if they already exist in the stack, adding the same key over
            # and over will not fill up the cache; we need to add uniquely-keyed
            # entries to the cache in order to fill up the cache
            cache.add_cache_entry(f"key_{i}", "bar")
        cache.add_cache_entry(last_entry_key, f"{last_entry_key}_value")
        with open(cache.get_cache_manifest_path(), "r") as manifest_file:
            entry_checksums = manifest_file.read().splitlines()
            first_entry_checksum = hashlib.sha1(
                first_entry_key.encode("utf-8")
            ).hexdigest()
            last_entry_checksum = hashlib.sha1(
                last_entry_key.encode("utf-8")
            ).hexdigest()
            self.assertNotIn(
                first_entry_checksum,
                entry_checksums,
                f"cache key {first_entry_key} exists in manifest when it should not",
            )
            self.assertFalse(
                os.path.exists(
                    os.path.join(
                        cache.get_cache_entry_dir_path(),
                        first_entry_checksum,
                    )
                ),
                f"cache entry {first_entry_key} exists on disk when it should not",
            )
            self.assertIn(
                last_entry_checksum,
                entry_checksums,
                f"cache key {last_entry_key} does not exist in manifest when it should",
            )
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        cache.get_cache_entry_dir_path(),
                        last_entry_checksum,
                    )
                ),
                f"cache entry {last_entry_key} does not exist on disk when it should",
            )
