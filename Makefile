
all:
# builds and runs the containers
	sudo docker compose -f docker-compose.prod.yml up --build -d
	sudo docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
	sudo docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

clean:
# stops and removes the containers
	sudo docker compose -f docker-compose.prod.yml down --rmi all -v

down:
# stops the containers
	sudo docker compose -f docker-compose.prod.yml down

up:
# starts the containers
	sudo docker compose -f docker-compose.prod.yml up -d
	
restart:
# stops and starts the containers
	sudo docker compose -f docker-compose.prod.yml down
	sudo docker compose -f docker-compose.prod.yml up -d

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

logs:
# shows the logs of the containers
	sudo docker compose -f docker-compose.yml logs -f

migrate:
# runs the migrations (creates the tables in the database)
	sudo docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

makemigrations:
# creates the migrations
	sudo docker compose -f docker-compose.prod.yml exec web python manage.py makemigrations
connect_db:
# connects to the database
	sudo docker compose -f docker-compose.prod.yml exec db psql --username=ping --dbname=pong_db_prod

.PHONY: all, clean, fclean, re, ls, restart, logs, down, up, migrate, connect_db