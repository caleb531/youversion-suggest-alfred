-- replace HTML entity with corresponding character
on replaceEntity(html, entityName, entityChar)
	set AppleScript's text item delimiters to ("&#" & entityName & ";")
	set htmlItems to text items of html
	set AppleScript's text item delimiters to entityChar
	return htmlItems as text
end replaceEntity

-- replace all HTML entities with their corresponding characters
on replaceEntities(html)
	set html to replaceEntity(html, "8211", "–")
	set html to replaceEntity(html, "8212", "—")
	set html to replaceEntity(html, "8216", "‘")
	set html to replaceEntity(html, "8217", "’")
	set html to replaceEntity(html, "8220", "“")
	set html to replaceEntity(html, "8221", "”")
	return html
end replaceEntities

-- retrieve query string
set query to "{query}"
-- is query was given
if query is not "" then
	-- copy verse to clipboard
	set the clipboard to replaceEntities(query)
	-- play completion sound
	do shell script "afplay '/System/Library/Sounds/Hero.aiff'"
else
	-- play error sound
	do shell script "afplay '/System/Library/Sounds/Basso.aiff'"
end if