#!/bin/bash

# if [ ! -f /etc/nginx/ssl/nginx.crt ]; then
# 	echo "Nginx: setting up ssl ...";
# 	# Fetch current local IP address
# 	IP=$(hostname -I | awk '{print $1}')
# 	openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/CN=10.15.201.1";
# 	echo "Nginx: ssl is set up!";
# fi
	# snap install --classic certbot
	# ln -s /snap/bin/certbot /usr/bin/certbot
	# certbot --nginx -d localhost --non-interactive --agree-tos -m admin@localhost

	# if [ ! -f /etc/nginx/ssl/nginx.crt ]; then
	# 	echo "Nginx: setting up ssl ...";
	# 	mkdir -p /etc/nginx/ssl
	# 	cd /etc/nginx/ssl
	# 	openssl genrsa -out rootCA.key 2048
	# 	openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 730 -out rootCert.pem -subj "/CN=localhost"
	# 	openssl genrsa -out nginx.key 2048
	# 	openssl req -new -key nginx.key -out nginx.csr -subj "/CN=localhost"
	# 	openssl x509 -req -in nginx.csr -CA rootCert.pem -CAkey rootCA.key -CAcreateserial -out nginx.crt -days 730 -sha256 -extfile /etc/nginx/ssl/openssl.cnf
	# 	openssl pkcs12 -export -out nginx.pfx -inkey nginx.key -in nginx.crt -password pass:$SSL_PW
	# 	echo "Nginx: ssl is set up!";
	# fi
exec "$@"