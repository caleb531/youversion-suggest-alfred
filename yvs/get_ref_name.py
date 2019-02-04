#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import sys

import yvs.core as core


def main(ref_uid):
    user_prefs = core.get_user_prefs()
    ref = core.get_ref(ref_uid, user_prefs)
    print(core.get_full_ref_name(ref).encode('utf-8'),
          end=''.encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
