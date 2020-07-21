from abc import ABC
from Cards import calculateScore, CARDS

class AiBase(ABC):
  def __init__(self, index):
    self.index = index
    self.selection = {}
    self.library = {}  # tracks how many of each card is in play this round

  def chooseCard(self, selection, hand, score, state):
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
      expectedScord += self.getCardWeight(card, selection)

      if expectedScord > bestScore:
        bestScore = expectedScord
        cardi = index

    print('AI picks {} which gives weighted score: {}'.format(hand[cardi], bestScore))
    return cardi

  # Add card to selection
  def buildSelection(self, selection, card):
    selection[card] = selection[card] + 1
    if card == CARDS.SALMON_N or card == CARDS.SQUID_N or card == CARDS.EGG_N:
      if selection[CARDS.WASABI] > selection[CARDS.WASABI_BONUS]:
        selection[CARDS(card.value + 7)] = selection[CARDS(card.value + 7)] + 1
        selection[CARDS.WASABI_BONUS] = selection[CARDS.WASABI_BONUS] + 1

  # Heuristic for card weights
  def getCardWeight(self, card, selection):
    if card == CARDS.TEMPURA:
      return 2
    elif card == CARDS.SASHIMI:
      return 3
    elif card == CARDS.DUMPLING:
      return 2.5
    elif card == CARDS.MAKI_1:
      return 1
    elif card == CARDS.MAKI_2:
      return 2
    elif card == CARDS.MAKI_3:
      return 3
    elif card == CARDS.SALMON_N:
      return 2
    elif card == CARDS.SQUID_N:
      return 3
    elif card == CARDS.EGG_N:
      return 1
    elif card == CARDS.WASABI:
      return 2
    else:
      print('Card {} does not currently have a weight.'.format(card))
      return 0