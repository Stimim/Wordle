#!/usr/bin/env python

import argparse
import typing

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

  possibilities = set(range(database.answer_count))
  for try_count in range(6):
    if try_count > 0:
      word_list = [database.guesses[i] for i in possibilities]
      print(f'{len(possibilities)} left: {word_list}')

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

    if guess_id == answer_id:
      print(f'Done')
      break


if __name__ == '__main__':
  Main()
