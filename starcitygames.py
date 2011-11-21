from BeautifulSoup import BeautifulSoup

import urllib
import re

import store

# Url to parse
url = "http://sales.starcitygames.com/category.php?cat=5215&start="

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("tr", {"class": ["deckdbbody", "deckdbbody2"]})
	for card in cards:
		field = card.findAll("td")[0].find("a")
		if field is not None:
			temp = re.compile("\"[.]*>(.*)", re.DOTALL).findall(field.text)[0].strip()
			name = re.sub(r"\|.*$", "", temp).strip()
			price = card.findAll(text=re.compile("\$(.*)", re.DOTALL))
			if len(price) > 0:
				# Check if the card should be allowed (non basic land / token)
				if store.filter_card(name):
					# Add the card to the store
					store.add_card(name, "", "")
					store.add_price(name, "Innistrad", "StarCityGames", price[0][1:])
				else:
					print("Ignoring %s" % name)

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
