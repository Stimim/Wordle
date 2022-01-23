A program for the game [Wordle](https://www.powerlanguage.co.uk/wordle/).

- words.json contains two lists:
  - `answers` is the list of possible answers
  - `guesses` contains other valid words that can be guesses

- preprocess.py: preprocess words.json.  The script will generate file
    `database.json`, which is required by all following programs.

- algo1.py:

    Implements an AI for the game. For each guess, the program finds the word
    whose possible results have the maximum entropy. For each valid guess, we
    define the entropy as:
    ```
    n_i = | { answer | ComputeGuessResult(guess, answer) == result_i} |
    N = SUM(n_i) == | { answer } |
    entropy = -SUM(n_i / N * log(n_i / N))
    ```

    `python algo1.py <answer>` to find the guessed words of a given answer.

- benchmark.py: Computes number of required guesses for each answer.

- manual.py: play the game interactively.  When the program guesses a word, you
  need to input the result, it's a 5-character string, each character is either:
    - `o` for letters in the word and in the correct spot.
    - `!` for letters in the word but in the wrong spot.
    - `_` for letters not in the word.


### Reference:
- https://medium.com/@tglaiel/the-mathematically-optimal-first-guess-in-wordle-cbcb03c19b0a

    The structure of my algorithm is based on this document. But, instead of
    using min-max to minimize the max size of remaining answers, my algorithm
    uses entropy instead.
