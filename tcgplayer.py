from BeautifulSoup import BeautifulSoup

import urllib
import re

import store

# Url to parse
url = "http://magic.tcgplayer.com/db/search_result.asp?Set_Name=Innistrad"

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("form")[1].findAll("table")[1].findAll("tr")
	for card in cards:
		name = card.findAll("td")[0].a.string
		price = card.findAll("td")[4].a.string[1:]
		
		# Check if the card should be allowed (non basic land / token)
		if store.filter_card(name):
			# Add the card to the store
			store.add_card(name, "", "")
			store.add_price(name, "Innistrad", "TCGPlayer", price)
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

# Find all cards on the page
findCards(soup)
