FROM python:3.8.5-slim-buster

ENV PIP_NO_CACHE_DIR 1

RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# Installing Required Packages
RUN apt update && apt upgrade -y && \
    apt-get install --no-install-recommends -y \
    aria2\
    debian-keyring \
    debian-archive-keyring \
    bash \
    bzip2 \
    curl \
    figlet \
    fonts-liberation \
    git \
    gnupg \
    util-linux \
    libappindicator3-1 \
    libffi-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libwebp-dev \
    linux-headers-amd64 \
    musl-dev \
    musl \
    neofetch \
    php-pgsql \
    python3-lxml \
    postgresql \
    postgresql-client \
    python3-psycopg2 \
    libpq-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libxss1 \
    python3-pip \
    python3-requests \
    python3-sqlalchemy \
    python3-tz \
    python3-aiohttp \
    openssl \
    pv \
    jq \
    wget \
    python3 \
    python3-dev \
    libreadline-dev \
    libyaml-dev \
    gcc \
    sqlite3 \
    libsqlite3-dev \
    sudo \
    zlib1g \
    ffmpeg \
    libssl-dev \
    libgconf-2-4 \
    libxi6 \
    xvfb \
    unzip \
    libopus0 \
    libopus-dev \
    xdg-utils \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp
    
# Pypi package Repo upgrade
RUN pip3 install --upgrade pip setuptools

# install google chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i ./google-chrome-stable_current_amd64.deb

#install chromedriver
RUN mkdir /tmp/
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip 
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/ 

# Copy Python Requirements to /root/userbot
RUN git clone https://github.com/sandy1709/catuserbot.git /root/userbot
WORKDIR /root/userbot
ENV PATH="/home/userbot/bin:$PATH"

# Install requirements
RUN pip3 install -U -r requirements.txt

# Starting Worker
CMD ["python3","-m","userbot"]
