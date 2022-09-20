FROM sa3ed266/catuserbot:slim-buster

#clonning repo 
RUN git clone https://github.com/TgCatUB/catuserbot /root/userbot
#working directory 
WORKDIR /root/userbot

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","userbot"]
