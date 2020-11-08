from card import Card, Hand, Move, BlankCard
import user_input as user_in
import user_interface as ui
import random
import math
from player import Player
from person import Person
from ai import AI
import card_tools as ct

# GLOBAL VARIABLES
TEST = True

total_rounds = None
num_players = None
players = []

def setup():
  '''Setup the game by allowing user to specify the number of rounds, players, and their names and AI status'''

  global total_rounds, num_players, players

  players.clear()

  intro_text = ("This is a card game with 3-8 players, where players "
  "can play moves, like single cards and poker combos, according to the "
  "previous move. Please specify the "
  "number of players and the number of rounds below. Note that each player "
  "can either be an AI, or an actual person, which can be specified as well. "
  "Hope you enjoy!")

  ui.print_box("Welcome to President!", intro_text)
  ui.print_title_input("Choose Game Options:")

  total_rounds = user_in.valid_input("Num Rounds: ", int, "Please enter a number.")
  num_players = user_in.valid_input_with_range("Num Players: ", int, 3, 8)

  for player_counter in range(num_players):
    player_name = user_in.input_ln("Player " + str(player_counter + 1) + " name: ")
    is_ai = user_in.valid_input_with_values("AI?", 'y', 'n')
    
    if is_ai == 'y':
      players.append(AI(player_name))
    else:
      players.append(Person(player_name))

  ui.print_end_input("Setting up the game", False)

def deal_to(*players):
  '''Deals an equal number of cards to each player from a full deck of cards'''

  deck = ct.full_deck()[:]
  cards_left = len(deck)
  leftover = cards_left % len(players)
  keep_dealing = True

  while keep_dealing:
    for player in players:
      if cards_left <= leftover: 
        keep_dealing = False
        break
      player.hand.append(deck.pop(random.randrange(0, len(deck))))
      cards_left -= 1

  return deck

def get_lowest_card(remainder_deck, lowest_possible = Card(3, 0)):
  '''Return the lowest card in the deck according to the cards leftover after dealing'''

  if lowest_possible in remainder_deck:
    return get_lowest_card(remainder_deck[:].remove(lowest_possible), lowest_possible.get_next())
  else:
    return lowest_possible

def do_round(round_number):
  '''Conducts one round of President'''

  remainder_deck = deal_to(*players)
  lowest_card = get_lowest_card(remainder_deck)

  starting_player_index = 0

  for player in players:
    player.hand.sort()
    if TEST: ui.print_ln(player.name + ":", player.hand)
    if (round_number == 1) and (lowest_card in player.hand): 
      starting_player_index = players.index(player)
      # ui.print_ln("sp_index [first]:" + str(starting_player_index))

  if round_number > 1:
    starting_player_index = 0
    # ui.print_ln("sp_index [subsequent]:" + str(starting_player_index))
    do_trade()

  ui.print_box("Round " + str(round_number), "This is the " + ui.to_ordinal(round_number) + " round.", "Players will see their cards in the following order: ", *players[starting_player_index:], *players[0:starting_player_index])
  input("> Press enter to proceed to the first player (" + players[starting_player_index].name + ")...")

  if TEST:
    ui.print_ln(*remainder_deck)
    ui.print_ln("Lowest Card:", lowest_card)

  round_ended = False
  is_first_turn = True
  prev_move = "*"
  num_passes = 0
  players_finished = 0
  
  moves = []

  while not round_ended:
    for index in range(len(players)):
      # ui.print_ln("index: " + str(index) + " -- sp_index: " + str(starting_player_index))
      if players[index].finished or (is_first_turn and index != starting_player_index):
        continue        

      ui.print_title("Round " + str(round_number) + " - " + players[index].name + "\'s turn")
      players[index].hand.sort()

      if isinstance(players[index], Person):
        other_indices = list(range(index+1, len(players))) + list(range(index))

        for other_index in other_indices:
          if players[other_index] != players[index]:
            if players[other_index].hand.size() != 0:
              ui.print_ln(players[other_index].name + "\'s hand:", *(players[other_index].hand.size() * [BlankCard()]))
            else:
              ui.print_ln(players[other_index].name + " has finished.")
            # ui.print_ln(players[other_index].name + "\'s hand:", player.hand)

        ui.print_ln("Your hand:", players[index].hand)
        if prev_move == "*":
          ui.print_ln("Previous Move: None")
        else:
          ui.print_ln("Previous Move:", prev_move)
        ui.print_end()
        ui.print_title_input("Options:")
      else:
        ui.print_ln("AI move complete.")
        ui.print_end()
        ui.print_title_input("Move:")

      move = None

      if not is_first_turn:
        move = players[index].do_move(prev_move)
        if move == "*":
          num_passes += 1
          if num_passes == num_players - 1:
            prev_move = "*"
        else:
          num_passes = 0
          prev_move = move
      elif index == starting_player_index:
        if round_number == 1:
          move = players[index].do_move(prev_move, lowest_card)
        else:
          move = players[index].do_move(prev_move)
        prev_move = move
        is_first_turn = False

      next_player = None

      for counter in range(index + 1, index + 5):
        next_index = counter

        if next_index >= len(players):
          next_index -= len(players)

        if not players[next_index].finished:
          next_player = players[next_index]
          break

      if players[index].finished:
        ui.print_end_input("Finished - No more cards. Proceeding to next player (" + next_player.name + ")")
        players_finished += 1
        ui.print_ln(players_finished)
        players[index].finishing_record.append(players_finished)
        if players_finished == num_players - 1:
          round_ended = True
      else:
        prefix = "Passing. "

        if move != "*":
          prefix = "Playing " + str(move) + "- "

        ui.print_end_input(prefix + "Proceeding to next player (" + next_player.name + ")")

       
      moves.append(move)

  for player in players:
    if len(player.finishing_record) < round_number:
      player.finishing_record.append(num_players)
  
  get_finishing_roles()

  if round_number == total_rounds:
    ui.print_title("Final roles for the game:")
  else:
    ui.print_title("Roles for next round:")

  for player in players:
    ui.print_ln(player.name + " -- " + player.role)
    player.reset()

  ui.print_end()

