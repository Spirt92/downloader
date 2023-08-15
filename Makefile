.PHONY: help build up down logs clean bash

# Docker commands
# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: build - build the Docker image for Flask app.
build:
	docker build -t flask-app-image -f Dockerfile .

# target: up - up the Flask app container.
up:
	docker run -d -p 8000:5000 --name flask-app-container flask-app-image

# target: down - stop and remove the Flask app container.
down:
	docker stop flask-app-container
	docker rm flask-app-container

# target: logs - show logs from the Flask app container.
logs:
	docker logs -f flask-app-container

# target: clean - remove the Docker image and stop container.
clean: down
	docker rmi flask-app-image

# target: bash - run bash in the Flask app container.
bash:
	docker exec -it flask-app-container bash