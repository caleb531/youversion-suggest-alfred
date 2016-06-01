# yvs.parse_copied_ref
# coding=utf-8
from __future__ import print_function
import sys


# Print only reference header from copied reference content
print(sys.argv[1].split('\n', 1)[0].rstrip(), end='')
