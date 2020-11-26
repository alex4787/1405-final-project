from card import Card, Hand
import os
import time

# Global Variables
ui_width = 80
box = ['┏', '┓', '┃', '━', '┗', '┛', '┣', '┫']

def to_ordinal(number):
  '''Converts number to ordinal representation as a string'''

  if 11 <= number <= 13 or number % 10 == 0 or number % 10 > 3:
    return str(number) + "th"
  elif number % 10 == 1:
    return str(number) + "st"
  elif number % 10 == 2:
    return str(number) + "nd"
  elif number % 10 == 3:
    return str(number) + "rd"

def print_hand_type(str_in):
  '''Return the display value of a card hand.'''

  list_in = str_in.split("_")
  for word_counter in range(len(list_in)):
    if not (list_in[word_counter] == 'of' or list_in[word_counter] == 'a'):
      list_in[word_counter] = list_in[word_counter].capitalize()
  print(" ".join(list_in))

def print_moves(player, moves = 'default', is_moves = True):
  '''
  Print a list of moves or cards in a format that allows for player selection\n
  By default, outputs a player's valid moves
  '''

  counter = 1
  choice_max_length = 1
  max_choice = len(moves) + 1

  if moves == 'default':
    moves = player._valid_moves
    max_choice = player._last_choice

  if len(moves) != 0 and is_moves:
    max_move_size = moves[0].size()

  if max_choice >= 100:
    choice_max_length = 3
  elif max_choice >= 10:
    choice_max_length = 2
    
  for move in moves:
    option_number = "[" + str(counter) + "]"
    print_ln_input(option_number.ljust(choice_max_length + 2), end=" ")

    if is_moves:
      move_max_size = (14 * move.size()) + move.size() + (4 * (max_move_size - move.size()))

      print(str(move).ljust(move_max_size), end="")
      print_hand_type(move.hand_type)
    else:
      print(move)

    counter += 1

  if player._can_pass and is_moves: 
    final_number = "[" + str(player._last_choice) + "]"

    print_ln_input(final_number.ljust(choice_max_length + 2) + " Pass")

def print_title(text, length = ui_width):
  '''Outputs a formatted title for a box'''

  os.system("clear")
  print_str = box[0]
  print_str += " "
  print_str += text.upper()
  print_str += " "
  print_str += (length - len(print_str) - 1) * box[3]
  print_str += box[1]

  print(print_str)

def print_end(length = ui_width):
  '''Outputs the bottom of a box'''

  print_str = box[4]
  print_str += (length - 2) * box[3]
  print_str += box[5]

  print(print_str)

# UNUSED
# def print_subtitle(text, length = ui_width):
#   '''Outputs a formatted subtitle for the middle of a box'''

#   print_str = box[6]
#   print_str += " "
#   print_str += text.upper()
#   print_str += " "
#   print_str += (length - len(print_str) - 1) * box[3]
#   print_str += box[7]

#   print(print_str)

def print_title_input(text, length = ui_width):
  '''Outputs a formatted title for input purposes'''

  print_str = box[0]
  print_str += " "
  print_str += text.upper()
  
  print(print_str)

def print_end_input(text, wait_for_enter = True):
  '''Outputs an ending message and prompt after input has been received'''

  print(box[4], text, end="")

  if wait_for_enter:
    input(". Press enter to continue...")
  else:
    for counter in range(3):
      print(".", end="", flush=True)
      time.sleep(0.3)
    print()
    time.sleep(0.5)

def print_ln_input(text, end='\n'):
  '''Outputs text formatted for inputting purposes'''

  print("┃ " + text, end=end)

def print_box(title, *text, length = ui_width):
  '''Outputs a fully formatted box with a title and text inside'''

  print_title(title, length)
  
  for item in text:
    split_text = item.__str__().split(" ")
    print_str = ""

    for word in split_text:
      test_str = print_str + (word + " ")
      
      if len(test_str) > length - 3:
        print_ln(print_str, length=length)
        print_str = word + " "
      else:
        print_str = test_str

    print_ln(print_str.strip(), length=length)

  print_end(length)

def print_ln(*objects, sep=' ', end='\n', length = ui_width):
  '''Outputs one line of text within a box'''

  if len(objects) == 0: print(end=end)

  print_str = box[2]
  print_str += " "
  num_cards = 0
  crown = 0
  
  for obj_index in range(len(objects)):
    print_str += str(objects[obj_index])
    if isinstance(objects[obj_index], Card):
      num_cards += 1
    elif isinstance(objects[obj_index], Hand):
      num_cards += objects[obj_index].size()

    if '👑' in print_str:
      crown = 1

    if obj_index < len(objects) - 1:
      print_str += sep

  print(print_str.ljust(length - 1 + (num_cards * 11) - crown) + box[2], end=end)
