#!/usr/bin/env python3
# coding=utf-8

from __future__ import unicode_literals

from tests import YVSTestCase
from yvs.mru_stack import MRUStack


class TestMRUStack(YVSTestCase):
    def test_init_normal_no_duplicates(self):
        """should initialize with unique elements preserving order"""
        seq = ["matthew", "mark", "luke"]
        stack = MRUStack(seq, maxsize=10)

        self.assertEqual(list(stack), ["matthew", "mark", "luke"])
        self.assertEqual(len(stack), 3)
        self.assertIn("mark", stack)
        self.assertNotIn("genesis", stack)

    def test_init_deduplicates_and_preserves_order(self):
        """should deduplicate while preserving MRU order on initialization"""
        seq = ["matthew", "mark", "matthew", "luke"]
        stack = MRUStack(seq, maxsize=10)

        # Expect last occurrence of a to be most recent among the duplicates
        self.assertEqual(list(stack), ["mark", "matthew", "luke"])
        self.assertEqual(len(stack), 3)
        self.assertIn("matthew", stack)
        self.assertNotIn("genesis", stack)

    def test_init_truncates_to_maxsize(self):
        """should keep only the first maxsize elements on initialization"""
        seq = ["matthew", "mark", "luke", "john", "acts", "romans"]
        stack = MRUStack(seq, maxsize=3)

        self.assertEqual(list(stack), ["matthew", "mark", "luke"])
        self.assertEqual(len(stack), 3)

    def test_add_moves_duplicate_to_top(self):
        """should move an existing key to the top when re-added"""
        stack = MRUStack(["matthew", "mark", "luke"], maxsize=3)

        stack.add("mark")  # re-adding moves to the top (end)

        self.assertEqual(list(stack), ["matthew", "luke", "mark"])
        self.assertEqual(len(stack), 3)

    def test_add_purges_oldest_when_full(self):
        """should purge the least-recent when adding beyond maxsize"""
        stack = MRUStack(["matthew", "mark", "luke"], maxsize=3)

        stack.add("john")  # pushes out "matthew"

        self.assertEqual(list(stack), ["mark", "luke", "john"])
        self.assertNotIn("matthew", stack)
        self.assertEqual(len(stack), 3)

    def test_remove_existing_and_missing(self):
        """should remove an existing key and ignore missing keys"""
        stack = MRUStack(["matthew", "mark", "luke"], maxsize=3)

        stack.remove("mark")
        self.assertEqual(list(stack), ["matthew", "luke"])  # order preserved
        self.assertEqual(len(stack), 2)

        # Removing a non-existent key should be a no-op
        stack.remove("genesis")
        self.assertEqual(list(stack), ["matthew", "luke"])  # unchanged
        self.assertEqual(len(stack), 2)

    def test_maxsize_zero_keeps_nothing(self):
        """should never retain entries when maxsize is zero"""
        stack = MRUStack(["matthew", "mark"], maxsize=0)
        self.assertEqual(len(stack), 0)
        self.assertEqual(list(stack), [])

        stack.add("john")  # adding should immediately purge due to maxsize=0
        self.assertEqual(len(stack), 0)
        self.assertEqual(list(stack), [])

    def test_repr(self):
        """should include class name and ordered elements in representation"""
        stack = MRUStack(["matthew", "mark"], maxsize=5)
        self.assertEqual(repr(stack), "MRUStack(['matthew', 'mark'])")
