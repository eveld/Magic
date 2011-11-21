import redis
import datetime

r = redis.Redis("localhost")

ignore = ["Wolf Token (A)", "Wolf Token (B)", "Wolf token (A)", "Wolf token (B)",
		  "Angel token", "Demon token", "Ooze token", "Spider token", "Spirit token", "Vampire token",
		  "Swamp", "Swamp (A)", "Swamp (B)", "Swamp (C)", "Swamp 256", "Swamp 257", "Swamp 258",
		  "Plains", "Plains (A)", "Plains (B)", "Plains (C)", "Plains 250", "Plains 251", "Plains 252",
		  "Mountain", "Mountain (A)", "Mountain (B)", "Mountain (C)", "Mountain 259", "Mountain 260", "Mountain 261",
		  "Island", "Island (A)", "Island (B)", "Island (C)", "Island 253", "Island 254", "Island 255",
		  "Forest", "Forest (A)", "Forest (B)", "Forest (C)", "Forest 262", "Forest 263", "Forest 264"]

def add_card(name, type, color):
	#id = r.scard("cards") + 1
	
	if r.sadd("cards", name):
		print("Adding new card: %s ( %s %s)" % (name, type, color))
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
		print("Adding new price: %s ( %s @ %s)" % (name, shop, price))
		return True
	else:
		if r.hset("price:%s:%s:%s" % (name, block, now), "%s" % shop, price):
			print("Adding new price: %s ( %s @ %s)" % (name, shop, price))	
			return True
		return False
		
#add_card("Snapcaster Mage", "Creature", ["Blue"], ["1"])
#add_card("Skaab Ruinator", "Creature", ["Blue"], ["1"])

#print(r.hget("card:1", "name"))
#print(r.hvals("price:1:1:20111121"))
#print(r.smembers("cards"))
#print(r.hget("price:1:1:20111121", "1"))
#print(r.smembers("prices"))

#print(delete_card("1"))

#add_price("1", "1", "2", 3.15)