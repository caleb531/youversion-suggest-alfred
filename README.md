# YouVersion Suggest

*Copyright 2015 Caleb Evans*  
*Released under the MIT license*

YouVersion Suggest is an Alfred workflow which allows you to search the online
[YouVersion](https://www.youversion.com/) bible quickly and conveniently.

![YouVersion Suggest in action](screenshots/chapters.png)

## Usage

Type the `yv` keyword, along with a space and a phrase representing the bible
reference you wish to find. The phrase can be partial book name, chapter, verse,
or range of verses. You may also include an option version (translation) at the
end of your query. As you type, YouVersion Suggest will display a list of
suggestions matching your query.

### Query Examples

* `luke` => Luke
* `eph 3` => Ephesians 3
* `1 t 3 e` => 1 Thessalonians 3 (ESV), 1 Timothy 3 (ESV)
* `mat 6:34 nlt` => Matthew 6:34 (NLT)
* `1 co 13.4-7` => 1 Corinthians 13.4-7

## Testing

If you are contributing to the project and would like to run the included unit
tests, run the `nosetests` command within the project directory.

```
nosetests
```

### Viewing test coverage

To view the test coverage report, run `nosetests` with the `--with-coverage` and
`--cover-erase` options.

```
nosetests --with-coverage --cover-erase
```

### Requirements for running tests

Note that all scripts apart of the workflow require Python 2.7 (Python 3 is not
supported). Running these unit tests requires `nose`, `coverage`, and `pep8` to
be installed. If you do not have these packages installed already, you can
install them via `pip`:

```
pip install nose coverage pep8
```
