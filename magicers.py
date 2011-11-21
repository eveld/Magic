from BeautifulSoup import BeautifulSoup

import urllib
import re

# Url to parse
url = "http://www.magicers.nl/webshop/innistrad_"

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("div", "list_option")
	for card in cards:
		name = card.find("span", "shadow").string
		price = card.find("div", "list_price_right_middle").text.replace("&#8364;", "$").replace(",", ".")
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
result = soup.find("div", "list_header").find("a", "pageswitch")["title"]
pages = int(re.compile("<a [a-zA-Z0-9_].*>(.*)</a>", re.DOTALL).findall(result)[0])

# Find all cards on the pages
for page in range(1, pages):
	soup = BeautifulSoup(read(url + str(page)))
	findCards(soup)
