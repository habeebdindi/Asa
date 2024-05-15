#!/usr/bin/env python3


from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_compute_dtype="float16",
   bnb_4bit_use_double_quant=True,
)
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig

# Define the configuration with adjusted settings
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=False,  # Adjust based on testing
    bnb_4bit_quant_storage=torch.uint8
)

# Load the model with the configuration
model = AutoModelForSeq2SeqLM.from_pretrained("CohereForAI/aya-101", quantization_config=bnb_config)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("CohereForAI/aya-101")

from transformers import pipeline
pipe = pipeline("text2text-generation",
                                    model = model,
                                    tokenizer = tokenizer,
                                    device_map = "auto",
                                    max_length = 512,
                                    early_stopping = True,
                                    num_return_sequences = 1,
                                    no_repeat_ngram_size = 4,)

output = pipe("Hello")
print(output)
