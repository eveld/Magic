from BeautifulSoup import BeautifulSoup
import urllib
import re

import store

# Url to parse
url = "http://store.channelfireball.com/catalog/innistrad/616?filter[256]=Regular&page="

def findCards(soup):
	# All cards in the list
	products = soup.findAll("tr", {"class": ["product_row even", "product_row odd"]})
	for product in products:
		#image = product.find("a", "thumbnail")["href"]
		card = product.findAll("td")[1]
		
		# Remove the double faced card names
		name = re.sub(r"/.*$", "", card.a.string).strip()
		price = card.find("td", "price", recursive=True).string.strip()
		print("%s @ %s" % (name, price))
		
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