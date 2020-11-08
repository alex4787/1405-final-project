from player import Player
import card_tools as ct
import card
import user_interface as ui

class AI(Player):
  def ai_choose_cards(self, number_of_cards = 1):
    best_hands = [None] * number_of_cards
    best_hand_moves = [None] * number_of_cards
    best_cards = [None] * number_of_cards

    for card_index in range(len(self.hand)):
      remaining_hand = self.hand.subtract(self.hand[card_index], False)

      for ranking in range(len(best_cards)):
        if best_hands[ranking] == None or ct.greater_than(remaining_hand.get_valid_moves(), best_hand_moves[ranking]):
          best_hands.insert(ranking, remaining_hand)
          best_hand_moves.insert(ranking, best_hands[ranking].get_valid_moves())
          best_cards.insert(ranking, self.hand[card_index])

          best_hands.pop()
          best_hand_moves.pop()
          best_cards.pop()
          break

      # print("bh: " + str(best_hand) + " bm: " + str(self._valid_moves[best_move]))

    if number_of_cards == 1:
      ui.print_end_input("AI giving " + str(best_cards[0]) , False)
    else:
      ui.print_end_input("AI giving " + str(best_cards[0]) + " and " + str(best_cards[1]), False)

    return best_cards
  
  def _get_move_parameters(self, previous_move = "*", lowest_card = None):
    super()._get_move_parameters(previous_move, lowest_card)
    self._valid_moves_highest = self.hand.get_valid_moves(previous_move, lowest_card, 'highest')
    self._valid_moves_lowest = self.hand.get_valid_moves(previous_move, lowest_card, 'lowest')

  def __get_other_possible_moves(self, past_moves, players, remainder_deck):
    other_possible_moves = ct.cards_remaining(remainder_deck, past_moves).get_valid_moves()
    max_hand_size = None

    for player in players:
      if player == self: continue

      hand_size = player.hand.size()

      if max_hand_size == None or hand_size > max_hand_size:
        max_hand_size = hand_size

    for move in other_possible_moves:
      if move.size() > max_hand_size:
        other_possible_moves.remove(move)

    return other_possible_moves

  def __moves_remaining(self, move):
    return self.hand.subtract(move, False).get_valid_moves()

  def __ai_determine_first_move(self):
    return 1

  def __ai_determine_subsequent_move(self):
    if self._can_pass and len(self._valid_moves) == 0:
      return 1

    best_hand = None
    best_hand_moves = None
    best_move = None

    for move_index in range(len(self._valid_moves)):
      remaining_hand = self.hand.subtract(self._valid_moves[move_index], False)

      # print("rh: " + str(remaining_hand) + " mm: " + str(self._valid_moves[move_index]))

      # print("r: " + str(remaining_hand))
      # print("b: " + str(best_hand))

      if best_hand == None or ct.greater_than(remaining_hand.get_valid_moves(), best_hand_moves):
        best_hand = remaining_hand
        best_hand_moves = best_hand.get_valid_moves()
        best_move = move_index

      # print("bh: " + str(best_hand) + " bm: " + str(self._valid_moves[best_move]) + "\n")

    return best_move + 1

  def ai_move(self, previous_move = "*", lowest_card = None):
    '''
    Return best move determined by AI:
    - If first move of game,
    - If all others have passed,
    - If following another move, play lowest possible move

    Exceptions:
    - If lowest possible move gets rid of a big combo
      - If different moves possible, choose the one that optimizes:
        - Lowest possible
        - Gets rid of least number of other possibilities
    - If highest card, we can block out others

    - We can recursively find the move that can allow us to win in minimum number of moves, considering:
      - What other people have
      - If tie, choose lowest one that gives us that chance
    '''

    self._get_move_parameters(previous_move, lowest_card)

    # ui.print_moves(self)
    # ui.print_title_input("If no previous move")
    # ui.print_moves(self, self.hand.get_valid_moves())

    if previous_move == '*':
      move_choice = self.__ai_determine_first_move()
    else:
      move_choice = self.__ai_determine_subsequent_move()

    # print("mc:" + str(move_choice))

    return self._get_move(move_choice)

  # def ai_move(self, past_moves, players, remainder_deck = [], previous_move = "*", lowest_card = None):

  def do_move(self, previous_move = "*", lowest_card = None):
    return self.ai_move(previous_move, lowest_card)
