import redis
import datetime

r = redis.Redis("localhost")

def add_card(name, types, colors, blocks):
	id = r.scard("cards") + 1
	
	print("Adding new card: %s - %s, %s from %s in slot %s" % (name, types, colors, blocks, id))
	
	if r.sadd("cards", id):
		r.hset("card:%s" % id, "name", name)
		r.hset("card:%s" % id, "types", types)
		r.hset("card:%s" % id, "colors", colors)
		r.hset("card:%s" % id, "blocks", blocks)
		return True
	else:
		return False
		
def delete_card(id):
	if id in r.smembers("cards"):
		r.srem("cards", id)
		r.delete("card:%s" % id)
		return True
	else:
		return False
		
def add_price(card, block, shop, price):
	now = datetime.datetime.now().strftime("%Y%m%d")
	if r.sadd("prices", "%s:%s:%s" % (card, block, now)):
		
		print("price:%s:%s:%s" % (card, block, now))
		print("%s" % shop)
		print(price)
		
		r.hset("price:%s:%s:%s" % (card, block, now), "%s" % shop, price)
		return True
	else:
		if r.hset("price:%s:%s:%s" % (card, block, now), "%s" % shop, price):
			print("price:%s:%s:%s" % (card, block, now))
			print("%s" % shop)
			print(price)
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