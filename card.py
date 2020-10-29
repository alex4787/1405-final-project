import itertools
import functools

@functools.total_ordering
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

@functools.total_ordering
class Hand(list):
  '''
  Types: Scattered Hand, Poker Hand
  Each function will return a list of Hands that match the type
  If it returns none, it doesn't contain it
  If it contains an array of hands, then multiple inside exist
  If it is only itself, it will return itself
  '''

  HAND_TYPES = ['empty', 'scattered', 'one_card', 'pair', 'three_of_a_kind', 'four_of_a_kind', 'straight', 'flush', 'full_house', 'four_of_a_kind_plus_one', 'straight_flush']    

  def valid_moves(self, previous_move = "*", lowest_card = None):
    if self.__valid_moves == -1: 
      self.__valid_moves = self.get_valid_moves(previous_move, lowest_card)

    return self.__valid_moves

  def get_valid_moves(self, previous_move = "*", lowest_card = None):
    print("PREV:", end=" ")
    print(previous_move)

    has_previous_move = isinstance(previous_move, Move)
    first_move = (lowest_card != None)

    if has_previous_move and self.size() < previous_move.size():
      return None
    elif has_previous_move and self.size() == previous_move.size():
      self_move = Move(iter(self))
      is_move = True
      if self_move.hand_type == 'empty' or self_move.hand_type == 'scattered':
        is_move = False

      if is_move:
        if self_move > previous_move:
          return self_move
        else:
          return None

    all_valid_moves = []
    self_value_frequencies = {}
    self_suit_frequencies = {}
    sorted_self = sorted(self)

    for card in self:
      if card.suit['value'] in self_suit_frequencies:
        self_suit_frequencies[card.suit['value']].append(card)
      else:
        self_suit_frequencies[card.suit['value']] = [card]
      
      if card.value in self_value_frequencies:
        self_value_frequencies[card.value].append(card)
      else:
        self_value_frequencies[card.value] = [card]
    
    if has_previous_move: previous_move_size = previous_move.size()

    if not has_previous_move or previous_move_size == 1:
      for card in self:
        all_valid_moves.append(Move(iter([card])))
    
    if not has_previous_move or 2 <= previous_move_size <= 4:
      if has_previous_move:
        move_sizes = [previous_move_size]
      else:
        move_sizes = [2, 3, 4]

      for move_size in move_sizes:
        for value in self_value_frequencies:
          if len(self_value_frequencies[value]) >= move_size:
            combinations = itertools.combinations(self_value_frequencies[value], move_size)
            for move in combinations:
              all_valid_moves.append(Move(move))

    if not has_previous_move or previous_move_size == 5:
      combinations = itertools.combinations(self, 5)

      for combo in combinations:
        move = Move(combo)
        if move.hand_type != 'scattered':
          all_valid_moves.append(move)

    number_moves = len(all_valid_moves)

    if has_previous_move:
      for move_counter in range(number_moves):
        if all_valid_moves[move_counter] > previous_move:
          all_valid_moves.append(all_valid_moves[move_counter])
    elif first_move:
      for move_counter in range(number_moves):
        if lowest_card in all_valid_moves[move_counter]:
          all_valid_moves.append(all_valid_moves[move_counter])
    else:
      return all_valid_moves
    
    return all_valid_moves[number_moves:]

  def size(self):
    return len(self)

  def __init__(self, iterable = ()):
    super().__init__(iterable)
    self.__valid_moves = -1

  def __str__(self):
    display_hand = ""
    
    for card in self:
      display_hand += (card.__str__() + " ")

    return display_hand

