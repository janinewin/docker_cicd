# Test Driven Development

Test-driven development (aka **TDD**) is a software development process that relies on the repetition of a very short development cycle: red-green-refactor. The idea of this process is to turn a requirement into one or a couple of specific test cases, run those tests to make sure they are red, then implementing the code to turn those tests green. A third step is to refactor the code while keeping the tests green.

![](https://res.cloudinary.com/wagon/image/upload/v1560715040/tdd_y0eq2v.png)

The testing pattern encouraged is a four-phase one and well described in this [blog article by Thoughtbot](https://robots.thoughtbot.com/four-phase-test)

## Longest Word

Let's practice TDD with a simple game that we will use until the end of the day. We will implement "The Longest Word", a game where given a list of nine letters, you have to find the longest possible English word formed by those letters.

Example:

```
Grid: OQUWRBAZE
Longest word: BAROQUE
```

The word [`baroque`](https://en.wiktionary.org/wiki/baroque) is valid as it exists in the English dictionary (even though its origin is French 🇫🇷 😋)

Note that the word [`bower`](https://en.wiktionary.org/wiki/bower) is also valid. The goal here is **not** to write code which finds the longest word, but to analyze a human player attempt and judge if this word is valid or not against the given grid!

### A first approach

We need to **break down** the problem in tiny pieces. We also need to find the right level of **modelling** against the Object-Oriented paradigm.

In the TDD paradigm, one question we always ask is:

> How can I test this?

Asking this question means you need to think about your code like a black box. It will take some parameters in entry and you will observe the output, comparing them to an expected result.

❓ Take a few minutes to think about the **two main functions** of our game.

<details><summary markdown="span">View solution
</summary>

We need a first function to compute a grid of nine random letters:

```python
def random_grid():
    pass
```

We need another function which, given a nine letter grid, tells if a word is valid:

```python
def is_valid(word, grid):
    pass
```

</details>

<br>

❓ How can we use the Object-Oriented paradigm on this problem? Again, take some time to think about it.

<details><summary markdown='span'>View solution
</summary>

We can create a `Game` class which will have the following blueprint:

1. Generate and hold a 9-letter random list
1. Test the validity of a word against this grid

</details>

<br>

### Starting the project with TDD

Now that we have a better idea of the object we want to build, we can start writing a test. First of all, let's create a new Python project:

```bash
cd ~/code/<user.github_nickname>
poetry new longest-word && cd $_
poetry add pytest pylint

touch longest_word/game.py
touch tests/test_game.py

code .
```

Let's set up our test class,

```python
# tests/test_game.py
import string
from longest_word.game import Game

class TestGame:
    def test_game_initialization(self):
        new_game = Game()
        grid = new_game.grid
        assert type(grid) == list
        assert len(grid) == 9
        for letter in grid:
            assert letter in string.ascii_uppercase
```

Read this code. If you have _any_ question about it, ask a teacher. You can copy/paste this code to `tests/test_game.py`.

Now it's time to run it first to make sure those tests are **failing**:

```bash
poetry run pytest
```

What next? Now you should **read the error message**, and try to **fix** it, and only this one (don't anticipate). Let's do the first one together:

```bash
============================= test session starts ==============================
platform darwin -- Python 3.8.14, pytest-7.1.3, pluggy-1.0.0
rootdir: /Users/olivergiles/code/ogiles1999/longest-word
collected 0 items / 1 error

==================================== ERRORS ====================================
_____________________ ERROR collecting tests/test_game.py ______________________
ImportError while importing test module '/Users/olivergiles/code/ogiles1999/longest-word/tests/test_game.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../../.pyenv/versions/3.8.14/lib/python3.8/importlib/__init__.py:127: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_game.py:2: in <module>
    from longest_word.game import Game
E   ImportError: cannot import name 'Game' from 'longest_word.game' (/Users/olivergiles/code/ogiles1999/longest-word/longest_word/game.py)
=========================== short test summary info ============================
ERROR tests/test_game.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.04s ===============================
FAIL
```

OK so the error message is `ImportError: cannot import name 'Game' from 'longest_word.game'`. It can't find a `Game` type.

❓ How can we fix it?

<details><summary markdown='span'>View solution
</summary>

We need to create a `Game` class in the `./game.py` file:

```python
# game.py
# pylint: disable=missing-docstring

class Game:
    pass
```

</details>

<br>

Let's run the tests again:

```bash
poetry run pytest
```

We get this error message:

```
============================= test session starts ==============================
platform darwin -- Python 3.8.14, pytest-7.1.3, pluggy-1.0.0
rootdir: /Users/olivergiles/code/ogiles1999/longest-word
collected 1 item

tests/test_game.py F                                                     [100%]

=================================== FAILURES ===================================
______________________ TestGame.test_game_initialization _______________________

self = <tests.test_game.TestGame object at 0x1016750a0>

    def test_game_initialization(self):
        new_game = Game()
>       grid = new_game.grid
E       AttributeError: 'Game' object has no attribute 'grid'

tests/test_game.py:7: AttributeError
=========================== short test summary info ============================
FAILED tests/test_game.py::TestGame::test_game_initialization - AttributeErro...
============================== 1 failed in 0.04s ===============================
FAIL
```

🎉 PROGRESS!!! We have a **new** error message: `AttributeError: 'Game' object has no attribute 'grid'`.

![](https://res.cloudinary.com/wagon/image/upload/v1560715000/new-error_pvqomj.jpg)

### Your turn!

Did you get this quick feedback loop? We run the test, we get an error message, we figure out how to fix only this, we run the test again and we move to a new error message!

❓ Try to implement the `Game` code to make this test pass. Don't look at the solution just yet, try to apply TDD on this problem!

💡 You can use you can use `pytest --pdb` to jump into the debugger on test failure.

<details><summary markdown='span'>View solution
</summary>

One possible implementation is:

```python
# game.py
# pylint: disable=missing-docstring

import string
import random

class Game:
    def __init__(self):
        self.grid = []
        for _ in range(9):
            self.grid.append(random.choice(string.ascii_uppercase))
```

</details>

<br>

## Checking the validity of a word

Let's move to the second method of our `Game` class.

We use **TDD**, which means that we need to write the test **first**. For the first test, we gave away the code.

❓ It's your turn to implement a test for this new `is_valid(self, word)` method! See, we already gave you the method [signature](https://en.wikipedia.org/wiki/Type_signature#Method_signature)...

<details><summary markdown='span'>View solution
</summary>

A possible implementation of the test would be:

```python
# tests/test_game.py

# [...]

    def test_empty_word_is_invalid(self):
        new_game = Game()
        assert new_game.is_valid('') is False

    def test_is_valid(self):
        new_game = Game()
        new_game.grid = list('KWEUEAKRZ') # Force the grid to a test case:
        assert new_game.is_valid('EUREKA') is True
        assert new_game.grid == list('KWEUEAKRZ') # Make sure the grid remained untouched

    def test_is_invalid(self):
        new_game = Game()
        new_game.grid = list('KWEUEAKRZ') # Force the grid to a test case:
        assert new_game.is_valid('SANDWICH') is False
        assert new_game.grid == list('KWEUEAKRZ') # Make sure the grid remained untouched
```
</details>

<br>

Run the tests to make sure they are not passing:

```bash
poetry run pytest
```

❓ It's your turn! Update the `game.py` implementation to make the tests pass!

<details><summary markdown='span'>View solution
</summary>

A possible implemantation is:

```python
# game.py

# [...]

    def is_valid(self, word):
        if not word:
            return False
        letters = self.grid.copy() # Consume letters from the grid
        for letter in word:
            if letter in letters:
                letters.remove(letter)
            else:
                return False
        return True
```

</details>

<br>


## Style

Make sure to make `pylint` happy:

```bash
poetry run pylint longest_word/game.py
```

pylint is the standard 'linter' for python, it checks the code without running. Its suggestions are mostly good practices to follow the [documentation](https://pylint.pycqa.org/en/latest/) is good if you want to follow it in more detail but most of the suggestions are pretty intuitive.

You can disable those rules which you don't think should apply here for example:

```python
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
```
