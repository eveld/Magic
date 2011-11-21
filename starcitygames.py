from BeautifulSoup import BeautifulSoup

import urllib
import re

# Url to parse
url = "http://sales.starcitygames.com/category.php?cat=5215&start="

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("tr", {"class": ["deckdbbody", "deckdbbody2"]})
	for card in cards:
		name = re.compile("\"[.]*>(.*)", re.DOTALL).findall(card.findAll("td")[0].find("a").text)[0].strip()
		price = card.findAll(text=re.compile("\$(.*)", re.DOTALL))
		if len(price) > 0:
			print(price[0] + " = " + name)

# Download the page
def read(url):
	connection = urllib.urlopen(url)
	content = connection.read()
	connection.close()
	return content

# Parse the page
soup = BeautifulSoup(read(url))

# Find the number of pages
pages = int(soup.find("td", "leftcolumn").findNextSibling().findAll("tr", limit=3)[2].findAll("a")[-2].string[2])

# Find all cards on the pages
for page in range(0, pages):
	soup = BeautifulSoup(read(url + str(page * 50)))
	findCards(soup)