class Move(Hand):
  def get_type(self):
    if self.size() == 0:
      self.hand_type = Hand.HAND_TYPES[0]
    elif self.size() <= 4:
      first_card = self[0]
      all_same = True

      for card in self:
        if card.value != first_card.value:
          all_same = False
          break

      if all_same:
        self.hand_type = Hand.HAND_TYPES[self.size() + 1]  # One card/pair/three/four
      else:
        self.hand_type = Hand.HAND_TYPES[1]            # Scattered

    elif self.size() == 5:
      sorted_hand = sorted(self)
      first_card = sorted_hand[0]
      is_straight = True
      is_flush = True
      repeat_value_counter = []
      repeat_values = 0

      if first_card.value == 11 or first_card.value == 12 or first_card.value == 13:
        is_straight = False

      for card_counter in range(len(sorted_hand)):
        if is_flush and sorted_hand[card_counter].suit != first_card.suit:
          is_flush = False

        if is_straight and card_counter > 0 and ((sorted_hand[card_counter].value != sorted_hand[card_counter - 1].value + 1) and (sorted_hand[card_counter].value != sorted_hand[card_counter - 1].value - 12)):
          is_straight = False

        if card_counter == 0:
          repeat_values = 1
        elif sorted_hand[card_counter].value == sorted_hand[card_counter - 1].value:
          repeat_values += 1
        else:
          repeat_value_counter.append(repeat_values)
          repeat_values = 1

      repeat_value_counter.append(repeat_values)

      if is_straight:
        if is_flush:
          self.hand_type = Hand.HAND_TYPES[10]
        else:
          self.hand_type = Hand.HAND_TYPES[6]
      elif is_flush:
        self.hand_type = Hand.HAND_TYPES[7]
      elif len(repeat_value_counter) == 2:
        if 1 in repeat_value_counter and 4 in repeat_value_counter:
          self.hand_type = Hand.HAND_TYPES[9]
        else:
          self.hand_type = Hand.HAND_TYPES[8]
      else:
        self.hand_type = Hand.HAND_TYPES[1]

    else:
      self.hand_type = Hand.HAND_TYPES[1]

  def __init__(self, iterable = ()):
    super().__init__(iterable)
    self.get_type()

  def __eq__(self, other):
    if not isinstance(other, Move): raise "Cannot compare card with non-move object."

    if self.hand_type == 'empty' or self.hand_type == 'scattered' or other.hand_type == 'empty' or other.hand_type == 'scattered':
      raise "Cannot compare empty/scattered moves."

    if self.size() != other.size(): return False

    sorted_self = sorted(self)
    sorted_other = sorted(other)

    for card_counter in range(self.size()):
      if sorted_self[card_counter] != sorted_other[card_counter]:
        return False

    return True
  
  def __lt__(self, other):
    if not isinstance(other, Move): raise "Cannot compare card with non-move object."

    if self.hand_type == 'empty' or self.hand_type == 'scattered' or other.hand_type == 'empty' or other.hand_type == 'scattered':
      raise "Cannot compare empty/scattered moves."

    self_hand_type_index = Hand.HAND_TYPES.index(self.hand_type)
    other_hand_type_index = Hand.HAND_TYPES.index(other.hand_type)

    if self.hand_type != other.hand_type:
      return self_hand_type_index < other_hand_type_index
    elif 2 <= self_hand_type_index <= 5:
      return self[0] < other[0]
    else:
      sorted_self = sorted(self)
      sorted_other = sorted(other)

      if self_hand_type_index == 8 or self_hand_type_index == 9:
        major_portion = self_hand_type_index - 5
        compare_cards = []
        
        for move in [sorted_self, sorted_other]:
          counter = None
          for card_counter in range(move.size()):
            if counter == None or move[card_counter] != move[card_counter - 1]:
              counter = 1
            else:
              counter += 1
              if counter == major_portion: compare_cards.append(move[card_counter])

        return compare_cards[0] < compare_cards[1]

      elif self_hand_type_index == 6 or self_hand_type_index == 10:
        max_self = max(sorted_self)
        max_other = max(sorted_other)

        if max_self.value == max_other.value == 2:
          next_max_self = sorted_self.pop(sorted_self.size() - 2)
          next_max_other = sorted_other.pop(sorted_self.size() - 2)

          if next_max_self.value == next_max_other.value:
            return max_self.suit['value'] < max_self.suit['value']
          else:
            max_self = next_max_self
            max_other = next_max_other

        if max_self.value != max_other.value: 
          return max_self < max_other

        return max_self.suit['value'] < max_self.suit['value']
      
      else:
        for card_counter in range(sorted_self.size() - 1, -1, -1):
          if sorted_self[card_counter] != sorted_other[card_counter]:
            return sorted_self[card_counter] < sorted_other[card_counter]

        return sorted_self[0].suit['value'] < sorted_other[0].suit['value']

deck = Hand()

def full_deck():
  global deck

  if deck == []:
    for suit in range(4):
      for value in range(1, 14):
        deck.append(Card(value, suit))

  return deck

# c1 = Card(5, 0)
# c2 = Card(5, 1)
# c3 = Card(5, 2)
# c4 = Card(5, 3)

# hand = Move((c1, c2, c3, c4))
# print(hand.hand_type)

# test_hand = Hand((c1, c2, c3, c4))
# valid_moves = []

# for card in test_hand:
#   valid_moves.append(Move(iter(card)))

# print(valid_moves)

# Test
import random

deck = full_deck()[:]

test_hand = Hand()

for i in range(12):
  test_hand.append(deck.pop(random.randrange(0, len(deck))))

test_hand.sort()
print(test_hand)

prev_cards = []
prev_cards.append(Card(3, 0))
prev_cards.append(Card(5, 1))
prev_cards.append(Card(4, 0))
prev_cards.append(Card(6, 0))
prev_cards.append(Card(7, 0))

# for i in range(3):
#   prev_cards.append(deck.pop(random.randrange(0, len(deck))))

prev_move = Move(iter(prev_cards))
valid_moves = test_hand.valid_moves(prev_move)

for move in valid_moves:
  print(move)
