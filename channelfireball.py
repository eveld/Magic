from BeautifulSoup import BeautifulSoup
import urllib

# Url to parse
url = "http://store.channelfireball.com/buylist/innistrad/616?filter[256]=Regular&filtered=1&page="

def findCards(soup):
	# All cards in the grid
	products = soup.findAll("div", "product_grid")
	for product in products:
		#image = product.find("a", "thumbnail")["href"]
		name = product.find("div", "name").a.string
		price = product.find("span", "price", recursive=True).string
		#print(price.strip() + ' = ' + name)
		
	# All cards in the list
	products = soup.findAll("tr", "product_row")
	for product in products:
		#image = product.find("a", "thumbnail")["href"]
		card = product.findAll("td")[1]
		name = card.a.string
		price = card.find("td", "price", recursive=True).string
		#print(price.strip() + ' = ' + name)

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
