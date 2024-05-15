#!/usr/bin/python3

import io
import os
import sys
import requests
from PIL import Image


def generate_image(text) -> bytes:
    """
    Generate an image from text using a pre-trained model
    """
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": "Bearer {}".format(os.environ.get("HF_TOKEN"))}

    refined_text = "The setting of the image is "
    response = requests.post(API_URL, headers=headers, json=text)
    return response.content

def openai_image(text) ->bytes:
    from openai import OpenAI
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"{text} in West-Africa (Benin Republic setting if possible)",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url
if __name__ == '__main__':
    image_bytes = generate_image({
            "inputs": "{}".format(sys.argv[1]),
    })
    image = Image.open(io.BytesIO(image_bytes))
    image.show()
