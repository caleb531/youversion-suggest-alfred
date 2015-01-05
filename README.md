# YouVersion Suggest
*Copyright 2014 Caleb Evans*  
*Released under the MIT license*

## Usage

YouVersion Suggest is an Alfred workflow which allows you to search the online [YouVersion](https://www.youversion.com/) bible quickly and conveniently.

Type the `yv` keyword, along with a space and a phrase representing your search query. The query can be the phrase you want to search, *or* the bible book/chapter/verse you want to search. As you type, YouVersion Suggest will display a list of suggestions matching your query.

### Query Examples

* `ephesians`
* `eph 3`
* `1 c 3 niv`

## Testing

If you are contributing to the project and would like to run the included unit tests, run the following command in the project directory:

```
python -m unittest tests
```

Additionally, if you'd like to see more detail on which tests passed and failed (including descriptions of each test), run the above command with the `-v` flag:

```
python -m unittest tests -v
```

### Running an individual test

If you wish to run a single test, reference the module name

```
python -m unittest tests.test_search_book
```
