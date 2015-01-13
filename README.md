# YouVersion Suggest

*Copyright 2015 Caleb Evans*  
*Released under the MIT license*

YouVersion Suggest is an Alfred workflow which allows you to search the online [YouVersion](https://www.youversion.com/) bible quickly and conveniently.

![YouVersion Suggest in action](screenshot.png)

## Usage

Type the `yv` keyword, along with a space and a phrase representing the bible reference you wish to find. The phrase can be partial book name, chapter, or verse. You may also include an option version (translation) at the end of your query. As you type, YouVersion Suggest will display a list of suggestions matching your query.

### Query Examples

* `luke`
* `eph 3`
* `1 c 3 esv`

## Testing

If you are contributing to the project and would like to run the included unit tests, run the following command in the project directory:

```
python -m unittest tests
```

Note that running these unit tests requires Python 2.7 or newer (Python 3 is not supported).

### Running an individual test case

If you wish to run a single test case, reference the module name like so:

```
python -m unittest tests.test_search_book
```
