#!/usr/bin/env python
# Open bible reference on YouVersion website

import webbrowser

# Base URL for Bible references
base_url = 'https://www.bible.com/bible/'

# Retrieve YouVersion URL for the given Bible reference ID
def get_ref_url(ref_uid):
	return '{base}{uid}'.format(base=base_url, uid=ref_uid)

# Open YouVersion URL for the given Bible reference ID
def open_ref_url(ref_uid):
	webbrowser.open(get_ref_url(ref_uid))

def main():
	uid = "{query}"
	open_ref_url(uid)

if __name__ == '__main__':
	main()
