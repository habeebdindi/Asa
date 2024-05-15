#!/usr/bin/env python3
# https://huggingface.co/microsoft/Phi-3-mini-4k-instruct

import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

output = query({
	"inputs": "Can you please let us know more details about your ",
})

print(output)
