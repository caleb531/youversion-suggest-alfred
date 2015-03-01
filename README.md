# YouVersion Suggest

*Copyright 2015 Caleb Evans*  
*Released under the MIT license*

YouVersion Suggest is an Alfred workflow which allows you to search the online
[YouVersion](https://www.youversion.com/) bible quickly and conveniently.

![YouVersion Suggest in action](screenshot.png)

## Usage

Type the `yv` keyword into Alfred, followed by a space and a phrase representing
the bible reference you wish to find. The phrase can be part of a book name,
chapter, verse, or range of verses. You may also include an optional version
(translation) at the end of your query. As you type, YouVersion Suggest will
display a list of suggestions matching your query.

Choosing a result will open the selected reference on the YouVersion website.
Choosing a result while holding down the *ctrl* key will open a Google
search for the selected reference.

### Example queries

* `yv luke` => Luke
* `yv eph 3` => Ephesians 3
* `yv 1t3e` => 1 Thessalonians 3 (ESV), 1 Timothy 3 (ESV)
* `yv mat 6:34 nlt` => Matthew 6:34 (NLT)
* `yv 1 co 13.4-7` => 1 Corinthians 13:4-7
* `yv relevations 7` => Revelation 7

### Setting your preferred language

YouVersion Suggest allows you to change the languages used for Bible references
and versions. To do so, type `yvset language` into Alfred, and the list of
supported languages will then appear. You may then choose another language as
your preferred language.


### Setting your preferred version

You may also set your preferred version (translation) used for Bible references
(where you haven't explicitly specified the version in the query). To do so,
type `yvset version` into Alfred, and the list of supported versions (for the
currently-set language) will appear.

To select a version from the list of versions more quickly, you may optionally
type a query after the initial query to filter the list of versions.

#### Example queries

* `yvset version esv`
* `yvset version a`

### Supported versions

#### English

AMP, ASV, BOOKS, CEB, ESV, GNT, KJV, MSG, NASB, NCV, NET, NIRV, NIV (default),
NIVUK, NKJV, NLT

#### Spanish (Español)

BLPH, DHHD, LBLA, NBLH, NTV, NVI (default), PDT, RVC, RVES, RVR1960, RVR95, TLA,
TLAD

## Testing

### Requirements for running tests

Running these unit tests requires Python 2.7, as well as the following packages:

* nose
* coverage
* pep8
* jsonschema

If you do not have these packages installed already, you can install them via
`pip`:

```
sudo pip install nose coverage pep8 jsonschema
```

### Running tests

To run all included unit tests, run the `nosetests` command at the root of the
project directory.

```
nosetests
```

### Viewing test coverage

To view the test coverage report, run `nosetests` with the `--with-coverage` and
`--cover-erase` flags.

```
nosetests --with-coverage --cover-erase
```

### Adding new languages

Currently, YouVersion Suggest only supports English and Spanish, with English as
the default. However, YouVersion Suggest v2 enables developers to add support
for *any* language via the workflow's public API. To do so, follow the steps
below.

#### 1. Define language information

To add a mew language, you must first add information about your language to the
`languages.json` file under the `yv_suggest/data/` directory. The value for the
`name` key should be the name of the language as written in said language.


#### 2. Define Bible data for language

All bible data files are located in the `yv_suggest/data/bible/` directory. Each
filename must be equal to the `id` of the corresponding language as defined in
`languages.json`.

#### 3. Run unit tests

To ensure that your modifications are complete, it is recommended that you run
all project unit tests (see above). The test runner will raise an error if any
of the modified data files do not conform to the defined schema.

#### 4. Copy changes into installed workflow

To test your changes within Alfred, you must copy the modified `data/`
directory to the installed workflow directory. To do so, open Alfred Preferences
and navigate to the Workflows pane. Right-click YouVersion Suggest in the
sidebar and choose *Show in Finder* from the contextual menu. You can then drag
the modified `data/` directory to the installed workflow directory to replace
it.

#### Schema

Please refer to the included JSON schemas (under the `yv_suggests/data/schema/`
directory) for the structure of each data file.
