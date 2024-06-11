#!/bin/bash
docker-compose down
docker system prune --volumes --force

docker-compose up -d
docker-compose logs -f
