from openai import OpenAI
import os
import streamlit as st
from PIL import Image
from audiorecorder import audiorecorder
import requests
import cohere
import WhispersOT
#from Asa.stt_lang_hf_api import openai_transcribe, transcribe_yoruba, transcribe_english


api_key = os.environ.get("OPENAI_API_KEY")

speech = text = upload = capture = False

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
        },
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You are a heritage and cultural ambassador for benin republic and you know so much about the history and culture. Provide the most relatable responses on an image in at least than 100 words. You can also tell stories and be humorous based on context."
            }
          ]
        },
      ],
      "max_tokens": 700
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    ret = response.json()
#    print(ret)
    return ret["choices"][0]["message"]["content"]


st.markdown(
    "<h1 style='text-align: center; #A86823: ; padding-top: 0px; margin-bottom: 2px;'>ImagiTale: Pictures that talk!</h1>",
    unsafe_allow_html=True
)
st.image("./images/Asa_benin_hack.jpg")

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
    "Where is this? and what is it's cultural significance",
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
    )

if prompt_option == "Speak":
    with col1:
        audio_file = "./audio_files/{}.wav".format(lang)
        audio = audiorecorder(start_prompt="", stop_prompt="", pause_prompt="", show_visualizer=True, key="a-ImagiTale")
        if len(audio) > 0:
            st.audio(audio.export().read())
            audio.export(audio_file, format="wav")
            speech = True
    text = False

if st.button("Generate", key="but_1_ImagiTale"):
    with st.spinner("Generating response..."):
        if speech:
            transcript, translation = WhispersOT.generate(lang, audio=audio_file)
            if lang == "Yoruba":
                response = vision(text=translation, img=filename)
            else:
                response = vision(text=transcript, img=filename)
        elif text:
            response = vision(text=prompt_text, img=filename)
#    st.success('Response generated!')
    st.success(response)

feedback = st.text_area("How can we improve, comment, thoughts?", height=40, key="text-ImagiTale")
if st.button("Submit", key="but_2_ImagiTale"):
    st.write("Thank you for your submission, we appreciate your feedback")
