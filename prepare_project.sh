#!/bin/bash

if ! command -v brew &>/dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if test -d ~/.linuxbrew; then
        eval "$(~/.linuxbrew/bin/brew shellenv)"
    fi
    if test -d /home/linuxbrew/.linuxbrew; then
        eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    fi
    echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.zshrc
else
    echo "Homebrew is already installed."
fi

if ! brew list mkcert &>/dev/null; then
    brew install mkcert
else
    echo "mkcert is already installed."
fi

if ! brew list nss &>/dev/null; then
    brew install nss
else
    echo "nss is already installed."
fi

CERT_DIR="${HOME}/certs"
mkdir -p "${CERT_DIR}"

mkcert -key-file "${CERT_DIR}/nginx.key" -cert-file "${CERT_DIR}/nginx.crt" localhost
mkcert -install

echo "SSL certificates are set up!"