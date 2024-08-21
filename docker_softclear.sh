#!/bin/bash
docker compose -f "docker-compose.yml" down 
docker image prune -f
docker container prune -f
docker volume prune -f
docker network prune -f

