import os
import streamlit as st
import pandas as pd
import uuid
import time
from io import StringIO, BytesIO
from audiorecorder import audiorecorder
from tti_stability import generate_image, openai_image
from cohere_translate import translate_yoruba, translate_english
from stt_lang_hf_api import transcribe_yoruba, transcribe_english, openai_transcribe


def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

def generate(lang, uploaded_file=None, audio=None):
    if lang == "Yoruba" and uploaded_file is not None:
        uploaded_file.seek(0)
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
    "<h1 style='text-align: center; #A86823: ; padding-top: 0px; margin-bottom: 2px;'>Whispers of Tradition</h1>",
    unsafe_allow_html=True
)
st.image("./images/Asa_benin_hack.jpg")

option = st.selectbox(
    "Select audio source",
    ("Record", "Upload")
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
        print(filename)
        upload = True
    else:
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
        audio = audiorecorder(start_prompt="", stop_prompt="", pause_prompt="", show_visualizer=True, key=None)
        if len(audio) > 0:
            st.audio(audio.export().read())
            audio.export(audio_file, format="wav")
        record = True

    upload = False

if st.button("Generate Art"):
    with st.spinner('Drawing...'):
        if upload:
            transcript, translation = generate(lang, uploaded_file=filename)
        else:
            transcript, translation = generate(lang, audio=audio_file)

        transcribe = st.text_input("Transcription", transcript)
        translate = st.text_input("Translation", translation)

        if lang == "Yoruba":
            image_bytes = generate_image(translation)
        else:
            image_bytes = openai_image(transcript)

    st.success('Art generation complete!')
    st.image(image_bytes, use_column_width=True, caption=translate)

feedback = st.text_area("How can we improve, comment, thoughts?", height=40)
if st.button("Submit"):
    st.write("Thank you for your submission, we appreciate your feedback")
