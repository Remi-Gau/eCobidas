# How to render the checklist

## manually

- Install [npm](https://www.npmjs.com/get-npm) or better install [node version manager](https://github.com/nvm-sh/nvm) to help you deal with different version of node.js.
- Clone the schema user interface [forked repository](https://github.com/Remi-Gau/schema-ui)
- Step inside the schema-ui directory and run `npm install`
- Run `npm run dev`
- Open your browser and go to [localhost:8080](localhost:8080)

### with docker

Done by following documentation from [this](https://nodejs.org/de/docs/guides/nodejs-docker-webapp/) and [this](https://gist.github.com/remarkablemark/aacf14c29b3f01d6900d13137b21db3a).

- create the docker image by running:

work in progress ...

docker build -t cobidas-checklist/node-web-app:0.0.1 .
docker run -it --rm -p 49160:8080 cobidas-checklist/node-web-app:0.0.1
