from card import *
from player import *

def valid_input(input_str, checker_func, error_message = "Please enter a valid input."):
  while True:
    try:
      return checker_func(input(input_str))
      break
    except:
      print(error_message)

def valid_input_with_range(input_str, checker_func, low, high):
  within_range = False
  error_message = ("Please enter a number from " + str(low) + " to " + str(high) + ".")

  while not within_range:
    user_in = valid_input(input_str, checker_func, error_message)

    if low <= user_in <= high:
      return user_in
    else:
      print(error_message)
    