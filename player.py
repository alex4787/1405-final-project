import card
from user_input import *
from user_interface import *
import functools

@functools.total_ordering
class Player():
  FINISHING_ROLES = ['President', 'Vice-President', 'Neutral', 'Vice-Bum', 'Bum']

  def __init__(self, name):
    self.hand = card.Hand()
    self.name = name
    self.finished = False
    self.finishing_record = []
    self.role = None

  def reset(self):
    '''Reset player hand and finished status.'''
    self.hand = card.Hand()
    self.finished = False

  def give_cards(self, other, *cards):
    for card in cards:
      if card not in self.hand:
        raise card + " Card not in hand!"
      else:
        self.hand.remove(card)
    
    other.hand.extend(cards)

  def __lt__(self, other):
    return self.finishing_record[-1] < other.finishing_record[-1]

class AI(Player):
  def __init__(self, name):
    super().__init__(name)
    self.is_ai = True

class Person(Player):
  def __init__(self, name):
    super().__init__(name)
    self.is_ai = False

  def choose_cards(self, number_of_cards = 1):
    counter = 1

    for card in self.hand:
      print("[" + str(counter) + "]", end=" ")
      print(card)
      counter += 1

    card_choices = []
    get_choices = True

    while get_choices:
      for card_number in range(1, number_of_cards + 1):
        card_choices.append(valid_input_with_range(("Card " + str(card_number) + ": "), int, 1, len(self.hand)))

      get_choices = False

      for card_choice in card_choices:
        if card_choices.count(card_choice) != 1: 
          print("Cards must be different!")
          get_choices = True
          card_choices.clear()
          break

    return list(map(lambda card_choice: self.hand[card_choice - 1], card_choices))

  def choose_move(self, previous_move = "*", lowest_card = None):
    '''Allow player to choose move out of valid moves or pass.'''

    valid_moves = self.hand.get_valid_moves(previous_move, lowest_card)
    
    can_pass = not ((lowest_card != None) or (previous_move == "*"))

    last_choice = len(valid_moves)

    if can_pass:
      last_choice += 1

    counter = 1
    
    for move in valid_moves:
      print("[" + str(counter) + "]", end=" ")
      print(move, end=" ")
      print_hand_type(move.hand_type)
      counter += 1

    if can_pass: print("[" + str(last_choice) + "] Pass")
    
    move_choice = valid_input_with_range("Move #: ", int, 1, last_choice)

    if move_choice == last_choice and can_pass:
      return "*"
    else:
      move = valid_moves[move_choice - 1]
      for card in self.hand:
        if card in move:
          self.hand.remove(card)
      
      if len(self.hand) == 0:
        self.finished = True

      return move

  def test_move(self, previous_move = "*", lowest_card = None):
    valid_moves = self.hand.get_valid_moves(previous_move, lowest_card)
    
    can_pass = not ((lowest_card != None) or (previous_move == "*"))

    last_choice = len(valid_moves)

    if can_pass:
      last_choice += 1

    counter = 1

    if 1 == last_choice and can_pass:
      return "*"
    else:
      move = valid_moves[0]
      for card in self.hand:
        if card in move:
          self.hand.remove(card)
      
      if len(self.hand) == 0:
        self.finished = True

      return move

    
