#!/usr/bin/env python3

import io
from PIL import Image
from recorder import record_audio
from tti_stability import generate_image
from cohere_translate import translate_yoruba, translate_english
from stt_lang_hf_api import transcribe_yoruba, transcribe_english

def main(lang:str="Yoruba") -> None:
    print("Speak now...")
    audio_file = record_audio(lang=lang)

    print("Transcribing...")
    if lang == "Yoruba":
        transcript = transcribe_yoruba(audio_file)
    else:
        transcript = transcribe_english(audio_file)
    transcript = transcript["text"].strip()
    print("transcript: ", transcript)

    print("Translating...")
    if lang == "Yoruba":
        en_transcript = translate_yoruba(transcript)
        print("Translation: ", en_transcript)
    else:
        yo_transcript = translate_english(transcript)
        print("Translation: ", yo_transcript)

    print("Generating image...")
    if lang == "Yoruba":
        image_bytes = generate_image(en_transcript)
    else:
        image_bytes = generate_image(transcript)
    image = Image.open(io.BytesIO(image_bytes))
    image.show()

if __name__ == '__main__':
    print("Welcome to the lablab benin multimodal hackathon!")

    try:
        while True:
            lang = input("Enter 'y' for Yoruba or 'e' for English: ").strip()
            if lang == 'y':
                main(lang="Yoruba")
            elif lang == 'e':
                main(lang="English")
            else:
                print("Invalid input. Please enter 'y' or 'e'.")
    except KeyboardInterrupt:
        print("Goodbye!")
