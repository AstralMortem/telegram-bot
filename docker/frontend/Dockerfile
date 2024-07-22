ARG NODE_VERSION=20.10.0


FROM node:${NODE_VERSION}-alpine as base
ENV NODE_ENV=development

WORKDIR /src

#build
FROM base as build
COPY ../../frontend/package*.json ../../frontend/package-lock.json ./
RUN npm install
#run 
FROM base
COPY ../../frontend/ /src/
COPY --from=build /src/node_modules /src/node_modules
ENV HOST 0.0.0.0
EXPOSE 3000

ENTRYPOINT [ "npm", "run", "dev-global" ]