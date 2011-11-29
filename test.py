import redis

r = redis.Redis("localhost")

list = r.smembers("prices")
for item in list:
	prices = r.hvals("price:%s" % item)
	for price in prices:
		print(price)