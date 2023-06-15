#! /bin/bash

curl -sfL https://get.k3s.io | K3S_TOKEN="${token}" INSTALL_K3S_VERSION="v1.26.0+k3s1" K3S_URL="https://${server_address}:6443" sh -s -
