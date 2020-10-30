import base_game

base_game.setup()

for round_number in range(1, base_game.total_rounds + 1):
  base_game.do_round(round_number)
  if round_number != base_game.total_rounds:
    base_game.next_round(round_number)