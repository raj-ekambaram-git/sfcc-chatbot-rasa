docker-compose pull

docker tag utcourtchatbotregistry.azurecr.io/utcourt-rasa-core:latest utcourtchatbotregistry.azurecr.io/utcourt-rasa-core:stable &
docker tag utcourtchatbotregistry.azurecr.io/utcourt-rasa-actions:latest utcourtchatbotregistry.azurecr.io/utcourt-rasa-actions:stable

docker push utcourtchatbotregistry.azurecr.io/utcourt-rasa-core:stable &
docker push utcourtchatbotregistry.azurecr.io/utcourt-rasa-actions:stable

docker rmi utcourtchatbotregistry.azurecr.io/utcourt-rasa-core:latest &
docker rmi utcourtchatbotregistry.azurecr.io/utcourt-rasa-actions:latest

bash swagger_client_generator.sh

rasa train

docker-compose build
docker-compose push
