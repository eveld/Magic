from BeautifulSoup import BeautifulSoup

import urllib
import math
import re

import store

# Url to parse
url = "http://www.dragonbreath.nl/index.php?main_page=index&cPath=149_176_434&sort=2a&page="

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("tr", {"class": ["productListing-odd", "productListing-even"]})
	for card in cards:
		# Remove the double faced card names
		name = re.sub(r"/.*$", "", card.findAll("td")[2].h3.a.string).strip()
		price = "$" + card.findAll("td")[5].text.replace("EUR... more info", "")
		
		# Check if the card should be allowed (non basic land / token)
		if store.filter_card(name):
			# Add the card to the store
			store.add_card(name, "", "")
			store.add_price(name, "Innistrad", "DragonBreath", price)
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
results = soup.find("div", "navSplitPagesResult").findAll("strong")
pages = int(math.ceil(float(results[2].string)/float(results[1].string)))

# Find all cards on the pages
for page in range(1, pages):
	soup = BeautifulSoup(read(url + str(page)))
	findCards(soup)
