import redis
import store

block = "Innistrad"

for card in store.get_cards(block):
	print("%s $%s" % (card, store.get_average_price(card, block, "20111128")))

#for card in store.get_cards():
#	print("%s $%s" % (card, store.get_average_price(card, "Innistrad", "20111126")))
