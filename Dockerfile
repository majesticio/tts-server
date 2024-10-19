FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    curl \
    git \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.9 get-pip.py && rm get-pip.py

WORKDIR /app

RUN python3.9 -m pip install --upgrade pip setuptools

COPY requirements.txt /app/requirements.txt

RUN python3.9 -m pip install -r requirements.txt

# Copy the pre-downloaded models to the appropriate directory in the container
# Assuming you have already downloaded the models to ./models on your local machine
COPY ./models /root/.local/share/tts/
COPY ./voices /app/voices
# Copy the rest of the app into the container
COPY . /app

EXPOSE 8889

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8889", "server:app"]
