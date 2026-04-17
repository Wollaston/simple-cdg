FROM node:24-alpine AS builder

ARG ORIGIN
ENV ORIGIN=$ORIGIN

ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL

ARG BACKEND_HOST
ENV BACKEND_URL=$BACKEND_HOST

ARG BACKEND_PORT
ENV BACKEND_PORT=$BACKEND_PORT

ENV BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET

WORKDIR /app

COPY package*.json ./
RUN npm i
COPY . .

RUN ORIGIN=$ORIGIN DATABASE_URL=$DATABASE_URL \
	BACKEND_HOST=$BACKEND_HOST BACKEND_PORT=$BACKEND_PORT \
	npm run build 
RUN npm prune --omit=dev

# Stage 2: Run the application
FROM node:24-alpine
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
ENV NODE_ENV=production

CMD ["node", "build"]

