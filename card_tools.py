from card import Hand, Card, Move

deck = Hand()

def full_deck():
  '''Return the full deck of cards.'''
  global deck

  if deck == []:
    for suit in range(4):
      for value in range(1, 14):
        deck.append(Card(value, suit))

  return deck

def lowest(cards):
  lowest = None

  for card in cards:
    if lowest == None or card < lowest:
      lowest = card

  return lowest

def highest(cards):
  highest = None

  for card in cards:
    if highest == None or card > highest:
      highest = card

  return highest

def cards_remaining(*used_cards):
  cards_left = full_deck()[:]

  for cards in used_cards:
    cards_left.subtract(cards)

  return cards_left

def move_with_minimum_possible_moves_to_victory(hand):
  if hand.size() <= 5 and Move(hand).hand_type != 'scattered':
    return 1, [1]

  valid_moves = hand.get_valid_moves()
  minimum = None
  move_options = None

  for move_index in range(len(valid_moves)):
    min_moves = move_with_minimum_possible_moves_to_victory(hand.subtract(valid_moves[move_index], False))[0]

    if minimum == None or min_moves + 1 < minimum:
      minimum = min_moves + 1
      move_options = [move_index]
    elif min_moves + 1 == minimum:
      move_options.append(move_index)

  return minimum, move_options

def greater_than(moves1, moves2):
  # if not isinstance(other, Hand): raise TypeError("Cannot compare hand with non-hand object.")

  moves1_type_indices = []
  moves2_type_indices = []

  for move in moves1:
    if len(moves1_type_indices) == 0 or moves1_type_indices[-1] != move.hand_type_index:
      moves1_type_indices.append(move.hand_type_index)

  for move in moves2:
    if len(moves2_type_indices) == 0 or moves2_type_indices[-1] != move.hand_type_index:
      moves2_type_indices.append(move.hand_type_index)

  upper_bound = len(moves1_type_indices)

  if len(moves2_type_indices) < upper_bound:
    upper_bound = len(moves2_type_indices)

  for index in range(upper_bound):
    if moves1_type_indices[index] == moves2_type_indices[index]:
      continue
    else:
      return moves1_type_indices[index] > moves2_type_indices[index]

  return len(moves1_type_indices) > len(moves2_type_indices)

def ranking_in_card_list(card, card_list):
  '''
  Return integer starting from 0 (highest) to last index of card_list (lowest) representing ranking within card_list
  If card is not found in card_list
  '''
  sorted_card_list = sorted(card_list, reverse=True)

  try:
    return sorted_card_list.index(card)
  except ValueError:
    for other_card in sorted_card_list:
      if card > other_card:
        return sorted_card_list.index(other_card)
