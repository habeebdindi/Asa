#!/usr/bin/env python3
# https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct

import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

output = query({
	"inputs": "Can you please let us know more details about your ",
})
print(output)
