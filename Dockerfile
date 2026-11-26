FROM catub/core:bookworm-3.11

# Working directory
WORKDIR /userbot

# Timezone
ENV TZ=Asia/Kolkata

## Copy files into the Docker image
COPY . .

ENV PATH="/home/userbot/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python3","-m","userbot"]
