FROM registry.gitlab.com/harukanetwork/oss/harukaaya:dockerstation

RUN git clone https://gitlab.com/HarukaNetwork/OSS/HarukaAya.git -b staging /data/HarukaAya

COPY ./config.yml /data/HarukaAya

WORKDIR /data/HarukaAya

CMD ["python", "-m", "haruka"]
