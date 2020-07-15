# Sushi Go Player class

from Cards import calculateScore

# Individual player state
class Player:
  def __init__(self, num):
    self.num = num
    # Map card type to count
    self.selection = {}

  # Calculate current score given current selection
  def calculateScore(self):
    return calculateScore(self.selection)

