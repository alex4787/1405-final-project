import card

class Player():
  def __init__(self):
    self.hand = card.Hand()

class AI(Player):
  def __init__(self):
    super().__init__()
    self.is_ai = True

class Person(Player):
  def __init__(self):
    super().__init__()
    self.is_ai = False