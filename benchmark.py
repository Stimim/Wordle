#!/usr/bin/env python


import argparse
import concurrent.futures
import logging
import os
import random
import typing

from tqdm import tqdm

import common
import algo1


class Benchmark:
  database: common.Database
  player_class: typing.Type[common.PlayerInterface]

  def __init__(self, database, player_class):
    self.database = database
    self.player_class = player_class

  def RunOne(self, answer_id):
    engine = common.GameEngine(answer_id, self.database, verbose=False)
    player = self.player_class(self.database)
    try_count = engine.Play(player)

    return try_count

  def RunBatch(self, batch: typing.List[int]):
    engine = common.GameEngine(-1, self.database, verbose=False)
    player = self.player_class(self.database)

    results = []
    for answer_id in batch:
      engine.answer_id = answer_id
      results.append(engine.Play(player))
    return results


  def RunAll(self, N: int=0, job_count: int=0):
    if N == 0:
      N = self.database.answer_count

    if job_count == 0:
      job_count = os.cpu_count() or 16

    batch_size = N // job_count
    print(f'start: job_count={job_count}, N={N}, batch_size={batch_size}')

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=job_count) as executor:
      futures = {}

      answer_ids = random.sample(range(self.database.answer_count), N)

      for start in range(0, len(answer_ids), batch_size):
        batch = answer_ids[start:(start + batch_size)]
        future = executor.submit(self.RunBatch, batch)
        futures[future] = batch

      tqdm_kwargs = {
        'total': len(futures),
        'unit': 'ans',
        'unit_scale': True,
        'leave': True
      }

      accumulated_value = 0
      try_count_to_words = [[] for _ in range(10)]

      for future in tqdm(concurrent.futures.as_completed(futures),
                         **tqdm_kwargs):
        batch = futures[future]
        try:
          results = future.result()
        except Exception:
          logging.exception('failed to process %s', batch)
        else:
          for answer_id, try_count in zip(batch, results):
            accumulated_value += try_count
            try_count_to_words[try_count].append(answer_id)

      print(f'average: {accumulated_value / N}')
      for try_count, answers in enumerate(try_count_to_words):
        if not answers:
          continue
        words = [self.database.guesses[word_id] for word_id in answers[:10]]
        print(f'{try_count}: {len(answers)} ==> {words}')


def Main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-N', type=int, default=0)
  parser.add_argument('--jobs', type=int, default=0)

  args = parser.parse_args()

  database = common.LoadData()
  benchmark = Benchmark(database, algo1.Player)

  benchmark.RunAll(args.N, args.jobs)


if __name__ == '__main__':
  Main()
