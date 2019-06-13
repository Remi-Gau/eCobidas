# taken from https://gist.github.com/remarkablemark/aacf14c29b3f01d6900d13137b21db3a

# set the base image to Debian
# https://hub.docker.com/_/debian/
FROM debian:latest

# replace shell with bash so we can source files
# RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# update the repository sources list
# and install dependencies
RUN apt-get update \
    && apt-get install -y curl git apt-utils \
    && apt-get -y autoclean

# nvm environment variables
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 10.16

# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# confirm installation
# RUN node -v
# RUN npm -v

# create COBIDAS folder and download schema-UI
RUN mkdir /cobidas && cd /cobidas
RUN git clone https://github.com/Remi-Gau/schema-ui.git && cd schema-ui
RUN git checkout COBIDAS

# create app and run
RUN npm install
EXPOSE 8080
RUN npm run dev
