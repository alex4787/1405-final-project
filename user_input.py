from user_interface import print_ln_input

def valid_input(input_str, checker_func, error_message = "Please enter a valid input."):
  '''Input with data validation according to checker_func that outputs error message if invalid'''

  while True:
    try:
      return checker_func(input_ln(input_str))
      break
    except ValueError:
      print_ln_input(error_message)

def valid_input_with_range(input_str, checker_func, low, high):
  '''Input with data validation according to checker_func and specific number range that outputs error message if invalid'''

  within_range = False
  error_message = ("Please enter a number from " + str(low) + " to " + str(high) + ".")

  while not within_range:
    user_in = valid_input(input_str, checker_func, error_message)

    if low <= user_in <= high:
      return user_in
    else:
      print_ln_input(error_message)

def valid_input_with_values(input_str, *possible_values):
  '''Input with data validation with a selection of valid values that outputs error message if invalid'''

  valid = False
  error_message = "Please enter one of the following: "
  values_str = ""

  for possible_value in possible_values:
    values_str += possible_value
    values_str += ', '

  values_str = values_str[:-2]

  error_message += values_str

  while not valid:
    user_in = input_ln(input_str + " (" + values_str + "): ")

    if user_in.lower() in possible_values:
      return user_in.lower()
    else:
      print_ln_input(error_message)

def input_ln(input_str):
  '''Return player input, but displayed in formatted manner'''
  
  return input("┃ " + input_str)
    