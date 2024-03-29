#!/bin/bash

# Define the path to the directories containing the NSS databases.
# This example targets Firefox profiles located in the user's home directory.
FIREFOX_DIR="/home/${USER}/.mozilla/firefox/"

# The name of the certificate to delete
certName="nginx.crt"

certutil -d sql:$HOME/.pki/nssdb -D -n nginx.crt &>/dev/null

# Loop through each directory
for folder in "${FIREFOX_DIR}"*; do
    if [[ $(basename "$folder") == *"default"* ]]; then
  
        # Check if a cert with the name exists, list certificates with certutil, grep for the name.
        exists=$(certutil -L -d sql:"$folder" | grep "$certName") #&>/dev/null

        # If the certificate exists, delete it.
        if [ ! -z "$exists" ]; then
            echo "Deleting certificate $certName from database in $folder"
            
            # Delete the certificate.
            # You might need to adjust the deletion command according to your certutil version or setup.
            certutil -D -d sql:"$folder" -n "$certName" #&>/dev/null
            
            # Check if the deletion was successful
            if [ $? -eq 0 ]; then
                echo "Certificate $certName deleted successfully from $folder."
            else
                echo "Failed to delete certificate $certName from $folder."
            fi
        else
            echo "Certificate $certName not found in $folder."
        fi
    fi
done


ddclient_conf="/home/${USER}/sgoinfre/homebrew/etc/ddclient.conf"

# Check if the file exists
if [ -f "$ddclient_conf" ]; then
    # If the file exists, remove it
    rm -f "$ddclient_conf"
    echo "File $ddclient_conf removed."

    # Uninstall ddclient using brew
    brew uninstall ddclient
else
    # If the file does not exist, print a message
    echo "File $ddclient_conf not found. Nothing to do."
fi

echo "Process completed."
