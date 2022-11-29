## The goal

Remember our CLI's `connect` function we build on setup day? It works great when the VM is running, but not so well if it is not running: it tries to connect. So instead lets create a check before we attempt to ssh in!

Our final goal will be to setup continuous deployment of our cli so that when we push an update to github it will also be automatically deployed on gemfury!


## Creating the CI

Lets return to our cli so far:

```bash
cd ~/code/<user.github_nickname>/<user.github_nickname>-de-toolkit
```

Before we get started lets initialize the repo, create a new branch and bump the minor version number:

Careful when using .env files don't forget to git ignore them!

```bash
echo ".env" > .gitignore
git init && ga . && gc -m "cli 0.0.1 code"
gh repo create --private --source=. && ggpush
gco -b connect-status-check
poetry version minor
```

We need to call the vm with `gcloud compute instances describe` so lets write a function calling that to spread our code lets create a new file to store these extra utilities which won't be directly accessible by the cli!

```bash
touch <user.github_nickname>-de-toolkit/vm_utils.py
```

## Testing functions

Lets test our function (ideally we would test all parts of our cli but lets stick to just this new helper function) the obvious difficulty is that currently the function relies on whether our vm is running or not so within our test file we need to create a function to create fake output.

The first step is to create a test file!

```bash
touch test/test_vm_utils.py
```

Next we want to create files which show the two states

```bash
gcloud compute instances describe --zone=europe-west1-b ogiles1999-data-eng-vm > tests/<state>.txt
```

Now inside `test/test_vm_utils.py` create a helper function which would return the same as calling our function!

```bash
import pathlib
from ogiles1999_de_toolkit.vm_utils import check_running

def fake_input(state):
    path = pathlib.Path(__file__).resolve().parent.joinpath(f'{state}.txt')
    with open(path, 'r') as file:
        data = file.read().replace('\n', '')
    return data

def test_state_check():
    assert check_running(fake_input("stopped")) is False
    assert check_running(fake_input("running")) is True
```

We can now include our ci implementation from the previous exercise!

```bash
cp -r ../longest-words/.github .
```

Now if we push our work and create a pull request you should see the ci running, one of the best parts about CI is how cookie cutter they are, once we have a workflow we like it is easy to use it on many repos.

It should fail try and debug it by reading the action output!

<details>
<summary markdown='span'>Solution</summary>

```bash
poetry add -G dev pytest
```
</details>

Now when you push again you should see green (ideally our ci would fully check our package but not today!)

### Protecting the primary branch!



### Implementing CD

cp .github/workflows/.python-ci.yml .github/workflows/.fury-cd.yml



gh secret set GEMFURY_TOKEN --body "$GEMFURY_TOKEN"


 pipx uninstall <user.github_nickname>-de-toolkit && pipx install $_ --pip-args='--extra-index-url https://<deploy token>@repo.fury.io/<user.github_nickname>/'