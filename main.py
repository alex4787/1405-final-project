import base_game as b

b.TEST = False            # Prints extra information to console if true
continue_playing = True   # Boolean that controls whether a new game restarts after game completes

while continue_playing:
  b.setup()

  for round_number in range(1, b.total_rounds + 1):
    b.do_round(round_number)
    if round_number != b.total_rounds:
      b.next_round(round_number)

  continue_playing = b.finish_game()


