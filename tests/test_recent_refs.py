#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.shared as yvs
import os.path
import context_managers as ctx


def test_max_len():
    """should cap length of recent list to defined length"""
    with ctx.preserve_recent_refs():
        yvs.update_recent_refs([])
        for verse in range(1, yvs.max_recent_refs + 5):
            yvs.push_recent_ref('59/jhn.3.{}'.format(verse))
        recent_refs = yvs.get_recent_refs()
        nose.assert_equal(len(recent_refs), yvs.max_recent_refs)


def test_dup_ref():
    """should not add reference already present in recent list"""
    with ctx.preserve_recent_refs():
        yvs.update_recent_refs([])
        dup_ref = '59/psa.73.26'
        for i in range(2):
            yvs.push_recent_ref(dup_ref)
        recent_refs = yvs.get_recent_refs()
        nose.assert_equal(recent_refs.count(dup_ref), 1)


def test_creation():
    """should create recent list if nonexistent"""
    with ctx.preserve_recent_refs():
        yvs.delete_recent_refs()
        nose.assert_false(os.path.exists(yvs.recent_refs_path))
        recent_refs = yvs.get_recent_refs()
        nose.assert_true(os.path.exists(yvs.recent_refs_path))
        nose.assert_equal(recent_refs, [])


def test_delete_nonexistent():
    """should attempt to delete nonexistent recent list without error"""
    with ctx.preserve_recent_refs():
        try:
            yvs.delete_recent_refs()
            yvs.delete_recent_refs()
        except Exception as error:
            nose.assert_true(False, error)
