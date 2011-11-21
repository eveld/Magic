import redis
import datetime

r = redis.Redis("localhost")

# Seriously get a little more consistent please ;P
ignore = [
"Wolf Token (A)", "Wolf Token (B)", "Wolf token (A)", "Wolf token (B)", "Wolf Token",
"Checklist DFC", "Checklist card", "Double-Sided Card Checklist", "[Checklist Card]",
"Angel token", "Demon token", "Ooze token", "Spider token", "Spirit token", "Vampire token", "Homunculus token",
"Angel Token", "Demon Token", "Ooze Token", "Spider Token", "Spirit Token", "Vampire Token", "Homunculus Token",
"Angel token (4/4)", "Demon token (5/5)", "Homunculus token (2/2)", "Ooze token (*/*)", "Spider token (1/2)", "Spirit Token (White 1/1)",
"Angel Token (White 4/4)", "Demon Token (Black 5/5)", "Homunculus Token (Blue 2/2)", "Ooze Token (Green */*)", "Spider Token (Green 1/2)",
"Spirit token (1/1)", "Vampire token (2/2)", "Zombie token (1) (2/2)", "Zombie token (2) (2/2)", "Zombie token (3) (2/2)",
"Wolf token (1) (1/1)", "Wolf token (2) (2/2)", "Wolf Token (Black)",
"Zombie Token A", "Zombie Token B", "Zombie Token C", "Wolf Token (Green)",
"Swamp", "Swamp (A)", "Swamp (B)", "Swamp (C)", "Swamp 256", "Swamp 257", "Swamp 258",
"Swamp (256)", "Swamp (257)", "Swamp (258)",
"Swamp (#256)", "Swamp (#257)", "Swamp (#258)",
"Swamp (1)", "Swamp (2)", "Swamp (3)",
"Swamp (Version 1)", "Swamp (Version 2)", "Swamp (Version 3)",
"Plains", "Plains (A)", "Plains (B)", "Plains (C)", "Plains 250", "Plains 251", "Plains 252", 
"Plains (250)", "Plains (251)", "Plains (252)",
"Plains (#250)", "Plains (#251)", "Plains (#252)",
"Plains (1)", "Plains (2)", "Plains (3)",
"Plains (Version 1)", "Plains (Version 2)", "Plains (Version 3)",
"Mountain", "Mountain (A)", "Mountain (B)", "Mountain (C)", "Mountain 259", "Mountain 260", "Mountain 261",
"Mountain (259)", "Mountain (260)", "Mountain (261)",
"Mountain (#259)", "Mountain (#260)", "Mountain (#261)",
"Mountain (1)", "Mountain (2)", "Mountain (3)",
"Mountain (Version 1)", "Mountain (Version 2)", "Mountain (Version 3)",
"Island", "Island (A)", "Island (B)", "Island (C)", "Island 253", "Island 254", "Island 255",
"Island (253)", "Island (254)", "Island (255)",
"Island (1)", "Island (2)", "Island (3)",
"Island (Version 1)", "Island (Version 2)", "Island (Version 3)",
"Forest", "Forest (A)", "Forest (B)", "Forest (C)", "Forest 262", "Forest 263", "Forest 264",
"Forest (262)", "Forest (263)", "Forest (264)",
"Forest (#262)", "Forest (#263)", "Forest (#264)",
"Forest (1)", "Forest (2)", "Forest (3)",
"Forest (Version 1)", "Forest (Version 2)", "Forest (Version 3)",
"[Zombie Token] (#9)", "[Zombie Token] (#8)", "[Zombie Token] (#7)",
"Zombie Token nr. 7", "Zombie Token nr. 8", "Zombie Token nr. 9",
"[Wolf Token] (Green)", "[Wolf Token] (Black)",
"Zombie Token (Black 2/2) (Version 1)", "Zombie Token (Black 2/2) (Version 2)", "Zombie Token (Black 2/2) (Version 3)",
"Vampire Token (Black 2/2)", 
"Wolf Token (Green 2/2)", "Wolf Token (Black 1/1)",

"[Spirit Token]", "[Vampire Token]", "[Spider Token]", "[Ooze Token]", "[Demon Token]", "[Angel Token]", "[Homunculus Token]"
]

def add_card(name, type, color):
	#id = r.scard("cards") + 1
	
	if r.sadd("cards", name):
		print("* CARD: %s (%s %s)" % (name, type, color))
		r.hset("card:%s" % id, "type", type)
		r.hset("card:%s" % id, "color", color)
		return True
	else:
		return False

def filter_card(name):
	if name in ignore:
		return False
	else:
		return True
	
def delete_card(name):
	if name is None:
		return False
	if name in r.smembers("cards"):
		r.srem("cards", name)
		r.delete("card:%s" % name)
		return True
	else:
		return False
		
def add_price(name, block, shop, price):
	now = datetime.datetime.now().strftime("%Y%m%d")
	
	if r.sadd("prices", "%s:%s:%s" % (name, block, now)):
		r.hset("price:%s:%s:%s" % (name, block, now), "%s" % shop, price)
		print("+ PRICE: %s ( %s @ %s)" % (name, shop, price))
		return True
	else:
		if r.hset("price:%s:%s:%s" % (name, block, now), "%s" % shop, price):
			print("+ PRICE: %s ( %s @ %s)" % (name, shop, price))	
			return True
		return False