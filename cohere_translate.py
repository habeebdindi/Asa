#!/usr/bin/python3

import os
import sys
import uuid
import cohere


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

if __name__ == "__main__":
    print(translate_yoruba("{}".format(sys.argv[1])))
