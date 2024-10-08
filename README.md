# YouVersion Suggest for Alfred

*Copyright 2014-2024 Caleb Evans*  
*Released under the MIT license*

[![tests](https://github.com/caleb531/youversion-suggest-alfred/actions/workflows/tests.yml/badge.svg)](https://github.com/caleb531/youversion-suggest-alfred/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/caleb531/youversion-suggest-alfred/badge.svg?branch=master)](https://coveralls.io/r/caleb531/youversion-suggest-alfred?branch=master)

YouVersion Suggest is an [Alfred](https://www.alfredapp.com/) workflow which
allows you to search the online [YouVersion](https://www.youversion.com/) Bible
quickly and conveniently.

The workflow will be solely supporting Alfred 5.5 going forward, but the latest
releases for Alfred 4 and earlier will remain available here for your
convenience.

## Disclaimer

This project is not affiliated with YouVersion, and all Bible content is
copyright of the respective publishers.

This tool also retrieves Bible content directly from YouVersion for personal
use. However, please be aware that this functionality does not fully comply with
YouVersion's Terms of Use.

## Installation

To download the workflow, simply click one of the download links below. Please
note that only the Alfred 5 version has all the latest features.

[Download YouVersion Suggest (Alfred 5)][workflow-download-alfred5]

[workflow-download-alfred5]: https://github.com/caleb531/youversion-suggest-alfred/raw/main/YouVersion%20Suggest%20(Alfred%205).alfredworkflow

[Download YouVersion Suggest (Alfred 4)][workflow-download-alfred4]

[workflow-download-alfred4]: https://github.com/caleb531/youversion-suggest-alfred/raw/main/YouVersion%20Suggest%20(Alfred%204).alfredworkflow

### Command Line Tools

If you are installing the workflow for the first time, you may be prompted to
install Apple's Command Line Tools. These developer tools are required
for the workflow to function, and fortunately, they have a much smaller size
footprint than full-blown Xcode.

<img src="screenshot-clt-installer.png" alt="Prompt to install Apple's Command Line Tools" width="461" />

## Usage

### Filtering by reference

The `yvfilter` keyword allows you to filter the YouVersion Bible by reference,
meaning you can jump to a particular Bible reference (book, chapter, verse, or
range of verses) with just a few keystrokes.

**Pro Tip:** Type `yvf` and press the `tab` key to quickly filter by reference
(as this will expand to `yvfilter`).

#### Example queries

- `yvfilter luke` => Luke
- `yvfilter eph 3` => Ephesians 3
- `yvfilter 1t3es` => 1 Thessalonians 3 (ESV), 1 Timothy 3 (ESV)
- `yvfilter mat 6:34 nlt` => Matthew 6:34 (NLT)
- `yvfilter 1 co 13.4-7` => 1 Corinthians 13:4-7

![Filtering by reference](screenshot-yvfilter.png)

#### Actions

- Choosing a result will open the Bible reference on the YouVersion website

- Choosing a result while pressing `command` will copy the contents of the Bible
reference to the clipboard

- Choosing a result while pressing `ctrl` will open a Google search for the
Bible reference.

- Choosing a result while pressing `shift` will preview the contents of the
Bible reference; hitting the Escape key will return you to the results

- Choosing a result while pressing `option` will copy the URL of the Bible
reference to the clipboard

- Pressing `command-c` while a result is selected will copy to the clipboard the
full Bible reference address, such as *1 Corinthians 13:4-7 (ESV)*

- Pressing `command-l` while a result is selected will show the full Bible
reference address as Large Type

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

![Searching by content](screenshot-yvsearch.png)

#### Actions

You can perform all the same actions on a result with `yvsearch` as you can with
`yvfilter`.

### Setting your preferred language

YouVersion Suggest allows you to change the languages used for Bible references
and versions. To do so, type `yvset language` into Alfred, and the list of
supported languages will then appear. You may then choose another language to be
your preferred language.

Currently, YouVersion Suggest supports the following languages:

- Arabic (arb)
- Bulgarian (bul)
- Dutch (nld)
- Chinese - Simplified (zho)
- Chinese - Traditional (zho-TW)
- English (eng)
- Finnish (fin)
- French (fra)
- German (deu)
- Hindi (hin)
- Indonesian (ind)
- Italian (ita)
- Japanese (jpn)
- Khmer (khm)
- Korean (kor)
- Persian (pes)
- Polish (pol)
- Portuguese (por)
- Portuguese - Portugal (por-PT)
- Romanian (ron)
- Russian (rus)
- Spanish (spa)
- Spanish - Spain (spa-ES)
- Swahili (swh)
- Swedish (swe)
- Ukrainian (ukr)
- Vietnamese (vie)

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
references. To do so, open the YouVersion Suggest workflow in Alfred Preferences
and double-click the *Default Web Search* object. You can then choose a search
engine to set as your preferred for YouVersion Suggest.

### Showing verse numbers in copied Bible content

You can choose whether or not to include verse numbers in copied Bible verses by
typing `yvset versenumbers yes`.

### Stripping line breaks in copied Bible content

You can choose whether or not to strip line breaks from copied Bible content, so
that the verses you copy appear all on one line (even if it's from a psalm, for
example). To do this, type `yvset linebreaks no`.

### Making "Copy to Clipboard" the default action

If you would prefer to just press `Enter` (without holding down the `command`
key) to copy the content of a Bible reference, type `yvset copybydefault yes`.
When this is enabled, you can still open the selected reference on the
YouVersion website by holding down the `command` key.

### Universal Actions

Version 15 of the workflow brings integration with Alfred's
[Universal Actions][universal-actions] feature, enabling you to pass any
arbitrary text to the workflow when you select it within an app or on a webpage.

To use this, you must enable the **Workflow Universal Actions** checkbox in
Alfred Preferences, under **Features > Universal Actions > Actions**.

In particularly, there are two universal actions available:

1. Look up Bible address
2. Search phrase in Bible

[universal-actions]: https://www.alfredapp.com/help/features/universal-actions/
