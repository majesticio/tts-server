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
### synthesize

```
curl -X POST -H "Content-Type: application/json" \      
    -d '{"text": "Hello, this is a test of the text to speech API."}' \
    http://localhost:8887/synthesize --output speech.wav
```

### clone
```
curl -X POST http://localhost:8889/clone \
    -H "Content-Type: application/json" \
    -d '{
        "text": "This is a cloned voice response.",
        "speaker_wav": "data:audio/wav;base64,'"$(base64 -w 0 /path/to/example.wav)"'"
    }' \
    --output cloned_speech.wav

```

### Todos
- [x] Add models
- [x] Voice cloning
- [ ] keep TTS models in repo to avoid multiple downloads
- [ ] add more voice samples for cloning
- [ ] add to dockerfile cp models to `/root/.local/share/tts/tts_models--en--jenny--jenny`
- [ ] add to dockerfile cp models to `/root/.local/share/tts/tts_models/multilingual/multi-dataset/xtts_v2`

### Shell into a container
`sudo docker exec -it 3b119ddb68e5 /bin/bash`