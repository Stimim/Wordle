import enum
import json
import os
import typing


class CharMatchResult(enum.IntEnum):
  NOT_FOUND = 0
  WRONG_SPOT = 1
  MATCH = 2

  RESULT_COUNT = enum.auto()


GuessIndex = int


class Database:
  answer_count: int
  guesses: typing.List[str]
  filters: typing.List[typing.List[typing.FrozenSet[GuessIndex]]]

  def __init__(self, answer_count, guesses, filters):
    self.answer_count = answer_count
    self.guesses = guesses
    # self.guess_to_id = {
      # guess : i for i, guess in enumerate(guesses)
    # }
    self.filters = [
      [ frozenset(result) for result in results ] for results in filters
    ]

  def IsAnswerId(self, guess_id):
    return guess_id < self.answer_count

  @staticmethod
  def LoadData() -> 'Database':
    with open('database.json') as f:
      db = json.load(f)
      answer_count = db['answer_count']
      guesses = db['guesses']
      filters = db['filters']

    return Database(answer_count, guesses, filters)


def LoadData() -> Database:
  return Database.LoadData()


def ComputeGuessResult(guess: str, answer: str) -> typing.List[CharMatchResult]:
  result = [CharMatchResult.NOT_FOUND] * 5

  answer_list: typing.List[str]
  answer_list = list(answer)

  for i, c in enumerate(guess):
    if c == answer_list[i]:
      result[i] = CharMatchResult.MATCH
      answer_list[i] = ''
  for i, c in enumerate(guess):
    if result[i] != CharMatchResult.NOT_FOUND:
      continue

    if c in answer_list:
      result[i] = CharMatchResult.WRONG_SPOT
      for j in range(5):
        if answer_list[j] == c:
          answer_list[j] = ''
          break
  return result


def ConvertGuessResultToStr(result: typing.List[CharMatchResult]) -> str:
  s = ''
  for x in result:
    if x == CharMatchResult.NOT_FOUND:
      s += '_'
    elif x == CharMatchResult.WRONG_SPOT:
      s += '!'
    elif x == CharMatchResult.MATCH:
      s += 'o'
  return s


def ConvertGuessResultToInt(result) -> int:
  retval = 0
  for x in result:
    retval = retval * CharMatchResult.RESULT_COUNT + x
  return retval


def ConvertIntToGuessResult(x: int) -> typing.List[CharMatchResult]:
  result = []

  for _ in range(5):
    result.append(x % CharMatchResult.RESULT_COUNT)
    x = x // CharMatchResult.RESULT_COUNT

  return list(reversed(result))


class PlayerInterface:
  database: Database

  def __init__(self, database):
    self.database = database

  def Init(self):
    raise NotImplementedError

  def MakeAGuess(self) -> GuessIndex:
    raise NotImplementedError

  def UpdateResult(self, guess: GuessIndex, result: int):
    raise NotImplementedError


class GameEngine:
  answer_id: GuessIndex
  database: Database

  def __init__(self, answer_id, database, verbose=False):
    self.database = database
    self.answer_id = answer_id
    self.verbose = verbose

  def Play(self, player: PlayerInterface):
    player.Init()
    for try_count in range(6):
      guess_id = player.MakeAGuess()

      result = -1
      for result_, remaining in enumerate(self.database.filters[guess_id]):
        if self.answer_id in remaining:
          result = result_
          break

      assert result != -1

      if VERBOSE_GAMEPLAY:
        print(f'guess {try_count + 1}:')
        print(self.database.guesses[guess_id])
        print(ConvertGuessResultToStr(ConvertIntToGuessResult(result)))

      if guess_id == self.answer_id:
        return try_count + 1
      player.UpdateResult(guess_id, result)
    else:
      return 7


VERBOSE_GAMEPLAY = os.environ.get('VERBOSE_GAMEPLAY') and True or False
