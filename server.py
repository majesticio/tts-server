# server.py

from flask import Flask, request, send_file, jsonify
from tts_handler import TTSHandler
import io

app = Flask(__name__)

# Initialize the TTSHandler with the desired model
tts_model_name = 'tts_models/en/jenny/jenny'  # Replace with your model
tts_handler = TTSHandler(model_name=tts_model_name)

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    audio_content = tts_handler.text_to_speech(text)

    if audio_content is None:
        return jsonify({'error': 'Text-to-Speech synthesis failed'}), 500

    # Send the audio content as a response
    return send_file(
        io.BytesIO(audio_content),
        mimetype='audio/wav',
        as_attachment=True,
        download_name='speech.wav'  # Updated to use 'download_name'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)
