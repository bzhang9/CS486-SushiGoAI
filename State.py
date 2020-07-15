# Sushi Go Game State

from Cards import CARDS, CARDS_COUNT
from Player import Player
import random

class State:
#TURN_COUNT = [-1, -1, ]
  HAND_COUNT = [-1, 2, 10, 9, 8, 7]

  CORRUPT_STRING = "***CORRUPT STATE***"
  
  def __init__(self, numPlayers):
    self.numPlayers = numPlayers
    self.turn = 0

    #Player's hand at current turn is pHands[turn % numPlayers]

    # Players
    self.players = []
    # Hands in play
    self.pHands = []
    for i in range(self.numPlayers):
      self.players.append(Player(i))
      self.pHands.append([])
    
    self.handSize = State.HAND_COUNT[numPlayers]
    # Set to false on init
    self.isCorrupt = True
  
  # Query current score of player
  def getPlayerScore(self, player):
    return self.players[player].calculateScore()

  # Calculate and return final score for each player in an array
  def finalScore(self):
    scores = []
    makiMax = -1
    makiSecond = -1

    for i in range(self.numPlayers):
      scores.append(self.getPlayerScore(i))
      selection = self.getPlayerSelection(i)
      mc = selection[CARDS.MAKI_1] + 2 * selection[CARDS.MAKI_2] + 3 * selection[CARDS.MAKI_3]

      if mc > makiMax:
        makiSecond = makiMax
        makiMax = mc
      elif mc > makiSecond:
        makiSecond = mc

    # TODO: Add pudding score calculation
    # For simplicity of AI, this will be left out for now
    # Also, maki cards behave similarly as pudding cards
    makiMaxSet = []
    makiSecondSet = []

    for i in range(self.numPlayers):
      selection = self.getPlayerSelection(i)
      mc = selection[CARDS.MAKI_1] + 2 * selection[CARDS.MAKI_2] + 3 * selection[CARDS.MAKI_3]
      if mc == makiMax:
        makiMaxSet.append(i)
      elif mc == makiSecond:
        makiSecondSet.append(i)
    
    for i in makiMaxSet:
      scores[i] = scores[i] + int(6 / len(makiMaxSet))
    for i in makiSecondSet:
      scores[i] = scores[i] + int(3 / len(makiSecondSet))

    return scores

  # Deal starting hands to players
  # and initialize game params
  def initGame(self):
    self.isCorrupt = False
    deck = []
    # Construct deck
    for card in CARDS:
      for i in range(CARDS_COUNT[card]):
        deck.append(card)
    
    
    for i in range(self.numPlayers):
      # Initialize players and hands
      self.players[i].selection.clear()
      for card in CARDS:
        self.players[i].selection[card] = 0

      self.pHands[i].clear()
      for j in range(self.handSize):
        deckIndex = random.randint(0, len(deck) - 1)
        self.pHands[i].append(deck[deckIndex])
        del deck[deckIndex]
        

  # Play a turn
  # cards is a list of pairs of card index (index of card in hand) and card type
  # Card type passed in to verify the index is correct
  def select(self, cards):
    if self.isCorrupt:
      print(State.CORRUPT_STRING)
      return False

    if self.numPlayers != len(cards):
      print("STATE ERROR: {0} cards given to select, expected {1}".format(len(cards), self.numPlayers))
      return False

    if self.isGameDone():
      print("GAME OVER")
      return False

    for i in range(self.numPlayers):
      hand = self.getHand(i)
      cardi = cards[i][0]
      cardt = cards[i][1]

      if hand[cardi] != cardt:
        print("STATE ERROR: Card {0} in hand {1} is not {2} (Actual: {3})".format(cardi, i, cardt, hand[cardi]))
        
        if i != 0:
          print(State.CORRUPT_STRING)
          self.isCorrupt = True
        return False
      else:
        #self.players[i].selection[cardt] = self.players[i].selection[cardt] + 1
        self.players[i].selectCard(cardt)
        del hand[cardi]

    self.turn = self.turn + 1
    return True
    
  # Checks if game is complete
  # Undealt games will return true
  def isGameDone(self):
    for hand in self.pHands:
      if len(hand) != 0:
        return False

    return True

  # Get the player's current hand
  def getHand(self, i):
    return self.pHands[(self.turn + i) % self.numPlayers]

  # Get player's currently selected cards
  def getPlayerSelection(self, i):
    return self.players[i].selection

  # Seed RNG
  def setRandSeed(self, seed):
    random.seed(seed)

