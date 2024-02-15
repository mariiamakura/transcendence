all:
	# @if [ -d "/Users/fhassoun/dev_area/core/container/data/" ]; then \
	# 	echo "/home/fhassoun/data already exists"; else \
	# 	mkdir /Users/fhassoun/dev_area/core/container/data; \
	# 	echo "data directory created successfully"; \
	# fi

	# @if [ -d "/Users/fhassoun/dev_area/core/container/data/wordpress" ]; then \
	# 	echo "/home/fhassoun/data/wordpress already exists"; else \
	# 	mkdir /Users/fhassoun/dev_area/core/container/data/wordpress; \
	# 	echo "wordpress directory created successfully"; \
	# fi

	# @if [ -d "/Users/fhassoun/dev_area/core/container/data/mariadb" ]; then \
	# 	echo "/home/fhassoun/data/mariadb already exists"; else \
	# 	mkdir /Users/fhassoun/dev_area/core/container/data/mariadb; \
	# 	echo "mariadb directory created successfully"; \
	# fi
	sudo docker compose -f ./srcs/docker-compose.yml up -d

clean:
	sudo docker compose -f ./srcs/docker-compose.yml down --rmi all -v

down:
	sudo docker compose -f ./srcs/docker-compose.yml down

up:
	sudo docker compose -f ./srcs/docker-compose.yml up -d
	
restart:
	sudo docker compose -f ./srcs/docker-compose.yml down
	sudo docker compose -f ./srcs/docker-compose.yml up -d

fclean: clean
	@sudo docker system prune -a

re: fclean all

ls:
	sudo docker image ls
	sudo docker ps

delete:
	sudo docker compose -f ./srcs/docker-compose.yml down --rmi all -v
	@if [ -d "/home/fhassoun/data/wordpress" ]; then \
	rm -rf /home/fhassoun/data/wordpress/* && \
	echo "successfully removed all contents from /home/fhassoun/data/wordpress/"; \
	fi;

	@if [ -d "/home/fhassoun/data/mariadb" ]; then \
	sudo rm -rf /home/fhassoun/data/mariadb/* && \
	echo "successfully removed all contents from /home/fhassoun/data/mariadb/"; \
	fi;


.PHONY: all, clean, fclean, re, ls, delete, restart