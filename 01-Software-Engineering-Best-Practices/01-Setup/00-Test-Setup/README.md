## Test the setup
This first challenge will test if your setup is correct, and make you understand how the bootcamp works.

Open two separate vscode windows (you can use `code folder_path`):
- one at this challenge-level folder (you should already be there)
- another one at `data-engineering-challenges` root level

## Understand your repository structure

❓ Take a look at your `data-engineering-challenges` structure with `tree -a -L 2` and take some time to understand it.

```bash
.
├── 01-Software-Engineering-Best-Practices # Module level
│   ├── 01-Setup                           # Unit level
│   │   ├── 00-Test-Setup                  # Challenge level
            ├── app
            │   ├── __init__.py
            │   └── main.py                # YOUR CODE HERE
            └── tests
            │   ├── __init__.py
            │   └── test_your_function.py  # OUR TEST CODE HERE
            ├── .venv                      # your virtual-env for this challenge, created automatically by poetry
            ├── .envrc                     # direnv call to activate your poetry venv as soon as you cd into the foler
            ├── makefile                   # Contains `make test` and `make install` commands for you
            ├── poetry.lock                # Created by you when running `make install`
            ├── pyproject.toml             # We already wrote this for you so that poetry install will create all you need
            ├── README.md                  # Kitt-displayed readme
...
...
...
├── .dockerignore
├── .gitignore          # globally ignore file pattern (.env, etc...)
├── CHEATSHEET.md       # Some tips for you
├── Makefile            # Gobal bootcamp commands (e.g. run all `make install` for each challenges, run all tests etc...)
├── make.inc            # This file is accessed by every challenges-level makefile (for refactoring purposes)
├── README.md
├── common              # Le Wagon shared logic between all challenges (used for test purposes)
├── direnvrc-template   # You can remove it once you've added it to your ~/.direnvrc
└── yapf                # Formatting rules for you to auto-format your code
```

## CHEATSHEET.md

👉 Read the `CHEATSHEET.md`  we created for you to help you throughout the camp! At least, focus on section 1️⃣ to 3️⃣ now

> 💡 You can use VScode to render HTML properly by clicking on the top-right icon, or "Command Palette (Cmd-Shift-P)" --> "Open Preview to the side".

## Try to pass the tests of this dummy challenge

❓ Open your VScode at 00-Test-Setup level, then try to fill your code in `app.main`

Have a look at the tests/ folder:
- there are some mandatory tests that will NOT be checked by running `make test` (which does a `pytest -m "not optional"` under the hood: checkout in `make.inc` !)
- optional tests can still be tested by running pytest manually (e.g `pytest tests/test_our_function.py`)

Run
```
make test
```
It should PASS (hopefully 😅), and you should see a new `test_output.txt` file created.
This file is used by Kitt to track your progress during the day. But for that to happen, you need to push your code to github first!

```
git add --all
git commit -m "010100 done"
git push origin main
```

👉 Go check on your progress status on Kitt's challenge page top right corner! It should be green
Don't forget to follow the progress of your buddy of the day and help him out if needs be!
