from abc import ABC

class AiBase(ABC):
  def __init__(self, index):
    self.index = index

  def chooseCard(self, selection, hand, score):
    cardi = None
    cardt = None
    if (len(hand) > 0):
      cardi = 0
      cardt = hand[cardi]
    return cardi, cardt

  def endOfTurn(self, selected):
# Add selected cards to internal state
    pass
