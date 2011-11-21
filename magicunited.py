from BeautifulSoup import BeautifulSoup

import urllib

# Url to parse
url = "http://www.magicunited.nl/sets/innistrad/?batch_offset="

def findCards(soup):
	# All cards in the list
	cards = soup.find("div", id="content-binnen").tbody.findAll("tr")
	for card in cards:
		name = card.findAll("td")[0].find("a", text=True)
		price = card.findAll("td")[3].string[2:].replace(",", ".")
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
pages = int(soup.thead.tr.findAll("a")[-2].string)

# Find all cards on the pages
for page in range(0, pages):
	soup = BeautifulSoup(read(url + str(page * 50)))
	findCards(soup)
