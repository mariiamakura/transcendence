#!/bin/bash

#!/bin/bash

# Define color codes for output
RED='\033[0;38;5;199m'
BLUE='\033[0;38;5;44m'
GREEN='\033[0;32m'
ORANGE='\033[0;38;5;208m'
NC='\033[0m' # No Color

# Define the certificate directory and name
CERT_DIR="${HOME}/certs"
CERT_NAME="nginx.crt"

# Function to delete existing certificate
delete_cert() {
    local database_path=$1
    local cert_name=$2
    # Check if the certificate exists
    if certutil -L -d sql:"${database_path}" | grep -q "$cert_name"; then
        # echo "Deleting existing certificate $cert_name from database in $database_path"
        certutil -D -d sql:"${database_path}" -n "$cert_name" &>/dev/null
        if [ $? -eq 0 ]; then
            # echo -e "${ORANGE}Certificate $cert_name deleted successfully from ${NC}$database_path."
			echo -e "${ORANGE}Deleting old certificate from:${NC} $database_path."
			 
        else
            echo -e "${RED}Failed to delete certificate $cert_name from ${NC}$database_path."
        fi
    else
        echo -e "${GREEN}No Certificate $cert_name found in ${NC} $database_path."
    fi
}

# Delete existing and install new certificate for Chrome
echo -e "${RED}Checking old certificate for Chrome...${NC}"
CHROME_DIR="${HOME}/.pki/nssdb"
delete_cert "$CHROME_DIR" "$CERT_NAME"
echo -e "${BLUE}Installing certificate for Chrome...${NC}\n"
certutil -d sql:"${CHROME_DIR}" -A -t "P,," -n "$CERT_NAME" -i "${CERT_DIR}/$CERT_NAME" &>/dev/null

# Process Firefox profiles
echo -e "${RED}Checking old certificate for Firefox...${NC}"
FIREFOX_DIR="/home/${USER}/.mozilla/firefox/"
for folder in "${FIREFOX_DIR}"*; do
    if [[ $(basename "$folder") == *"default"* ]]; then
        # echo -e "${RED}Deleting old certificate for:${NC} $folder"
        delete_cert "$folder" "$CERT_NAME"
        # echo -e "${BLUE}Adding new certificate to:${NC} $folder"
		echo -e "${BLUE}Adding a new certificate to  :${NC} $folder\n"
        certutil -A -n "$CERT_NAME" -t "TCu,Cuw,Tuw" -i "${CERT_DIR}/$CERT_NAME" -d sql:"${folder}/" &>/dev/null
		# echo -e "\n"
	fi
done

echo -e "${GREEN}Certificate process completed!${NC}"


# RED='\033[0;38;5;199m'
# BLUE='\033[0;38;5;44m'
# GREEN='\033[0;32m'
# NC='\033[0m' # No Color
# CERT_DIR="${HOME}/certs"

# echo -e "${BLUE}Installing certificate for Chrome...${NC}"
# certutil -d sql:${HOME}/.pki/nssdb -A -t "P,," -n "nginx.crt" -i "${CERT_DIR}/nginx.crt" #&>/dev/null


# echo -e "${BLUE}Installing certificate for Firefox...${NC}"
# FIREFOX_DIR="/home/${USER}/.mozilla/firefox/"
# for folder in "${FIREFOX_DIR}"*; do
#     if [[ $(basename "$folder") == *"default"* ]]; then
#         echo -e "${BLUE}Adding certificate to:${NC} $folder"
#         certutil -A -n "nginx.crt" -t "TCu,Cuw,Tuw" -i "${CERT_DIR}/nginx.crt" -d "sql:${folder}/" #&>/dev/null
#     fi
# done

# echo -e "${GREEN}Certificates installed!${NC}"