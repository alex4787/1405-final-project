import itertools
import functools

@functools.total_ordering
class Card:
  '''
  Creates card objects that can be displayed and compared based on their:
  - Suit (0 = Diamond, 1 = Club, 2 = Heart, 3 = Spade)
  - Value (1 to 13, where 1 = A, 11 = J, 12 = Q, 13 = K)
  '''

  # Colour constants
  RED = '\033[31;47m'
  BLACK = '\033[30;47m'

  # Suit dictionaries with constant values, symbols, and colours
  DIAMOND = {'value': 0, 'symbol': '\u2666', 'colour': RED}
  CLUB = {'value': 1, 'symbol': '\u2663', 'colour': BLACK}
  HEART = {'value': 2, 'symbol': '\u2665', 'colour': RED}
  SPADE = {'value': 3, 'symbol': '\u2660', 'colour': BLACK}
  SUITS = [DIAMOND, CLUB, HEART, SPADE]

  def set_display_value(self, number_value):
    '''Set the display value of the card.'''
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
    '''Set the value of the card.'''
    if number_value == 1 or number_value == 2:
      self.value = number_value + 13
    else:
      self.value = number_value
  
  def get_next(self):
    '''Return the following card, in order of ranking.'''
    if self.suit['value'] == 3:
      if self.value == 15:
        return None
      else:
        return Card(self.value + 1, 0)
    else:
      return Card(self.value, self.suit['value'] + 1)

  def __init__(self, number_value, suit_value):
    self.suit = Card.SUITS[suit_value]
    self.set_display_value(number_value)
    self.set_value(number_value)
  
  def __str__(self):
    return self.suit['colour'] + str(self.display_value) + self.suit['symbol'] + '\033[m'

  def __eq__(self, other):
    if not isinstance(other, Card): return False
    return self.value == other.value and self.suit['value'] == other.suit['value']
  
  def __lt__(self, other):
    if not isinstance(other, Card): raise "Cannot compare card with non-card object."
    return self.value < other.value or (self.value == other.value and self.suit['value'] < other.suit['value'])

@functools.total_ordering
class Hand(list):
  '''
  Mutable sequence of Cards.
  If no argument is given, the constructor creates a new empty hand. The argument must consist of cards and be iterable if specified.
  '''

  HAND_TYPES = ['empty', 'scattered', 'one_card', 'pair', 'three_of_a_kind', 'four_of_a_kind', 'straight', 'flush', 'full_house', 'four_of_a_kind_plus_one', 'straight_flush']    

  def get_valid_moves(self, previous_move = "*", lowest_card = None):
    '''
    Return all valid moves of a hand as an array of moves.

    If no arguments is given, the function returns all valid moves with no previous move (i.e. pass or start of game).
    If previous move is specified, it must be a move, and only returns valid moves according to the previous move.
    If lowest card is specified, it must be a card, and only returns valid moves containing the lowest card.
    Return None if there are no valid moves in the hand.
    '''

    self.sort()
    # print("LOWEST:", end=" ")
    # print(lowest_card)

    has_previous_move = isinstance(previous_move, Move)
    first_move = (lowest_card != None)

    # print(has_previous_move)
    # print(first_move)

    if has_previous_move and self.size() < previous_move.size():
      return []
    elif has_previous_move and self.size() == previous_move.size():
      self_move = Move(iter(self))
      is_move = True
      if self_move.hand_type == 'empty' or self_move.hand_type == 'scattered':
        is_move = False

      if is_move:
        if self_move > previous_move:
          return [self_move]
        else:
          return []

    all_valid_moves = []
    self_value_frequencies = {}
    self_suit_frequencies = {}
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
    return_moves = []

    if has_previous_move:
      for move_counter in range(number_moves):
        if all_valid_moves[move_counter] > previous_move:
          # print(str(all_valid_moves[move_counter].__class__) + " " + str(previous_move.__class__))
          # print(str(Hand.HAND_TYPES.index(all_valid_moves[move_counter].hand_type)) + " " + str(Hand.HAND_TYPES.index(previous_move.hand_type)))
          # print(move_counter)
          return_moves.append(all_valid_moves[move_counter])
      return sorted(return_moves)
    elif first_move:
      for move_counter in range(number_moves):
        if lowest_card in all_valid_moves[move_counter]:
          return_moves.append(all_valid_moves[move_counter])
    else:
      return_moves = all_valid_moves[:]

    # for move in return_moves:
    #   print(move)
      
    # print(return_moves)
    return sorted_by_hand_type(return_moves)

  def size(self):
    '''Return the size of the hand.'''
    return len(self)

  def __str__(self):
    display_hand = ""
    
    for card in self:
      display_hand += (card.__str__() + " ")

    return display_hand

