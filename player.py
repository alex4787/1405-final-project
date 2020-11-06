import card
import functools

@functools.total_ordering
class Player():
  FINISHING_ROLES = ['President', 'Vice-President', 'Neutral', 'Vice-Bum', 'Bum']

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

  def __get_move_parameters(self, previous_move = "*", lowest_card = None):
    self.__valid_moves = self.hand.get_valid_moves(previous_move, lowest_card)
    self.__can_pass = not ((lowest_card != None) or (previous_move == "*"))
    self.__last_choice = len(self.__valid_moves)
    
    if self.__can_pass: self.__last_choice += 1

  def __do_move(self, move_choice):
    if move_choice == self.__last_choice and self.__can_pass:
      return "*"
    else:
      move = self.__valid_moves[move_choice - 1]
      for card in self.hand:
        if card in move:
          self.hand.remove(card)
      
      if len(self.hand) == 0:
        self.finished = True

      return move

  def test_move(self, previous_move = "*", lowest_card = None):
    self.__get_move_parameters(previous_move, lowest_card)
    self.__do_move(1)

  def __init__(self, name):
    self.hand = card.Hand()
    self.name = name
    self.finished = False
    self.finishing_record = []
    self.role = None

  def __lt__(self, other):
    return self.finishing_record[-1] < other.finishing_record[-1]
