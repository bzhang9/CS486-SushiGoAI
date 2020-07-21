from enum import Enum

class CARDS(Enum):
  TEMPURA = 0
  SASHIMI = 1
  DUMPLING = 2
  MAKI_1 = 3
  MAKI_2 = 4
  MAKI_3 = 5
  SALMON_N = 6
  SQUID_N = 7
  EGG_N = 8
# TODO we are currently not considering pudding cards
  PUDDING = 9
  WASABI = 10
  CHOPSTICKS = 11
  # Used for score calculation
  WASABI_BONUS = 12
  SALMON_N_BONUS = 13
  SQUID_N_BONUS = 14
  EGG_N_BONUS = 15

CARDS_COUNT = {
  CARDS.TEMPURA : 14,
  CARDS.SASHIMI : 14,
  CARDS.DUMPLING : 14,
  CARDS.MAKI_1 : 6,
  CARDS.MAKI_2 : 12,
  CARDS.MAKI_3 : 8,
  CARDS.SALMON_N : 10,
  CARDS.SQUID_N : 5,
  CARDS.EGG_N : 5,
  # Ignoring pudding for now
  CARDS.PUDDING : 0,
  CARDS.WASABI : 6,
  CARDS.CHOPSTICKS : 4,
  # Used for score calculation
  CARDS.WASABI_BONUS : 0,
  CARDS.SALMON_N_BONUS : 0,
  CARDS.SQUID_N_BONUS : 0,
  CARDS.EGG_N_BONUS : 0
}

def calculateScore(hand):
  DUMPLING_SCORE = [0, 1, 3, 6, 10, 15]
  sTempura = int(hand[CARDS.TEMPURA] / 2) * 5
  sSashimi = int(hand[CARDS.SASHIMI] / 3) * 10

  cDumplings = hand[CARDS.DUMPLING]
  if cDumplings > 5:
    cDumplings = 5
  sDumplings = DUMPLING_SCORE[cDumplings]

  sBSalmon = hand[CARDS.SALMON_N_BONUS] * 9
  sBSquid = hand[CARDS.SQUID_N_BONUS] * 6
  sBEgg = hand[CARDS.EGG_N_BONUS] * 3

  sSalmon = (hand[CARDS.SALMON_N] - hand[CARDS.SALMON_N_BONUS]) * 3
  sSquid = (hand[CARDS.SQUID_N] - hand[CARDS.SQUID_N_BONUS]) * 2
  sEgg = hand[CARDS.EGG_N] - hand[CARDS.EGG_N_BONUS]

  return (sTempura + sSashimi) + sDumplings + (sBSalmon + sBSquid + sBEgg) + (sSalmon + sSquid + sEgg)
