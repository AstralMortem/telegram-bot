FROM --platform=$BUILDPLATFORM node:latest-alpine AS development

RUN mkdir /src
WORKDIR /src

COPY ../../frontend/ /src/

RUN npm install
ENV HOST=0.0.0.0

CMD ["npm", "run", "dev"]