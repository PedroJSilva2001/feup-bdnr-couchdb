FROM node:14-alpine

WORKDIR /usr/app

COPY package*.json ./

RUN npm install

RUN npm install -g nodemon

COPY src/ src/

COPY ./.env ./

EXPOSE 80

CMD ["npm", "start"]