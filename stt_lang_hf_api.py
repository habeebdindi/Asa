#!/usr/bin/env python3

import os
import time
import requests
from openai import OpenAI

def transcribe_yoruba(filename):
    """
    Transcribe an audio file to text using a pre-trained model
    """
    API_URL = "https://api-inference.huggingface.co/models/neoform-ai/whisper-medium-yoruba"
    headers = {"Authorization": "Bearer {}".format(os.environ.get("HF_TOKEN"))}

    with open(filename, "rb") as f:
        data = f.read()
    while True:
        try:
            response = requests.post(API_URL, headers=headers, data=data)
            response_data = response.json()

            if 'error' in response_data:
                print("An error occurred:", response_data['error'])
                print("Retrying in 10 seconds...")
                time.sleep(5)
            else:
                return response_data
        except requests.exceptions.RequestException as e:
            print("An error occurred while transcribing:", e)
            return None
        except KeyboardInterrupt:
            return None

def openai_transcribe(filename):
    """
    Transcribe an audio file to text using a pre-trained model
    """
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    client = OpenAI()
    audio_file= open(filename, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription.text

def transcribe_english(filename):
    """
    Transcribe an audio file to text using a pre-trained model
    """
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": "Bearer {}".format(os.environ.get("HF_TOKEN"))}

    with open(filename, "rb") as f:
        data = f.read()
    while True:
        try:
            response = requests.post(API_URL, headers=headers, data=data)
            response_data = response.json()

            if 'error' in response_data:
                print("An error occurred:", response_data['error'])
                print("Retrying in 10 seconds...")
                time.sleep(5)
            else:
                return response_data
        except requests.exceptions.RequestException as e:
            print("An error occurred while transcribing:", e)
            return None
        except KeyboardInterrupt:
            return None


if __name__ == "__main__":
    output = openai_transcribe("./audio_files/english2.wav")
    print("Transcription:", output)
