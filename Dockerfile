# taken from https://gist.github.com/remarkablemark/aacf14c29b3f01d6900d13137b21db3a

# set the base image to Debian
# https://hub.docker.com/_/debian/
FROM debian:latest

# replace shell with bash so we can source files
# RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# update the repository sources list
# and install dependencies
RUN apt-get update \
    && apt-get install -y apt-utils curl git  \
    && apt-get -y autoclean

# nvm environment variables
ENV NODE_VERSION v10.16
ENV NVM_DIR /usr/local/nvm
RUN mkdir $NVM_DIR

# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

RUN echo "source $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default" | bash

# add sym links
RUN ln -sf $NVM_DIR/versions/node/$NODE_VERSION/bin/node /usr/bin/node
RUN ln -sf $NVM_DIR/versions/node/$NODE_VERSION/bin/npm /usr/bin/npm

# create COBIDAS folder and download schema-UI
RUN git clone https://github.com/Remi-Gau/schema-ui.git cobidas/
# RUN git checkout COBIDAS

EXPOSE 8080

# confirm installation
# RUN node -v
# RUN npm -v

# create app and run
# RUN npm install
# RUN npm run dev
