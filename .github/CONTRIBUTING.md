# Contributing to YouVersion Suggest

## Submitting an issue

### Bug reports

If you are submitting a bug report, please answer the following questions:

- What version of YouVersion Suggest were you using?
- What were you doing?
- What did you expect to happen?
- What happened instead?

### Requesting language support

If you would like to see YouVersion Suggest support a language not in the above
list, please [submit an GitHub issue][issues-page] with the following details:

- The name and IETF language tag of the language from [this list][language-list] (*e.g.* `spa_es`)

- The name of the YouVersion-supported Bible version to use as the default for
this language; click the language name on the page linked above to view the
versions available for the language

If you're feeling adventurous, you may also try adding your own language using
the language utility apart the data module. See the [youversion-suggest-data
contributing guide][data-contributing-guide] for more information.

## Contributing code

Pull requests for bug fixes and new features are always welcome. Please be sure
to add or update unit tests as appropriate. Follow the steps below to set up the
repository for contributing.

### Cloning data submodule

All of the Bible data used by YouVersion Suggest is sourced from a separate
repository. You must pull this data down to properly run this project:

```bash
git submodule update --recursive --init
```

### Installing project dependencies

You can install all project dependencies via `uv`. This will automatically install a virtualenv for you.

```bash
uv sync
```

### Running unit tests

The project's unit tests are written using and managed under the [nose2][nose2]
Python package. You can run all unit tests via the `nose2` command.

```bash
nose2
```

## Code coverage

The project currently boasts high code coverage across all source files.
Contributions are expected to maintain this high standard. You can view the
current coverage report via the `coverage` command:

```bash
coverage run -m nose2
coverage report
```

If you want to examine which lines are/aren't covered, you can generate and view
a detailed HTML view of the coverage report like so:

```bash
coverage html
open htmlcov/index.html
```

[issues-page]: https://github.com/caleb531/youversion-suggest-alfred/issues
[language-list]: https://www.bible.com/languages
[data-contributing-guide]: https://github.com/caleb531/youversion-suggest-data/blob/master/CONTRIBUTING.md
[nose2]: https://docs.nose2.io/en/latest/
