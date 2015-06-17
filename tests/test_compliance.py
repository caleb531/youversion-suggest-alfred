#!/usr/bin/env python

import nose.tools as nose
import glob
import json
import jsonschema
import pep8


def test_pep8():
    '''all Python files should comply with PEP 8'''
    files = glob.iglob('*/*.py')
    for file in files:
        style_guide = pep8.StyleGuide(quiet=True)
        total_errors = style_guide.input_file(file)
        msg = '{} does not comply with PEP 8'.format(file)
        yield nose.assert_equal, total_errors, 0, msg


def test_json():
    '''all JSON files should comply with respective schemas'''
    schemas = {
        'schema-languages': 'yv_suggest/data/languages.json',
        'schema-defaults': 'yv_suggest/data/defaults.json',
        'schema-chapters': 'yv_suggest/data/bible/chapters.json',
        'schema-bible': 'yv_suggest/data/bible/language-*.json'
    }
    for schema_name, data_path_pattern in schemas.iteritems():
        schema_path = 'yv_suggest/data/schema/{}.json'.format(schema_name)
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)
            data_paths = glob.iglob(data_path_pattern)
            for data_path in data_paths:
                with open(data_path) as data_file:
                    data = json.load(data_file)
                    validator = jsonschema.validate(data, schema)
                    yield nose.assert_is_none, validator
