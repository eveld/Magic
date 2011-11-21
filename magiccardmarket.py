from BeautifulSoup import BeautifulSoup

import urllib
import re

# Url to parse
url = "http://www.magiccardmarket.eu/?mainPage=browseCategory&idCategory=1&idExpansion=1327&resultsPage="

def findCards(soup):
	# All cards in the list
	cards = soup.find("form", attrs={"name": "filterForm"}).findNextSibling("table").find("th", "col_price").parent.parent.findAll("tr", {"class": ["odd", "even"]})
	for card in cards:
		name = card.findAll("td")[2].a.string
		price = "$" + card.findAll("td")[6].string.replace(" &#x20AC;", "").replace(",", ".")
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
pages = int(soup.find("form", attrs={"name": "filterForm"}).findNextSibling("table").find("select", "queryNavigation").findAll("option")[-1].string)

# Find all cards on the pages
for page in range(0, pages):
	soup = BeautifulSoup(read(url + str(page)))
	findCards(soup)

