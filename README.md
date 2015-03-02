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

Currently, YouVersion Suggest supports the following languages:

* English
* Spanish
* Dutch

If you would like support added for another language, please [submit an issue on
GitHub](https://github.com/caleb531/youversion-suggest/issues).

### Setting your preferred version

You may also set your preferred version (translation) used for Bible references
(where you have not explicitly specified the version in the query). To do so,
type `yvset version` into Alfred, and the list of supported versions (for the
currently-set language) will appear.

To select a version from the list of versions more quickly, you may optionally
type a query after the initial query to filter the list of versions.

#### Example queries

* `yvset version esv`
* `yvset version a`
