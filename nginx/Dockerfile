FROM debian:buster

RUN apt-get update && apt-get install -y nginx openssl gettext


RUN mkdir /etc/nginx/ssl

COPY ./nginx.conf /etc/nginx/sites-enabled/default
# COPY ./nginx_start.sh /var/www
# COPY ./cert/nginx.key /etc/nginx/ssl
# COPY ./cert/nginx.crt /etc/nginx/ssl

COPY ./certs/nginx.key /etc/nginx/ssl
COPY ./certs/nginx.crt /etc/nginx/ssl

# RUN chmod +x /var/www/nginx_start.sh
RUN mkdir -p /run/nginx


# ENTRYPOINT ["var/www/nginx_start.sh"]

EXPOSE 9999

CMD ["nginx", "-g", "daemon off;"]