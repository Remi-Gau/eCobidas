# set the base image to node 9
FROM node:9

# create COBIDAS folder and download schema-UI
RUN git clone https://github.com/Remi-Gau/schema-ui.git cobidas/
WORKDIR cobidas/
RUN git checkout COBIDAS

EXPOSE 8080

# create app and run
RUN npm install
RUN npm run dev
