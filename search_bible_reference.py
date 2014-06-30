#!/usr/bin/env python

# Import print function
from __future__ import print_function
# Import required modules
import cgi, re, time, urllib
# Ensure compatibility with Python 3
if hasattr(urllib, 'quote_plus') == False:
	import urllib.parse as urllib

# Base class for creating objects of attributes
class AttrObject:
	def __init__(self, attrs=None):
		if attrs:
			for key, value in attrs.items():
				setattr(self, key, value)

# Subclasses used for data storage
class Book(AttrObject): pass
class Query(AttrObject): pass
class Reference(AttrObject): pass

# Books of the Bible
books = [
	Book({
		'name': 'Genesis',
		'id': 'gen',
		'chapters': 50
	}),
	Book({
		'name': 'Exodus',
		'id': 'exo',
		'chapters': 40
	}),
	Book({
		'name': 'Leviticus',
		'id': 'lev',
		'chapters': 27
	}),
	Book({
		'name': 'Numbers',
		'id': 'num',
		'chapters': 36
	}),
	Book({
		'name': 'Deuteronomy',
		'id': 'deu',
		'chapters': 34
	}),
	Book({
		'name': 'Joshua',
		'id': 'jos',
		'chapters': 24
	}),
	Book({
		'name': 'Judges',
		'id': 'jdg',
		'chapters': 21
	}),
	Book({
		'name': 'Ruth',
		'id': 'rut',
		'chapters': 4
	}),
	Book({
		'name': '1 Samuel',
		'id': '1sa',
		'chapters': 31
	}),
	Book({
		'name': '2 Samuel',
		'id': '2sa',
		'chapters': 24
	}),
	Book({
		'name': '1 Kings',
		'id': '1ki',
		'chapters': 22
	}),
	Book({
		'name': '2 Kings',
		'id': '2ki',
		'chapters': 25
	}),
	Book({
		'name': '1 Chronicles',
		'id': '1ch',
		'chapters': 29
	}),
	Book({
		'name': '2 Chronicles',
		'id': '2ch',
		'chapters': 36
	}),
	Book({
		'name': 'Ezra',
		'id': 'ezr',
		'chapters': 10
	}),
	Book({
		'name': 'Nehemiah',
		'id': 'neh',
		'chapters': 13
	}),
	Book({
		'name': 'Esther',
		'id': 'est',
		'chapters': 10
	}),
	Book({
		'name': 'Job',
		'id': 'job',
		'chapters': 42
	}),
	Book({
		'name': 'Psalm',
		'id': 'psa',
		'chapters': 150
	}),
	Book({
		'name': 'Proverbs',
		'id': 'pro',
		'chapters': 31
	}),
	Book({
		'name': 'Ecclesiastes',
		'id': 'ecc',
		'chapters': 12
	}),
	Book({
		'name': 'Song of Songs',
		'id': 'sng',
		'chapters': 8
	}),
	Book({
		'name': 'Isaiah',
		'id': 'isa',
		'chapters': 66
	}),
	Book({
		'name': 'Jeremiah',
		'id': 'jer',
		'chapters': 52
	}),
	Book({
		'name': 'Lamentations',
		'id': 'lam',
		'chapters': 5
	}),
	Book({
		'name': 'Ezekiel',
		'id': 'ezk',
		'chapters': 48
	}),
	Book({
		'name': 'Daniel',
		'id': 'dan',
		'chapters': 12
	}),
	Book({
		'name': 'Hosea',
		'id': 'hos',
		'chapters': 14
	}),
	Book({
		'name': 'Joel',
		'id': 'jol',
		'chapters': 3
	}),
	Book({
		'name': 'Amos',
		'id': 'amo',
		'chapters': 9
	}),
	Book({
		'name': 'Obadiah',
		'id': 'oba',
		'chapters': 1
	}),
	Book({
		'name': 'Jonah',
		'id': 'jon',
		'chapters': 4
	}),
	Book({
		'name': 'Micah',
		'id': 'mic',
		'chapters': 7
	}),
	Book({
		'name': 'Nahum',
		'id': 'nah',
		'chapters': 3
	}),
	Book({
		'name': 'Habakkuk',
		'id': 'hab',
		'chapters': 3
	}),
	Book({
		'name': 'Zephaniah',
		'id': 'zep',
		'chapters': 3
	}),
	Book({
		'name': 'Haggai',
		'id': 'hag',
		'chapters': 2
	}),
	Book({
		'name': 'Zechariah',
		'id': 'zec',
		'chapters': 14
	}),
	Book({
		'name': 'Malachi',
		'id': 'mal',
		'chapters': 4
	}),
	Book({
		'name': 'Matthew',
		'id': 'mat',
		'chapters': 28
	}),
	Book({
		'name': 'Mark',
		'id': 'mrk',
		'chapters': 16
	}),
	Book({
		'name': 'Luke',
		'id': 'luk',
		'chapters': 24
	}),
	Book({
		'name': 'John',
		'id': 'jhn',
		'chapters': 21
	}),
	Book({
		'name': 'Acts',
		'id': 'act',
		'chapters': 28
	}),
	Book({
		'name': 'Romans',
		'id': 'rom',
		'chapters': 16
	}),
	Book({
		'name': '1 Corinthians',
		'id': '1co',
		'chapters': 16
	}),
	Book({
		'name': '2 Corinthians',
		'id': '2co',
		'chapters': 13
	}),
	Book({
		'name': 'Galatians',
		'id': 'gal',
		'chapters': 6
	}),
	Book({
		'name': 'Ephesians',
		'id': 'eph',
		'chapters': 6
	}),
	Book({
		'name': 'Philippians',
		'id': 'php',
		'chapters': 4
	}),
	Book({
		'name': 'Colossians',
		'id': 'col',
		'chapters': 4
	}),
	Book({
		'name': '1 Thessalonians',
		'id': '1th',
		'chapters': 5
	}),
	Book({
		'name': '2 Thessalonians',
		'id': '2th',
		'chapters': 3
	}),
	Book({
		'name': '1 Timothy',
		'id': '1ti',
		'chapters': 6
	}),
	Book({
		'name': '2 Timothy',
		'id': '2ti',
		'chapters': 4
	}),
	Book({
		'name': 'Titus',
		'id': 'tit',
		'chapters': 3
	}),
	Book({
		'name': 'Philemon',
		'id': 'phm',
		'chapters': 1
	}),
	Book({
		'name': 'Hebrews',
		'id': 'heb',
		'chapters': 13
	}),
	Book({
		'name': 'James',
		'id': 'jas',
		'chapters': 5
	}),
	Book({
		'name': '1 Peter',
		'id': '1pe',
		'chapters': 5
	}),
	Book({
		'name': '2 Peter',
		'id': '2pe',
		'chapters': 3
	}),
	Book({
		'name': '1 John',
		'id': '1jn',
		'chapters': 5
	}),
	Book({
		'name': '2 John',
		'id': '2jn',
		'chapters': 1
	}),
	Book({
		'name': '3 John',
		'id': '3jn',
		'chapters': 1
	}),
	Book({
		'name': 'Jude',
		'id': 'jud',
		'chapters': 1
	}),
	Book({
		'name': 'Revelation',
		'id': 'rev',
		'chapters': 22
	})
]
# Available Bible translations
all_versions = (
	'AMP',
	'ASV',
	'BOOKS',
	'CEB',
	'CEV',
	'CEV',
	'CEVUK',
	'CPDV',
	'DARBY',
	'DRA',
	'ESV',
	'ERV',
	'GNB',
	'GNBDC',
	'GNBDK',
	'GNT',
	'GNTD',
	'GWT',
	'HCSB',
	'ISR98',
	'KJV',
	'LEB',
	'MSG',
	'NIV',
	'NIVUK',
	'NLT',
	'NET',
	'NKJV',
	'NCV',
	'NASB',
	'NABRE',
	'NIRV',
	'OJB',
	'RV1885',
	'TLV',
	'WEB'
)
# Default translation for all results
default_version = 'NIV'

