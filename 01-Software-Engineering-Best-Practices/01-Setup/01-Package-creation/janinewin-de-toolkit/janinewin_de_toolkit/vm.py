import click
import subprocess

@click.command()
def start():
    """Start your VM"""
    subprocess.run("gcloud compute instances start --zone=europe-west1-b lewagon-data-eng-vm-janinewin")

@click.command()
def stop():
    """Stop your VM"""
    subprocess.run("gcloud compute instances stop --zone=europe-west1-b lewagon-data-eng-vm-janinewin")

@click.command()
def connect():
    """Connect to your VM in VSCode inside your ~/code/janinewin/ folder"""
    subprocess.run("code --folder-uri vscode-remote://ssh-remote+janine.windhoff@35.187.1.167/~/code/janinewin/")
