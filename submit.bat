@echo off

docker-compose -f docker-compose.yml down -v
docker-compose -f docker-compose.yml up -d --build --remove-orphans

docker rmi -f $(docker images -f dangling=true -q)
echo "Removed none images"
docker logs --follow voice-assisstant
