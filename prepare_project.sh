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

mkcert -pkcs12 -key-file "${CERT_DIR}/nginx.key" -cert-file "${CERT_DIR}/nginx.crt" -p12-file "${CERT_DIR}/nginx.pfx"  localhost
# password for importing the pfx file to the browser : changeit 
# the password is hardcoded in the mkcert source code and cannot be changed

# this command failes for missing sudo permissions, but the files are created in the CERT_DIR, so 
# need to check if we need to install the root certificate, as we are importing the pfx file to the browser manually
# mkcert -install

certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n "nginx.crt" -i /home/${USER}/certs/nginx.crt

FIREFOX_DIR="/home/${USER}/.mozilla/firefox/"
for folder in "${FIREFOX_DIR}"*; do
    if [[ $(basename "$folder") == *"default"* ]]; then
        echo "Adding certificate to: $folder"
        certutil -A -n "nginx.crt" -t "TCu,Cuw,Tuw" -i "/home/${USER}/certs/nginx.crt" -d "sql:${folder}/"
    fi
done

echo "SSL certificates are set up!"