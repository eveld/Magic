from BeautifulSoup import BeautifulSoup
import urllib
import re

import store

# Url to parse
url = "http://store.channelfireball.com/buylist/innistrad/616?filter[256]=Regular&filtered=1&page="

def findCards(soup):
	# All cards in the grid
	products = soup.findAll("div", "product_grid")
	for product in products:
		#image = product.find("a", "thumbnail")["href"]
		name = re.sub(r"/.*$", "", product.find("div", "name").a.string).strip()
		price = product.find("span", "price", recursive=True).string.strip()
		
		# Check if the card should be allowed (non basic land / token)
		if store.filter_card(name):
			# Add the card to the store
			store.add_card(name, "", "")
			store.add_price(name, "Innistrad", "ChannelFireball", price)
		else:
			print("Ignoring %s" % name)
		
	# All cards in the list
	products = soup.findAll("tr", "product_row")
	for product in products:
		#image = product.find("a", "thumbnail")["href"]
		card = product.findAll("td")[1]
		
		# Remove the double faced card names
		name = re.sub(r"/.*$", "", card.a.string).strip()
		price = card.find("td", "price", recursive=True).string.strip()
		
		# Check if the card should be allowed (non basic land / token)
		if store.filter_card(name):
			# Add the card to the store
			store.add_card(name, "", "")
			store.add_price(name, "Innistrad", "ChannelFireball", price)
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
pages = int(soup.find("div", "pagination").findAll("a")[-2].string) + 1

# Find all cards on the pages
for page in range(1, pages):
	soup = BeautifulSoup(read(url + str(page)))
	findCards(soup)
