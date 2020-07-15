# Sushi Go Player class

from Cards import calculateScore, CARDS

# Individual player state
class Player:
  def __init__(self, num):
    self.num = num
    # Map card type to count
    self.selection = {}

  # Add card to selection
  def selectCard(self, card):
    self.selection[card] = self.selection[card] + 1
    if card == CARDS.SALMON_N or card == CARDS.SQUID_N or card == CARDS.EGG_N:
      if self.selection[CARDS.WASABI] > self.selection[CARDS.WASABI_BONUS]:
        self.selection[CARDS(card.value + 7)] = self.selection[CARDS(card.value + 7)] + 1
        self.selection[CARDS.WASABI_BONUS] = self.selection[CARDS.WASABI_BONUS] + 1
      
      

  # Calculate current score given current selection
  def calculateScore(self):
    return calculateScore(self.selection)

