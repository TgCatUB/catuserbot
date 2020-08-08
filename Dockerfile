FROM sandy1709/catuserbot:slim-buster

RUN rm -rf /root/userbot/userbot/
RUN git clone -b test https://github.com/sandy1709/catuserbot.git /root/userbot

CMD ["python3","-m","userbot"]
