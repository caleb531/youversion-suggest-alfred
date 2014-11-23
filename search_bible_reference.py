# Search bible references corresponding to the typed query

# Import print function
from __future__ import print_function
# Import required modules
import cgi, json, re, time, urllib

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

# Load in books of the Bible
with open('books.json', 'r') as file:
	books = tuple(Book(book) for book in json.loads(file.read()))

# Load in Bible translations
with open('versions.json', 'r') as file:
	all_versions = tuple(json.loads(file.read()))

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
