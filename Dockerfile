# We using apt-chrome-pip to install everything.
# Check different tags >>> https://hub.docker.com/repository/docker/jisan09/catuserbot/tags

FROM jisan09/catuserbot:apt-chrome-pip

# Working directory 
WORKDIR ./userbot

## Copy files into the Docker image
COPY . .

ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","userbot"]