@functools.total_ordering
class Move(Hand):
  def __str__(self):
    display_hand = ""
    
    for card in self:
      display_hand += (card.__str__() + " ")

    return display_hand

  def get_type(self):
    HAND_TYPES = ['empty', 'scattered', 'one_card', 'pair', 'three_of_a_kind', 'four_of_a_kind', 'straight', 'flush', 'full_house', 'four_of_a_kind_plus_one', 'straight_flush']    

    '''
    Return the type of the move.
    
    Possible hand types:
    'empty' -- move contains no cards
    'scattered' -- cards do not consist of a move
    'one_card' -- move is one card
    'pair' -- move is two cards of the same value
    'three_of_a_kind' -- move is three cards of the same value
    'four_of_a_kind' -- move is four cards of the same value
    'straight' -- move is five cards with values in ascending order, increasing by one
    'flush' -- move is five cards with all the same suit
    'full_house' -- move is five cards, consisting of a three-of-a-kind and a pair
    'four_of_a_kind_plus_one' -- move is five cards, consisting of a four-of-a-kind and an additional card
    'straight_flush' -- move is both a straight and a flush
    '''
    self.sort()

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
      first_card = self[0]
      is_straight = True
      is_flush = True
      repeat_value_counter = []
      repeat_values = 0

      if first_card.value == 11 or first_card.value == 12 or first_card.value == 13:
        is_straight = False

      for card_counter in range(self.size()):
        if is_flush and self[card_counter].suit != first_card.suit:
          is_flush = False

        if is_straight and card_counter > 0 and ((self[card_counter].value != self[card_counter - 1].value + 1) and (self[card_counter].value != self[card_counter - 1].value - 12)):
          is_straight = False

        if card_counter == 0:
          repeat_values = 1
        elif self[card_counter].value == self[card_counter - 1].value:
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
    self.hand_type_index = Hand.HAND_TYPES.index(self.hand_type)

  def __eq__(self, other):
    if not isinstance(other, Move): return False

    if self.hand_type == 'empty' or self.hand_type == 'scattered' or other.hand_type == 'empty' or other.hand_type == 'scattered':
      raise "Cannot compare empty/scattered moves."

    if self.size() != other.size(): return False

    for card_counter in range(self.size()):
      if self[card_counter] != other[card_counter]:
        return False

    return True
  
  def __gt__(self, other):
    return not self.__lt__(other) and not self.__eq__(other)

  def __lt__(self, other):
    if not isinstance(other, Move): raise "Cannot compare card with non-move object."

    if self.hand_type == 'empty' or self.hand_type == 'scattered' or other.hand_type == 'empty' or other.hand_type == 'scattered':
      raise "Cannot compare empty/scattered moves."

    if self.hand_type_index != other.hand_type_index:
      return self.hand_type_index < other.hand_type_index

    elif 2 <= self.hand_type_index <= 5:
      return self[0] < other[0]

    elif self.hand_type_index == 8 or self.hand_type_index == 9:
      major_portion = self.hand_type_index - 5
      compare_cards = []
      
      for move in [self, other]:
        counter = None
        for card_counter in range(move.size()):
          if counter == None or move[card_counter].value != move[card_counter - 1].value:
            counter = 1
          else:
            counter += 1
            if counter == major_portion: 
              compare_cards.append(move[card_counter])
              break

      return compare_cards[0] < compare_cards[1]

    elif self.hand_type_index == 6 or self.hand_type_index == 10:
      max_self = self[self.size() - 1]
      max_other = other[other.size() - 1]

      if max_self.value == max_other.value == 2:
        next_max_self = self.pop(self.size() - 2)
        next_max_other = other.pop(self.size() - 2)

        if next_max_self.value == next_max_other.value:
          return max_self.suit['value'] < max_self.suit['value']
        else:
          max_self = next_max_self
          max_other = next_max_other

      if max_self.value != max_other.value: 
        return max_self < max_other

      return max_self.suit['value'] < max_self.suit['value']
    
    else:
      for card_counter in range(self.size() - 1, -1, -1):
        if self[card_counter] != other[card_counter]:
          return self[card_counter] < other[card_counter]

      return self[0].suit['value'] < other[0].suit['value']

deck = Hand()

def sorted_by_hand_type(in_list, reverse=True, reverse_in_hand_type=False):
  all_moves = {}

  for move in in_list:
    if move.hand_type_index in all_moves:
      all_moves[move.hand_type_index].append(move)
    else:
      all_moves[move.hand_type_index] = [move]

  # print(all_moves)

  for move_type in all_moves:
    all_moves[move_type].sort(reverse=reverse_in_hand_type)

  # for move in in_list:
  #     print(move)
  # print(all_moves)

  hand_types = list(all_moves.keys())
  hand_types.sort(reverse=reverse)

  return_list = []

  for hand_type in hand_types:
    return_list.extend(all_moves[hand_type])

  return return_list

def full_deck():
  '''Return the full deck of cards.'''
  global deck

  if deck == []:
    for suit in range(4):
      for value in range(1, 14):
        deck.append(Card(value, suit))

  return deck
