#!/usr/bin/python3

import os
import sys
from openai import OpenAI


def openai_translate_yoruba(src: str, dest:str, txt:str):
    """
    Translate text from Yoruba to English.
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a yoruba assistant who understands the language very well. You also know english. Therefore when you are spoken to in yoruba you can translate to english and when you are spoken to in English you can translate to yoruba. Put signs where necessary when translating to yoruba"},
            {"role": "user", "content": f"Translate from {src} to {dest}: {txt}"}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(openai_translate_yoruba("{}".format(sys.argv[1])))
