from card import *
from player import *
import random

def deal_to(*players):
  deck = full_deck()[:]
  cards_left = len(deck)
  leftover = cards_left % len(players)
  keep_dealing = True

  while keep_dealing:
    for player in players:
      if cards_left <= leftover: 
        keep_dealing = False
        break
      player.hand.append(deck.pop(random.randrange(0, len(deck))))
      cards_left -= 1

p1 = Player()
p2 = Player()
p3 = Player()
p4 = Player()
p5 = Player()

deal_to(p1, p2, p3, p4, p5)

print(p1.hand)


# print("p1")
# for card in p1.hand:
#   print(card)

# print("p2")
# for card in p2.hand:
#   print(card)

# print("p3")
# for card in p3.hand:
#   print(card)

# print("p4")
# for card in p4.hand:
#   print(card)

# print("p5")
# for card in p5.hand:
#   print(card)




