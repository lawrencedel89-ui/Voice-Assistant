from flask import Flask, request, jsonify, render_template
from worker import speech_to_text, text_to_speech, openai_process_message
import os, json, base64

app = Flask(__name__)

# Serve the main HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Make sure index.html exists in templates/

# Speech-to-text endpoint
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    audio_binary = request.data
    text = speech_to_text(audio_binary)
    return app.response_class(
        response=json.dumps({'text': text}),
        status=200,
        mimetype='application/json'
    )

# Process message endpoint
@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json['userMessage']
    voice = request.json.get('voice', '')
    openai_response_text = openai_process_message(user_message)
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])
    openai_response_speech = text_to_speech(openai_response_text, voice)
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')
    return app.response_class(
        response=json.dumps({
            "openaiResponseText": openai_response_text,
            "openaiResponseSpeech": openai_response_speech
        }),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
