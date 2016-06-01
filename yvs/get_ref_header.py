# yvs.get_ref_header
# coding=utf-8
from __future__ import print_function
import sys


# Parse reference header from copied reference content for output
print(sys.argv[1].split('\n', 1)[0].rstrip(), end='')
