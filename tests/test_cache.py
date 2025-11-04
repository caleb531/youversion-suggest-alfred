#!/usr/bin/env python3
# coding=utf-8

import hashlib
import os
import os.path
from unittest.mock import patch

import yvs.cache as cache


def test_cache_purge_oldest():
    """should purge oldest entry when cache grows too large"""
    entry_key = "a"
    num_entries = cache.MAX_NUM_CACHE_ENTRIES + 2
    purged_entry_checksum = hashlib.sha1(("a" * 1).encode("utf-8")).hexdigest()
    last_entry_checksum = hashlib.sha1(("a" * num_entries).encode("utf-8")).hexdigest()

    assert not os.path.exists(cache.get_cache_entry_dir_path()), (
        "local cache entry directory exists"
    )

    for _ in range(num_entries):
        cache.add_cache_entry(entry_key, "blah blah")
        entry_key += "a"

    entry_checksums = os.listdir(cache.get_cache_entry_dir_path())
    assert len(entry_checksums) == cache.MAX_NUM_CACHE_ENTRIES
    assert purged_entry_checksum not in entry_checksums
    assert last_entry_checksum in entry_checksums

    with open(cache.get_cache_manifest_path(), "r") as manifest_file:
        entry_checksums = manifest_file.read().splitlines()
        assert len(entry_checksums) == cache.MAX_NUM_CACHE_ENTRIES
        assert purged_entry_checksum not in entry_checksums
        assert last_entry_checksum in entry_checksums


def test_cache_truncate():
    """should truncate cache if max entries count changes between versions"""

    entry_key = "a"
    new_max_count = cache.MAX_NUM_CACHE_ENTRIES // 2
    num_entries = cache.MAX_NUM_CACHE_ENTRIES + 2
    purged_entry_checksum = hashlib.sha1(("a" * 1).encode("utf-8")).hexdigest()
    last_entry_checksum = hashlib.sha1(("a" * num_entries).encode("utf-8")).hexdigest()

    assert not os.path.exists(cache.get_cache_entry_dir_path()), (
        "local cache entry directory exists"
    )

    for _ in range(num_entries // 2):
        cache.add_cache_entry(entry_key, "blah blah")
        entry_key += "a"

    with patch("yvs.cache.MAX_NUM_CACHE_ENTRIES", new_max_count):
        for _ in range(num_entries // 2):
            cache.add_cache_entry(entry_key, "blah blah")
            entry_key += "a"

    entry_checksums = os.listdir(cache.get_cache_entry_dir_path())
    assert len(entry_checksums) == new_max_count
    assert purged_entry_checksum not in entry_checksums
    assert last_entry_checksum in entry_checksums

    with open(cache.get_cache_manifest_path(), "r") as manifest_file:
        entry_checksums = manifest_file.read().splitlines()
        assert len(entry_checksums) == new_max_count
        assert purged_entry_checksum not in entry_checksums
        assert last_entry_checksum in entry_checksums


def test_cache_add_duplicate_keys():
    """should delete duplicate cache entries without error"""

    num_entries = cache.MAX_NUM_CACHE_ENTRIES + 10
    first_entry_key = "first_foo"
    last_entry_key = "last_foo"

    cache.add_cache_entry(first_entry_key, f"{first_entry_key}_value")
    cache.add_cache_entry(first_entry_key, f"{first_entry_key}_value")

    for i in range(num_entries):
        cache.add_cache_entry(f"key_{i}", "bar")

    cache.add_cache_entry(last_entry_key, f"{last_entry_key}_value")

    with open(cache.get_cache_manifest_path(), "r") as manifest_file:
        entry_checksums = manifest_file.read().splitlines()
        first_entry_checksum = hashlib.sha1(first_entry_key.encode("utf-8")).hexdigest()
        last_entry_checksum = hashlib.sha1(last_entry_key.encode("utf-8")).hexdigest()

        assert first_entry_checksum not in entry_checksums, (
            f"cache key {first_entry_key} exists in manifest when it should not"
        )
        assert not os.path.exists(
            os.path.join(cache.get_cache_entry_dir_path(), first_entry_checksum)
        ), f"cache entry {first_entry_key} exists on disk when it should not"
        assert last_entry_checksum in entry_checksums, (
            f"cache key {last_entry_key} does not exist in manifest when it should"
        )
        assert os.path.exists(
            os.path.join(cache.get_cache_entry_dir_path(), last_entry_checksum)
        ), f"cache entry {last_entry_key} does not exist on disk when it should"
