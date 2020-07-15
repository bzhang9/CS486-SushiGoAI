from State import State


###from <AI> import <AI>

# ### means to be implemented for AI player

# Have player choose a card
def chooseCard(s, h, sc):
  print("Your current score is {0}".format(sc))
  print("Your current hand:")
  for key in s:
    print("{0}: {1}".format(key, s[key]))
    
  print("\nChoose from the cards below:")
  for i in range(len(h)):
    print("{0}: {1}".format(i, h[i]))
  
  cardi = int(input("\nCard number:"))
  cardt = None
  if cardi >= len(h) or cardi < 0:
    cardi = None
  else:
    cardt = h[cardi]

  print()

  return cardi, cardt

def printSelected(s):
  for i in range(len(s)):
    print("Player {0} chose {1}".format(i, s[i][1]))

# Play a turn of the game 
# given state and the ai
# if aiIndex is passed in, the ai will select a card for the player at index aiIndex
def play(state, ai, aiIndex = None):
  if aiIndex == None and ai != None:
    ###aiIndex = ai.index
    pass

  # list of pairs
  selected = []
  for i in range(state.numPlayers):
    cardi = None
    cardt = None

    hand = state.getHand(i)
    selection = state.getPlayerSelection(i)
    score = state.getPlayerScore(i)
    if i != aiIndex:
      while cardi == None or cardt == None:
        cardi, cardt = chooseCard(selection, hand, score)
        if cardi == None or cardt == None:
          print("ERROR: Invalid selection (ci:{0}, ct{1}".format(cardi, cardt))
    else:
      cardi, cardt = ai.chooseCard(selection, hand, score)
    if cardi != None and cardt != None:
      selected.append([cardi, cardt])
        
    else:
      print("ERROR: No card selected")

  success = state.select(selected)
  if success:
    printSelected(selected)
    if ai != None:
      ###ai.endOfTurn(selected)
      pass
  #else:
    #TODO may not need to do anything

if __name__ == '__main__':
  numPlayers = int(input("Number of Players:"))
  state = State(numPlayers)


#TODO multiple AI Player indices
  aiIndex = int(input("AI Player Index:"))
  ai = None

  if aiIndex >= numPlayers:
    print("ERROR: {0} greater than max value {1}, defaulting to no AI".format(aiIndex, numPlayers))
    aiIndex = None
  elif aiIndex < 0:
    print("No AI player set")
    aiIndex = None
  else:
    ###ai = AI(aiIndex)
    pass
  
  seed = input("Provide seed for shuffling? (enter single character for no, else provide seed >= 10)")
  if len(seed) > 1:
    state.setRandSeed(seed)

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
    if (w != aiIndex):
      print("Player {0}".format(w))
    else:
      print("The AI! (Player {0})".format(w))

