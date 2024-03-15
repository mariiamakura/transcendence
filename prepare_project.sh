#!/bin/bash

cd /home/${USER}/sgoinfre #change for your machine!!!

if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    git clone https://github.com/Homebrew/brew homebrew
    eval "$(homebrew/bin/brew shellenv)"
    brew update --force --quiet
    chmod -R go-w "$(brew --prefix)/share/zsh"
    echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.zshrc
else
    echo "Homebrew is already installed."
fi


if ! brew list mkcert &>/dev/null; then
    echo "Installing mkcert..."
    brew install mkcert
else
    echo "mkcert is already installed."
fi


if ! brew list nss &>/dev/null; then
    echo "Installing nss..."
    brew install nss
else
    echo "nss is already installed."
fi


CERT_DIR="${HOME}/certs"
mkdir -p "${CERT_DIR}"

CURRENT_IP=$(hostname -I | awk '{print $1}')
echo "Setting up SSL certificates..."
mkcert -key-file "${CERT_DIR}/nginx.key" -cert-file "${CERT_DIR}/nginx.crt" localhost "${CURRENT_IP}"


echo "Installing certificate for Chrome..."
certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n "nginx.crt" -i "${CERT_DIR}/nginx.crt" &>/dev/null


echo "Installing certificate for Firefox..."
FIREFOX_DIR="/home/${USER}/.mozilla/firefox/"
for folder in "${FIREFOX_DIR}"*; do
    if [[ $(basename "$folder") == *"default"* ]]; then
        echo "Adding certificate to: $folder"
        certutil -A -n "nginx.crt" -t "TCu,Cuw,Tuw" -i "${CERT_DIR}/nginx.crt" -d "sql:${folder}/" &>/dev/null
    fi
done

echo "SSL certificates are set up!"