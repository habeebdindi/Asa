import time
import requests
from openai import OpenAI
import os
import streamlit as st
from PIL import Image
from io import StringIO, BytesIO
from audiorecorder import audiorecorder
import base64
import requests
import uuid
import cohere
import sys
#from Asa.stt_lang_hf_api import openai_transcribe, transcribe_yoruba, transcribe_english


api_key = os.environ.get("OPENAI_API_KEY")

speech = text = upload = capture = False


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


def translate_yoruba(text_input: str):
    """
    Translate text from Yoruba to English.
    """
    co = cohere.Client(api_key=os.environ.get("COHERE_TOKEN"))
    response = co.chat(
        model="command-r-plus",
        preamble="You are a yoruba model assistant. You are responsible for \
        translating yoruba words and sentences to english without any \
        additional texts. Do not forget to translate based on context",
        message="Translate this from Yoruba to English: " +
        text_input,
    )
    return response.text

def translate_english(text_input: str):
    """
    Translate text from English to Yoruba.
    """
    co = cohere.Client(api_key=os.environ.get("COHERE_TOKEN"))
    response = co.chat(
        model="command-r-plus",
        preamble="You are an english model assistant. You are responsible for \
        translating english words and sentences to yoruba(with signs if possible) \
        without any additional texts. Do not forget to translate based on context",
        message="Translate this from English to Yoruba: " +
        text_input,
    )
    return response.text

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def vision(text=None, img=None):
    image_path = img

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": text
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 600
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    ret = response.json()
    return ret["choices"][0]["message"]["content"]

def generate(lang, uploaded_file=None, audio=None):
    if lang == "Yoruba" and uploaded_file is not None:
        transcript = transcribe_yoruba(uploaded_file)
        transcript = transcript["text"].strip()
        translation = translate_yoruba(transcript)
    elif lang == "Yoruba" and uploaded_file is None:
        transcript = transcribe_yoruba("./audio_files/{}.wav".format(lang))
        transcript = transcript["text"].strip()
        translation = translate_yoruba(transcript)
    elif lang == "English" and uploaded_file is not None:
        transcript = openai_transcribe(uploaded_file)
        translation = translate_english(transcript)
    else:
        transcript = openai_transcribe("./audio_files/{}.wav".format(lang))
        translation = translate_english(transcript)

    return transcript, translation

st.markdown(
    "<h1 style='text-align: center; #A86823: ; padding-top: 0px; margin-bottom: 2px;'>ImagiTale:  that talk!</h1>",
    unsafe_allow_html=True
)
st.image("./images/Asa_benin_hack.jpg")
st.sidebar.success("Select an AI above")

st.info("Upload an image and ask anything about it")

option = st.selectbox(
    "Select image source",
    ("Upload", "Camera")
)
if option == "Upload":
    picture = st.file_uploader(
        "Select an image file",
        type=["jpg", "png", "jpeg"],
        help="Upload only image files.",
        label_visibility="collapsed",
    )

    if picture is not None:
        filename = os.path.join("./uploaded_image/", picture.name)
        with open(filename, "wb") as f:
            f.write(picture.read())
        upload = True
    else:
        upload = False
if option == "Camera":
    picture = st.camera_input("Take a picture")
    if picture is not None:
        filename = os.path.join("./uploaded_image/", picture.name)
        with open(filename, "wb") as f:
            f.write(picture.read())

        capture = True
    else:
        capture = False
    upload = False

prompt_option = st.selectbox(
    "Would you like to type your prompt or say it?",
    ("Speak", "Type")
)
if prompt_option == "Type":
    prompt_text = st.text_area(
    "Prompt",
    "Who is in the image? Where is this? and what is it's cultural significance",
    label_visibility="collapsed"
    )
    if prompt_text:
        text = True
    else:
        text = False

col1, col2 = st.columns([0.7, 0.3])
with col2:
    lang = st.radio(
        "Select language",
        ["English", "Yoruba"],
        horizontal=True,
        key="lang_radio"
    )

if prompt_option == "Speak":
    with col1:
        audio_file = "./audio_files/{}.wav".format(lang)
        audio = audiorecorder(start_prompt="", stop_prompt="", pause_prompt="", show_visualizer=True, key=None)
        if len(audio) > 0:
            st.audio(audio.export().read())
            audio.export(audio_file, format="wav")
            speech = True
    text = False

if st.button("Respond"):
    with st.spinner("Writing..."):
        if speech:
            transcript, translation = generate(lang, audio=audio_file)
            if lang == "Yoruba":
                response = vision(text=translation, img=filename)
            else:
                response = vision(text=transcript, img=filename)
        elif text:
            response = vision(text=prompt_text, img=filename)
    st.success('Response generated!')
    st.write(response)

feedback = st.text_area("How can we improve, comment, thoughts?", height=40)
if st.button("Submit"):
    st.write("Thank you for your submission, we appreciate your feedback")
