# yvs.get_ref_url
# coding=utf-8

from __future__ import print_function, unicode_literals

import sys

import yvs.shared as shared


def main(ref_uid):
    print(shared.get_ref_url(ref_uid).encode('utf-8'), end=''.encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
