def print_hand_type(str_in):
  '''Return the display value of a card hand.'''

  list_in = str_in.split("_")
  for word_counter in range(len(list_in)):
    if not (list_in[word_counter] == 'of' or list_in[word_counter] == 'a'):
      list_in[word_counter] = list_in[word_counter].capitalize()
  print(" ".join(list_in))
