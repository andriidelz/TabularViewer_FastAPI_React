FROM node:16

WORKDIR /app

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend /app

RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "5000"]
