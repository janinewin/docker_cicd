# Using poetry

This exercise will use poetry to create a toolbox that will be published and available to install anywhere!

## Creating a package

Lets start by creating a new poetry package!

```bash
poetry new ~/code/<user.github_nickname>/<user.github_nickname>-de-toolkit && cd $_
```

Here we are using poetry to create a new package and then a useful terminal command in `$_` which is the most recent parameter in this case the folder we just creater with `poetry new` letting us cd right into it.

At this point we will have our README.md, basic pyproject.toml, <user.github_nickname>_de_toolkit to populate, and a tests folder if needed

Our goal is to create a basic cli to help us with some of our common workflows interacting with our virtual machine!

Lets add [click](https://click.palletsprojects.com/en/8.1.x/) to our project to help develop our cli:
```bash
poetry add click
```

Let begin by creating a main file to create our entrypoint in:

<user.github_nickname>_de_toolkit/main.py
```python
import click

@click.group()
def cli():
    pass

if __name__ == '__main__':
    cli()
```
Here we are are setting up the skeleton of a cli using [group](https://click.palletsprojects.com/en/8.1.x/commands/). This is where we will add other commands to flesh it out.

Now if you run `poetry run python <user.github_nickname>_de_toolkit/main.py` you should see some empty
documentation appear, one of the great features of click is how it uses doc strings in order to generate readable cli feedback!

This is not how we want to use our cli so we need to add a line to our pyproject.toml to allow it to be run more easily:

```toml
[tool.poetry.scripts]
deng = '<user.github_nickname>.main:cli'
```
Now we can run our cli with `poetry run deng` instead, if we wanted multiple cli commands in one package we could just add another line in this section!

Now lets generate the first part of our toolkit create a new file `touch <user.github_nickname>_de_toolkit/vm.py` to contain our vm commands.

Here your goal is now to fill out the commands to fufil the main functions you need:

- start the vm
- stop the vm
- connect directly vscode in the vm

❓ **Try to implement these** in the function shells below using the inbuilt [subprocess](https://docs.python.org/3/library/subprocess.html) module!

```python
import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    # your code here

@click.command()
def stop():
    """Stop your vm"""
    # your code here

@click.command()
def connect():
    """Connect to your vm in vscode"""
    # your code here
```

<details>
<summary markdown='span'>start command</summary>

```bash
gcloud compute instances start --zone=<vm zone> <vm name>
```

</details>

<details>
<summary markdown='span'>start command</summary>

```bash
gcloud compute instances stop --zone=<vm zone> <vm name>
```

</details>

</details>

<details>
<summary markdown='span'>start command</summary>

```bash
gcloud compute instances stop --zone=<vm zone> <vm name>
```

</details>

<details>
<summary markdown='span'>jump into vm</summary>

```bash
code --folder-uri vscode-remote://ssh-remote+<vm ip><path inside vm>
```

</details>

Now we have our commands we are ready to add them to the main cli go back to our original `main.py` try to add all three to our cli!

<details>
<summary markdown='span'>If you get stuck</summary>

```bash
cli.add_command(<your command>)
```

</details>

Now we are ready to publish our cli!

## Publish to pypi

The python package index (know as pypi) is where packages that you can install directly with `pip` or in our case `poetry` so that your package can available on a new setup without having to re-clone the repository.

![pypi logo](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D1/pypi-logo.png)

Signup to [pypi](https://pypi.org/account/register/). Then create an api token from
[account settings](https://pypi.org/manage/account/) and make sure it has the scope entire account so that it can generate new projects!

Then create a .env containing the following to store your token:

```bash
PYPI_USERNAME==__token__
PYPI_TOKEN=<Your Token>
```

This is the perfect place to use a .envrc. Lets create a .envrc to load our .env file:

```bash
echo "dotenv" > .envrc
```

Now you can verify that your token is available as an environment variable with:
```bash
echo $PYPI_TOKEN
```

Let use poetry to quickly build and publish our package!

```bash
poetry publish --build --username $PYPI_USERNAME --password $PYPI_TOKEN
```

Now go to [your package](https://pypi.org/project/<user.github_nickname>-de-toolkit/) directly on pypi. You could now install this package from any machine. Here the package is new publicly available which is okay but generally pypi is for packages intended for public consumption and you probably do not want to share code for colleagues with world. So the solution is using private package repositories instead! Go to this [page](https://pypi.org/manage/project/<user.github_nickname>-de-toolkit-de-toolkit/settings/) to delete your package.


#

## Publish to private repository
There are plenty of solutions for private repositories even hosting them [yourself](https://pypi.org/project/pypiserver/)! For ease we will use [gemfury](https://gemfury.com/), you can login with github and then go to this [page](https://manage.fury.io/manage/<user.github_nickname>/tokens/full) to get a full access token.

Add this to the .env file:

```bash
GEMFURY_TOKEN=<your token>
```

Now to publish to your private repository you can follow this workflow!

```bash
poetry config repositories.fury https://pypi.fury.io/<user.github_nickname>/

poetry config http-basic.fury $GEMFURY_TOKEN ""

poetry publish --build --repository fury
```

Then use your packages from your private repo in another package now all you need to do is add.

```bash
poetry source add fury https://pypi.fury.io/<user.github_nickname>/
poetry add --source fury <user.github_nickname>_de_toolkit
```

To install your cli globally on your host machine you can use
```bash
pipx install <user.github_nickname>-de-toolkit --pip-args='--extra-index-url https://<deploy_token>@repo.fury.io/<user.github_nickname>/'
```
Now `deng` will be globally available for you to start, stop and enter your vm!
