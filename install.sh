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
sudo apt update -y
sudo apt install -y docker.io
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Docker Compose
# Download docker-compose standalone
sudo curl -SL https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
# Apply executable permissions
sudo chmod +x /usr/local/bin/docker-compose
# Link
sudo rm /usr/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# TLDR
# Remove previous installs
sed -i "s|alias tldr='docker run --rm -it -v ~/.tldr/:/root/.tldr/ nutellinoit/tldr'||g" ~/.aliases
sudo apt remove tldr -y
source ~/.aliases
cd ~/ && pip3 install tldr

# GRPCurl
# -- Skipped

# Python, pip, Poetry
# -- Skipped

# Direnv
# -- Skipped
