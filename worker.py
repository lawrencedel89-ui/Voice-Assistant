# worker.py

import requests
from openai import OpenAI

import os
import json
import base64

# Initialize OpenAI client
openai_client = OpenAI()


# --------------------------
# Speech-to-Text Function
# --------------------------
def speech_to_text(audio_binary):
    """
    Converts audio binary data to text using Watson Speech-to-Text API.
    """
    # Replace with your Watson Speech-to-Text model URL
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = f"{base_url}/speech-to-text/api/v1/recognize"

    params = {
        'model': 'en-US_Multimedia',
    }

    response = requests.post(api_url, params=params, data=audio_binary).json()

    text = "null"
    if response.get("results"):
        print("speech-to-text response:", response)
        text = response.get("results").pop().get("alternatives").pop().get("transcript")
        print("recognized text:", text)
    return text


# --------------------------
# Text-to-Speech Function
# --------------------------
def text_to_speech(text, voice=""):
    """
    Converts text to speech using Watson Text-to-Speech API.
    Returns audio data in WAV format.
    """
    # Replace with your Watson Text-to-Speech model URL
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = f"{base_url}/text-to-speech/api/v1/synthesize?output=output_text.wav"

    # If a preferred voice is specified
    if voice != "" and voice != "default":
        api_url += f"&voice={voice}"

    headers = {
        "Accept": "audio/wav",
        "Content-Type": "application/json",
    }

    json_data = {
        "text": text
    }

    response = requests.post(api_url, headers=headers, json=json_data)
    print("text-to-speech response:", response)
    return response.content


# --------------------------
# OpenAI Process Message Function
# --------------------------
def openai_process_message(user_message):
    """
    Sends the user message to OpenAI GPT model and returns the AI's response text.
    """
    # System prompt to define assistant behavior
    prompt = (
        "Act like a personal assistant. You can respond to questions, translate sentences, "
        "summarize news, and give recommendations. Keep responses concise - 2 to 3 sentences maximum."
    )

    openai_response = openai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_completion_tokens=1000
    )

    print("openai response:", openai_response)
    response_text = openai_response.choices[0].message.content
    return response_text
