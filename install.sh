#!/usr/bin/zsh

# VSCode extensions
code --install-extension ms-vscode.sublime-keybindings
code --install-extension emmanuelbeziat.vscode-great-icons
code --install-extension ms-python.python
code --install-extension KevinRose.vsc-python-indent
code --install-extension ms-python.vscode-pylance
code --install-extension redhat.vscode-yaml
code --install-extension ms-azuretools.vscode-docker
code --install-extension bungcip.better-toml

# APT
sudo apt update -y
sudo apt install -y vim tmux tree git ca-certificates curl jq unzip zsh apt-transport-https gnupg software-properties-common direnv sqlite3 make

# Github CLI
# -- Skipped

# Oh my ZSH
# -- Skipped

# Google CLI
# -- Skipped

# Docker
# -- Skipped

# Docker Compose
# -- Skipped

# TLDR
# Remove previous installs
# -- Skipped

# GRPCurl
# -- Skipped

# Python, pip, Poetry
# -- Skipped

# Direnv
# -- Skipped
