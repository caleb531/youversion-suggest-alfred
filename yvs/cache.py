#!/usr/bin/env python3
# coding=utf-8

import contextlib
import hashlib
import os
import os.path
import shutil

import yvs.core as core
from yvs.mru_stack import MRUStack

# Path to the directory where this workflow stores volatile local data (this
# will be overridden during tests, so CI will still work fine)
LOCAL_CACHE_DIR_PATH = os.environ.get(
    "alfred_workflow_cache",
    os.path.join(
        core.HOME_DIR_PATH,
        "Library",
        "Caches",
        "com.runningwithcrayons.Alfred",
        "Workflow Data",
        core.WORKFLOW_BUNDLE_ID,
    ),
)

# The maximum number of cache entries to store
MAX_NUM_CACHE_ENTRIES = 50


# Creates the directory (and any nonexistent parent directories) where this
# workflow stores volatile local data (i.e. cache data)
def create_local_cache_dirs():
    try:
        os.makedirs(get_cache_entry_dir_path())
    except OSError:
        pass


# Calculates the unique SHA1 checksum used as the filename for a cache entry
def get_cache_entry_checksum(entry_key):
    return hashlib.sha1(entry_key.encode("utf-8")).hexdigest()


# Retrieves the local filepath for a cache entry
def get_cache_entry_path(entry_key):
    entry_checksum = get_cache_entry_checksum(entry_key)
    return os.path.join(get_cache_entry_dir_path(), entry_checksum)


# Retrieves the path to the directory where all cache entries are stored
def get_cache_entry_dir_path():
    return os.path.join(LOCAL_CACHE_DIR_PATH, "entries")


# Retrieves the path to the manifest file listing all cache entries
def get_cache_manifest_path():
    return os.path.join(LOCAL_CACHE_DIR_PATH, "manifest.txt")


# Purge all expired entries in the cache
def purge_expired_cache_entries(removed_checksums):
    # Remove any files that are no longer referenced in the manifest
    for checksum in removed_checksums:
        # if checksum == entry_checksum:
        #     # Never remove the cache entry we just wrote
        #     continue
        purged_path = os.path.join(get_cache_entry_dir_path(), checksum)
        with contextlib.suppress(FileNotFoundError):
            os.remove(purged_path)


# Adds to the cache a new entry with the given content
def add_cache_entry(entry_key, entry_content):
    create_local_cache_dirs()

    # Write/overwrite entry content to entry file
    entry_path = get_cache_entry_path(entry_key)
    with open(entry_path, "w") as entry_file:
        entry_file.write(entry_content)

    entry_checksum = os.path.basename(entry_path)
    cache_manifest_path = get_cache_manifest_path()

    # Update manifest using MRU semantics

    try:
        with open(cache_manifest_path, "r") as manifest_file:
            existing_lines = manifest_file.read().splitlines()
    except FileNotFoundError:
        existing_lines = []

    # Build MRU from existing entries
    mru_cache = MRUStack(existing_lines, maxsize=MAX_NUM_CACHE_ENTRIES)
    # Add the new entry, moving it to the top if it already exists
    mru_cache.add(entry_checksum)

    with open(cache_manifest_path, "w+") as manifest_file:
        manifest_file.write("\n".join(mru_cache) + "\n")

    # Determine which checksums were removed by normalization/truncation
    removed_checksums = set(existing_lines) - set(mru_cache)
    purge_expired_cache_entries(removed_checksums)


# Retrieves the unmodified content of a cache entry
def get_cache_entry_content(entry_key):
    create_local_cache_dirs()
    entry_path = get_cache_entry_path(entry_key)
    try:
        with open(entry_path, "r") as entry_file:
            return entry_file.read()
    except IOError:
        return None


# Removes all cache entries and the directory itself
def clear_cache():
    try:
        shutil.rmtree(LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass
