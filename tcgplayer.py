from BeautifulSoup import BeautifulSoup

import urllib
import re

# Url to parse
url = "http://magic.tcgplayer.com/db/search_result.asp?Set_Name=Innistrad"

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("form")[1].findAll("table")[1].findAll("tr")
	for card in cards:
		name = card.findAll("td")[0].a.string
		price = card.findAll("td")[4].a.string
		print(price + " = " + name)

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
