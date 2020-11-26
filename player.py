import card
import functools
import user_interface as ui

@functools.total_ordering
class Player():
  '''Player in the game of President'''

  FINISHING_ROLES = ['President 👑', 'Vice-President', 'Neutral', 'Vice-Bum', 'Bum']

  def reset(self):
    '''Reset player hand and finished status.'''
    self.hand = card.Hand()
    self.finished = False

  def give_cards(self, other, *cards):
    '''Gives specified cards to other player'''

    # Loops through own cards and removes those which are specified in argument
    for card in cards:
      if card not in self.hand:
        raise card + " Card not in hand!"
      else:
        self.hand.remove(card)
    
    other.hand.extend(cards)

  def _get_move_parameters(self, previous_move = "*", lowest_card = None):
    '''Sets parameters to enable move selection'''

    # Sets own valid moves and ability to pass, so it can be accessed afterwards without re-evaluation
    self._valid_moves = self.hand.get_valid_moves(previous_move, lowest_card)
    self._can_pass = not ((lowest_card != None) or (previous_move == "*"))
    
    try:
      self._last_choice = len(self._valid_moves)
    except TypeError:
      self._last_choice = 1
    
    if self._can_pass: self._last_choice += 1

  def print_from_valid_moves(self, index):
    '''Allows protected attribute, _valid_moves, to be printed outside of class'''

    print(self._valid_moves[index])

  def _get_move(self, move_choice):
    '''Performs and returns move specified'''

    if move_choice == self._last_choice and self._can_pass:
      return "*"  # Return pass
    else:
      move = self._valid_moves[move_choice - 1]   # Gets move based on specified index
      
      self.hand.subtract(move)  # Removes move from hand
      
      if len(self.hand) == 0:
        self.finished = True    # Sets attribute finished to true if no more cards remain in hand

      return move

  def test_move(self, previous_move = "*", lowest_card = None, move_choice = 1):
    '''Return the first available move every time'''

    self._get_move_parameters(previous_move, lowest_card)
    return self._get_move(move_choice)

  def do_move(self, previous_move = "*", lowest_card = None):
    '''When Player object created and not a Person or AI, defaults to using test_move() to select move'''

    return self.test_move(previous_move, lowest_card)

  def __init__(self, name):
    self.hand = card.Hand()
    self.name = name
    self.finished = False
    self.finishing_record = []
    self.role = None

  def __lt__(self, other):
    return self.finishing_record[-1] < other.finishing_record[-1]

  def __str__(self):
    return self.name
