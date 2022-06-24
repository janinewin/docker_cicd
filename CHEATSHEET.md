# Cheatsheet 💡

Below you'll find a bunch of pre-requisite and useful knowledge for the bootcamp.

## Tips on any linux command ❓

You're wondering what `cat`, `make`, `wget` do and how to use them?

Two tools to the rescue, pre-installed on your servers:
- Type `tldr tar` to get info about the `tar` command. That's [tldr](https://tldr.sh/).
- Or type `man tar` to get the "official", but more old school manual.

## Download a file to the Virtual Machine 📁

Either **directly download the file**, for that

- In your browser, right click and "Copy link address" to get the URL
- Use `wget` to download the file: open a terminal and type `wget -O <name for the file> <url>`. For more information and examples, use `tldr wget`.

Or by downloading it to your laptop then copying it over to the virtual machine.
- Download it on your laptop, as you usually do, or use `wget` as described above 👆.
- Copy it to the server with `scp -i <path to your private SSH key> /path/to/the/file <username on the VM>@<VM IP>:/path/on/the/vm`. For instance:
  - My SSH key is located at `~/.ssh/id_rsa`
  - I've downloaded the file on my machine at `~/Downloads/some-file.txt`
  - On the server, my username is `joe` and IP is 33.442.44.112
  - I'd like to copy it to `/home/joe/hello/world/` on the server (this folder must already exist)
  - I'll do 👉 - `ssh -i ~/.ssh/id_rsa ~/Downloads/some-file.txt joe@33.442.44.112:/home/joe/hello/world/some-file.txt`

## Managing Python libraries in your projects with Poetry 📃

... pip ... poetry

### Within Docker

- Install Poetry with `pip3 install poetry`
- Copy your code, most importantly the `poetry.lock` and `pyproject.toml`
- Run `poetry install`
- Prefix commands with `poetry run ...`

### Our setup with `direnv`

... cd into dirs
[direnv](https://direnv.net/)

## Makefile 🔃

... Makefile in each directory
... make.inc at the top

## Tests 🚫

... make test
... pytest
... poetry test -v


- when it passes `tests/test_all.py::test_csv PASSED`
- when there are errors
```======================================================= short test summary info ========================================================
FAILED tests/test_all.py::test_csv - AssertionError: file ratings.csv not found under data/
```

## Manage your VM

- Navigate to the [cloud instances](https://console.cloud.google.com/compute/).
- Turn on your VM every morning by selecting its checkbox ✅, clicking on the three dots, then "Start / Resume"
- Turn it off every evening by selecting its checkbox ✅, clicking on the three dots, then "Stop". That'll save money and energy.

## VSCode - how to open a port and connect to your apps and databases from your machine

... explain

## VSCode - Select the correct "Python interpreter"

... explain
... hopefully we can automate it
