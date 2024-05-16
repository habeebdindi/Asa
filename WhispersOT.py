import glob
import uuid
import os
import streamlit as st
import time
import base64
import requests
import io
from PIL import Image
from audiorecorder import audiorecorder
from tti_stability import generate_image, openai_image
from cohere_translate import translate_yoruba, translate_english
from openai_translate import openai_translate_yoruba
from stt_lang_hf_api import transcribe_yoruba, transcribe_english, openai_transcribe

def delete_files(pattern):
    files = glob.glob(pattern)
    for file_path in files:
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        except OSError as e:
            print(f"Error: {file_path} : {e.strerror}")
delete_files("./generated_image/*.webp")
delete_files("./generated_image/*.png")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

def save_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        image.save(file_name, "WEBP")
        return True
    return False

def convert_webp_to_png(input_webp_path, output_png_path):
    with Image.open(input_webp_path) as img:
        img.save(output_png_path, "PNG")
        return True
    return False

def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

def generate(lang, uploaded_file=None, audio=None):
    if lang == "Yoruba" and uploaded_file is not None:
        transcript = transcribe_yoruba(uploaded_file)
        transcript = transcript["text"].strip()
        translation = openai_translate_yoruba("Yoruba", "English", transcript)
    elif lang == "Yoruba" and uploaded_file is None:
        transcript = transcribe_yoruba("./audio_files/{}.wav".format(lang))
        transcript = transcript["text"].strip()
        translation = openai_translate_yoruba("Yoruba", "English", transcript)
    elif lang == "English" and uploaded_file is not None:
        transcript = openai_transcribe(uploaded_file)
        translation = translate_english(transcript)
    else:
        transcript = openai_transcribe("./audio_files/{}.wav".format(lang))
        translation = translate_english(transcript)

    return transcript, translation

record = text = upload = False

st.sidebar.success("Select an AI above")

st.markdown(
    "<h1 style='text-align: center; #A86823: ; padding-top: 0px; margin-bottom: 2px;'>Whispers of Tradition</h1>",
    unsafe_allow_html=True
)
st.image("./images/Asa_benin_hack.jpg")
st.info("Let's create art by talking about our rich culture!")

option = st.selectbox(
    "Select input source",
    ("Record", "Upload", "Text")
)
#option = st.radio("Select audio source", ("Record", "Upload"))
if option == "Upload":
    uploaded_file = st.file_uploader(
        "Select an audio file",
        type=["wav", "flac"],
        help="Upload only audio files.",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        filename = os.path.join("./uploaded_audio/", uploaded_file.name)
        with open(filename, "wb") as f:
            f.write(uploaded_file.read())
        upload = True
    else:
        upload = False

if option == "Text":
    prompt_text = st.text_area(
    "Prompt",
    "A man eating a tasty Benin delicacy",
    label_visibility="collapsed"
    )
    if prompt_text:
        text = True
    else:
        text = False
    upload = False

col1, col2 = st.columns([0.7, 0.3])
with col2:
    lang = st.radio(
        "Select audio language",
        ["English", "Yoruba"],
        horizontal=True,
        key="lang_radio"
    )
if option == "Record":
    with col1:
        audio_file = "./audio_files/{}.wav".format(lang)
        audio = audiorecorder(start_prompt="", stop_prompt="", pause_prompt="", show_visualizer=True, key="a-WhispersOT")
        if len(audio) > 0:
            st.audio(audio.export().read())
            audio.export(audio_file, format="wav")
        record = True
    text = False
    upload = False

if st.button("Generate Art"):
    with st.spinner('Drawing...'):
        if upload:
            transcript, translation = generate(lang, uploaded_file=filename)
        elif record:
            transcript, translation = generate(lang, audio=audio_file)
        else:
            if lang == "Yoruba":
                translation = openai_translate_yoruba(lang, "English", prompt_text)
            else:
                translation = openai_translate_yoruba("English", "Yoruba", prompt_text)
            transcript = prompt_text
        if not text:
            transcribe = st.text_input("Transcription", transcript)
        translate = st.text_input("Translation", translation)

        if lang == "Yoruba":
            image_url = openai_image(translation)
        else:
            image_url = openai_image(transcript)
#        image_url = "https://www.gstatic.com/webp/gallery/3.webp"
    st.success('Art generation complete!')
    st.image(image_url, use_column_width=True)
    img_id = str(uuid.uuid4()).split('-')[4]
    webp_path = f"./generated_image/{img_id}.webp"
    if save_image(image_url, webp_path):
        output_png_path=f"./generated_image/{img_id}.png"
        if convert_webp_to_png(webp_path, output_png_path):
            col3, col4 = st.columns([0.9, 0.1])
            with open(output_png_path, 'rb') as f:
                png_data = f.read()
            with col4:
                print(f"{output_png_path}")
                save = st.download_button(
                    label="Save",
                    data=png_data,
                    file_name=f"{translate}.png",
                    mime="image/png"
                )
    if upload:
        delete_file(filename)
    if record:
        delete_file(audio_file)

st.text("")
st.text("")
st.text("")
feedback = st.text_area("How can we improve, comment, thoughts?", height=40, key="text-WhispersOT")
if st.button("Submit"):
    st.write("Thank you for your submission, we appreciate your feedback")
