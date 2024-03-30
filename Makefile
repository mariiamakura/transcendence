
all:
# builds and runs the containers
	docker compose -f docker-compose.yml up --build -d 
	docker compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
	docker compose -f docker-compose.yml exec web python manage.py makemigrations
	docker compose -f docker-compose.yml exec web python manage.py migrate --noinput
	docker compose -f docker-compose.yml exec web python manage.py compilemessages

#start the watchdog - wuff!
watch:
	docker compose watch --no-up

prepare: create_cert #install_browser_cert

create_cert:
	@chmod +x scripts/create_cert.sh
	@./scripts/create_cert.sh
	@chmod +x scripts/copy_certs.sh
	@./scripts/copy_certs.sh

install_browser_cert:
	@chmod +x ./install_browser_cert.sh
	@./install_browser_cert.sh

delete_browser_cert:
	@chmod +x scripts/delete_browser_cert.sh
	@./scripts/delete_browser_cert.sh

delete_container_certs:
	@chmod +x scripts/delete_container_certs.sh
	@./scripts/delete_container_certs.sh

compile_messages:
	docker compose -f docker-compose.yml exec web python manage.py compilemessages

messages:
	docker compose -f docker-compose.yml exec web python manage.py makemessages -l ko -l fr -l uk -a

clean:
# stops and removes the containers
	docker compose -f docker-compose.yml down --rmi all -v

down:
# stops the containers
	docker compose -f docker-compose.yml down

up:
# starts the containers
	docker compose -f docker-compose.yml up -d 
	
restart:
# stops and starts the containers
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up -d

fclean: clean #delete_container_certs
# removes all the images
	@docker system prune -a

re: down all
# stops the containers, removes the images, builds and runs the containers
	@echo "restarting the containers"

ls:
# lists the images and containers
	docker image ls
	docker ps

reload_static:
	docker compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear

logs:
# shows the logs of the containers
	docker compose -f docker-compose.yml logs -f

migrate:
# runs the migrations (creates the tables in the database)
	docker compose -f docker-compose.yml exec web python manage.py migrate --noinput

makemigrations:
# creates the migrations
	docker compose -f docker-compose.yml exec web python manage.py makemigrations

show_migrations:
# shows the migrations
	docker compose -f docker-compose.yml exec web python manage.py showmigrations

connect_db:
# connects to the database
	docker compose -f docker-compose.yml exec db psql --username=ping --dbname=pong_db_prod

create_superuser:
# creates a superuser
	docker compose -f docker-compose.yml exec web python manage.py createsuperuser

fclean_force:
	@printf "Total clean of all configurations docker\n"
	@docker stop $$(docker ps -qa)
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force

.PHONY: all, clean, fclean, re, ls, restart, logs, reload_static, down, up, migrate, connect_db, makemigrations, show_migrations, create_superuser , prepare, create_cert, install_cert, watch