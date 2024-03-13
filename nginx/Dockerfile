FROM debian:buster

RUN apt-get update && apt-get install -y nginx openssl

RUN mkdir /etc/nginx/ssl


COPY ./nginx.conf /etc/nginx/sites-enabled/default
COPY ./nginx_start.sh /var/www

RUN chmod +x /var/www/nginx_start.sh
RUN mkdir -p /run/nginx

ENTRYPOINT ["var/www/nginx_start.sh"]

EXPOSE 9999

CMD ["nginx", "-g", "daemon off;"]