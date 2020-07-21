from abc import ABC
from Cards import calculateScore, CARDS

class AiBase(ABC):
  def __init__(self, index):
    self.index = index
    self.selection = {}

  def chooseCard(self, selection, hand, score):
    cardi = self.bestSelection(selection, hand)
    cardt = hand[cardi]
      
    return cardi, cardt

  def endOfTurn(self, selected):
# Add selected cards to internal state
    pass

  def bestSelection(self, selection, hand):
    bestScore = 0
    cardi = 0

    # Find the card to give the best point value
    for index, card in enumerate(hand):
      potentialSelection = selection.copy()
      self.buildSelection(potentialSelection, card)
      expectedScord = calculateScore(potentialSelection)

      if expectedScord > bestScore:
        bestScore = expectedScord
        cardi = index

    print('AI picks {} which gives total score: {}'.format(hand[cardi], bestScore))
    return cardi

  # Add card to selection
  def buildSelection(self, selection, card):
    selection[card] = selection[card] + 1
    if card == CARDS.SALMON_N or card == CARDS.SQUID_N or card == CARDS.EGG_N:
      if selection[CARDS.WASABI] > selection[CARDS.WASABI_BONUS]:
        selection[CARDS(card.value + 7)] = selection[CARDS(card.value + 7)] + 1
        selection[CARDS.WASABI_BONUS] = selection[CARDS.WASABI_BONUS] + 1
