
all:
# builds and runs the containers
	sudo docker compose -f docker-compose.prod.yml up --build -d
	sudo docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

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




.PHONY: all, clean, fclean, re, ls, restart