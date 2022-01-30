#!/usr/bin/env python


import argparse
import math
import typing

import common

# TOLERANCE = 0.5  # 3.735637149028078
# TOLERANCE = 0.1  # 3.4531317494600433
TOLERANCE = 0.08  # 3.4475161987041036
# TOLERANCE = 0.08  # 3.451403887688985
# TOLERANCE = 0.05  # 3.475593952483801
# TOLERANCE = 0.01  # 3.4721382289416844

print(f'TOLERANCE={TOLERANCE}')

class Player(common.PlayerInterface):
  possibilities: typing.Optional[typing.Set[common.GuessIndex]]
  first_choice: int

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.first_choice = -1

  def Init(self):
    self.possibilities = None

  def _PrintResult(self, best_id, best_value):
    assert self.possibilities
    N = len(self.possibilities)
    best_word = self.database.guesses[best_id]
    if best_id not in self.possibilities:
      best_word += '(!)'
    print(f'return {best_word}, best_value: {best_value} remaining: {N}')
    if N < 10:
      print([self.database.guesses[k] for k in self.possibilities])

  def MakeAGuess(self) -> common.GuessIndex:
    best_id = -1
    best_value = 0

    if self.possibilities is None:
      self.possibilities = set(range(self.database.answer_count))

      if self.first_choice != -1:
        return self.first_choice

      for guess_id, results in enumerate(self.database.filters):
        N = self.database.answer_count
        entropy = math.log(N)
        for r in results:
          n = len(r)
          if n:
            entropy -= n * math.log(n) / N
        if abs(entropy - best_value) < TOLERANCE:
          if guess_id < self.database.answer_count:
            best_id = guess_id
        elif entropy > best_value:
          best_id = guess_id
          best_value = entropy

      self.first_choice = best_id
      if common.VERBOSE_GAMEPLAY:
        self._PrintResult(best_id, best_value)
      return best_id

    N = len(self.possibilities)
    if N == 1:
      guess_id = next(iter(self.possibilities))
      if common.VERBOSE_GAMEPLAY:
        print(f'return {self.database.guesses[guess_id]}, the only choice')
      return guess_id

    for guess_id, results in enumerate(self.database.filters):
      entropy = math.log(N)
      for r in results:
        n = len(self.possibilities & r)
        if n:
          entropy -= n * math.log(n) / N
      if abs(entropy - best_value) < TOLERANCE:
        if guess_id in self.possibilities:
          best_id = guess_id
      elif entropy > best_value:
        best_id = guess_id
        best_value = entropy

    assert best_id >= 0

    if common.VERBOSE_GAMEPLAY:
      self._PrintResult(best_id, best_value)
    return best_id

  def UpdateResult(self, guess_id, result):
    self.possibilities &= self.database.filters[guess_id][result]


def Main():
  parser = argparse.ArgumentParser()
  parser.add_argument('answer')

  args = parser.parse_args()

  answer = args.answer

  database = common.LoadData()
  answer_id = database.guesses.index(answer)
  assert answer_id < database.answer_count

  player = Player(database)

  engine = common.GameEngine(answer_id, database, verbose=True)
  engine.Play(player)


if __name__ == '__main__':
  Main()
