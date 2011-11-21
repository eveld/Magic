from BeautifulSoup import BeautifulSoup

import urllib
import re

# Url to parse
url = "http://www.nedermagic.nl/magic-cards.asp?rec=277&s=83&page="

def findCards(soup):
	# All cards in the list
	cards = soup.findAll("tr", "searchrow")
	for card in cards:
		name = card.find("a", "kaartnaam").string.replace("&rsquo;", "'")
		price = card.findAll("td")[2].b.string.replace("&euro; ", "$").replace(",", ".")
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
result = soup.find(text=re.compile("pagina 1 van de"))
pages = int(re.compile("pagina 1 van de (.*)", re.DOTALL).findall(result)[0].strip())

# Find all cards on the pages
for page in range(1, pages):
	soup = BeautifulSoup(read(url + str(page)))
	findCards(soup)
