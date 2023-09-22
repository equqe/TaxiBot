FROM node:16-alpine as build

WORKDIR /app

COPY . .


FROM nginx:1.16.0-alpine
COPY --from=build /app/build /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
