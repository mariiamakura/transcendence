#!/bin/bash

RED='\033[0;38;5;199m'
BLUE='\033[0;38;5;44m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing certificate for Chrome...${NC}"
certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n "nginx.crt" -i "${CERT_DIR}/nginx.crt" &>/dev/null


echo -e "${BLUE}Installing certificate for Firefox...${NC}"
FIREFOX_DIR="/home/${USER}/.mozilla/firefox/"
for folder in "${FIREFOX_DIR}"*; do
    if [[ $(basename "$folder") == *"default"* ]]; then
        # echo -e "${BLUE}Adding certificate to:${NC} $folder"
        certutil -A -n "nginx.crt" -t "TCu,Cuw,Tuw" -i "${CERT_DIR}/nginx.crt" -d "sql:${folder}/" &>/dev/null
    fi
done

echo -e "${GREEN}Certificates installed!${NC}"