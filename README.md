# TTS Server
`docker build -t tts-api-gpu .`

```
sudo docker run -d --gpus all --restart unless-stopped \
  -p 8889:8889 \
  tts-api-gpu
```

`sudo docker run -d -p 5002:5002 --gpus all --restart unless-stopped tts-jenny`

```
docker run -d -p 5002:5002 --gpus all --restart unless-stopped \
  -v tts_models:/root/.local/share/tts \
  -e TTS_MODEL_NAME=tts_models/en/jenny/jenny \
  -e USE_CUDA=true \
  tts-jenny

```

## Test the API

```
curl -X POST -H "Content-Type: application/json" \      
    -d '{"text": "Hello, this is a test of the text to speech API."}' \
    http://localhost:8889/synthesize --output speech.wav
```