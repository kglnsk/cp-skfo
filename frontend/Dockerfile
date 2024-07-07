FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine
RUN mkdir -p var/www/vue_app
COPY --from=build /app/dist var/www/vue_app 
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80