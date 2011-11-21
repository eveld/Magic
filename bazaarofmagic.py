from BeautifulSoup import BeautifulSoup

import urllib

# Url to parse
url = "http://www.bazaarofmagic.nl/magic/innistrad-c-2888.html?page="

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("tr", {"class": ["product-listing-odd1", "product-listing-even1"]})
	for card in cards:
		name = card.findAll("td")[1].a.string
		price = card.findAll("td")[5].string.replace("&euro;&nbsp;", "$").replace(",", ".")
		print(price + " = " + name)

# Download the page
def read(url):
	connection = urllib.urlopen(url)
	content = connection.read()
	connection.close()
	return content

# Parse the page
soup = BeautifulSoup(read(url))

# Find the number of pages
pages = int(soup.find("td", "split-results", align="left").findAll("b")[1].string)

# Find all cards on the pages
for page in range(1, pages):
	soup = BeautifulSoup(read(url + str(page)))
	findCards(soup)
