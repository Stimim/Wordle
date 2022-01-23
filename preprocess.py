#!/usr/bin/env python


import concurrent.futures
import json
import typing

import common


def ProcessOneGuess(
    guess: str,
    answers: typing.List[str]) -> typing.List[typing.List[int]]:
  entry = [[] for _ in range(243)]
  for answer_id, answer in enumerate(answers):
    result = common.ComputeGuessResult(guess, answer)
    result = common.ConvertGuessResultToInt(result)
    entry[result].append(answer_id)
  return entry


def Main():
  with open('./words.json') as f:
    data = json.load(f)

  answers = data['answers']
  guesses = data['guesses']

  ANSWER_COUNT = len(answers)
  guesses = answers + guesses

  print(f'answers: {len(answers)}')
  print(f'guesses: {len(guesses)}')

  print(int(common.CharMatchResult.RESULT_COUNT))

  database = {
    'answer_count': ANSWER_COUNT,
    'guesses': guesses,
    'filters': [[] for _ in range(len(guesses))]
  }

  with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = {
      executor.submit(ProcessOneGuess, guess, answers) : (index,
                                                                       guess)
      for (index, guess) in enumerate(guesses)
    }
    for future in concurrent.futures.as_completed(futures):
      (index, guess) = futures[future]
      try:
        entry = future.result()
        database['filters'][index] = entry
      except Exception as e:
        print(f'failed to process {guess}: {e}')

  with open('database.json', 'w') as f:
    json.dump(database, f)


if __name__ == '__main__':
  Main()
