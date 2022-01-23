#!/usr/bin/env python

import common
import algo1


class ManualGameEngine:
  database: common.Database

  def __init__(self, database, verbose=True):
    self.database = database
    self.verbose = verbose

  def Play(self, player: common.PlayerInterface):
    player.Init()
    for try_count in range(6):
      guess_id = player.MakeAGuess()

      print(f'guess {try_count + 1}:')
      if self.database.IsAnswerId(guess_id):
        print(self.database.guesses[guess_id])
      else:
        print(f'{self.database.guesses[guess_id]} (not answer)')

      # Get result
      while True:
        raw_result = input('Please input the result: ')
        if len(raw_result) == 5:
          break

      result = []
      for x in raw_result:
        if x == 'o':
          result.append(common.CharMatchResult.MATCH)
        elif x == '!':
          result.append(common.CharMatchResult.WRONG_SPOT)
        else:
          result.append(common.CharMatchResult.NOT_FOUND)

      result = common.ConvertGuessResultToInt(result)
      if result == common.CharMatchResult.RESULT_COUNT ** 5 - 1:
        print('Done!')
        return try_count + 1

      player.UpdateResult(guess_id, result)
    else:
      return 7


def Main():
  database = common.LoadData()
  player = algo1.Player(database)
  engine = ManualGameEngine(database)
  while True:
    engine.Play(player)


if __name__ == '__main__':
  Main()
