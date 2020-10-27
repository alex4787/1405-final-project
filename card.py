class Card:
  '''
  Creates card objects that can be displayed and compared based on their:
  - Suit (0 = Diamond, 1 = Club, 2 = Heart, 3 = Spade)
  - Value (1 to 13, where 1 = A, 11 = J, 12 = Q, 13 = K)
  '''

  RED = '\033[31;47m'
  BLACK = '\033[30;47m'

  DIAMOND = {'value': 0, 'symbol': '\u2666', 'colour': RED}
  CLUB = {'value': 1, 'symbol': '\u2663', 'colour': BLACK}
  HEART = {'value': 2, 'symbol': '\u2665', 'colour': RED}
  SPADE = {'value': 3, 'symbol': '\u2660', 'colour': BLACK}
  SUITS = [DIAMOND, CLUB, HEART, SPADE]

  def set_display_value(self, number_value):
    if number_value == 1:
      self.display_value = 'A'
    elif number_value == 11:
      self.display_value = 'J'
    elif number_value == 12:
      self.display_value = 'Q'
    elif number_value == 13:
      self.display_value = 'K'
    else:
      self.display_value = number_value

  def set_value(self, number_value):
    if number_value == 1 or number_value == 2:
      self.value = number_value + 13
    else:
      self.value = number_value
  
  def __init__(self, number_value, suit_value):
    self.suit = Card.SUITS[suit_value]
    self.set_display_value(number_value)
    self.set_value(number_value)
  
  def __str__(self):
    return self.suit['colour'] + str(self.display_value) + self.suit['symbol'] + '\033[m'

  def __eq__(self, other):
    if not isinstance(other, Card): raise "Cannot compare card with non-card object."
    return self.value == other.value and self.suit['value'] == other.suit['value']
  
  def __lt__(self, other):
    if not isinstance(other, Card): raise "Cannot compare card with non-card object."
    return self.value < other.value or (self.value == other.value and self.suit['value'] < other.suit['value'])

class Hand(list):
  def __str__(self):
    display_hand = ""
    
    for card in self:
      display_hand += (card.__str__() + " ")

    return display_hand

deck = Hand()

def full_deck():
  global deck

  if deck == []:
    for suit in range(4):
      for value in range(1, 14):
        deck.append(Card(value, suit))

  return deck


# Test
# import random

# test_deck = []

# for i in range(30):
#   test_deck.append(Card(random.randint(1, 13), random.randint(0, 3)))

# test_deck.sort()

# for card in test_deck:
#   print(card)
