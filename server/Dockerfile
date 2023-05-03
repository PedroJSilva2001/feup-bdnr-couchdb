FROM node:18-alpine

WORKDIR /usr/app

COPY package*.json ./

RUN npm install

RUN npm install -g nodemon

COPY src/ src/

COPY ./.env ./

COPY datasets/ datasets/

EXPOSE 80

CMD ["npm", "start"]