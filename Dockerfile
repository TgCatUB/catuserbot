FROM sandy1709/catuserbot:slim-buster

RUN mkdir /root/userbot/bin/
RUN chmod 777 /root/userbot
WORKDIR /root/userbot/

CMD ["python3","-m","userbot"]
