from player import Player
import user_input as user_in
import user_interface as ui

class Person(Player):
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
        card_choices.append(user_in.valid_input_with_range(("Card " + str(card_number) + ": "), int, 1, len(self.hand)))

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

    self.__get_move_parameters(previous_move, lowest_card)

    ui.print_moves(self)
    
    move_choice = user_in.valid_input_with_range("Move #: ", int, 1, self.__last_choice)
    self.__do_move(move_choice)
