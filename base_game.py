from card import *
from player import *
import user_input
import random
import math

# GLOBAL VARIABLES
total_rounds = None
num_players = None
players = []

def deal_to(*players):
  deck = full_deck()[:]
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
  if lowest_possible in remainder_deck:
    return get_lowest_card(remainder_deck[:].remove(lowest_possible), lowest_possible.get_next())
  else:
    return lowest_possible

def setup():
  global total_rounds, num_players, players

  print("Welcome to President!")
  
  total_rounds = user_input.valid_input("Num Rounds: ", int, "Please enter a number.")
  num_players = user_input.valid_input_with_range("Num Players: ", int, 3, 8)

  for player_counter in range(num_players):
    player_name = input("Player " + str(player_counter + 1) + " name: ")
    players.append(Person(player_name))

def do_round(round_number):
  remainder_deck = deal_to(*players)
  lowest_card = get_lowest_card(remainder_deck)

  print("Round " + str(round_number))

  for card in remainder_deck:
    print(card, end=" ")

  print("Lowest Card: ", end="")
  print(lowest_card)

  for player in players:
    print(player.name, end=": ")
    player.hand.sort()
    print(player.hand)
    if (round_number == 1) and (lowest_card in player.hand): 
      starting_player_index = players.index(player)
      # print("sp_index [first]:" + str(starting_player_index))
  
  if round_number > 1:
    starting_player_index = 0
    # print("sp_index [subsequent]:" + str(starting_player_index))
    do_trade()

  round_ended = False
  is_first_turn = True
  move_counter = 0
  prev_move = "*"
  num_passes = 0
  players_finished = 0
  
  moves = []

  while not round_ended:
    for index in range(len(players)):
      # print("index: " + str(index) + " -- sp_index: " + str(starting_player_index))
      if players[index].finished or (is_first_turn and index != starting_player_index):
        continue        

      print(players[index].name)
      players[index].hand.sort()
      print(players[index].hand)
      print("PREV:", end=" ")
      print(prev_move)

      if not is_first_turn:
        move = players[index].test_move(prev_move)
        if move == "*":
          num_passes += 1
          if num_passes == num_players - 1:
            prev_move = "*"
        else:
          num_passes = 0
          prev_move = move
      elif index == starting_player_index:
        if round_number == 1:
          move = players[index].test_move(prev_move, lowest_card)
        else:
          move = players[index].test_move(prev_move)
        prev_move = move
        is_first_turn = False

      if players[index].finished:
        print("Finished - No more cards")
        players_finished += 1
        print(players_finished)
        players[index].finishing_record.append(players_finished)
        if players_finished == num_players - 1:
          round_ended = True
       
      moves.append(move)
      move_counter += 1

  for player in players:
    if len(player.finishing_record) < round_number:
      player.finishing_record.append(num_players)
  
  get_finishing_roles()

  print("Roles for next round:")

  for player in players:
    print(player.name + " -- " + player.role)
    player.reset()

def next_round(round_number):
  input("Press any button to continue to next round") # TEST

def get_finishing_roles():
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
  print("TRADE")
  for counter in range(math.ceil(num_players / 2)):
    if counter >= 2 or (counter == (num_players - 1 - counter)):
      break
    
    president = players[counter]
    bum = players[(counter * -1) - 1]
    print("BETWEEN " + president.name + " (" + president.role + ") and " + bum.name + " (" + bum.role + ")")
    
    trade_between(president, bum)

def trade_between(president, bum):
  num_cards = 3 - president.finishing_record[-1]

  if president.is_ai:
    pass
  else:
    print(president.name)
    print("Pick " + str(num_cards) + " of the following to give:")
    president_cards = president.choose_cards(num_cards)

  bum_cards = bum.hand[(-1 * num_cards):]

  president.give_cards(bum, *president_cards)
  bum.give_cards(president, *bum_cards)
