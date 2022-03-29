rm -rf ./client
mkdir client
java -jar deployment/swagger-codegen-cli-3.0.30.jar generate -i deployment/utcourts-api.yaml -o client -l python
cd client
python3 setup.py install --user
