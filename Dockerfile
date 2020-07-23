FROM alpine:edge

RUN git clone https://github.com/Sur-vivor/CatUserbot /root/userbot
RUN mkdir /root/userbot/bin/
RUN chmod 777 /root/userbot
WORKDIR /root/userbot/

CMD ["python3","-m","userbot"]
