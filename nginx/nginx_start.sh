#!/bin/bash

if [ ! -f /etc/nginx/ssl/nginx.crt ]; then
	echo "Nginx: setting up ssl ...";
	# Fetch current local IP address
	IP=$(hostname -I | awk '{print $1}')
	openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/CN=10.15.201.1";
	echo "Nginx: ssl is set up!";
fi

exec "$@"