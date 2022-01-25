#!/usr/bin/env python

import algo1
import argparse

import common

def Main():
  parser = argparse.ArgumentParser()
  parser.add_argument('answer')
  args = parser.parse_args()

  database = common.Database.LoadData()
  guess_to_id = {
    guess: i for i, guess in enumerate(database.guesses)
  }

  answer = args.answer
  answer_id = guess_to_id[answer]

  player = algo1.Player(database)
  player.Init()

  possibilities = set(range(database.answer_count))
  for try_count in range(6):
    if try_count > 0:
      word_list = [database.guesses[i] for i in possibilities]
      print(f'{len(possibilities)} left: {word_list}')

    player_guess = player.MakeAGuess()
    print(f'{database.guesses[player_guess]}')
    guess = input(f'guess {try_count + 1}: ')
    if guess not in guess_to_id:
      continue
    guess_id = guess_to_id[guess]
    result = -1
    for i, ws in enumerate(database.filters[guess_id]):
      if answer_id in ws:
        result = i
        possibilities &= ws
        break
    assert result != -1

    player.UpdateResult(guess_id, result)
    if guess_id == answer_id:
      print(f'Done')
      break


if __name__ == '__main__':
  Main()
