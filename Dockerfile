FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    curl \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.9 get-pip.py && rm get-pip.py

WORKDIR /app

RUN python3.9 -m pip install --upgrade pip setuptools

COPY requirements.txt /app/requirements.txt

RUN python3.9 -m pip install -r requirements.txt

RUN python3.9 -c "from TTS.api import TTS; TTS('tts_models/en/jenny/jenny')"

COPY . /app

EXPOSE 8889

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8889", "server:app"]
