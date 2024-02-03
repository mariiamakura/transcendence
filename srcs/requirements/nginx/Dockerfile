# Use the official Nginx image
FROM nginx:latest

# Copy custom Nginx configuration file
# COPY nginx.conf /etc/nginx/nginx.conf
# COPY config/default.conf /etc/nginx/conf.d/default.conf
# COPY ./config/default.conf /etc/nginx/sites-available/default
COPY ./pong /var/www/
COPY ./config/default.conf /etc/nginx/conf.d/default.conf
# Copy site configurations
# COPY sites/* /etc/nginx/conf.d/

# Expose port 80
EXPOSE 9999

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
