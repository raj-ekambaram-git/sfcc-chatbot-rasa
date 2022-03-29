docker-compose pull

docker tag utcourtchatbotregistry.azurecr.io/utcourt-botfront:latest utcourtchatbotregistry.azurecr.io/utcourt-botfront:stable
docker push utcourtchatbotregistry.azurecr.io/utcourt-botfront:stable

docker rmi utcourtchatbotregistry.azurecr.io/utcourt-botfront:latest

npm run build

docker-compose build
docker-compose push