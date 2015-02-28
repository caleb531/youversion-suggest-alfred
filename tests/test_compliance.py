#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import glob
import json
import pep8
import jsonschema


def test_pep8():
    files = glob.iglob('*/*.py')
    for file in files:
        test_pep8.__doc__ = '{} should comply with pep8'.format(file)
        style_guide = pep8.StyleGuide(quiet=True)
        total_errors = style_guide.input_file(file)
        msg = '{} is not pep8-compliant'.format(file)
        yield nose.assert_equal, total_errors, 0, msg


def test_json():
    schemas = {
        'schema_language': 'yv_suggest/data/language.json',
        'schema_defaults': 'yv_suggest/data/defaults.json',
        'schema_bible': 'yv_suggest/data/bible/*.json'
    }
    for schema_name, data_path_pattern in schemas.iteritems():
        schema_path = 'yv_suggest/data/schema/{}.json'.format(schema_name)
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)
            data_paths = glob.iglob(data_path_pattern)
            for data_path in data_paths:
                with open(data_path) as data_file:
                    data = json.load(data_file)
                    try:
                        validator = jsonschema.validate(data, schema)
                        yield nose.assert_is_none, validator
                    except jsonschema.exceptions.ValidationError as error:
                        assert False, error
