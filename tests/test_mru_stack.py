#!/usr/bin/env python3
# coding=utf-8

from yvs.mru_stack import MRUStack


def test_init_normal_no_duplicates():
    """should initialize with unique elements preserving order"""

    seq = ["matthew", "mark", "luke"]
    stack = MRUStack(seq, maxsize=10)

    assert list(stack) == ["matthew", "mark", "luke"]
    assert len(stack) == 3
    assert "mark" in stack
    assert "genesis" not in stack


def test_init_deduplicates_and_preserves_order():
    """should deduplicate while preserving MRU order on initialization"""

    seq = ["matthew", "mark", "matthew", "luke"]
    stack = MRUStack(seq, maxsize=10)

    assert list(stack) == ["mark", "matthew", "luke"]
    assert len(stack) == 3
    assert "matthew" in stack
    assert "genesis" not in stack


def test_init_truncates_to_maxsize():
    """should keep only the first maxsize elements on initialization"""

    seq = ["matthew", "mark", "luke", "john", "acts", "romans"]
    stack = MRUStack(seq, maxsize=3)

    assert list(stack) == ["matthew", "mark", "luke"]
    assert len(stack) == 3


def test_add_moves_duplicate_to_top():
    """should move an existing key to the top when re-added"""

    stack = MRUStack(["matthew", "mark", "luke"], maxsize=3)

    stack.add("mark")

    assert list(stack) == ["matthew", "luke", "mark"]
    assert len(stack) == 3


def test_add_purges_oldest_when_full():
    """should purge the least-recent when adding beyond maxsize"""

    stack = MRUStack(["matthew", "mark", "luke"], maxsize=3)

    stack.add("john")

    assert list(stack) == ["mark", "luke", "john"]
    assert "matthew" not in stack
    assert len(stack) == 3


def test_remove_existing_and_missing():
    """should remove an existing key and ignore missing keys"""

    stack = MRUStack(["matthew", "mark", "luke"], maxsize=3)

    stack.remove("mark")
    assert list(stack) == ["matthew", "luke"]
    assert len(stack) == 2

    stack.remove("genesis")
    assert list(stack) == ["matthew", "luke"]
    assert len(stack) == 2


def test_maxsize_zero_keeps_nothing():
    """should never retain entries when maxsize is zero"""

    stack = MRUStack(["matthew", "mark"], maxsize=0)

    assert len(stack) == 0
    assert list(stack) == []

    stack.add("john")
    assert len(stack) == 0
    assert list(stack) == []


def test_repr():
    """should include class name and ordered elements in representation"""

    stack = MRUStack(["matthew", "mark"], maxsize=5)

    assert repr(stack) == "MRUStack(['matthew', 'mark'])"
