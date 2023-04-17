#!/bin/bash

# Stop all containers and remove all images and volumes
docker-compose down --remove-orphans --rmi all --volumes 

# confirm that containers, images and volumes are removed
docker rm $(docker ps -a -q)
docker rmi $(docker images -a -q)
docker volume rm $(docker volume ls -q)

# prune docker
docker system prune -a

# delete all migrations
rm -rf betteretf/migrations

# Start all containers
docker-compose up
