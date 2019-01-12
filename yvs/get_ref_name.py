# yvs.get_ref_name
# coding=utf-8

from __future__ import print_function, unicode_literals

import sys

import yvs.shared as shared


def main(ref_uid):
    user_prefs = shared.get_user_prefs()
    ref_object = shared.get_ref_object(ref_uid, user_prefs)
    print(shared.get_full_ref_name(ref_object).encode('utf-8'),
          end=''.encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