# Base query URL
bible_url = 'https://www.bible.com/bible'
search_url = 'https://www.bible.com/search/bible'

# Regular expression for parsing a bible reference
bible_ref_patt = '(^((\d+ )?[a-z ]+)( (\d+)(\:(\d+)?)?)?( [a-z\d]+)?)$'

# Guess a translation based on the given text
def guess_version(text):
		text = text.upper()
		
		if text in all_versions:
			version_guess = text
		else:
			# Use a predetermined version by default
			version_guess = default_version
			if text != '':
				# Attempt to guess the version used
				for version in all_versions:
					if version.startswith(text):
						version_guess = version
						break
		
		return version_guess

# Search the bible for the given book/chapter/verse/version
def search_bible(query_str):
	results = []
	
	# Remove extra whitespace
	query_str = query_str.strip()
	query_str = re.sub('(\s)+', ' ', query_str)
	# Lowercase query for consistency
	query_str = query_str.lower()
	# Convert chapter.verse to chapter:verse
	query_str = re.sub('(\d+)\.(\d+)', '\\1:\\2', query_str)
	
	# Give the user the option to search the given query (instead of choosing a suggested reference)
	result = Reference()
	result.id = 'search-youversion'
	# Determine if the query includes the translation with which to search
	version_match = re.findall('( [a-z\d]+)$', query_str)
	if len(version_match) != 0:
		version = version_match[0][1:]
		result.version = guess_version(version)
	else:
		# Otherwise, search using the default translation
		result.version = default_version
	result.title = 'Search YouVersion for \'' + cgi.escape(query_str) + '\''
	result.subtitle = result.version.upper() + ' translation'
	result.url = '{base}?q={query}&amp;version_id={version}'.format(base=search_url, query=urllib.quote_plus(query_str), version=result.version.lower())
	
	# Prompt user to search the typed query before showing suggestions
	results.append(result)
	
	# Match section of the bible based on query
	parts = re.findall(bible_ref_patt, query_str)
	
	# 0 = full query
	# 1 = book name
	# 2 = leading book number (if any)
	# 3 = chapter and verse
	# 4 = chapter
	# 5 = :verse
	# 6 = verse
	# 7 = version
	
	if parts != []:
	
		parts = parts[0]
		
		# Create query object for storing query data
		query = Query()
		
		# Parse partial book name if given
		if parts[1] != None and parts[1] != '':
			query.book = parts[1]
		else:
			query.book = None

		# Parse chapter if given
		if parts[4] != None and parts[4] != '':
			query.chapter = int(parts[4])
		else:
			query.chapter = None
		
		# Parse verse if given
		if parts[6] != None and parts[6] != '':
			query.verse = int(parts[6])
		else:
			query.verse = None
		
		# Parse version if given
		if parts[7] != None:
			query.version = parts[7].lstrip().upper()
		else:
			query.version = None
		
		# Filter book list to match query
		matches = []
		for book in books:
		
			# Check if book name begins with the typed book name
			if book.name.lower().startswith(query.book.lower()):
				matches.append(book)
		
		# Loop through the books that mathed the query
		for book in matches:
			
			# Result information
			result = Reference()
			result.id = None
			result.url = bible_url
			
			if query.version != None:
				# Guess translation if possible
				query.version = guess_version(query.version)
			else:
				# Otherwise, use default translation
				query.version = default_version
			
			# Append version to URL
			result.url += '/{version}/'.format(version=query.version.lower())
			
			if query.chapter != None:
				# Find chapter or verse
				
				if query.chapter <= book.chapters:
					
					if query.verse != None:
						# Find verse if given
						
						result.id = '{book}.{chapter}.{verse}'.format(book=book.id, chapter=query.chapter, verse=query.verse)
					
						result.title = '{book} {chapter}:{verse}'.format(book=book.name, chapter=query.chapter, verse=query.verse)
					
					else:
						# Find chapter if given
					
						result.id = '{book}.{chapter}'.format(book=book.id, chapter=query.chapter)
						
						result.title = '{book} {chapter}'.format(book=book.name, chapter=query.chapter)
						
			else:
				# Find book if no chapter or verse is given
				
				result.id = '{book}.1'.format(book=book.id)
				
				result.title = book.name
			
			# Create result data using the given information
			if result.id != None:
				result.id += '.{version}'.format(version=query.version.lower())
				result.url += result.id
				result.version = query.version.upper()
				result.subtitle = '{version} translation'.format(version=result.version)
				results.append(result)
	
	xml = '<?xml version="1.0"?>\n<items>\n'
	for result in results:	
	
		if result.id != None:
			xml += """
			<item uid='{id}' arg='{url}'>
				<title>{title}</title>
				<subtitle>{subtitle}</subtitle>
				<icon>icon.png</icon>
			</item>
			""".format(**result.__dict__)
	
	xml += '\n</items>'
	return xml
	
print(search_bible("{query}"), end='')