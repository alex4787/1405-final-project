from player import Player
import user_input as user_in
import user_interface as ui

class Person(Player):
  '''Player than is controlled by an actual person'''

  def choose_cards(self, number_of_cards = 1):
    '''Allows player to choose cards from their hand and returns them'''

    counter = 1

    # Prints all possible moves for player to see before determining their choice
    ui.print_moves(self, self.hand, False)

    card_choices = []
    get_choices = True

    while get_choices:
      for card_number in range(1, number_of_cards + 1):
        # Adds player choice (in the form of choice number) to list of card choices
        card_choices.append(user_in.valid_input_with_range(("Card " + str(card_number) + ": "), int, 1, len(self.hand)))

      get_choices = False

      for card_choice in card_choices:
        # Ensures that all selected cards are unique, and not the same
        # Otherwise, it repeats the process until valid cards are chosen
        if card_choices.count(card_choice) != 1: 
          ui.print_ln_input("Cards must be different!")
          get_choices = True
          card_choices.clear()
          break

    # Outputs to user which cards have been chosen to give
    if number_of_cards == 1:
      ui.print_end_input("Giving " + str(self.hand[card_choices[0] - 1]) , False)
    else:
      ui.print_end_input("Giving " + str(self.hand[card_choices[0] - 1]) + " and " + str(self.hand[card_choices[1] - 1]), False)

    # Returns a list of cards according to the choice numbers as indices in the player's hand within the card_choices list
    return list(map(lambda card_choice: self.hand[card_choice - 1], card_choices))

  def choose_move(self, previous_move = "*", lowest_card = None):
    '''Allow player to choose move out of valid moves or pass.'''

    self._get_move_parameters(previous_move, lowest_card)

    ui.print_moves(self)

    move_choice = user_in.valid_input_with_range("Move #: ", int, 1, self._last_choice)
    return self._get_move(move_choice)

  def do_move(self, previous_move = "*", lowest_card = None):
    '''Overrided method from parent class to allow player to manually choose which move to play'''

    return self.choose_move(previous_move, lowest_card)
