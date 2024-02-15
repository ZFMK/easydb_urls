# -------------------------------------------------------- #
# Dockerfile for easyDB URLS Search Interface
# Build with:         docker build -t docker.zfmk.de:5000/easydb_urls:latest \
#                     --build-arg CACHE=$(curl -s --header 'PRIVATE-TOKEN: <API access token from gitlab>' \
#                     https://gitlab.leibniz-lib.de/api/v4/projects/147/repository/commits  | jq -r '.[0].id') .
# Commit to Registry: docker push docker.zfmk.de:5000/easydb_urls:latest
# Deploy:             docker-compose config > docker-swarm.yml \
#                     && docker stack deploy --with-registry-auth -c docker-swarm.yml easydb_urls
# -------------------------------------------------------- #

FROM python:3.8-buster AS build0

ENV DEBIAN_FRONTEND noninteractive
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    apt-utils \
    git \
    locales \
    odbcinst \
    unixodbc \
    unixodbc-dev \
    software-properties-common \
    vim \
    && rm -rf /var/lib/apt/lists/*

FROM build0 AS build_venv

ARG BASE_DIR
ENV BASE_DIR ${BASE_DIR}
WORKDIR $BASE_DIR

COPY ./requirements.txt $BASE_DIR/

RUN groupadd -g 1005 bdi-dev && useradd -u 1005 -g bdi-dev bdi-dev \
    && chown bdi-dev.bdi-dev $BASE_DIR/
USER bdi-dev

ENV VIRTUAL_ENV=$BASE_DIR/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir --upgrade setuptools \
    && pip3 install --no-cache-dir wheel \
    && pip3 install --no-cache-dir -r requirements.txt

FROM build_venv AS build_app

ARG EXPOSE_PORT
ENV PYRAMID_PORT ${EXPOSE_PORT}
# Ensure rebuild on new commit
ARG CACHE=0
COPY --chown=bdi-dev:bdi-dev ./ $BASE_DIR/

# must be develop, othervise relative imports will fail....
RUN python3 setup.py develop

EXPOSE $PYRAMID_PORT

CMD [ "pserve", "production.ini" ]
#CMD sleep infinity
