#!/bin/bash

cd /home/${USER}/sgoinfre #change for your machine!!!

git clone https://github.com/Homebrew/brew homebrew

eval "$(homebrew/bin/brew shellenv)"
brew update --force --quiet
chmod -R go-w "$(brew --prefix)/share/zsh"

echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.zshrc



brew install mkcert

echo "mkcert is already installed."



brew install nss

echo "nss is already installed."


CERT_DIR="${HOME}/certs"
mkdir -p "${CERT_DIR}"

mkcert -key-file "${CERT_DIR}/nginx.key" -cert-file "${CERT_DIR}/nginx.crt" localhost
mkcert -install

echo "SSL certificates are set up!"