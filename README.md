# TTS Server
----
*TTS is served at the `/synthesize` endpoint. Must have nvidia container toolkit and docker installed*

## Build the image from Dockerfile
`docker build -t tts-api-gpu .`

```
sudo docker run -d --gpus all --restart unless-stopped \
  -p 8889:8889 \                                                                     
  tts-api-gpu                
```

## Test the API

```
curl -X POST -H "Content-Type: application/json" \      
    -d '{"text": "Hello, this is a test of the text to speech API."}' \
    http://localhost:8889/synthesize --output speech.wav
```

### Todos
- [ ] Add models
- [ ] Voice cloning