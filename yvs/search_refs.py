#!/usr/bin/env python3
# coding=utf-8

import sys
import urllib.parse

import yvs.core as core
import yvs.web as web


# Parses unique reference identifier from the given reference URL
def get_uid_from_url(url):
    return (
        url.replace(core.BASE_REF_URL, "")
        # Handle case where origin may be absent from 'href' value
        .replace(urllib.parse.urlparse(core.BASE_REF_URL).path, "")
    )


# Parser for search result HTML
class SearchResultParser(web.YVParser):
    def __init__(self, user_prefs):
        super().__init__()
        self.user_prefs = user_prefs

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        super().reset()
        self.depth = 0
        self.in_ref = False
        self.in_heading = False
        self.in_verse = False
        self.in_verse_content = False
        self.verse_content_depth = 0
        self.results = []
        self.current_result = None

    # Detects the start of search results, titles, reference content, etc.
    def handle_starttag(self, tag, attrs):
        self.depth += 1
        attrs = dict(attrs)
        # Detect beginning of search result
        if tag == "a" and "/bible/" in attrs.get("href", ""):
            self.in_ref = True
            self.in_heading = True
            self.current_result = {"arg": "", "title": "", "subtitle": ""}
            self.results.append(self.current_result)
            self.current_result["arg"] = get_uid_from_url(attrs["href"])
            self.current_result["variables"] = {
                "ref_uid": self.current_result["arg"],
                "ref_url": core.get_ref_url(self.current_result["arg"]),
                "copybydefault": str(self.user_prefs["copybydefault"]),
            }
            # Make "Copy" the default action (instead of "View") when the
            # copybydefault preference is set to true
            if self.user_prefs["copybydefault"]:
                self.current_result["mods"] = {
                    "cmd": {"subtitle": "View on YouVersion"}
                }
            else:
                self.current_result["mods"] = {
                    "cmd": {"subtitle": "Copy content to clipboard"}
                }
        # Detect beginning of search result content
        elif self.in_ref and tag == "p":
            self.in_verse = True
            self.in_verse_content = True
            self.verse_content_depth = self.depth

    # Detects the end of search results, titles, reference content, etc.
    def handle_endtag(self, tag):
        if self.in_ref and tag == "p":
            self.in_ref = False
            self.in_verse = False
            self.in_verse_content = False
            self.current_result["variables"]["full_ref_name"] = self.current_result[
                "title"
            ]
            self.current_result["subtitle"] = core.normalize_ref_content(
                self.current_result["subtitle"]
            )
        elif self.in_heading and tag == "a":
            self.in_heading = False
        self.depth -= 1

    # Handles verse content
    def handle_data(self, data):
        if self.in_heading:
            self.current_result["title"] += data
        elif self.in_verse_content:
            self.current_result["subtitle"] += data


# Retrieves HTML for reference with the given ID
def get_search_html(query_str, user_prefs, revalidate=False):
    url = "https://www.bible.com/search/bible?q={}&version_id={}".format(
        urllib.parse.quote_plus(query_str), user_prefs["version"]
    )
    entry_key = "{}/{}.html".format(user_prefs["version"], query_str)

    return web.get_url_content_with_caching(url, entry_key, revalidate=revalidate)


# Parses actual reference content from reference HTML
def get_result_list(query_str):
    query_str = core.normalize_query_str(query_str)
    user_prefs = core.get_user_prefs()
    parser = SearchResultParser(user_prefs)

    web.get_and_parse_html(
        parser=parser,
        html_getter=get_search_html,
        html_getter_args=(query_str, user_prefs),
        parser_results_attr="results",
    )

    return parser.results


def main(query_str):
    results = get_result_list(query_str)
    if not results:
        results.append(
            {
                "title": "No Results",
                "subtitle": "No references matching '{}'".format(query_str),
                "valid": False,
            }
        )

    print(core.get_result_list_feedback_str(results))


if __name__ == "__main__":
    main(sys.argv[1])
