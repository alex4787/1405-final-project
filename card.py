import itertools
import functools

@functools.total_ordering
class Card:
  '''
  Creates card objects that can be displayed and compared based on their:
  - Value <number_value> (1 to 13, where 1 = A, 11 = J, 12 = Q, 13 = K)
  - Suit <suit_value> (0 = Diamond, 1 = Club, 2 = Heart, 3 = Spade)
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

  def to_hashable(self):
    '''Returns a hashable (string) representation of the card'''
    return "C#" + str(self.value) + "#" + str(self.suit['value'])

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
    if not isinstance(other, Card): raise TypeError("Cannot compare card with non-card object.")
    return self.value < other.value or (self.value == other.value and self.suit['value'] < other.suit['value'])

class BlankCard(Card):
  '''Special card object used specifically to display the reverse side of cards.'''

  BLUE = '\033[37;44m'

  def __init__(self):
    self.display_value = BlankCard.BLUE + "[]" + '\033[m'

  def __str__(self):
    return self.display_value

@functools.total_ordering
class Hand(list):
  '''
  Mutable sequence of Cards.
  If no argument is given, the constructor creates a new empty hand. The argument must consist of cards and be iterable if specified.
  '''

  def get_valid_moves(self, previous_move = "*", lowest_card = None, option = 'default'):
    '''
    Return all valid moves of a hand as an array of moves.

    If no arguments is given, the function returns all valid moves with no previous move (i.e. pass or start of game).\n
    If previous move is specified, it must be a move, and only returns valid moves according to the previous move.\n
    If lowest card is specified, it must be a card, and only returns valid moves containing the lowest card.\n
    The option argument has three possible values:
    'default' -- return all valid moves
    'highest' -- return only the highest move for each number of cards (1, 2, 3, 4, 5)
    'lowest' -- return only the lowest move for each number of cards
    Return None if there are no valid moves in the hand.
    '''

    self.sort()

    has_previous_move = isinstance(previous_move, Move)
    first_move = (lowest_card != None)

    if first_move: option = 'default'

    if has_previous_move and self.size() < previous_move.size():
      return []
    elif has_previous_move and self.size() == previous_move.size():
      return self.__get_same_sized_move(previous_move)

    all_valid_moves = []
    self_value_frequencies = self.__value_frequencies()
    
    get_moves = {
      self.__get_one_cards: {'range': 1, 'args': [all_valid_moves, option]},
      self.__get_two_to_four_cards: {'range': [2, 4], 'args': [all_valid_moves, option, self_value_frequencies, has_previous_move, previous_move]},
      self.__get_five_cards: {'range': 5, 'args': [all_valid_moves, option]}
    }

    for func in get_moves:
      within_range = True
      
      if has_previous_move:
        if isinstance(get_moves[func]['range'], list):
          within_range = get_moves[func]['range'][0] <= previous_move.size() <= get_moves[func]['range'][1]
        else:
          within_range = (previous_move.size() == get_moves[func]['range'])
        
        if not within_range:
          continue

      func(*get_moves[func]['args'])

      if has_previous_move:
        return self.__get_moves_with_previous(all_valid_moves, previous_move)

    return_moves = []

    if first_move:
      for move_counter in range(len(all_valid_moves)):
        if lowest_card in all_valid_moves[move_counter]:
          return_moves.append(all_valid_moves[move_counter])
    else:
      return_moves = all_valid_moves[:]

    return sorted_by_hand_type(return_moves)

  def __get_same_sized_move(self, previous_move):
    '''Return moves if hand is the same size as the previous move'''

    self_move = Move(self)
    is_move = True
    if self_move.hand_type == 'empty' or self_move.hand_type == 'scattered':
      is_move = False

    if is_move and self_move > previous_move:
      return [self_move]
    
    return []

  def __value_frequencies(self):
    '''Return a dictionary that represents the frequency of each card value in the hand'''

    self_value_frequencies = {}

    for card in self:  
      if card.value in self_value_frequencies:
        self_value_frequencies[card.value].append(card)
      else:
        self_value_frequencies[card.value] = [card]

    return self_value_frequencies

  def __get_one_cards(self, moves, option):
    '''Return a list of all single card moves within the hand'''

    if option == 'default':
      for card in self:
        moves.append(Move([card]))
    elif option == 'highest':
      moves.append(Move([self[-1]]))
    elif option == 'lowest':
      moves.append(Move([self[0]]))

  def __get_two_to_four_cards(self, moves, option, value_frequencies, has_previous_move, previous_move):
    '''Return a list of all two, three, and four card moves within the hand'''

    if has_previous_move:
      move_sizes = [previous_move.size()]
    else:
      move_sizes = [2, 3, 4]

    move_type_dict = {}

    for move_size in move_sizes:
      for value in value_frequencies:
        if len(value_frequencies[value]) < move_size: continue

        combinations = itertools.combinations(value_frequencies[value], move_size)

        for move in combinations:
          this_move = Move(move)

          if option == 'default':
            moves.append(this_move)
          elif this_move.size() not in move_type_dict:
            move_type_dict[this_move.size()] = this_move
          elif (option == 'highest' and this_move > move_type_dict[this_move.size()]) or (option == 'lowest' and this_move < move_type_dict[this_move.size()]):
            move_type_dict[this_move.size()] = this_move

    if option != 'default':
      for move_type in move_type_dict:
        moves.append(move_type_dict[move_type])

  def __get_five_cards(self, moves, option):
    '''Return a list of all five-card moves within the hand'''

    combinations = itertools.combinations(self, 5)

    move_type_dict = {}

    for combo in combinations:
      move = Move(combo)
      if move.hand_type != 'scattered':
        if option == 'default':
          moves.append(move)
        elif move.hand_type not in move_type_dict:
          move_type_dict[move.hand_type] = move
        elif (option == 'highest' and move > move_type_dict[move.hand_type]) or (option == 'lowest' and move < move_type_dict[move.hand_type]):
          move_type_dict[move.hand_type] = move

    if option != 'default':
      for move_type in move_type_dict:
        moves.append(move_type_dict[move_type])

  def __get_moves_with_previous(self, moves, previous_move):
    '''Return a sorted of all possible moves in the hand when a previous move is provided'''

    return_moves = []

    for move_counter in range(len(moves)):
      if moves[move_counter] > previous_move:
        # print(str(all_valid_moves[move_counter].__class__) + " " + str(previous_move.__class__))
        # print(str(Move.HAND_TYPES.index(all_valid_moves[move_counter].hand_type)) + " " + str(Move.HAND_TYPES.index(previous_move.hand_type)))
        # print(move_counter)
        return_moves.append(moves[move_counter])

    return merge_sort(return_moves)

  def size(self):
    '''Return the size of the hand.'''
    return len(self)

  def subtract(self, other, in_place = True):
    '''
    Return the hand after the other cards/moves/hands have been removed
    - in_place: (True: subtracts from hand in place), (False: returns a copy of the string with cards removed)
    '''

    other_cards = {}

    return_hand = self

    if not in_place:
      return_hand = Hand()

      for card in self:
        return_hand.append(card)

    if isinstance(other, Card):
      return_hand.remove(other)
      return return_hand
    elif not isinstance(other, list):
      raise TypeError("Cannot subtract non-list/hand object from hand")

    for element in other:
      if isinstance(element, list):
        return_hand.subtract(element)
      elif not isinstance(element, Card):
        raise TypeError("Cannot remove non-card objects")
      elif element.to_hashable() not in other_cards:
        other_cards[element.to_hashable()] = True

    for other_card in other_cards:
      return_hand.remove(hashable_to_card(other_card))

    if not in_place:
      return return_hand

  def to_blank_hand(self):
    '''Return the hand, but with all cards showing their reverse'''

    return_hand = Hand()

    return_hand.extend(self.size() * [BlankCard()])

    return return_hand

  def __str__(self):
    display_hand = ""
    
    for card in self:
      display_hand += (card.__str__() + " ")

    return display_hand.strip()

class InvalidMoveError(Exception):
  '''Exception for when move is invalid when comparing moves'''

  pass

@functools.total_ordering
class Move(Hand):
  '''Hand object that has added functionality of being a playable move by players'''

  HAND_TYPES = ['empty', 'scattered', 'one_card', 'pair', 'three_of_a_kind', 'four_of_a_kind', 'straight', 'flush', 'full_house', 'four_of_a_kind_plus_one', 'straight_flush']    

  def get_type(self):
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
      self.hand_type = Move.HAND_TYPES[0]
    elif self.size() <= 4:
      first_card = self[0]
      all_same = True

      for card in self:
        if card.value != first_card.value:
          all_same = False
          break

      if all_same:
        self.hand_type = Move.HAND_TYPES[self.size() + 1]  # One card/pair/three/four
      else:
        self.hand_type = Move.HAND_TYPES[1]            # Scattered

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
          self.hand_type = Move.HAND_TYPES[10]
        else:
          self.hand_type = Move.HAND_TYPES[6]
      elif is_flush:
        self.hand_type = Move.HAND_TYPES[7]
      elif len(repeat_value_counter) == 2:
        if 1 in repeat_value_counter and 4 in repeat_value_counter:
          self.hand_type = Move.HAND_TYPES[9]
        else:
          self.hand_type = Move.HAND_TYPES[8]
      else:
        self.hand_type = Move.HAND_TYPES[1]

    else:
      self.hand_type = Move.HAND_TYPES[1]

  def __init__(self, iterable = ()):
    try:
      super().__init__(iterable)
    except TypeError:
      super().__init__(*iterable)

    self.get_type()
    self.hand_type_index = Move.HAND_TYPES.index(self.hand_type)

  def __str__(self):
    display_hand = ""
    
    for card in self:
      display_hand += (card.__str__() + " ")

    return display_hand

  def __eq__(self, other):
    if not isinstance(other, Move): return False

    if self.hand_type == 'empty' or self.hand_type == 'scattered' or other.hand_type == 'empty' or other.hand_type == 'scattered':
      raise InvalidMoveError("Cannot compare empty/scattered moves.")

    if self.size() != other.size(): return False

    for card_counter in range(self.size()):
      if self[card_counter] != other[card_counter]:
        return False

    return True
  
  def __gt__(self, other):
    return not self.__lt__(other) and not self.__eq__(other)

  def __lt__(self, other):
    if not isinstance(other, Move): raise TypeError("Cannot compare card with non-move object.")

    if self.hand_type == 'empty' or self.hand_type == 'scattered' or other.hand_type == 'empty' or other.hand_type == 'scattered':
      raise InvalidMoveError("Cannot compare empty/scattered moves.")

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
          return max_self.suit['value'] < max_other.suit['value']
        else:
          max_self = next_max_self
          max_other = next_max_other

      if max_self.value != max_other.value: 
        return max_self < max_other

      return max_self.suit['value'] < max_other.suit['value']
    
    else:
      for card_counter in range(self.size() - 1, -1, -1):
        if self[card_counter] != other[card_counter]:
          return self[card_counter] < other[card_counter]

      return self[0].suit['value'] < other[0].suit['value']

def sorted_by_hand_type(in_list, reverse=True, reverse_in_hand_type=False):
  '''Return list of moves, that is customizable to be sorted within the hand type'''

  all_moves = {}

  for move in in_list:
    if move.hand_type_index in all_moves:
      all_moves[move.hand_type_index].append(move)
    else:
      all_moves[move.hand_type_index] = [move]

  for move_type in all_moves:
    all_moves[move_type] = merge_sort(all_moves[move_type], reverse_in_hand_type)

  hand_types = list(all_moves.keys())
  hand_types = merge_sort(hand_types, reverse)

  return_list = []

  for hand_type in hand_types:
    return_list.extend(all_moves[hand_type])

  return return_list

def merge(lst1, lst2, reverse = False):
  i = 0
  j = 0
  merged = []
  
  while len(merged) < len(lst1) + len(lst2):
    if i == len(lst1):
      merged.extend(lst2[j:])
      break
    elif j == len(lst2):
      merged.extend(lst1[i:])
      break
    elif reverse:
      if lst1[i] > lst2[j]:
        merged.append(lst1[i])
        i += 1
      else:
        merged.append(lst2[j])
        j += 1
    else:
      if lst1[i] < lst2[j]:
        merged.append(lst1[i])
        i += 1
      else:
        merged.append(lst2[j])
        j += 1
      
  return merged
      

def merge_sort(lst, reverse = False):
  if len(lst) <= 1:
    return lst
  
  left = merge_sort(lst[:len(lst)//2], reverse)
  right = merge_sort(lst[len(lst)//2:], reverse)
  
  return merge(left, right, reverse)

def hashable_to_card(hashable):
  '''Converts hashable representation of card [see Card.to_hashable()] to its corresponding Card object'''

  params = hashable.split("#")
  return Card(int(params[1]), int(params[2]))
