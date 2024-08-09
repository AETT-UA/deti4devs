FROM node:20.10.0-alpine AS build

WORKDIR /app

COPY ./package.json /app/package.json

RUN npm install

COPY . /app

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]