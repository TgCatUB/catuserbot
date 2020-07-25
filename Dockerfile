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
 
RUN curl https://cli-assets.heroku.com/install.sh

RUN python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# Copy Python Requirements to /root/userbot
RUN git clone -b newupdate https://github.com/sandy1709/catuserbot /root/userbot
RUN mkdir /root/userbot/.bin
WORKDIR /root/userbot
ENV PATH="/root/userbot/.bin:$PATH"
WORKDIR /root/userbot

# Install requirements
RUN pip3 install -U -r requirements.txt

# Starting Worker
CMD ["python3","-m","userbot"]
