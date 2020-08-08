FROM sandy1709/catuserbot

RUN git clone -b tree https://github.com/sandy1709/catuserbot.git /root/userbot
WORKDIR /root/userbot
ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","userbot"]
