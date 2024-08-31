import random
import numpy as np


class Scoreboard:
  def __init__(self, players):
    self._players = players
    self._options = ["aces", "twos", "threes", "fours", "fives", "sixes", "pair", "two pairs", "three of a kind", "four of a kind", "full house", "small straight", "large straight", "chance", "yahtzee"]
    self._scores = []
    for p in range(len(players)):
      player_scores = []
      for option in self._options:
        player_scores.append(None)
      self._scores.append(player_scores)

  def available_options(self, player):
    return [option for option in self._options if self.is_option_available(player, option)]

  def is_option_available(self, player, option):
    p = player
    if option in self._options:
      o = self._options.index(option)
      return self._scores[p][o] == None  # Available, has not been set yet
    return False

  def calculate_and_add_score(self, player, option, dices):
    if self.is_option_available(player, option):
      score = calculate_score_for_option(dices, option)
      p = player
      o = self._options.index(option)
      self._scores[p][o] = score
      return True
    return False

  def print(self):
    print("\nSCOREBOARD")
    print(f"Player     {self._options}")
    print(f"-----------------------------")
    number_of_players = len(self._players)
    for p in range(number_of_players):
      print(f"{self._players[p]}:  {self._scores[p]}")
    print()


# Roll all "dices" (list w ints).
# Don't re-roll "dices" at index specified in dices_to_keep.
def roll_dices(dices, dices_to_keep = []):
  for i in range(0,5):
    if not i + 1 in dices_to_keep:
      dices[i] = random.randint(1,6)
  dices.sort(reverse=True)  # Sorted dices always allows for highest possible score in calculations


# User interactions for one turn.
# Give a player three rolls, and asks for what dices to keep, inbetween.
def player_roll_dices(dices):
  roll_dices(dices)
  print(f"\nRoll: {dices}")
  for _ in range(2):
    dices_to_keep = input("Dices to keep (1-5), space separated, enter to roll all: ").split()
    dices_to_keep_ints = [eval(i) for i in dices_to_keep]
    roll_dices(dices, dices_to_keep_ints)
    print(f"\nRoll: {dices}")


def calculate_sum_for_value(dices, value):
  return sum([d for d in dices if d == value])


def calculate_best_n_of_a_kind(dices, number_of_a_kind):
  for dice in dices:
    matching_dices = [d for d in dices if d == dice]
    if len(matching_dices) >= number_of_a_kind:
      # First match is the greatest, thanks to sort
      return number_of_a_kind * dice
  return 0


def calculate_two_pairs(dices):
  unique_dice_value, count = np.unique(dices, return_counts=True)
  pairs = unique_dice_value[count >= 2]
  if pairs.size == 2:
    return sum(pairs * 2)
  else:
    return calculate_best_n_of_a_kind(dices, 4)  # Four equal could also count as two pairs


def calculate_full_house(dices):
  unique_dice_value, count = np.unique(dices, return_counts=True)
  pair = unique_dice_value[count == 2]
  threes = unique_dice_value[count == 3]
  if pair.size > 0 and threes.size > 0:
    return pair[0] * 2 + threes[0] * 3
  else:
    return 0
  

def calculate_small_straight(dices):
  if dices == [5,4,3,2,1]:
    return 15
  else:
    return 0


def calculate_large_straight(dices):
  if dices == [6,5,4,3,2]:
    return 20
  else:
    return 0


def calculate_score_for_option(dices, option):
  if option == "aces":
    return calculate_sum_for_value(dices, 1)
  elif option == "twos":
    return calculate_sum_for_value(dices, 2)
  elif option == "threes":
    return calculate_sum_for_value(dices, 3)
  elif option == "fours":
    return calculate_sum_for_value(dices, 4)
  elif option == "fives":
    return calculate_sum_for_value(dices, 5)
  elif option == "sixes":
    return calculate_sum_for_value(dices, 6)
  elif option == "Pair":
    return calculate_best_n_of_a_kind(dices, 2)
  elif option == "Two pairs":
    return calculate_two_pairs([dices])
  elif option == "Three of a kind":
    return calculate_best_n_of_a_kind(dices, 3)
  elif option == "Four of a kind":
    return calculate_best_n_of_a_kind(dices, 4)
  elif option == "Full house":
    return calculate_full_house(dices)
  elif option == "Small straight":
    return calculate_small_straight(dices)
  elif option == "Large straight":
    return calculate_large_straight(dices)
  elif option == "Chance":
    return sum(dices)
  elif option == "Yahtzee":
    return calculate_best_n_of_a_kind(dices, 5)


# Get player's options for the current setup of dices
def print_score_options(dices, selected_options=["aces", "twos", "threes", "fours", "fives", "sixes", "pair", "two pairs", "three of a kind", "four of a kind", "full house", "small straight", "large straight", "chance", "yahtzee"]):
  for option in selected_options:
    score = calculate_score_for_option(dices, option)
    print(f"{option.capitalize()}:\t{int(score)}")


def print_total_scores(players, scores):
  for player in range(len(players)):
    print(f"{players[player]} total score: {scores[player]}")


def calculate_score_for_option(dices, option):
  if option == "aces":
    return calculate_sum_for_value(dices, 1)
  elif option == "twos":
    return calculate_sum_for_value(dices, 2)
  elif option == "threes":
    return calculate_sum_for_value(dices, 3)
  elif option == "fours":
    return calculate_sum_for_value(dices, 4)
  elif option == "fives":
    return calculate_sum_for_value(dices, 5)
  elif option == "sixes":
    return calculate_sum_for_value(dices, 6)
  elif option == "pair":
    return calculate_best_n_of_a_kind(dices, 2)
  elif option == "two pairs":
    return calculate_two_pairs(dices)
  elif option == "three of a kind":
    return calculate_best_n_of_a_kind(dices, 3)
  elif option == "four of a kind":
    return calculate_best_n_of_a_kind(dices, 4)
  elif option == "full house":
    return calculate_full_house(dices)
  elif option == "small straight":
    return calculate_small_straight(dices)
  elif option == "large straight":
    return calculate_large_straight(dices)
  elif option == "chance":
    return sum(dices)
  elif option == "yahtzee":
    return calculate_best_n_of_a_kind(dices, 5)
  else:
    return 0


def calculate_winners(players, players_scores):
  top_score = 0
  winners = []
  for player in range(len(players_scores)):
    if players_scores[player] > top_score:
      # new top score
      top_score = players_scores[player]
      winners = [player]
    elif players_scores[player] == top_score:
      # new draw
      winners.append(player)
  winners_names = [players[w] for w in winners]
  return winners_names


# Setup
dices = [0,0,0,0,0]
players = ["Player 1", "Player 2"]
players_scores = [0,0]
scoreboard = Scoreboard(players=players)
scoreboard.print()

# Turns
for _ in range(15):
  for player in range(len(players)):
    print(f"\n{players[player]}s turn:")
    player_roll_dices(dices)
    print_score_options(dices, scoreboard.available_options(player))
    added = False
    while not added:
      option = input("Select option (or select option to zero out): ")
      added = scoreboard.calculate_and_add_score(player, option, dices)
      if not added:
        print(f"'{option.capitalize()}' can´t be selected.")

# Total results
print("\nGame over!")
winners = calculate_winners(players, players_scores)
if len(winners) == 1:
  print(f"Winner: ", end="")
else:
  print("Draw: ", end="")
print(*winners, sep=", ")
print_total_scores(players, players_scores)
