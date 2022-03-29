FROM node:12.16.1-alpine

WORKDIR /app

COPY package.json .

COPY lib/index.js /app/lib/index.js

RUN npm install http-server

CMD ["npm", "run", "prod"]
