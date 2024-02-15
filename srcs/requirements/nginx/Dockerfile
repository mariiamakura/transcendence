FROM debian:buster

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y nginx openssl 
RUN apt-get install -y python3 python3-pip python3-django python3-psycopg2
# Copy custom Nginx configuration file
# COPY nginx.conf /etc/nginx/nginx.conf
# COPY config/default.conf /etc/nginx/conf.d/default.conf
# COPY ./config/default.conf /etc/nginx/sites-available/default
COPY ./pong /var/www/
COPY ./config/default.conf /etc/nginx/conf.d/default.conf
COPY ./config/nginx_start.sh /var/www
# Copy site configurations
# COPY sites/* /etc/nginx/conf.d/


RUN chmod +x /var/www/nginx_start.sh
RUN mkdir -p /run/nginx
# Expose port 80

ENTRYPOINT ["var/www/nginx_start.sh"]

EXPOSE 9999

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]