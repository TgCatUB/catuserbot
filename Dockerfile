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
	libgconf-2-4 \	
	libjpeg-dev \	
	libjpeg62-turbo-dev \	
    libopus-dev \	
	libopus0 \	
	libpq-dev \	
	libreadline-dev \	
	libsqlite3-dev \	
	libssl-dev \    
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
	python3-aiohttp \	
	python3-dev \	
	python3-lxml \	
	python3-pip \	
	python3-psycopg2 \	
	python3-requests \	
	python3-sqlalchemy \	
	python3-tz \	
	sqlite3 \
    readline-dev \
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
