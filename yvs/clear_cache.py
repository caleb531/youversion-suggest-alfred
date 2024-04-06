#!/usr/bin/env python3
# coding=utf-8

import json

import yvs.cache as cache


def main():

    cache.clear_cache()
    print(json.dumps({"alfredworkflow": {"variables": {"did_clear_cache": "True"}}}))


if __name__ == "__main__":
    main()
