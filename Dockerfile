FROM sandy1709/catuserbot

#clonning repo 
RUN git clone -b test https://github.com/sandy1709/catuserbot.git /root/userbot
#working directory 
WORKDIR /root/userbot
ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","userbot"]
