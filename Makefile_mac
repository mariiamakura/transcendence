
all:
# builds and runs the containers
	sudo docker compose -f docker-compose.yml up --build -d 
	sudo docker compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
	sudo docker compose -f docker-compose.yml exec web python manage.py makemigrations
	sudo docker compose -f docker-compose.yml exec web python manage.py migrate --noinput

#start the watchdog - wuff!
watch:
	sudo docker compose watch --no-up

clean:
# stops and removes the containers
	sudo docker compose -f docker-compose.yml down --rmi all -v

down:
# stops the containers
	sudo docker compose -f docker-compose.yml down

up:
# starts the containers
	sudo docker compose -f docker-compose.yml up -d 
	
restart: down up
# stops and starts the containers
# docker compose -f docker-compose.yml down
# docker compose -f docker-compose.yml up -d

fclean: clean
# removes all the images
	@sudo docker system prune -a

re: down all
# stops the containers, removes the images, builds and runs the containers
	@echo "restarting the containers"

ls:
# lists the images and containers
	sudo docker image ls
	sudo docker ps

reload_static:
	sudo docker compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear

logs:
# shows the logs of the containers
	sudo docker compose -f docker-compose.yml logs -f

migrate:
# runs the migrations (creates the tables in the database)
	sudo docker compose -f docker-compose.yml exec web python manage.py migrate --noinput

makemigrations:
# creates the migrations
	sudo docker compose -f docker-compose.yml exec web python manage.py makemigrations

show_migrations:
# shows the migrations
	sudo docker compose -f docker-compose.yml exec web python manage.py showmigrations

connect_db:
# connects to the database
	sudo docker compose -f docker-compose.yml exec db psql --username=ping --dbname=pong_db_prod

create_superuser:
# creates a superuser
	sudo docker compose -f docker-compose.yml exec web python manage.py createsuperuser

.PHONY: all, clean, fclean, re, ls, restart, logs, reload_static, down, up, migrate, connect_db, makemigrations, show_migrations, create_superuser