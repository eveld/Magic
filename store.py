import redis
import datetime

# Connect to the redis host
r = redis.Redis("localhost")

# Seriously get a little more consistent please ;P
ignore = [
# Checklist
"Checklist DFC", "Checklist card", "Double-Sided Card Checklist", "[Checklist Card]",

# Tokens
"Angel token", "Demon token", "Ooze token", "Spider token", "Spirit token", "Vampire token", "Homunculus token", "Wolf token",

# Lands
"Forest", "Swamp", "Island", "Mountain", "Plains",

# BazaarOfMagic
"Swamp (1)", "Swamp (2)", "Swamp (3)",
"Plains (1)", "Plains (2)", "Plains (3)",
"Mountain (1)", "Mountain (2)", "Mountain (3)",
"Island (1)", "Island (2)", "Island (3)",
"Forest (1)", "Forest (2)", "Forest (3)",
"Angel token (4/4)", "Demon token (5/5)", "Homunculus token (2/2)", "Ooze token (*/*)", "Spider token (1/2)", "Spirit Token (White 1/1)",
"Spirit token (1/1)", "Vampire token (2/2)", "Zombie token (1) (2/2)", "Zombie token (2) (2/2)", "Zombie token (3) (2/2)",
"Wolf token (1) (1/1)", "Wolf token (2) (2/2)",

# MagicCardMarket
"Swamp (Version 1)", "Swamp (Version 2)", "Swamp (Version 3)",
"Plains (Version 1)", "Plains (Version 2)", "Plains (Version 3)",
"Mountain (Version 1)", "Mountain (Version 2)", "Mountain (Version 3)",
"Island (Version 1)", "Island (Version 2)", "Island (Version 3)",
"Forest (Version 1)", "Forest (Version 2)", "Forest (Version 3)",
"Zombie Token (Black 2/2) (Version 1)", "Zombie Token (Black 2/2) (Version 2)", "Zombie Token (Black 2/2) (Version 3)",
"Wolf Token (Green 2/2)", "Wolf Token (Black 1/1)", "Vampire Token (Black 2/2)", 
"Angel Token (White 4/4)", "Demon Token (Black 5/5)", "Homunculus Token (Blue 2/2)", "Ooze Token (Green */*)", "Spider Token (Green 1/2)",

# NederMagic
"Plains (A)", "Plains (B)", "Plains (C)", 
"Mountain (A)", "Mountain (B)", "Mountain (C)",
"Island (A)", "Island (B)", "Island (C)",
"Forest (A)", "Forest (B)", "Forest (C)",
"Swamp (A)", "Swamp (B)", "Swamp (C)",
"Wolf token (A)", "Wolf token (B)",
"Zombie token (A)", "Zombie token (B)", "Zombie token (C)",

# ChannelFireball
"Forest (262)", "Forest (263)", "Forest (264)",
"Island (253)", "Island (254)", "Island (255)",
"Mountain (259)", "Mountain (260)", "Mountain (261)",
"Plains (250)", "Plains (251)", "Plains (252)",
"Swamp (256)", "Swamp (257)", "Swamp (258)",
"Angel Token", "Demon Token", "Ooze Token", "Spider Token", "Spirit Token", "Vampire Token", "Homunculus Token",
"Zombie Token A", "Zombie Token B", "Zombie Token C", "Wolf Token (Green)", "Wolf Token (Black)",

# StarCityGames
"Forest (#262)", "Forest (#263)", "Forest (#264)",
"Swamp (#256)", "Swamp (#257)", "Swamp (#258)",
"Plains (#250)", "Plains (#251)", "Plains (#252)",
"Mountain (#259)", "Mountain (#260)", "Mountain (#261)",
"Island (#253)", "Island (#254)", "Island (#255)",
"[Spirit Token]", "[Vampire Token]", "[Spider Token]", "[Ooze Token]", "[Demon Token]", "[Angel Token]", "[Homunculus Token]",
"[Zombie Token] (#7)", "[Zombie Token] (#8)", "[Zombie Token] (#9)", 
"[Wolf Token] (Green)", "[Wolf Token] (Black)",

# Magicers
"Mountain 259", "Mountain 260", "Mountain 261",
"Island 253", "Island 254", "Island 255",
"Forest 262", "Forest 263", "Forest 264",
"Plains 250", "Plains 251", "Plains 252",
"Swamp 256", "Swamp 257", "Swamp 258",
"Zombie Token nr. 7", "Zombie Token nr. 8", "Zombie Token nr. 9"
]

'''
Add a card to the database
@ name 		(str)	name of the card
@ block 	(str)	block in which the card was released e.g. Innistrad, Urza's Sage, etc.
@ type		(str)	type of the card e.g. creature, land, etc.
@ color		(str)	color of the card e.g. blue, colorless, land, etc.
'''
def add_card(name, type, color):
	if r.sadd("cards", name):
		r.hset("card:%s" % name, "type", type)
		r.hset("card:%s" % name, "color", color)
		return True
	else:
		return False

'''
Prevent a card from being inserted into the database
@ name		(str)	name of the card
'''
def filter_card(name):
	if name in ignore:
		return False
	else:
		return True
	
'''
Delete a card from the database
@ name		(str)	name of the card
'''
def delete_card(name):
	if name is None:
		return False
	if name in r.smembers("cards"):
		r.srem("cards", name)
		r.delete("card:%s" % name)
		return True
	else:
		return False

'''
Add a price to a card in the database
@ name		(str)	name of the card
@ block		(str)	block in which the card was released e.g. Innistrad, Urza's Sage, etc.
@ shop		(str)	the shop where the price is from e.g. NederMagic, ChannelFireball, etc.
@ price		(float)	the price of the card at the shop e.g. 0.10
'''	
def add_price(name, block, shop, price):
	now = datetime.datetime.now().strftime("%Y%m%d")
	if r.sadd("prices", "%s:%s:%s" % (name, block, now)):
		r.hset("price:%s:%s:%s" % (name, block, now), "%s" % shop, price)
		return True
	else:
		if r.hset("price:%s:%s:%s" % (name, block, now), "%s" % shop, price):
			return True
		return False

'''
Get all cards
'''
def get_cards():
	return r.smembers("cards")
	
'''
Get all cards from a specific block
@ block		(str)	block in which the card was released e.g. Innistrad, Urza's Sage, etc.
'''
def get_cards(block):
	return r.smembers("cards")

'''
Get all prices for a card
@ name		(str)	name of the card
@ block		(str)	block in which the card was released e.g. Innistrad, Urza's Sage, etc.
@ date		(str)	the date of which the average price needs to be calculated e.g. 20111126
'''
def get_prices(name, block, date):
	return r.hgetall("price:%s:%s:%s" % (name, block, date))

'''
Get the average price of a card
@ name		(str)	name of the card
@ block		(str)	block in which the card was released e.g. Innistrad, Urza's Sage, etc.
@ date		(str)	the date of which the average price needs to be calculated e.g. 20111126
'''
def get_average_price(name, block, date):
	average = 0.0
	prices = r.hvals("price:%s:%s:%s" % (name, block, date))
	for price in prices:
		average = average + float(price)
	return average/len(prices)