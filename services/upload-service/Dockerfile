FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./src /app/src
CMD ["node", "src/app.js"]