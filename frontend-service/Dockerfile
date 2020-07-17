FROM node:10

# server
WORKDIR /app
COPY server/package*.json ./
RUN npm install

# client
WORKDIR /app/client
COPY client/package*.json ./
RUN npm install

WORKDIR /app
CMD npm start
