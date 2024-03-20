#!/bin/bash

RED="\033[0;38;5;199m"
BLUE="\033[0;38;5;44m"
GREEN="\033[0;32m"
NC="\033[0m" # No Color

cd /home/${USER}/sgoinfre #change for your machine!!!
# cd /home/fhassoun


if ! command -v brew &>/dev/null; then
    echo -e "${BLUE}Installing Homebrew...${NC}"
    git clone https://github.com/Homebrew/brew homebrew
    eval "$(homebrew/bin/brew shellenv)"
    brew update --force --quiet
    chmod -R go-w "$(brew --prefix)/share/zsh"
    echo -e "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.zshrc
else
    echo -e "${GREEN}Homebrew is already installed.${NC}"
fi

if ! brew list ddclient &>/dev/null; then
	echo -e "${BLUE}Installing ddclient...${NC}"
	brew install ddclient
	cp ddcclient.conf /home/${USER}/sgoinfre/homebrew/etc/ddclient.conf
else
	echo -e "${GREEN}ddclient is already installed.${NC}"
fi

if ! brew list mkcert &>/dev/null; then
    echo -e "${BLUE}Installing mkcert...${NC}"
    brew install mkcert
else
    echo -e "${GREEN}mkcert is already installed.${NC}"
fi


if ! brew list nss &>/dev/null; then
    echo -e "${BLUE}Installing nss...${NC}"
    brew install nss
else
    echo -e "${GREEN}nss is already installed.${NC}"
fi


CERT_DIR="${HOME}/certs"
rm -rf "${CERT_DIR}"
mkdir -p "${CERT_DIR}" 


CURRENT_IP=$(hostname -I | awk '{print $1}')
echo -e "${BLUE}Setting up SSL certificates...${NC}"
mkcert -key-file "${CERT_DIR}/nginx.key" -cert-file "${CERT_DIR}/nginx.crt" localhost "${CURRENT_IP}" "42pong.ddns.net" &>/dev/null


echo -e "${GREEN}SSL certificates created!${NC}"