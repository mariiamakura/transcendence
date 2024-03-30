#!/bin/bash

# Debug message
echo "Checking if ../nginx/certs directory exists..."

# Check if the ../nginx/certs directory exists
if [ -d "./nginx/certs" ]; then
    echo "Directory already exists."
else
    # Debug message
    echo "Directory does not exist. Creating it..."

    # Create the ../nginx/certs directory if it doesn't exist
    mkdir -p ./nginx/certs
    echo "Directory created."
fi

# Debug message
echo "Setting permissions for ./nginx/certs directory..."

# Set permissions for ../nginx/certs directory
chmod -R 777 ./nginx/certs
echo "Permissions set for ./nginx/certs directory."

# Debug message
echo "Copying certificates to ./nginx/certs directory..."

# Copy certificates to ../nginx/certs directory
cp -r ${HOME}/certs/nginx.crt ./nginx/certs
cp -r ${HOME}/certs/nginx.key ./nginx/certs
cp -r ${HOME}/certs/certs_prometheus ./prometheus
cp -r ${HOME}/certs/certs_node ./node_export
cp -r ${HOME}/certs/certs_alert ./alertmanager
cp -r ${HOME}/certs/certs_grafana ./grafana
cp -r ${HOME}/.local/share/mkcert/rootCA.pem ./prometheus
cp -r ${HOME}/.local/share/mkcert/rootCA.pem ./grafana

chmod 777 ./prometheus/rootCA.pem
chmod 777 ./grafana/rootCA.pem

# Add 8 spaces before each line in rootCA.pem
sed -i 's/^/        /' ./grafana/rootCA.pem

echo "Certificates copied successfully."