def next_round(round_number):
  '''Proceeds to next round (this may be expanded if time permits)'''

  input("> Press enter to continue to next round...")

def get_finishing_roles():
  '''Obtains finishing roles after each round according to the order in which each player finished'''

  global players

  players.sort()

  for counter in range(math.ceil(num_players / 2)):
    if counter >= 2 or (counter == (num_players - 1 - counter)):
      players[counter].role = players[(counter * -1) - 1].role = Player.FINISHING_ROLES[2]
      continue

    players[counter].role = Player.FINISHING_ROLES[counter]
    players[(counter * -1) - 1].role = Player.FINISHING_ROLES[(counter * -1) - 1]

  # 1 2 president bum [0]
  # 1 2 3 president netural bum [0, 1]
  # 1 2 3 4 p vp vb b [0,1]
  # 1 2 3 4 5 p vp n vb b [0, 1, 2]
  # 1 2 3 4 5 6 p vp n n vb b [0, 1, 2]
  # 1 2 3 4 5 6 7 p vp n n n vb b [0, 1, 2, 3]

def do_trade():
  '''Conducts trade between players according to number of players and each of their roles'''

  if num_players >= 4:
    ui.print_box("Trade", "Trade will occur between first the president and bum, and then the vice-president and vice-bum.")
  else:
    ui.print_box("Trade", "Trade will now occur between the president and bum.")

  input("> Press enter to continue...")

  for counter in range(math.ceil(num_players / 2)):
    if counter >= 2 or (counter == (num_players - 1 - counter)):
      break
    
    president = players[counter]
    bum = players[(counter * -1) - 1]
    ui.print_box("Trade " + str(counter + 1), "This trade is between " + president.name + " (" + president.role + ") and " + bum.name + " (" + bum.role + ")")
    input("> Press enter for " + president.name + " (" + president.role + ") to select cards to give...")

    trade_between(president, bum)

def trade_between(president, bum):
  '''Facilitates the actual trading mechanism between players/AI'''

  num_cards = 3 - president.finishing_record[-1]

  if isinstance(president, AI):
    ui.print_title_input(president.name + " (AI) picking " + str(num_cards) + " cards to give")
    president_cards = president.ai_choose_cards(num_cards)
  else:
    ui.print_title_input(president.name + ", pick " + str(num_cards) + " of the following to give:")
    president_cards = president.choose_cards(num_cards)

  bum_cards = bum.hand[(-1 * num_cards):]

  president.give_cards(bum, *president_cards)
  bum.give_cards(president, *bum_cards)

def finish_game():
  '''Finishes the game and return true/false based on whether player wants to play again'''

  input("> Press enter to continue...")

  ui.print_box("End of Game", "Thank you for playing President! We hope you enjoyed.")
  ui.print_title_input("Would you like to play again?")
  
  play_again = user_in.valid_input_with_values("Your choice", "y", "n")

  if play_again == 'y':
    ui.print_end_input("You chose to continue playing")
    return True

  ui.print_end_input("Thanks for playing! We hope you play again")
  return False