FROM rasa/rasa:2.8.25-full

WORKDIR /app

COPY . .

EXPOSE 5005

CMD [ "run", "--enable-api", "--cors", "'*'"]
