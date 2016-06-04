# YouVersion Suggest

*Copyright 2016 Caleb Evans*  
*Released under the MIT license*

[![Build Status](https://travis-ci.org/caleb531/youversion-suggest.svg?branch=master)](https://travis-ci.org/caleb531/youversion-suggest)
[![Coverage Status](https://coveralls.io/repos/caleb531/youversion-suggest/badge.svg?branch=master)](https://coveralls.io/r/caleb531/youversion-suggest?branch=master)

YouVersion Suggest is an [Alfred](https://www.alfredapp.com/) workflow which
allows you to search the online [YouVersion](https://www.youversion.com/) Bible
quickly and conveniently.

The workflow will be solely supporting Alfred 3 going forward, but the latest
Alfred 2-compatible release (v5.0.0) will remain available here for your
convenience.

![YouVersion Suggest in action](screenshot.png)

## Usage

### Filtering by reference

To filter the YouVersion Bible by reference, type the `yvfilter` keyword into
Alfred, followed by a space and a phrase representing the bible reference you
wish to find. The phrase can be part of a book name, chapter, verse, or range of
verses. You may also include an optional version (translation) at the end of
your query. As you type, YouVersion Suggest will display a list of suggestions
matching your query.

**Pro Tip:** Type `yvf` and press the `tab` key to quickly filter by reference
(as this will expand to `yvfilter`).

#### Example queries

- `yvfilter luke` => Luke
- `yvfilter eph 3` => Ephesians 3
- `yvfilter 1t3e` => 1 Thessalonians 3 (ESV), 1 Timothy 3 (ESV)
- `yvfilter mat 6:34 nlt` => Matthew 6:34 (NLT)
- `yvfilter 1 co 13.4-7` => 1 Corinthians 13:4-7
- `yvfilter relevations 7` => Revelation 7

#### Actions

- Choosing a result will open the respective reference on the YouVersion website

- Choosing a result while pressing `command` will copy the contents of
the respective reference to the clipboard

- Choosing a result while pressing `ctrl` will open a Google search
for the respective reference.

- Pressing `shift` while a result is selected will preview the contents
of the respective reference (new in v6.1.0; Alfred 3 only)

- Pressing `command-c` while a result is selected will copy to the clipboard the respective reference's identifier, such as *1 Corinthians 13:4-7 (ESV)*

- Pressing `command-l` while a result is selected will show the respective reference's identifier as Large Type

### Searching by content

You can also search the YouVersion Bible by content using the `yvsearch`
keyword. As you type, YouVersion Suggest will display Bible verses whose content
contains your given keywords.

Note that when using the `yvsearch` filter, YouVersion Suggest will only search
for verses in your preferred version. To learn more about setting your preferred
version in YouVersion Suggest, see *Setting your preferred version*.

#### Example queries

- `yvsearch without faith` => Hebrews 11:6
- `yvsearch do not worry` => Matthew 6:34

#### Actions

You can perform all the same actions on a result with `yvsearch` as you can with
`yvfilter`.

### Setting your preferred language

YouVersion Suggest allows you to change the languages used for Bible references
and versions. To do so, type `yvset language` into Alfred, and the list of
supported languages will then appear. You may then choose another language to be
your preferred language.

Currently, YouVersion Suggest supports the following languages:

- Arabic (ar)
- Bulgarian (bg)
- Dutch (nl)
- English (en)
- Finnish (fi)
- French (fr)
- German (de)
- Hindi (hi)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Persian (fa)
- Polish (pl)
- Portuguese - Brazil (pt)
- Portuguese - Portugal (pt-PT)
- Russian (ru)
- Simplified Chinese (zh-CN)
- Spanish (es)
- Spanish - Spain (es-ES)
- Swahili (sw)
- Swedish (sv)

#### Requesting language support

If you would like to see YouVersion Suggest support a language not in the above
list, please [submit an issue on
GitHub](https://github.com/caleb531/youversion-suggest/issues) with the
following details:

- The name and ISO-639 code of the language from [this
list](https://www.bible.com/languages)

- The name of the YouVersion-supported Bible version to use as the default for
this language; click the language name on the page linked above to view the
versions available for the language

### Setting your preferred version

You may also set your preferred version (translation) used for Bible references
(where you have not explicitly specified the version in the query). To do so,
type `yvset version` into Alfred, and the list of supported versions (for the
currently-set language) will appear.

**Pro Tip:** Type `yvset v` and press the `tab` key to quickly see the list of
available versions to set (as this will expand to `yvset version`).

To select a version from the list of versions more quickly, you may optionally
type a query after `yvset version` to filter the list of versions.

#### Example queries

- `yvset version esv` => ESV
- `yvset version a` => AMP

### Setting your preferred search engine

You may also set your preferred search engine used for searching selected Bible
references. To do so, type `yvset search_engine` into Alfred (again, the tab
autocompletion will allow you to minimize typing).

#### Example queries

- `yvset search_engine b` => Bing
- `yvset search_engine d` => DuckDuckGo

## Disclaimer

This project is not affiliated with YouVersion, and all Bible content is
copyright of the respective publishers.
