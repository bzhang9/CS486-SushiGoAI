from abc import ABC
from Cards import calculateScore, CARDS
import random

class AiBase(ABC):
  def __init__(self, index, random):
    self.index = index
    self.random = random
    self.selection = {}

  def chooseCard(self, selection, hand, score, state):
    cardi = random.randint(0, len(hand) - 1) if self.random else self.bestSelection(selection, hand, state)
    cardt = hand[cardi]
      
    return cardi, cardt

  def endOfTurn(self, selected):
# Add selected cards to internal state
    pass

  def bestSelection(self, selection, hand, state):
    bestScore = 0
    cardi = 0

    # Find the card to give the best point value
    for index, card in enumerate(hand):
      potentialSelection = selection.copy()
      self.buildSelection(potentialSelection, card)
      expectedScore = calculateScore(potentialSelection) - calculateScore(selection)
      expectedScore += self.getCardWeight(card, selection, state)

      #print('Considering {}, with score {}'.format(card, expectedScore))

      if expectedScore > bestScore:
        bestScore = expectedScore
        cardi = index

    # print('AI picks {} which gives weighted score: {}'.format(hand[cardi], bestScore))
    return cardi

  # Add card to selection
  def buildSelection(self, selection, card):
    selection[card] = selection[card] + 1
    if card == CARDS.SALMON_N or card == CARDS.SQUID_N or card == CARDS.EGG_N:
      if selection[CARDS.WASABI] > selection[CARDS.WASABI_BONUS]:
        selection[CARDS(card.value + 7)] = selection[CARDS(card.value + 7)] + 1
        selection[CARDS.WASABI_BONUS] = selection[CARDS.WASABI_BONUS] + 1

  # Heuristic for card weights
  def getCardWeight(self, card, selection, state):
    # construct a list of hands that proceed this hand
    hands = []
    for i in range(min(state.numPlayers, state.turn + 1)):
      d = {
        CARDS.TEMPURA: 0,
        CARDS.SASHIMI: 0,
        CARDS.DUMPLING: 0,
        CARDS.MAKI_1: 0,
        CARDS.MAKI_2: 0,
        CARDS.MAKI_3: 0,
        CARDS.SALMON_N: 0,
        CARDS.SQUID_N: 0,
        CARDS.EGG_N: 0,
        CARDS.WASABI: 0
      }
      for c in state.getHand(self.index - i):
        d[c] = d[c] + 1
      hands.append(d)
    hands.reverse()

    # construct a dict of card counts that are in play this round
    library = {
      CARDS.TEMPURA: 0,
      CARDS.SASHIMI: 0,
      CARDS.DUMPLING: 0,
      CARDS.MAKI_1: 0,
      CARDS.MAKI_2: 0,
      CARDS.MAKI_3: 0,
      CARDS.SALMON_N: 0,
      CARDS.SQUID_N: 0,
      CARDS.EGG_N: 0,
      CARDS.WASABI: 0
    } 
    for hand in hands:
      for k in hand.keys():
        library[k] = library[k] + hand[k]

    if card == CARDS.TEMPURA:
      if selection[CARDS.TEMPURA]%2 == 1:
        return 5
      if library[CARDS.TEMPURA] == 1:
        return 0
      if len(hands) == state.numPlayers:
        if hands[1][CARDS.TEMPURA] >= 2:
          return 5
        if hands[1][CARDS.TEMPURA] == 1:
          return 4
      if library[CARDS.TEMPURA] == 2:
        return 2
      return 2.5

    elif card == CARDS.SASHIMI:
      if selection[CARDS.SASHIMI]%3 == 2:
        return 10
      if selection[CARDS.SASHIMI]%3 == 1:
        if library[CARDS.SASHIMI] == 1:
          return 0
        if library[CARDS.SASHIMI] == 2:
          return 3
        if len(hands) == state.numPlayers:
          if hands[1][CARDS.SASHIMI] >= 2:
            return 6
          if hands[1][CARDS.SASHIMI] == 1:
            return 5
        return 4
      if library[CARDS.SASHIMI] <= 2:
        return 0
      if library[CARDS.SASHIMI] == 3:
        return 2
      if library[CARDS.SASHIMI] == 4:
        return 2.5
      if len(hands) == state.numPlayers:
        if hands[1][CARDS.SASHIMI] >= 2:
          return 4
        if hands[1][CARDS.SASHIMI] == 1:
          return 3.5
      return 3
    
    elif card == CARDS.DUMPLING:
      if selection[CARDS.DUMPLING] > 4:
        return 0
      if selection[CARDS.DUMPLING] == 4:
        return 5
      if selection[CARDS.DUMPLING] == 3:
        if library[CARDS.DUMPLING] > 2:
          return 4.5
        return 4
      if selection[CARDS.DUMPLING] == 2:
        if library[CARDS.DUMPLING] > 2:
          return 3.5
        return 3
      if selection[CARDS.DUMPLING] == 1:
        if library[CARDS.DUMPLING] > 2:
          return 2.5
        return 2
      if library[CARDS.DUMPLING] > 3:
        return 2
      return 1.1
    
    elif card == CARDS.MAKI_1 or card == CARDS.MAKI_2 or card == CARDS.MAKI_3:
      myMaki = 0
      maki = []
      for i in range(state.numPlayers):
        if i == self.index:
          myMaki = state.getPlayerMaki(i)
        else:
          maki.append(state.getPlayerMaki(i))

      value = 2
      if card == CARDS.MAKI_1:
        value = 1
      if card == CARDS.MAKI_3:
        value = 3

      if library[CARDS.MAKI_1] + library[CARDS.MAKI_2] + library[CARDS.MAKI_3] == 1:
        if max(maki) < myMaki+value:
          return 6
        if max(maki) == myMaki+value:
          return 3

      if max(maki) > myMaki+value+5:
        return 0
      if card == CARDS.MAKI_2:
        return 1.5
      if card == CARDS.MAKI_1:
        return 0.5 # 1 maki is dog shit don't @ me
      return 2

    # add 0.1 to each base nigiri score because denying nigiri is good
    elif card == CARDS.SALMON_N:
      if selection[CARDS.WASABI] > 0:
        if library[CARDS.SALMON_N] + library[CARDS.SQUID_N] > state.numPlayers:
          return 4.5
        return 6
      return 2.1
    elif card == CARDS.SQUID_N:
      if selection[CARDS.WASABI] > 0:
        return 9
      return 3.1
    elif card == CARDS.EGG_N:
      if selection[CARDS.WASABI] > 0:
        if len(hands) == state.numPlayers:
          if hands[1][CARDS.SALMON_N] + hands[1][CARDS.SQUID_N] > 1:
            return 0
        elif library[CARDS.SALMON_N] + library[CARDS.SQUID_N] >= state.numPlayers:
          return 1
        return 3
      return 1.1

    elif card == CARDS.WASABI:
      if len(hands) == state.numPlayers:
        if hands[1][CARDS.SALMON_N] + hands[1][CARDS.SQUID_N] > 1:
          return 5
        if hands[1][CARDS.SALMON_N] + hands[1][CARDS.SQUID_N] + hands[1][CARDS.EGG_N] > 1:
          return 3
      if library[CARDS.SALMON_N] + library[CARDS.SQUID_N] >= state.numPlayers:
        return 4
      if library[CARDS.SALMON_N] + library[CARDS.SQUID_N] + library[CARDS.EGG_N] > state.numPlayers:
        return 3
      if library[CARDS.SALMON_N] + library[CARDS.SQUID_N] + library[CARDS.EGG_N] >= state.numPlayers - 1:
        return 1.5
      return 0
    else:
      print('Card {} does not currently have a weight.'.format(card))
      return 0