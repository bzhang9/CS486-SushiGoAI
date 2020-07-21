import sys
from State import State


from AiBase import AiBase

# ### means to be implemented for AI player

# CONSTANTS
SEPARATOR = "------------------------------"

# Silent output
silent = False

# Have player choose a card
def chooseCard(s, h, sc):
  print("Your current score is {0}".format(sc))
  print("Your current hand:")
  for key in s:
    print("{0}: {1}".format(key, s[key]))
    
  print("\nChoose from the cards below:")
  for i in range(len(h)):
    print("{0}: {1}".format(i, h[i].name))
  
  cardi = int(input("\nCard number: "))
  cardt = None
  if cardi >= len(h) or cardi < 0:
    cardi = None
  else:
    cardt = h[cardi]
  
  print()

  return cardi, cardt

def printSelected(s):
  if silent:
    return
  print(SEPARATOR)
  for i in range(len(s)):
    print("Player {0} chose {1}".format(i, s[i][1].name))
  print(SEPARATOR)

# Play a turn of the game 
# given state and the ai
def play(state, ai):
  # list of pairs
  selected = []
  for i in range(state.numPlayers):
    cardi = None
    cardt = None

    hand = state.getHand(i)
    selection = state.getPlayerSelection(i)
    score = state.getPlayerScore(i)

    if not silent:
      print(SEPARATOR)
      print("PLAYER {0} TURN".format(i))
      print(SEPARATOR)

    if ai.get(i) == None:
      while cardi == None or cardt == None:
        cardi, cardt = chooseCard(selection, hand, score)
        if cardi == None or cardt == None:
          print("ERROR: Invalid selection (ci:{0}, ct{1}".format(cardi, cardt))
    else:
      cardi, cardt = ai[i].chooseCard(selection, hand, score, state)
      pass
    if cardi != None and cardt != None:
      selected.append([cardi, cardt])
        
    else:
      print("ERROR: No card selected")

  success = state.select(selected)
  if success:
    printSelected(selected)
    for k in ai:
      ai[k].endOfTurn(selected)
      pass
  #else:
    #TODO may not need to do anything

if __name__ == '__main__':
  numPlayers = None
  ai = {}
  seed = "0"
  

  if len(sys.argv) > 1:
    argi = 1
    numPlayers = int(sys.argv[argi])
    argi = argi + 1
    seed = sys.argv[argi]
    argi = argi + 1
    while argi < (len(sys.argv) - 1):
      aiIndex = int(sys.argv[argi])
      if aiIndex >= numPlayers:
        raise Exception("CRITICAL ERROR: {0} greater than max value {1}".format(aiIndex, numPlayers))
      elif aiIndex < 0:
        raise Exception("CRITICAL ERROR: {0} less than 0".format(aiIndex))
      argi = argi + 1
      aiType = int(sys.argv[argi])
      argi = argi + 1
      if ai.get(aiIndex) != None:
        raise Exception("CRITICAL ERROR: Duplicate AI Index, {0}".format(aiIndex))

      if aiType == 0:
        ai[aiIndex] = AiBase(aiIndex)
      # Add more aiTypes here

      # silent mode
      if argi == (len(sys.argv) - 1) and sys.argv[argi] == "-s":
        silent = True
        
  else:
    numPlayers = int(input("Number of Players: "))
    while True:
      aiIndex = int(input("AI Player Index (Negative value for no more additional): "))

      if aiIndex >= numPlayers:
        print("ERROR: {0} greater than max value {1}".format(aiIndex, numPlayers))
      
      elif aiIndex < 0:
        print(SEPARATOR)
        print("Index {0}: No AI player set".format(aiIndex))
        print(SEPARATOR)
        break
      elif ai.get(aiIndex) == None:
        ai[aiIndex] = AiBase(aiIndex)
      else:
        print("ERROR: Duplicate AI Index")
  
    seed = input("Provide seed for shuffling? (enter single character for no, else provide seed >= 10): ")

  state = State(numPlayers)
  if len(seed) > 1:
    state.setRandSeed(int(seed))

  state.initGame()

  while not state.isGameDone():
    play(state, ai)

  scores = state.finalScore()

  winners = []
  maxScore = -1
  for s in scores:
    if s > maxScore:
      maxScore = s

  for i in range(state.numPlayers):
    if scores[i] == maxScore:
      winners.append(i)

  print()
  print("The winners are:")
  for w in winners:
    if (ai.get(w) == None):
      print("Player {0}".format(w))
    else:
      print("The AI! (Player {0})".format(w))
  print()
  for i in range(len(scores)):
    print("Player " + str(i) + " score: " + str(scores[i]))
