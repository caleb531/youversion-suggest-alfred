#!/usr/bin/env python

# Import print function
from __future__ import print_function, unicode_literals
# Import regular expression module
import re
# Import URL library
try:
	from urllib import urlopen
except ImportError:
	from urllib.request import urlopen
# Import HTML parser module
try:
	from HTMLParser import HTMLParser
except ImportError:
	from html.parser import HTMLParser

# Class for creating collections of regular expression patterns
class Patterns():
	pass

# List of allowed entity codes
allowed_entities = [
	# En-dash
	'8211',
	# Em-dash
	'8212',
	# Left single curly quote
	'8216',
	# Right single curly quote
	'8217',
	# Left double curly quote
	'8220',
	# Right double curly quote
	'8221']

# Create object for storing patterns
patt = Patterns()
patt.base_url = '^https?://www\.bible\.com/bible/([a-z\d]+)/'
patt.verse_id = '(\d?[a-z]+)\.(\d+)\.(\d+)'
patt.chapter_id = '([a-z\d]+)\.(\d+)'
patt.version_id = '(?<=/bible/)([a-z\d]+)'

# Remove extra whitespace from the given string
def remove_extra_whitespace(string):
	string = string.strip()
	string = re.sub('\s+', ' ', string)
	return string

# Class to parse the bible verse
class VerseParser(HTMLParser):
	def __init__(self, verse_id):
		# Initialize object using parent class
		HTMLParser.__init__(self)
		# Initialize state variables
		self.in_verse_name = False
		self.in_verse = False
		self.in_content = False
		self.verse_found = False
		self.depth = 0
		# Initialize data variables
		self.verse_id = verse_id
		self.verse = ''
		self.verse_name = ''
		
	# Handle HTML start tags
	def handle_starttag(self, tag, attrs):
		if tag == 'span':
			dattrs = dict(attrs)
			elem_data = dattrs.get('data-usfm')
			# If element is a verse container
			if elem_data and elem_data.lower().startswith(self.verse_id):
				# Signify that parser is within verse
				self.in_verse = True
			else:
				if self.in_verse:
					# Otherwise, retrieve element class
					elem_class = dattrs.get('class')
					# If element is a designated verse
					if elem_class and 'content' in elem_class:
						# Signify that parser is within verse fragment
						self.in_content = True
					self.depth += 1
				else:
					elem_id = dattrs.get('id')
					# If element is the verse reference
					if elem_id and 'modal_ref' in elem_id:
						self.in_verse_name = True
					
	# Handle HTML end tags
	def handle_endtag(self, tag):
		if tag == 'span':
			if self.in_content:
				# Signify that verse fragment has ended
				self.in_content = False
			elif self.in_verse and self.depth == 0:
				# Signify that verse has ended
				self.verse_found = True
				self.in_verse = False
				# Remove extran whitespace from verse
				self.verse = remove_extra_whitespace(self.verse)
				if self.verse.startswith('\"') and self.verse.count('\"') == 1:
					self.verse = self.verse[1:]
			elif self.in_verse_name:
				# Signify end of verse name
				self.in_verse_name = False
			# Ascend into parent
			if self.in_verse:
				self.depth -= 1
		
	# Handle data (e.g. text nodes)
	def handle_data(self, data):
		# If parser is in verse fragment and verse has not already been found
		if self.in_verse and self.in_content and not self.verse_found:
			self.verse += data
		elif self.in_verse_name:
			# Otherwise, if parser is in verse name
			# Add its content to data string
			self.verse_name += data
		
	# Handle numbered character entities
	def handle_charref(self, name):
		if self.in_verse and self.in_content and name in allowed_entities:
			self.verse += '&#{num};'.format(num=name)
	
# Retrieve bible reference using the given URL
def get_bible_reference(query_str):
	
	# If the given query string is a valid bible URL
	if re.search(patt.base_url + patt.verse_id, query_str):
		
		# Parse version from URL
		version = re.search(patt.version_id, query_str).group(1).upper()
		
		# Retrieve bible verse using GET request
		response = urlopen(query_str)
		html = response.read().decode('utf-8')

		# Parse verse ID from URL
		verse_id = re.search(patt.verse_id, query_str).group(0)
		
		# Parse HTML content
		parser = VerseParser(verse_id)
		parser.feed(html)
		# Print formatted verse reference
		return '{verse}\n({verse_name} {version})'.format(verse=parser.verse, verse_name=parser.verse_name, version=version)
	
	else:
		# Otherwise, return an empty string
		
		return ''

print(get_bible_reference("{query}"), end='')