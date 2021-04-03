# Getting the latest alpine linux image
FROM alpine:latest

# Install necessary packages like Python3 etc
RUN apk --no-cache add python3 \
    python3-dev \
    build-base \
    libffi-dev \
    openssl-dev

# Install pip...
run echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

# Run the following commands within /app/Telegrambot
WORKDIR /app/rtxcrawler

# Copy everything inside /app/Telegrambot except directories and files listed in the .dockerignore file.
COPY * /app/rtxcrawler/

# Install the required packages with pip
RUN pip3 install --upgrade pip && \
    pip3 install -r /app/rtxcrawler/requirements.txt 

# Save the API key in the environment
ENV bot_api_key=0123456789:ABCqxtafQx-5aYP8U1zRB9oEgXTzZ2Awx1M

CMD ["python3", "/app/rtxcrawler/crawler.py"]