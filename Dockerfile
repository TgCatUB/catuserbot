FROM alpine:edge

RUN sed -e 's;^#http\(.*\)/edge/community;http\1/edge/community;g' -i /etc/apk/repositories

# Installing Required Packages
RUN apk add --no-cache=true --update \
    aria2 \
    bash \
    build-base \
    bzip2-dev \
    chromium \
    chromium-chromedriver \
    coreutils \
    curl \
    docker \
    ffmpeg \
    figlet \
    freetype-dev \
    g++ \
    gcc \
    git \
    jpeg \
    jpeg-dev \
    jq \
    libevent \
    libffi-dev \
    libpq \
    libwebp-dev \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    musl \
    neofetch \
    nodejs \
    openssl \
    openssl-dev \
    postgresql \
    postgresql-client \
    postgresql-dev \
    pv \
    python3 \
    python3-dev \
    readline-dev \
    sqlite \
    sqlite-dev \
    sudo \
    util-linux \
    wget \
    zip \
    zlib-dev
    
# Pypi package Repo upgrade
RUN pip3 install --upgrade pip setuptools

# Copy Python Requirements to /root/userbot
RUN git clone -b newupdate https://github.com/sandy1709/catuserbot.git /root/userbot
WORKDIR /root/userbot

ENV PATH="/home/userbot/bin:$PATH"

# Install requirements
RUN pip3 install -U -r requirements.txt

# Starting Worker
CMD ["python3","-m","userbot"]
