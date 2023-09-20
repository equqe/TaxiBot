FROM node:16-alpine as build

WORKDIR /app

COPY package.json .
RUN npm install --save --legacy-peer-deps
RUN mkdir /app/node_modules/.cache && chmod -R 777 /app/node_modules/.cache

COPY . .

RUN npm run build

FROM nginx:1.16.0-alpine
COPY --from=build /app/build /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
