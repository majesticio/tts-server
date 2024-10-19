from flask import Flask, request, send_file, jsonify
from tts_handler import TTSHandler
import io

app = Flask(__name__)

# Initialize the TTSHandler with the desired models
tts_model_name = 'tts_models/en/jenny/jenny'  # Jenny model for /synthesize
tts_handler = TTSHandler(model_name=tts_model_name)
default_speaker_wav = 'assets/bria.wav'  # Ensure this file exists

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    audio_content = tts_handler.text_to_speech(text)

    if audio_content is None:
        return jsonify({'error': 'Text-to-Speech synthesis failed'}), 500

    return send_file(
        io.BytesIO(audio_content),
        mimetype='audio/wav',
        as_attachment=True,
        download_name='speech.wav'
    )

@app.route('/clone', methods=['POST'])
def clone():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    speaker_wav = '/app/voices/bria.wav'  # Set default speaker wav

    audio_content = tts_handler.clone_speech(text, speaker_wav)

    if audio_content is None:
        return jsonify({'error': 'Voice cloning failed'}), 500

    # Send the audio content as a response
    return send_file(
        io.BytesIO(audio_content),
        mimetype='audio/wav',
        as_attachment=True,
        download_name='cloned_speech.wav'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)
