#!/bin/bash

sudo docker-compose -f docker-compose.yml down -v
sudo docker-compose -f docker-compose.yml up -d --build --remove-orphans
# shellcheck disable=SC2046
sudo docker rmi -f $(sudo docker images -f dangling=true -q)
echo "Removed none images"
sudo docker logs --follow voice-assisstant
